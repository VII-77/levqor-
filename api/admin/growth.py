"""
Growth intelligence API - funnel analytics and referral ROI tracking.
"""
from flask import Blueprint, request, jsonify
import os
import sqlite3
import time
import logging

logger = logging.getLogger("levqor.growth_admin")
bp = Blueprint("growth_admin", __name__)

def _check_auth(req):
    """Validate admin token"""
    auth_header = req.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip()
    admin_token = os.getenv("ADMIN_TOKEN", "")
    return token == admin_token and admin_token != ""

@bp.route("/api/admin/growth")
def growth_analytics():
    """
    GET /api/admin/growth
    
    Returns funnel metrics and ROI by source:
    - Visits → Signups → Paid conversions
    - Revenue by source
    - ARPU (Average Revenue Per User)
    - Conversion rates
    
    Requires: Authorization: Bearer $ADMIN_TOKEN
    """
    if not _check_auth(request):
        return jsonify({"error": "unauthorized"}), 401
    
    try:
        conn = sqlite3.connect("levqor.db")
        c = conn.cursor()
        
        # 30-day window for funnel analysis
        window_start = int(time.time()) - (30 * 86400)
        
        # Visits by source
        c.execute("""
            SELECT source, COUNT(*) 
            FROM growth_events 
            WHERE event='visit' AND ts > ? 
            GROUP BY source
        """, [window_start])
        visits = dict(c.fetchall())
        
        # Signups by source
        c.execute("""
            SELECT source, COUNT(*) 
            FROM growth_events 
            WHERE event='signup' AND ts > ? 
            GROUP BY source
        """, [window_start])
        signups = dict(c.fetchall())
        
        # Revenue by source
        c.execute("""
            SELECT source, SUM(revenue_cents) 
            FROM growth_events 
            WHERE event='paid' AND ts > ? 
            GROUP BY source
        """, [window_start])
        revenue_raw = c.fetchall()
        revenue = {k: int(v or 0) for k, v in revenue_raw}
        
        conn.close()
        
        # Build funnel analysis
        all_sources = set(list(visits.keys()) + list(signups.keys()) + list(revenue.keys()))
        funnel = []
        
        for source in all_sources:
            v = visits.get(source, 0)
            su = signups.get(source, 0)
            rev_cents = revenue.get(source, 0)
            rev_dollars = round(rev_cents / 100.0, 2)
            
            conv_rate = round((su / max(v, 1)) * 100, 2)
            arpu = round((rev_dollars / max(su, 1)), 2)
            
            funnel.append({
                "source": source,
                "visits": v,
                "signups": su,
                "conversion_pct": conv_rate,
                "revenue_usd": rev_dollars,
                "arpu_usd": arpu,
                "roi_proxy": round(rev_dollars / max(v, 1), 4)  # Revenue per visitor
            })
        
        # Sort by revenue descending
        funnel_sorted = sorted(funnel, key=lambda x: -x["revenue_usd"])
        
        # Calculate totals
        total_visits = sum(visits.values())
        total_signups = sum(signups.values())
        total_revenue = sum(revenue.values()) / 100.0
        
        return jsonify({
            "window_days": 30,
            "summary": {
                "total_visits": total_visits,
                "total_signups": total_signups,
                "total_revenue_usd": round(total_revenue, 2),
                "overall_conversion_pct": round((total_signups / max(total_visits, 1)) * 100, 2)
            },
            "sources": funnel_sorted
        })
        
    except Exception as e:
        logger.error(f"Growth analytics error: {e}")
        return jsonify({"error": str(e)}), 500
