"""
Rate Limiting Middleware
Per-API-key and per-IP rate limits using Redis token bucket
"""
import os
import time
import logging
from flask import request, jsonify
from functools import wraps

logger = logging.getLogger(__name__)

RATELIMIT_ENABLED = os.getenv("RATELIMIT_ENABLED", "false").lower() == "true"
REDIS_URL = os.getenv("REDIS_URL")

# Rate limit configuration
RATE_LIMITS = {
    "free": {
        "api_key": 60,  # requests per minute
        "ip": 30
    },
    "pro": {
        "api_key": 600,
        "ip": 120
    }
}

# Redis connection
try:
    import redis
    _redis_client = None
    REDIS_AVAILABLE = bool(REDIS_URL)
except ImportError:
    REDIS_AVAILABLE = False
    redis = None


def get_redis_client():
    """Get Redis client for rate limiting"""
    global _redis_client
    
    if not REDIS_AVAILABLE or not REDIS_URL:
        return None
    
    if _redis_client is None:
        try:
            _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
            _redis_client.ping()
        except Exception as e:
            logger.warning(f"Redis unavailable for rate limiting: {e}")
            return None
    
    return _redis_client


# In-memory fallback for rate limiting (not distributed)
_memory_buckets = {}


def check_rate_limit(key: str, limit: int, window: int = 60) -> tuple[bool, int]:
    """
    Check rate limit using token bucket algorithm
    Returns (allowed, retry_after_seconds)
    """
    if not RATELIMIT_ENABLED:
        return True, 0
    
    client = get_redis_client()
    current_time = int(time.time())
    
    if client:
        # Redis-based rate limiting (distributed)
        try:
            bucket_key = f"ratelimit:{key}"
            pipe = client.pipeline()
            
            # Get current bucket state
            pipe.get(bucket_key)
            pipe.ttl(bucket_key)
            result = pipe.execute()
            
            count = int(result[0]) if result[0] else 0
            ttl = result[1] if result[1] > 0 else window
            
            if count >= limit:
                # Rate limit exceeded
                retry_after = ttl
                return False, retry_after
            
            # Increment counter
            pipe = client.pipeline()
            pipe.incr(bucket_key)
            if count == 0:
                pipe.expire(bucket_key, window)
            pipe.execute()
            
            return True, 0
        
        except Exception as e:
            logger.error(f"Rate limit check failed: {e}, allowing request")
            return True, 0
    
    else:
        # Memory-based fallback (single process only)
        if key not in _memory_buckets:
            _memory_buckets[key] = {"count": 0, "reset_at": current_time + window}
        
        bucket = _memory_buckets[key]
        
        # Reset bucket if window expired
        if current_time >= bucket["reset_at"]:
            bucket["count"] = 0
            bucket["reset_at"] = current_time + window
        
        if bucket["count"] >= limit:
            retry_after = bucket["reset_at"] - current_time
            return False, max(retry_after, 1)
        
        bucket["count"] += 1
        return True, 0


def get_client_plan(api_key: str = None) -> str:
    """Determine client plan (free or pro)"""
    # TODO: Look up actual plan from database
    # For now, default to free
    return "free"


def rate_limit(scope: str = "both"):
    """
    Rate limiting decorator
    scope: "api_key", "ip", or "both"
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not RATELIMIT_ENABLED:
                return func(*args, **kwargs)
            
            # Extract identifiers
            api_key = request.headers.get("X-API-Key") or request.args.get("api_key")
            client_ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()
            
            plan = get_client_plan(api_key)
            limits = RATE_LIMITS.get(plan, RATE_LIMITS["free"])
            
            # Check API key limit
            if scope in ["api_key", "both"] and api_key:
                allowed, retry_after = check_rate_limit(
                    f"key:{api_key}",
                    limits["api_key"],
                    60
                )
                if not allowed:
                    return jsonify({
                        "error": "rate_limited",
                        "message": "API key rate limit exceeded",
                        "retry_after": retry_after,
                        "limit": limits["api_key"],
                        "scope": "api_key"
                    }), 429
            
            # Check IP limit
            if scope in ["ip", "both"]:
                allowed, retry_after = check_rate_limit(
                    f"ip:{client_ip}",
                    limits["ip"],
                    60
                )
                if not allowed:
                    return jsonify({
                        "error": "rate_limited",
                        "message": "IP rate limit exceeded",
                        "retry_after": retry_after,
                        "limit": limits["ip"],
                        "scope": "ip"
                    }), 429
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# Metrics tracking
_rate_limit_hits = {"ip": 0, "key": 0}


def get_rate_limit_metrics():
    """Get rate limit metrics for /metrics endpoint"""
    return _rate_limit_hits
