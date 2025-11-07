"""
Referral Fraud Guard
Prevents abuse of referral system with IP limits and disposable email detection
"""
import sqlite3
from flask import request

# Known disposable email domains
DISPOSABLE_DOMAINS = {
    "mailinator.com",
    "tempmail.com",
    "guerrillamail.com",
    "10minutemail.com",
    "throwaway.email",
    "temp-mail.org",
    "fakeinbox.com",
    "trashmail.com",
    "yopmail.com",
    "emailondeck.com"
}

# Maximum signups per IP address
MAX_SIGNUPS_PER_IP = 3

def is_allowed_signup(ip_address, email):
    """
    Check if signup is allowed based on fraud detection rules
    
    Args:
        ip_address: IP address of signup request
        email: Email address being registered
    
    Returns:
        (bool, str): (allowed, reason_if_blocked)
    """
    # Check IP address limit
    try:
        conn = sqlite3.connect('levqor.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE ip = ?", (ip_address,))
        count = cursor.fetchone()[0]
        conn.close()
        
        if count >= MAX_SIGNUPS_PER_IP:
            return False, f"Too many signups from this IP ({count}/{MAX_SIGNUPS_PER_IP})"
    
    except Exception as e:
        print(f"[!] Error checking IP limit: {e}")
        # Allow signup if database check fails (fail open for user experience)
        pass
    
    # Check disposable email domain
    domain = email.split("@")[-1].lower()
    if domain in DISPOSABLE_DOMAINS:
        return False, f"Disposable email domain not allowed: {domain}"
    
    return True, None

def get_client_ip():
    """Get client IP from request, accounting for proxies"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr

def check_referral_fraud(email):
    """
    Convenience function to check signup fraud from Flask request
    
    Returns:
        (bool, str): (allowed, reason_if_blocked)
    """
    ip = get_client_ip()
    return is_allowed_signup(ip, email)
