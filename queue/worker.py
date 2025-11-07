"""
Queue Worker with DLQ, Retry, and Idempotency
Gracefully degrades to sync mode when Redis unavailable
"""
import os
import time
import logging
from typing import Callable, Any, Optional
from functools import wraps

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL")
NEW_QUEUE_ENABLED = os.getenv("NEW_QUEUE_ENABLED", "false").lower() == "true"

# Redis/RQ imports with graceful fallback
try:
    import redis
    from rq import Queue, Worker
    from rq.job import Job
    from rq.registry import FailedJobRegistry
    REDIS_AVAILABLE = bool(REDIS_URL)
except ImportError:
    REDIS_AVAILABLE = False
    redis = None
    Queue = None
    Worker = None
    Job = None

# Global connection and queue
_redis_conn = None
_task_queue = None
_dlq = None


def get_redis_connection():
    """Get Redis connection with lazy initialization"""
    global _redis_conn
    if not REDIS_AVAILABLE or not REDIS_URL:
        return None
    
    if _redis_conn is None:
        try:
            _redis_conn = redis.from_url(REDIS_URL, decode_responses=True)
            _redis_conn.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}, falling back to sync mode")
            return None
    return _redis_conn


def get_queue():
    """Get RQ queue instance"""
    global _task_queue
    if not REDIS_AVAILABLE or not NEW_QUEUE_ENABLED:
        return None
    
    if _task_queue is None:
        conn = get_redis_connection()
        if conn:
            _task_queue = Queue('default', connection=conn)
            logger.info("RQ queue initialized")
    return _task_queue


def get_dlq():
    """Get Dead Letter Queue (failed jobs registry)"""
    global _dlq
    if not REDIS_AVAILABLE or not NEW_QUEUE_ENABLED:
        return None
    
    if _dlq is None:
        conn = get_redis_connection()
        if conn:
            _dlq = FailedJobRegistry('default', connection=conn)
            logger.info("DLQ initialized")
    return _dlq


def idempotent(key_fn: Callable[[Any], str], ttl: int = 3600):
    """
    Decorator for idempotent task execution
    Stores execution keys in Redis set with TTL
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate idempotency key
            idem_key = f"idem:{func.__name__}:{key_fn(*args, **kwargs)}"
            
            conn = get_redis_connection()
            if conn and NEW_QUEUE_ENABLED:
                # Check if already executed
                if conn.exists(idem_key):
                    logger.info(f"Skipping duplicate execution: {idem_key}")
                    return {"status": "skipped", "reason": "duplicate"}
                
                # Mark as executed
                conn.setex(idem_key, ttl, "1")
            
            # Execute function
            result = func(*args, **kwargs)
            return result
        
        return wrapper
    return decorator


def enqueue_task(func: Callable, *args, retry_backoff: bool = True, max_retries: int = 3, **kwargs):
    """
    Enqueue task with retry and DLQ support
    Falls back to sync execution if queue unavailable
    """
    queue = get_queue()
    
    if not queue or not NEW_QUEUE_ENABLED:
        # Sync fallback
        logger.info(f"Executing {func.__name__} synchronously (queue disabled)")
        return func(*args, **kwargs)
    
    try:
        # Enqueue with retry settings
        job = queue.enqueue(
            func,
            args=args,
            kwargs=kwargs,
            retry=redis.retry.Retry(max=max_retries, interval=[1, 5, 15]),  # Exponential backoff
            failure_ttl=86400 * 7,  # Keep failed jobs for 7 days
        )
        logger.info(f"Enqueued {func.__name__} as job {job.id}")
        return {"job_id": job.id, "status": "enqueued"}
    
    except Exception as e:
        logger.error(f"Failed to enqueue {func.__name__}: {e}, falling back to sync")
        return func(*args, **kwargs)


def get_queue_health():
    """Get queue health metrics"""
    if not REDIS_AVAILABLE or not NEW_QUEUE_ENABLED:
        return {
            "mode": "sync",
            "queue_available": False,
            "depth": 0,
            "retry": 0,
            "dlq": 0
        }
    
    try:
        queue = get_queue()
        dlq = get_dlq()
        
        if not queue:
            return {
                "mode": "sync",
                "queue_available": False,
                "depth": 0,
                "retry": 0,
                "dlq": 0
            }
        
        return {
            "mode": "async",
            "queue_available": True,
            "depth": len(queue),
            "retry": queue.started_job_registry.count,
            "dlq": len(dlq) if dlq else 0
        }
    
    except Exception as e:
        logger.error(f"Queue health check failed: {e}")
        return {
            "mode": "error",
            "queue_available": False,
            "error": str(e),
            "depth": 0,
            "retry": 0,
            "dlq": 0
        }


def retry_dlq_jobs(limit: int = 10):
    """
    Retry failed jobs from DLQ
    Admin-only operation
    """
    if not REDIS_AVAILABLE or not NEW_QUEUE_ENABLED:
        return {"error": "Queue not available", "retried": 0}
    
    dlq = get_dlq()
    queue = get_queue()
    
    if not dlq or not queue:
        return {"error": "DLQ not available", "retried": 0}
    
    try:
        job_ids = dlq.get_job_ids(0, limit - 1)
        retried = 0
        
        for job_id in job_ids:
            try:
                job = Job.fetch(job_id, connection=get_redis_connection())
                queue.enqueue_job(job)
                dlq.remove(job)
                retried += 1
                logger.info(f"Retried DLQ job {job_id}")
            except Exception as e:
                logger.error(f"Failed to retry job {job_id}: {e}")
        
        return {
            "retried": retried,
            "remaining": len(dlq) - retried
        }
    
    except Exception as e:
        logger.error(f"DLQ retry failed: {e}")
        return {"error": str(e), "retried": 0}


if __name__ == "__main__":
    # Worker process
    if REDIS_AVAILABLE and NEW_QUEUE_ENABLED:
        conn = get_redis_connection()
        if conn:
            logger.info("Starting RQ worker...")
            worker = Worker(['default'], connection=conn)
            worker.work()
        else:
            logger.error("Cannot start worker: Redis unavailable")
    else:
        logger.info("Worker mode disabled (use NEW_QUEUE_ENABLED=true)")
