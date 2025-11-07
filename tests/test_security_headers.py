"""
Security Headers Tests
"""
import os
import pytest


def test_security_headers_disabled():
    """Test security headers when flag is disabled"""
    os.environ["SECURITY_HEADERS_ENABLED"] = "false"
    
    from middleware.security_headers import SECURITY_HEADERS_ENABLED
    assert SECURITY_HEADERS_ENABLED is False


def test_security_headers_enabled():
    """Test security headers when flag is enabled"""
    os.environ["SECURITY_HEADERS_ENABLED"] = "true"
    
    from importlib import reload
    import middleware.security_headers
    reload(middleware.security_headers)
    
    from middleware.security_headers import SECURITY_HEADERS_ENABLED, SECURITY_HEADERS
    
    assert SECURITY_HEADERS_ENABLED is True
    assert "Content-Security-Policy" in SECURITY_HEADERS
    assert "Strict-Transport-Security" in SECURITY_HEADERS
    assert "X-Frame-Options" in SECURITY_HEADERS
    
    # Verify CSP includes expected directives
    csp = SECURITY_HEADERS["Content-Security-Policy"]
    assert "default-src 'self'" in csp
    assert "script-src" in csp
    
    # Verify HSTS max-age
    hsts = SECURITY_HEADERS["Strict-Transport-Security"]
    assert "max-age=15552000" in hsts


if __name__ == "__main__":
    test_security_headers_disabled()
    test_security_headers_enabled()
    print("✅ All security header tests passed")
