"""
Per-User Rate Limiting Middleware
Implements token bucket algorithm with Redis fallback to in-memory
"""
from flask import request, jsonify
import time
import os
from functools import wraps
from typing import Dict, Tuple

# In-memory storage (fallback if Redis unavailable)
_limits: Dict[str, Tuple[int, float]] = {}

# Configuration
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds
RATE_LIMIT_MAX = int(os.getenv("RATE_LIMIT_MAX", "60"))  # requests per window

def get_redis_client():
    """Get Redis client if available"""
    try:
        import redis
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            return redis.from_url(redis_url)
    except Exception:
        pass
    return None

def get_client_identifier() -> str:
    """Get unique identifier for rate limiting"""
    # Try to get authenticated user email first
    user_email = getattr(request, 'user_email', None)
    if user_email:
        return f"user:{user_email}"
    
    # Fall back to IP address
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        ip = request.remote_addr
    
    return f"ip:{ip}"

def check_rate_limit(identifier: str) -> Tuple[bool, int]:
    """
    Check if request is within rate limit
    
    Args:
        identifier: Unique client identifier
    
    Returns:
        (allowed, remaining_requests)
    """
    now = time.time()
    window_key = f"{identifier}:{int(now / RATE_LIMIT_WINDOW)}"
    
    # Try Redis first
    redis_client = get_redis_client()
    if redis_client:
        try:
            count = redis_client.incr(window_key)
            if count == 1:
                redis_client.expire(window_key, RATE_LIMIT_WINDOW)
            
            remaining = max(0, RATE_LIMIT_MAX - count)
            allowed = count <= RATE_LIMIT_MAX
            return allowed, remaining
        except Exception as e:
            print(f"[!] Redis rate limit error: {e}, falling back to memory")
    
    # Fall back to in-memory
    if window_key not in _limits:
        _limits[window_key] = (1, now + RATE_LIMIT_WINDOW)
        return True, RATE_LIMIT_MAX - 1
    
    count, expires = _limits[window_key]
    
    # Clean expired entries
    if now > expires:
        _limits[window_key] = (1, now + RATE_LIMIT_WINDOW)
        return True, RATE_LIMIT_MAX - 1
    
    count += 1
    _limits[window_key] = (count, expires)
    
    remaining = max(0, RATE_LIMIT_MAX - count)
    allowed = count <= RATE_LIMIT_MAX
    
    return allowed, remaining

def rate_limit(f):
    """
    Decorator to apply rate limiting to Flask routes
    
    Usage:
        @app.route('/api/endpoint')
        @rate_limit
        def my_endpoint():
            return jsonify({"status": "ok"})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        identifier = get_client_identifier()
        allowed, remaining = check_rate_limit(identifier)
        
        if not allowed:
            response = jsonify({
                "error": "Rate limit exceeded",
                "message": f"Too many requests. Limit: {RATE_LIMIT_MAX}/{RATE_LIMIT_WINDOW}s"
            })
            response.status_code = 429
            response.headers['X-RateLimit-Limit'] = str(RATE_LIMIT_MAX)
            response.headers['X-RateLimit-Remaining'] = '0'
            response.headers['X-RateLimit-Reset'] = str(int(time.time()) + RATE_LIMIT_WINDOW)
            return response
        
        # Add rate limit headers to response
        response = f(*args, **kwargs)
        if hasattr(response, 'headers'):
            response.headers['X-RateLimit-Limit'] = str(RATE_LIMIT_MAX)
            response.headers['X-RateLimit-Remaining'] = str(remaining)
            response.headers['X-RateLimit-Reset'] = str(int(time.time()) + RATE_LIMIT_WINDOW)
        
        return response
    
    return decorated_function

def cleanup_expired_limits():
    """Clean up expired rate limit entries from memory"""
    now = time.time()
    expired = [k for k, (_, expires) in _limits.items() if now > expires]
    for key in expired:
        del _limits[key]
    return len(expired)
