"""
Rate Limiting Tests
"""
import os
import time
import pytest


def test_ratelimit_disabled():
    """Test rate limiting when disabled"""
    os.environ["RATELIMIT_ENABLED"] = "false"
    
    from middleware.ratelimit import check_rate_limit
    
    # Should always allow when disabled
    allowed, retry_after = check_rate_limit("test_key", 10, 60)
    assert allowed is True
    assert retry_after == 0


def test_ratelimit_memory_fallback():
    """Test rate limiting with memory fallback (no Redis)"""
    os.environ["RATELIMIT_ENABLED"] = "true"
    os.environ.pop("REDIS_URL", None)
    
    from importlib import reload
    import middleware.ratelimit
    reload(middleware.ratelimit)
    
    from middleware.ratelimit import check_rate_limit
    
    # First requests should succeed
    for i in range(5):
        allowed, retry_after = check_rate_limit("test_user", 5, 60)
        if i < 5:
            assert allowed is True
    
    # 6th request should be rate limited
    allowed, retry_after = check_rate_limit("test_user", 5, 60)
    assert allowed is False
    assert retry_after > 0


def test_rate_limit_metrics():
    """Test rate limit metrics tracking"""
    from middleware.ratelimit import get_rate_limit_metrics
    
    metrics = get_rate_limit_metrics()
    assert isinstance(metrics, dict)
    assert "ip" in metrics
    assert "key" in metrics


if __name__ == "__main__":
    test_ratelimit_disabled()
    test_ratelimit_memory_fallback()
    test_rate_limit_metrics()
    print("✅ All rate limiting tests passed")
