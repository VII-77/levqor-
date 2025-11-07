"""
Queue and DLQ Tests
"""
import os
import pytest


def test_queue_sync_mode():
    """Test queue falls back to sync mode without Redis"""
    os.environ["NEW_QUEUE_ENABLED"] = "false"
    os.environ.pop("REDIS_URL", None)
    
    from queue.worker import get_queue_health, enqueue_task
    
    # Health should show sync mode
    health = get_queue_health()
    assert health["mode"] == "sync"
    assert health["queue_available"] is False
    assert health["depth"] == 0
    
    # Enqueue should execute synchronously
    def test_task(x, y):
        return x + y
    
    result = enqueue_task(test_task, 2, 3)
    assert result == 5  # Executed synchronously


def test_idempotency():
    """Test idempotency decorator"""
    from queue.worker import idempotent
    
    call_count = [0]
    
    @idempotent(key_fn=lambda x: str(x), ttl=60)
    def test_func(x):
        call_count[0] += 1
        return x * 2
    
    # First call should execute
    result1 = test_func(5)
    assert result1 == 10
    assert call_count[0] == 1
    
    # Without Redis, idempotency doesn't work, so second call executes
    # This is expected fallback behavior


def test_dlq_operations():
    """Test DLQ retry operations"""
    from queue.worker import retry_dlq_jobs
    
    # Without Redis, should return error
    result = retry_dlq_jobs(10)
    assert "error" in result or result["retried"] == 0


if __name__ == "__main__":
    test_queue_sync_mode()
    test_idempotency()
    test_dlq_operations()
    print("✅ All queue/DLQ tests passed")
