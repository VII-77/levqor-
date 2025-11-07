"""
Abuse Control System
- Free plan device binding
- Referral anti-fraud detection
"""
import os
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Optional
import psycopg2
from flask import request

logger = logging.getLogger(__name__)

ABUSE_GUARDS_ENABLED = os.getenv("ABUSE_GUARDS_ENABLED", "false").lower() == "true"

# PostgreSQL connection
DATABASE_URL = os.getenv("DATABASE_URL")

# Metrics
_abuse_blocks = {"device": 0, "referral": 0}


def get_device_fingerprint() -> str:
    """Generate device fingerprint from request"""
    # Combine User-Agent, Accept-Language, and screen resolution hints
    user_agent = request.headers.get("User-Agent", "")
    accept_lang = request.headers.get("Accept-Language", "")
    
    # Hash for privacy
    fingerprint_str = f"{user_agent}:{accept_lang}"
    return hashlib.sha256(fingerprint_str.encode()).hexdigest()[:16]


def get_client_asn() -> Optional[str]:
    """Get client ASN from IP (simplified - would use GeoIP in production)"""
    # This is a placeholder - in production, use MaxMind GeoIP2 or similar
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()
    
    # For now, use IP as ASN proxy
    return hashlib.md5(client_ip.encode()).hexdigest()[:8]


def check_device_binding(user_id: str, plan: str = "free") -> tuple[bool, Optional[str]]:
    """
    Check if user is bound to a specific device (free plan only)
    Returns (allowed, reason)
    """
    if not ABUSE_GUARDS_ENABLED or plan != "free":
        return True, None
    
    try:
        current_fingerprint = get_device_fingerprint()
        current_asn = get_client_asn()
        
        # Connect to database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Check if user has device binding
        cursor.execute("""
            SELECT first_device_hash, first_asn, device_changes_24h, last_device_change
            FROM user_device_binding
            WHERE user_id = %s
        """, (user_id,))
        
        result = cursor.fetchone()
        
        if not result:
            # First time user - create binding
            cursor.execute("""
                INSERT INTO user_device_binding 
                (user_id, first_device_hash, first_asn, device_changes_24h, last_device_change)
                VALUES (%s, %s, %s, 0, NOW())
            """, (user_id, current_fingerprint, current_asn))
            conn.commit()
            cursor.close()
            conn.close()
            return True, None
        
        first_device, first_asn, changes_24h, last_change = result
        
        # Check if device/ASN changed
        device_changed = current_fingerprint != first_device
        asn_changed = current_asn != first_asn
        
        if device_changed or asn_changed:
            # Check 24-hour change threshold
            now = datetime.utcnow()
            if last_change and (now - last_change) < timedelta(hours=24):
                # Within 24h window
                if changes_24h >= 3:
                    # Too many changes - block
                    _abuse_blocks["device"] += 1
                    cursor.close()
                    conn.close()
                    logger.warning(f"Device binding abuse detected for user {user_id}")
                    return False, "Too many device changes detected. Please upgrade to continue."
                
                # Increment change counter
                cursor.execute("""
                    UPDATE user_device_binding
                    SET device_changes_24h = device_changes_24h + 1,
                        last_device_change = NOW()
                    WHERE user_id = %s
                """, (user_id,))
            else:
                # Reset counter (new 24h window)
                cursor.execute("""
                    UPDATE user_device_binding
                    SET device_changes_24h = 1,
                        last_device_change = NOW()
                    WHERE user_id = %s
                """, (user_id,))
            
            conn.commit()
        
        cursor.close()
        conn.close()
        return True, None
    
    except Exception as e:
        logger.error(f"Device binding check failed: {e}")
        # Fail open - allow request if check fails
        return True, None


def check_referral_fraud(referrer_code: str, new_user_email: str) -> tuple[bool, Optional[str]]:
    """
    Check for referral fraud
    Blocks if:
    - >5 signups/day from same ASN
    - Distance between signups < 100m (if geo available)
    
    Returns (allowed, reason)
    """
    if not ABUSE_GUARDS_ENABLED:
        return True, None
    
    try:
        current_asn = get_client_asn()
        
        # Connect to database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Count signups from same ASN in last 24h
        cursor.execute("""
            SELECT COUNT(*)
            FROM referral_signups
            WHERE referrer_code = %s
              AND asn = %s
              AND created_at > NOW() - INTERVAL '24 hours'
        """, (referrer_code, current_asn))
        
        asn_signup_count = cursor.fetchone()[0]
        
        if asn_signup_count >= 5:
            # Too many signups from same ASN
            _abuse_blocks["referral"] += 1
            cursor.close()
            conn.close()
            logger.warning(f"Referral fraud detected: {referrer_code} - too many signups from ASN {current_asn}")
            return False, "Referral limit exceeded from this network"
        
        # Record this signup
        cursor.execute("""
            INSERT INTO referral_signups 
            (referrer_code, new_user_email, asn, created_at)
            VALUES (%s, %s, %s, NOW())
        """, (referrer_code, hashlib.sha256(new_user_email.encode()).hexdigest(), current_asn))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True, None
    
    except Exception as e:
        logger.error(f"Referral fraud check failed: {e}")
        # Fail open
        return True, None


def get_abuse_metrics():
    """Get abuse control metrics"""
    return {
        "device_blocks_total": _abuse_blocks["device"],
        "referral_blocks_total": _abuse_blocks["referral"]
    }


# Database schema (to be added via migration)
"""
CREATE TABLE IF NOT EXISTS user_device_binding (
    user_id VARCHAR(255) PRIMARY KEY,
    first_device_hash VARCHAR(32) NOT NULL,
    first_asn VARCHAR(16),
    device_changes_24h INTEGER DEFAULT 0,
    last_device_change TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS referral_signups (
    id SERIAL PRIMARY KEY,
    referrer_code VARCHAR(50) NOT NULL,
    new_user_email VARCHAR(64) NOT NULL,  -- SHA-256 hash
    asn VARCHAR(16),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_referrer_asn_time (referrer_code, asn, created_at)
);
"""
