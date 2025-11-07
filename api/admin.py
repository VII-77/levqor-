"""
Admin API Module for Phase-5
Provides revenue dashboard endpoints and admin analytics
"""

import logging
from time import time
from flask import jsonify

log = logging.getLogger(__name__)

def get_db():
    """Import from run.py to avoid circular dependency"""
    from run import get_db as _get_db
    return _get_db()

def require_admin():
    """Import from api.partners to avoid circular dependency"""
    from api.partners import require_admin as _require_admin
    return _require_admin()

def get_revenue_stats():
    """
    GET /api/admin/revenue-stats
    Get comprehensive revenue statistics for admin dashboard
    """
    user, error = require_admin()
    if error:
        return error
    
    try:
        db = get_db()
        
        this_month_start = time() - (30 * 86400)
        last_month_start = time() - (60 * 86400)
        
        current_month_revenue = db.execute("""
            SELECT COALESCE(SUM(revenue_amount), 0)
            FROM partner_conversions
            WHERE created_at > ?
        """, (this_month_start,)).fetchone()[0]
        
        last_month_revenue = db.execute("""
            SELECT COALESCE(SUM(revenue_amount), 0)
            FROM partner_conversions
            WHERE created_at BETWEEN ? AND ?
        """, (last_month_start, this_month_start)).fetchone()[0]
        
        mrr = current_month_revenue
        arr = mrr * 12
        
        mrr_growth = 0
        if last_month_revenue > 0:
            mrr_growth = ((current_month_revenue - last_month_revenue) / last_month_revenue) * 100
        
        active_partners = db.execute("""
            SELECT COUNT(DISTINCT id)
            FROM partners
            WHERE status = 'active'
        """).fetchone()[0]
        
        new_partners_this_month = db.execute("""
            SELECT COUNT(*)
            FROM partners
            WHERE created_at > ?
        """, (this_month_start,)).fetchone()[0]
        
        pending_commissions = db.execute("""
            SELECT COALESCE(SUM(pending_commission), 0)
            FROM partners
        """).fetchone()[0]
        
        top_partners = db.execute("""
            SELECT 
                p.partner_code,
                p.total_referrals,
                p.total_revenue,
                p.total_commission,
                p.status
            FROM partners p
            WHERE p.total_revenue > 0
            ORDER BY p.total_revenue DESC
            LIMIT 10
        """).fetchall()
        
        recent_conversions = db.execute("""
            SELECT 
                c.created_at,
                p.partner_code,
                c.conversion_type,
                c.revenue_amount,
                c.commission_amount,
                c.status
            FROM partner_conversions c
            JOIN partners p ON c.partner_id = p.id
            ORDER BY c.created_at DESC
            LIMIT 20
        """).fetchall()
        
        return jsonify({
            "mrr": mrr,
            "arr": arr,
            "mrr_growth": round(mrr_growth, 2),
            "active_partners": active_partners,
            "partners_growth": new_partners_this_month,
            "pending_commissions": pending_commissions,
            "partners": [
                {
                    "code": p[0],
                    "referrals": p[1],
                    "revenue": p[2],
                    "commission": p[3],
                    "status": p[4]
                }
                for p in top_partners
            ],
            "conversions": [
                {
                    "date": c[0],
                    "partner_code": c[1],
                    "type": c[2],
                    "revenue": c[3],
                    "commission": c[4],
                    "status": c[5]
                }
                for c in recent_conversions
            ]
        }), 200
        
    except Exception as e:
        log.exception("Revenue stats error")
        return jsonify({"error": str(e)}), 500

def get_analytics_funnel():
    """
    GET /api/admin/analytics/funnel
    Get conversion funnel analytics
    """
    user, error = require_admin()
    if error:
        return error
    
    try:
        db = get_db()
        
        this_month_start = time() - (30 * 86400)
        
        total_visitors = db.execute("""
            SELECT COUNT(DISTINCT ref_code)
            FROM referrals
            WHERE created_at > ?
        """, (this_month_start,)).fetchone()[0]
        
        total_signups = db.execute("""
            SELECT COUNT(DISTINCT u.id)
            FROM users u
            WHERE u.created_at > ?
        """, (this_month_start,)).fetchone()[0]
        
        total_conversions = db.execute("""
            SELECT COUNT(*)
            FROM partner_conversions
            WHERE created_at > ?
        """, (this_month_start,)).fetchone()[0]
        
        paid_users = db.execute("""
            SELECT COUNT(DISTINCT u.id)
            FROM users u
            WHERE u.credits_remaining > 50 AND u.created_at > ?
        """, (this_month_start,)).fetchone()[0]
        
        visitor_to_signup = (total_signups / total_visitors * 100) if total_visitors > 0 else 0
        signup_to_paid = (paid_users / total_signups * 100) if total_signups > 0 else 0
        overall_conversion = (paid_users / total_visitors * 100) if total_visitors > 0 else 0
        
        return jsonify({
            "period": "30_days",
            "funnel": {
                "visitors": total_visitors,
                "signups": total_signups,
                "paid_users": paid_users,
                "conversions": total_conversions
            },
            "rates": {
                "visitor_to_signup": round(visitor_to_signup, 2),
                "signup_to_paid": round(signup_to_paid, 2),
                "overall_conversion": round(overall_conversion, 2)
            }
        }), 200
        
    except Exception as e:
        log.exception("Analytics funnel error")
        return jsonify({"error": str(e)}), 500

def get_cohort_analysis():
    """
    GET /api/admin/analytics/cohorts
    Get cohort retention and revenue analysis
    """
    user, error = require_admin()
    if error:
        return error
    
    try:
        db = get_db()
        
        cohorts = []
        for weeks_ago in range(8):
            week_start = time() - ((weeks_ago + 1) * 7 * 86400)
            week_end = time() - (weeks_ago * 7 * 86400)
            
            users_in_cohort = db.execute("""
                SELECT COUNT(*)
                FROM users
                WHERE created_at BETWEEN ? AND ?
            """, (week_start, week_end)).fetchone()[0]
            
            active_this_week = db.execute("""
                SELECT COUNT(DISTINCT user_id)
                FROM usage_daily
                WHERE user_id IN (
                    SELECT id FROM users WHERE created_at BETWEEN ? AND ?
                ) AND created_at > ?
            """, (week_start, week_end, time() - (7 * 86400))).fetchone()[0]
            
            retention = (active_this_week / users_in_cohort * 100) if users_in_cohort > 0 else 0
            
            cohorts.append({
                "week": f"Week {weeks_ago + 1}",
                "users": users_in_cohort,
                "active": active_this_week,
                "retention": round(retention, 2)
            })
        
        return jsonify({"cohorts": cohorts}), 200
        
    except Exception as e:
        log.exception("Cohort analysis error")
        return jsonify({"error": str(e)}), 500
