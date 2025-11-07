"""
Security Headers Middleware
Implements CSP, HSTS, X-Frame-Options, etc.
"""
import os
from flask import Response

SECURITY_HEADERS_ENABLED = os.getenv("SECURITY_HEADERS_ENABLED", "false").lower() == "true"

# Security header definitions
SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; "
        "img-src * blob: data:; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://plausible.io; "
        "style-src 'self' 'unsafe-inline'; "
        "connect-src 'self' https:"
    ),
    "Strict-Transport-Security": "max-age=15552000; includeSubDomains",
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
}


def add_security_headers(response: Response) -> Response:
    """Add security headers to response"""
    if not SECURITY_HEADERS_ENABLED:
        return response
    
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value
    
    return response


def init_security_headers(app):
    """Initialize security headers middleware"""
    @app.after_request
    def apply_security_headers(response):
        return add_security_headers(response)
    
    if SECURITY_HEADERS_ENABLED:
        app.logger.info("Security headers middleware enabled")
    else:
        app.logger.info("Security headers middleware disabled (set SECURITY_HEADERS_ENABLED=true)")
