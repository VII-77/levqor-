"""
DSAR (Data Subject Access Request) Export Endpoint
GDPR Article 15 - Right to Access Personal Data
"""
from flask import Blueprint, request, jsonify
import sqlite3
import json
from datetime import datetime

bp = Blueprint("export_user_data", __name__)

def get_user_data(email: str) -> dict:
    """
    Retrieve all user data for DSAR compliance
    
    Args:
        email: User email address
    
    Returns:
        Complete user data export
    """
    conn = sqlite3.connect('levqor.db')
    conn.row_factory = sqlite3.Row  # Enable column access by name
    cur = conn.cursor()
    
    export_data = {
        "export_timestamp": datetime.utcnow().isoformat(),
        "email": email,
        "user_profile": None,
        "partner_profile": None,
        "metrics": [],
        "referrals": [],
        "partner_conversions": [],
        "partner_payouts": [],
        "usage_history": []
    }
    
    # Get user profile
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    
    if not user:
        conn.close()
        return {"error": "User not found"}
    
    export_data["user_profile"] = dict(user)
    user_id = user["id"]
    
    # Get partner profile if exists
    cur.execute("SELECT * FROM partners WHERE user_id = ?", (user_id,))
    partner = cur.fetchone()
    if partner:
        export_data["partner_profile"] = dict(partner)
        partner_id = partner["id"]
        
        # Get partner conversions
        cur.execute("""
            SELECT * FROM partner_conversions 
            WHERE partner_id = ?
            ORDER BY created_at DESC
        """, (partner_id,))
        export_data["partner_conversions"] = [dict(row) for row in cur.fetchall()]
        
        # Get partner payouts
        cur.execute("""
            SELECT * FROM partner_payouts 
            WHERE partner_id = ?
            ORDER BY created_at DESC
        """, (partner_id,))
        export_data["partner_payouts"] = [dict(row) for row in cur.fetchall()]
    
    # Get metrics
    cur.execute("""
        SELECT * FROM metrics 
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 1000
    """, (user_id,))
    export_data["metrics"] = [dict(row) for row in cur.fetchall()]
    
    # Get referrals (both as referrer and referred)
    cur.execute("""
        SELECT * FROM referrals 
        WHERE referrer_user_id = ? OR referred_user_id = ?
        ORDER BY created_at DESC
    """, (user_id, user_id))
    export_data["referrals"] = [dict(row) for row in cur.fetchall()]
    
    # Get usage history
    cur.execute("""
        SELECT * FROM usage_daily 
        WHERE user_id = ?
        ORDER BY date DESC
        LIMIT 365
    """, (user_id,))
    export_data["usage_history"] = [dict(row) for row in cur.fetchall()]
    
    conn.close()
    
    # Add summary stats
    export_data["summary"] = {
        "total_metrics": len(export_data["metrics"]),
        "total_referrals": len(export_data["referrals"]),
        "is_partner": export_data["partner_profile"] is not None,
        "total_conversions": len(export_data["partner_conversions"]),
        "total_payouts": len(export_data["partner_payouts"])
    }
    
    return export_data

@bp.route("/api/user/export", methods=["POST"])
def export_user():
    """
    Export all user data (GDPR DSAR compliance)
    
    Request:
        {
            "email": "user@example.com"
        }
    
    Returns:
        Complete user data export in JSON format
    """
    # Require authentication
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "unauthorized"}), 401
    
    data = request.get_json()
    if not data or "email" not in data:
        return jsonify({"error": "missing email"}), 400
    
    email = data.get("email")
    
    # Get user data
    export_data = get_user_data(email)
    
    if "error" in export_data:
        return jsonify(export_data), 404
    
    # Return as downloadable JSON
    response = jsonify(export_data)
    response.headers["Content-Disposition"] = f"attachment; filename=levqor_data_export_{email}_{datetime.utcnow().strftime('%Y%m%d')}.json"
    
    return response

@bp.route("/api/user/export/summary", methods=["POST"])
def export_summary():
    """
    Get summary of exportable data (lightweight check)
    """
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "unauthorized"}), 401
    
    data = request.get_json()
    if not data or "email" not in data:
        return jsonify({"error": "missing email"}), 400
    
    export_data = get_user_data(data["email"])
    
    if "error" in export_data:
        return jsonify(export_data), 404
    
    # Return only summary
    return jsonify({
        "email": export_data["email"],
        "summary": export_data["summary"],
        "export_timestamp": export_data["export_timestamp"]
    })
