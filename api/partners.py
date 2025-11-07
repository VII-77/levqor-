"""
Partner/Affiliate API Module for Phase-5
Handles partner registration, stats, and commission management
"""

import uuid
import logging
from time import time
from flask import jsonify, request

log = logging.getLogger(__name__)

def get_db():
    """Import from run.py to avoid circular dependency"""
    from run import get_db as _get_db
    return _get_db()

def require_user():
    """Import from run.py to avoid circular dependency"""
    from run import require_user as _require_user
    return _require_user()

def require_admin():
    """Check if user is admin (for now, check if user has admin flag)"""
    user, error = require_user()
    if error:
        return None, error
    
    db = get_db()
    admin_check = db.execute(
        "SELECT is_admin FROM users WHERE id = ?",
        (user["user_id"],)
    ).fetchone()
    
    if not admin_check or not admin_check[0]:
        return None, (jsonify({"error": "admin_required"}), 403)
    
    return user, None

def create_partner():
    """
    POST /api/partners/create
    Create or upgrade user to partner status
    """
    user, error = require_user()
    if error:
        return error
    
    try:
        db = get_db()
        user_id = user["user_id"]
        
        existing = db.execute(
            "SELECT id FROM partners WHERE user_id = ?",
            (user_id,)
        ).fetchone()
        
        if existing:
            return jsonify({"error": "already_partner", "partner_id": existing[0]}), 400
        
        partner_id = str(uuid.uuid4())
        partner_code = f"LEVQOR-{uuid.uuid4().hex[:8].upper()}"
        now = time()
        
        db.execute("""
            INSERT INTO partners 
            (id, user_id, partner_code, commission_rate, total_referrals, 
             total_revenue, total_commission, paid_commission, pending_commission, 
             created_at, updated_at)
            VALUES (?, ?, ?, 0.20, 0, 0.0, 0.0, 0.0, 0.0, ?, ?)
        """, (partner_id, user_id, partner_code, now, now))
        
        db.commit()
        
        log.info(f"Partner created: {partner_id} for user {user_id}")
        
        return jsonify({
            "status": "ok",
            "partner_id": partner_id,
            "partner_code": partner_code,
            "commission_rate": 0.20
        }), 201
        
    except Exception as e:
        log.exception("Partner creation error")
        return jsonify({"error": str(e)}), 500

def get_partner_stats():
    """
    GET /api/partners/stats
    Get partner statistics and commission info
    """
    user, error = require_user()
    if error:
        return error
    
    try:
        db = get_db()
        user_id = user["user_id"]
        
        partner = db.execute("""
            SELECT id, partner_code, commission_rate, status, total_referrals,
                   total_revenue, total_commission, paid_commission, pending_commission,
                   created_at
            FROM partners WHERE user_id = ?
        """, (user_id,)).fetchone()
        
        if not partner:
            return jsonify({"error": "not_a_partner"}), 404
        
        partner_id = partner[0]
        
        recent_conversions = db.execute("""
            SELECT id, user_id, conversion_type, revenue_amount, commission_amount,
                   status, created_at
            FROM partner_conversions
            WHERE partner_id = ?
            ORDER BY created_at DESC
            LIMIT 10
        """, (partner_id,)).fetchall()
        
        this_month_start = time() - (30 * 86400)
        monthly_stats = db.execute("""
            SELECT 
                COUNT(*) as conversions,
                SUM(revenue_amount) as revenue,
                SUM(commission_amount) as commission
            FROM partner_conversions
            WHERE partner_id = ? AND created_at > ?
        """, (partner_id, this_month_start)).fetchone()
        
        return jsonify({
            "partner_code": partner[1],
            "commission_rate": partner[2],
            "status": partner[3],
            "lifetime": {
                "referrals": partner[4],
                "revenue": partner[5],
                "commission_earned": partner[6],
                "commission_paid": partner[7],
                "commission_pending": partner[8]
            },
            "this_month": {
                "conversions": monthly_stats[0] or 0,
                "revenue": monthly_stats[1] or 0.0,
                "commission": monthly_stats[2] or 0.0
            },
            "recent_conversions": [
                {
                    "id": c[0],
                    "user_id": c[1],
                    "type": c[2],
                    "revenue": c[3],
                    "commission": c[4],
                    "status": c[5],
                    "date": c[6]
                }
                for c in recent_conversions
            ]
        }), 200
        
    except Exception as e:
        log.exception("Partner stats error")
        return jsonify({"error": str(e)}), 500

def get_partner_dashboard():
    """
    GET /api/partners/dashboard
    Get partner-specific dashboard data with conversion funnel
    """
    user, error = require_user()
    if error:
        return error
    
    try:
        db = get_db()
        user_id = user["user_id"]
        
        partner = db.execute(
            "SELECT id, partner_code FROM partners WHERE user_id = ?",
            (user_id,)
        ).fetchone()
        
        if not partner:
            return jsonify({"error": "not_a_partner"}), 404
        
        partner_id = partner[0]
        partner_code = partner[1]
        
        total_clicks = db.execute("""
            SELECT COUNT(*) FROM referrals 
            WHERE referrer_user_id = ?
        """, (user_id,)).fetchone()[0]
        
        total_signups = db.execute("""
            SELECT COUNT(DISTINCT r.referee_email)
            FROM referrals r
            JOIN users u ON r.referee_email = u.email
            WHERE r.referrer_user_id = ?
        """, (user_id,)).fetchone()[0]
        
        total_conversions = db.execute("""
            SELECT COUNT(*) FROM partner_conversions
            WHERE partner_id = ?
        """, (partner_id,)).fetchone()[0]
        
        conversion_rate = (total_conversions / total_signups * 100) if total_signups > 0 else 0
        
        return jsonify({
            "partner_code": partner_code,
            "funnel": {
                "clicks": total_clicks,
                "signups": total_signups,
                "conversions": total_conversions,
                "conversion_rate": round(conversion_rate, 2)
            },
            "share_link": f"https://levqor.ai?ref={partner_code}"
        }), 200
        
    except Exception as e:
        log.exception("Partner dashboard error")
        return jsonify({"error": str(e)}), 500

def record_conversion(partner_code, user_id, conversion_type, revenue_amount):
    """
    Internal function to record a conversion when a referred user makes a purchase
    Called from Stripe webhook handler
    """
    try:
        db = get_db()
        
        partner = db.execute(
            "SELECT id, commission_rate FROM partners WHERE partner_code = ?",
            (partner_code,)
        ).fetchone()
        
        if not partner:
            log.warning(f"Partner not found for code: {partner_code}")
            return False
        
        partner_id = partner[0]
        commission_rate = partner[1]
        commission_amount = revenue_amount * commission_rate
        
        conversion_id = str(uuid.uuid4())
        now = time()
        
        db.execute("""
            INSERT INTO partner_conversions
            (id, partner_id, user_id, conversion_type, revenue_amount, 
             commission_amount, commission_rate, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)
        """, (conversion_id, partner_id, user_id, conversion_type, 
              revenue_amount, commission_amount, commission_rate, now))
        
        db.execute("""
            UPDATE partners
            SET total_revenue = total_revenue + ?,
                total_commission = total_commission + ?,
                pending_commission = pending_commission + ?,
                total_referrals = total_referrals + 1,
                updated_at = ?
            WHERE id = ?
        """, (revenue_amount, commission_amount, commission_amount, now, partner_id))
        
        db.commit()
        
        log.info(f"Conversion recorded: partner={partner_id}, revenue=${revenue_amount}, commission=${commission_amount}")
        return True
        
    except Exception as e:
        log.exception("Conversion recording error")
        return False

def process_payout():
    """
    POST /api/partners/payout
    Admin endpoint to process partner payouts
    """
    user, error = require_admin()
    if error:
        return error
    
    body = request.get_json(silent=True) or {}
    partner_id = body.get("partner_id")
    
    if not partner_id:
        return jsonify({"error": "partner_id required"}), 400
    
    try:
        db = get_db()
        
        partner = db.execute("""
            SELECT pending_commission, user_id 
            FROM partners WHERE id = ?
        """, (partner_id,)).fetchone()
        
        if not partner:
            return jsonify({"error": "partner_not_found"}), 404
        
        pending = partner[0]
        
        if pending < 50:
            return jsonify({"error": "minimum_payout_not_met", "minimum": 50, "pending": pending}), 400
        
        payout_id = str(uuid.uuid4())
        now = time()
        
        db.execute("""
            INSERT INTO partner_payouts
            (id, partner_id, amount, status, created_at)
            VALUES (?, ?, ?, 'pending', ?)
        """, (payout_id, partner_id, pending, now))
        
        db.execute("""
            UPDATE partners
            SET pending_commission = 0,
                paid_commission = paid_commission + ?,
                updated_at = ?
            WHERE id = ?
        """, (pending, now, partner_id))
        
        db.execute("""
            UPDATE partner_conversions
            SET status = 'paid', paid_at = ?
            WHERE partner_id = ? AND status = 'pending'
        """, (now, partner_id))
        
        db.commit()
        
        log.info(f"Payout created: {payout_id} for partner {partner_id}, amount ${pending}")
        
        return jsonify({
            "status": "ok",
            "payout_id": payout_id,
            "amount": pending,
            "message": "Payout initiated. Funds will be transferred within 2-3 business days."
        }), 200
        
    except Exception as e:
        log.exception("Payout processing error")
        return jsonify({"error": str(e)}), 500
