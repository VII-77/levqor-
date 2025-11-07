"""
GDPR User Deletion Endpoint
Allows users to request account deletion for compliance
"""
from flask import Blueprint, request, jsonify
import sqlite3
import os

bp = Blueprint("user_delete", __name__)

@bp.route("/api/user/delete", methods=["POST"])
def delete_user():
    """
    Delete user account and all associated data (GDPR compliance)
    Requires authentication token
    """
    token = request.headers.get("Authorization")
    if not token:
        return jsonify(error="unauthorized"), 401
    
    data = request.get_json()
    if not data or "email" not in data:
        return jsonify(error="missing email"), 400
    
    email = data.get("email")
    
    try:
        conn = sqlite3.connect('levqor.db')
        cursor = conn.cursor()
        
        # Verify user exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return jsonify(error="user not found"), 404
        
        user_id = user[0]
        
        # Delete user data from all tables
        cursor.execute("DELETE FROM metrics WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM referrals WHERE referrer_user_id = ?", (user_id,))
        cursor.execute("DELETE FROM referrals WHERE referred_user_id = ?", (user_id,))
        cursor.execute("DELETE FROM usage_daily WHERE user_id = ?", (user_id,))
        
        # Delete partner data if exists
        cursor.execute("SELECT id FROM partners WHERE user_id = ?", (user_id,))
        partner = cursor.fetchone()
        if partner:
            partner_id = partner[0]
            cursor.execute("DELETE FROM partner_conversions WHERE partner_id = ?", (partner_id,))
            cursor.execute("DELETE FROM partner_payouts WHERE partner_id = ?", (partner_id,))
            cursor.execute("DELETE FROM partners WHERE id = ?", (partner_id,))
        
        # Finally delete user
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify(status="deleted", email=email, message="All user data removed")
    
    except Exception as e:
        return jsonify(error=str(e)), 500
