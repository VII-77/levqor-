"""
Admin API: Profitability ledger
Shows revenue, costs, partner payouts, and net profitability
"""
from flask import Blueprint, jsonify, request
import sqlite3
import os
import logging

logger = logging.getLogger("levqor.ledger")
bp = Blueprint("ledger", __name__)


def _is_authorized(req):
    """Check if request has valid admin token"""
    token = (req.headers.get("Authorization") or "").replace("Bearer ", "")
    admin_token = os.getenv("ADMIN_TOKEN", "")
    return token and token == admin_token


@bp.get("/api/admin/ledger")
def get_ledger():
    """
    GET /api/admin/ledger
    
    Requires: Authorization: Bearer <ADMIN_TOKEN>
    
    Returns profitability breakdown:
    - Revenue (Stripe)
    - OpenAI costs
    - Infrastructure costs
    - Partner payouts (20% of conversions)
    - Net profitability
    """
    if not _is_authorized(request):
        return jsonify({"error": "unauthorized"}), 401
    
    try:
        conn = sqlite3.connect("levqor.db")
        cursor = conn.cursor()
        
        # Get partner conversions (if table exists)
        try:
            cursor.execute("SELECT SUM(amount) FROM partner_conversions")
            partner_gross = cursor.fetchone()[0] or 0.0
        except sqlite3.OperationalError:
            partner_gross = 0.0
        
        # Get costs and revenue from KV store
        def get_kv(key, default):
            try:
                cursor.execute("SELECT value FROM kv WHERE key=?", (key,))
                row = cursor.fetchone()
                return float(row[0]) if row else default
            except (sqlite3.OperationalError, ValueError, TypeError):
                return default
        
        openai_cost = get_kv("openai_cost_30d", 0.0)
        infra_cost = get_kv("infra_cost_30d", 20.0)
        stripe_revenue = get_kv("stripe_revenue_30d", 1.0)
        
        # Calculate partner payouts (20% of conversions)
        pending_partner = round(partner_gross * 0.20, 2)
        
        # Calculate net profitability
        total_costs = openai_cost + infra_cost + pending_partner
        net = round(stripe_revenue - total_costs, 2)
        
        conn.close()
        
        return jsonify({
            "revenue_30d": stripe_revenue,
            "openai_cost_30d": openai_cost,
            "infra_cost_30d": infra_cost,
            "partner_payouts_pending": pending_partner,
            "total_costs_30d": round(total_costs, 2),
            "net_30d": net,
            "margin_pct": round((net / stripe_revenue * 100) if stripe_revenue > 0 else 0, 1)
        })
    
    except Exception as e:
        logger.exception("Ledger query failed")
        return jsonify({"error": "internal_error"}), 500
