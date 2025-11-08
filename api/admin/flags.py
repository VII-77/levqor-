"""
Admin API: Database-backed feature flags
"""
from flask import Blueprint, jsonify, request
import sqlite3
import os
import logging
from datetime import datetime

logger = logging.getLogger("levqor.flags")
bp = Blueprint("flags_admin", __name__)


def _is_authorized(req):
    """Check if request has valid admin token"""
    token = (req.headers.get("Authorization") or "").replace("Bearer ", "")
    admin_token = os.getenv("ADMIN_TOKEN", "")
    return token and token == admin_token


@bp.get("/api/admin/flags")
def get_flags():
    """
    GET /api/admin/flags
    
    Requires: Authorization: Bearer <ADMIN_TOKEN>
    
    Returns all feature flags
    """
    if not _is_authorized(request):
        return jsonify({"error": "unauthorized"}), 401
    
    try:
        conn = sqlite3.connect("levqor.db")
        cursor = conn.cursor()
        cursor.execute("SELECT key, value, updated_at FROM feature_flags ORDER BY key")
        
        flags = {
            row[0]: {
                "value": row[1],
                "updated_at": row[2]
            }
            for row in cursor.fetchall()
        }
        
        conn.close()
        
        return jsonify(flags)
    
    except Exception as e:
        logger.exception("Failed to fetch flags")
        return jsonify({"error": "internal_error"}), 500


@bp.post("/api/admin/flags")
def set_flag():
    """
    POST /api/admin/flags
    
    Requires: Authorization: Bearer <ADMIN_TOKEN>
    
    Body: {"key": "FLAG_NAME", "value": "true/false"}
    
    Updates or creates a feature flag
    """
    if not _is_authorized(request):
        return jsonify({"error": "unauthorized"}), 401
    
    try:
        data = request.get_json(force=True)
        key = data.get("key")
        value = data.get("value")
        
        if not key:
            return jsonify({"error": "bad_request", "message": "key required"}), 400
        
        conn = sqlite3.connect("levqor.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO feature_flags (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                updated_at = CURRENT_TIMESTAMP
        """, (key, str(value)))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Feature flag updated: {key}={value}")
        
        return jsonify({"ok": True, "key": key, "value": value})
    
    except Exception as e:
        logger.exception("Failed to set flag")
        return jsonify({"error": "internal_error"}), 500


def get_flag(key, default="false"):
    """
    Helper function to read a feature flag from database.
    
    Args:
        key: Flag name
        default: Default value if flag doesn't exist
    
    Returns:
        bool: True if flag value is "true" (case-insensitive)
    """
    try:
        conn = sqlite3.connect("levqor.db")
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM feature_flags WHERE key=?", (key,))
        row = cursor.fetchone()
        conn.close()
        
        value = row[0] if row else default
        return value.lower() == "true"
    
    except Exception as e:
        logger.warning(f"Failed to read flag {key}: {e}")
        return default.lower() == "true"
