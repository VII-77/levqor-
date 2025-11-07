"""
JWT Token Manager with Rotation & Revocation
Provides secure token issuance, verification, and revocation capabilities
"""
import os
import time
import jwt
import sqlite3
import uuid
from typing import Optional, Dict, Any

SECRET = os.getenv("JWT_SECRET", "change_me_in_production")
ACCESS_TOKEN_EXPIRY = 900  # 15 minutes
REFRESH_TOKEN_EXPIRY = 604800  # 7 days

def init_revocation_table():
    """Initialize revoked tokens table"""
    conn = sqlite3.connect('levqor.db')
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS revoked_tokens (
            jti TEXT PRIMARY KEY,
            ts REAL NOT NULL,
            revoked_at REAL DEFAULT (julianday('now'))
        )
    """)
    
    # Create index for efficient cleanup
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_revoked_tokens_ts 
        ON revoked_tokens(ts)
    """)
    conn.commit()
    conn.close()

def issue_token(email: str, refresh: bool = False) -> str:
    """
    Issue a JWT token (access or refresh)
    
    Args:
        email: User email
        refresh: If True, issue refresh token, else access token
    
    Returns:
        JWT token string
    """
    exp = time.time() + (REFRESH_TOKEN_EXPIRY if refresh else ACCESS_TOKEN_EXPIRY)
    payload = {
        "email": email,
        "exp": exp,
        "iat": time.time(),
        "refresh": refresh,
        "jti": str(uuid.uuid4())
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_token(token: str, refresh: bool = False) -> Optional[Dict[str, Any]]:
    """
    Verify and decode a JWT token
    
    Args:
        token: JWT token string
        refresh: If True, expect refresh token, else access token
    
    Returns:
        Decoded payload if valid, None otherwise
    """
    try:
        # Decode token
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        
        # Check token type matches
        if payload.get("refresh") != refresh:
            return None
        
        # Check if revoked
        conn = sqlite3.connect('levqor.db')
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM revoked_tokens WHERE jti = ?", (payload["jti"],))
        if cur.fetchone():
            conn.close()
            return None
        conn.close()
        
        return payload
    
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception as e:
        print(f"[!] Token verification error: {e}")
        return None

def revoke_token(jti: str, exp_time: float = None):
    """
    Revoke a token by its JTI
    
    Args:
        jti: JWT ID to revoke
        exp_time: Token expiration time (for cleanup)
    """
    conn = sqlite3.connect('levqor.db')
    cur = conn.cursor()
    ts = exp_time if exp_time else time.time() + REFRESH_TOKEN_EXPIRY
    cur.execute(
        "INSERT OR IGNORE INTO revoked_tokens (jti, ts) VALUES (?, ?)",
        (jti, ts)
    )
    conn.commit()
    conn.close()

def cleanup_expired_revocations():
    """Remove expired tokens from revocation list"""
    conn = sqlite3.connect('levqor.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM revoked_tokens WHERE ts < ?", (time.time(),))
    deleted = cur.rowcount
    conn.commit()
    conn.close()
    return deleted

def refresh_access_token(refresh_token: str) -> Optional[str]:
    """
    Exchange refresh token for new access token
    
    Args:
        refresh_token: Valid refresh token
    
    Returns:
        New access token if valid, None otherwise
    """
    payload = verify_token(refresh_token, refresh=True)
    if not payload:
        return None
    
    return issue_token(payload["email"], refresh=False)

# Initialize on import
init_revocation_table()
