"""
Dynamic discount system - Creates and manages promotional discount codes.
Flag-gated by PRICING_AUTO_APPLY.
"""
from flask import Blueprint, request, jsonify
import os
import sqlite3
import time
import random
import string
import logging

logger = logging.getLogger("levqor.discounts")
bp = Blueprint("discounts", __name__)

def _check_admin(req):
    """Validate admin token"""
    auth_header = req.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip()
    admin_token = os.getenv("ADMIN_TOKEN", "")
    return token == admin_token and admin_token != ""

def _get_flag(key: str, default: str = "false") -> str:
    """Get feature flag value from database"""
    try:
        conn = sqlite3.connect("levqor.db")
        c = conn.cursor()
        c.execute("SELECT value FROM feature_flags WHERE key = ?", [key])
        row = c.fetchone()
        conn.close()
        return row[0] if row else default
    except:
        return default

def _pricing_auto_apply_enabled() -> bool:
    """Check if PRICING_AUTO_APPLY flag is enabled"""
    return _get_flag("PRICING_AUTO_APPLY", "false").lower() == "true"

@bp.route("/billing/discounts/preview")
def preview_discount():
    """
    GET /billing/discounts/preview
    
    Analyzes recent signups and suggests a discount if conversions are low.
    
    Returns:
    - suggested_pct: Discount percentage
    - duration_days: How long the code should be valid
    - reason: Why this discount is suggested
    """
    try:
        conn = sqlite3.connect("levqor.db")
        c = conn.cursor()
        
        # Check signups in last 7 days
        week_ago = int(time.time()) - (7 * 86400)
        c.execute("""
            SELECT COUNT(*) FROM growth_events 
            WHERE event='signup' AND ts > ?
        """, [week_ago])
        recent_signups = c.fetchone()[0]
        
        # Check conversions in last 7 days
        c.execute("""
            SELECT COUNT(*) FROM growth_events 
            WHERE event='paid' AND ts > ?
        """, [week_ago])
        recent_conversions = c.fetchone()[0]
        
        conn.close()
        
        # Suggest discount based on activity
        if recent_signups < 5:
            suggestion = {
                "suggested_pct": 15,
                "duration_days": 14,
                "reason": "low_signups",
                "note": "Less than 5 signups in 7 days - boost acquisition"
            }
        elif recent_conversions < 2:
            suggestion = {
                "suggested_pct": 10,
                "duration_days": 7,
                "reason": "low_conversions",
                "note": "Low conversion rate - incentivize trials"
            }
        else:
            suggestion = {
                "suggested_pct": 5,
                "duration_days": 30,
                "reason": "healthy_growth",
                "note": "Steady growth - maintain momentum"
            }
        
        suggestion["auto_apply_enabled"] = _pricing_auto_apply_enabled()
        
        return jsonify(suggestion)
        
    except Exception as e:
        logger.error(f"Discount preview error: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route("/billing/discounts/create", methods=["POST"])
def create_discount():
    """
    POST /billing/discounts/create
    
    Create a new discount code.
    
    Body:
    {
        "pct": 10,           // Discount percentage
        "days": 7,           // Validity duration in days
        "reason": "promo"    // Reason for discount
    }
    
    Requires: Authorization: Bearer $ADMIN_TOKEN
    
    Returns:
    {
        "code": "LEVQOR-ABC12345",
        "pct": 10,
        "expires_ts": 1234567890,
        "auto_apply": false
    }
    """
    if not _check_admin(request):
        return jsonify({"error": "unauthorized"}), 401
    
    try:
        body = request.get_json(force=True)
        pct = int(body.get("pct", 10))
        days = int(body.get("days", 7))
        reason = body.get("reason", "manual")
        
        # Validate percentage
        if pct < 0 or pct > 100:
            return jsonify({"error": "percentage must be 0-100"}), 400
        
        # Generate unique code
        code = "LEVQOR-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        expires_ts = int(time.time() + (days * 86400))
        
        # Store in database
        conn = sqlite3.connect("levqor.db")
        conn.execute("""
            INSERT OR REPLACE INTO discounts 
            (code, kind, pct, expires_ts, reason, active) 
            VALUES (?, ?, ?, ?, ?, 1)
        """, [code, "percent", pct, expires_ts, reason])
        conn.commit()
        conn.close()
        
        logger.info(f"Created discount code: {code} ({pct}% off, {days} days)")
        
        return jsonify({
            "code": code,
            "pct": pct,
            "expires_ts": expires_ts,
            "expires_in_days": days,
            "reason": reason,
            "auto_apply": _pricing_auto_apply_enabled(),
            "status": "created"
        })
        
    except Exception as e:
        logger.error(f"Discount creation error: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route("/billing/discounts/active")
def active_discounts():
    """
    GET /billing/discounts/active
    
    List all active discount codes that haven't expired.
    
    Returns:
    {
        "codes": [
            {
                "code": "LEVQOR-ABC12345",
                "pct": 10,
                "expires_ts": 1234567890,
                "reason": "promo"
            }
        ]
    }
    """
    try:
        conn = sqlite3.connect("levqor.db")
        c = conn.cursor()
        
        now = int(time.time())
        c.execute("""
            SELECT code, kind, pct, expires_ts, reason
            FROM discounts
            WHERE active = 1 AND expires_ts > ?
            ORDER BY expires_ts DESC
        """, [now])
        
        codes = []
        for row in c.fetchall():
            codes.append({
                "code": row[0],
                "kind": row[1],
                "pct": row[2],
                "expires_ts": row[3],
                "reason": row[4]
            })
        
        conn.close()
        
        return jsonify({
            "codes": codes,
            "count": len(codes)
        })
        
    except Exception as e:
        logger.error(f"Active discounts error: {e}")
        return jsonify({"error": str(e)}), 500
