"""
Admin Refund Endpoint
Allows admins to process Stripe refunds for customer service
"""
from flask import Blueprint, request, jsonify
import stripe
import os

bp = Blueprint("refund", __name__)

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@bp.route("/api/admin/refund", methods=["POST"])
def process_refund():
    """
    Process a Stripe refund (admin only)
    Requires ADMIN_TOKEN in Authorization header
    """
    # Check admin authorization
    admin_token = os.getenv("ADMIN_TOKEN")
    auth_header = request.headers.get("Authorization", "")
    
    if not admin_token or auth_header != f"Bearer {admin_token}":
        return jsonify(error="unauthorized - admin access required"), 401
    
    data = request.get_json()
    if not data:
        return jsonify(error="missing request body"), 400
    
    # Get charge ID or payment intent ID
    charge_id = data.get("charge_id")
    payment_intent_id = data.get("payment_intent_id")
    amount = data.get("amount")  # Optional partial refund
    reason = data.get("reason", "requested_by_customer")
    
    if not charge_id and not payment_intent_id:
        return jsonify(error="missing charge_id or payment_intent_id"), 400
    
    try:
        # Create refund parameters
        refund_params = {}
        
        if charge_id:
            refund_params["charge"] = charge_id
        elif payment_intent_id:
            refund_params["payment_intent"] = payment_intent_id
        
        if amount:
            refund_params["amount"] = int(amount)  # Amount in cents
        
        refund_params["reason"] = reason
        
        # Process refund
        refund = stripe.Refund.create(**refund_params)
        
        return jsonify(
            status="success",
            refund_id=refund.id,
            amount=refund.amount / 100,  # Convert to dollars
            currency=refund.currency,
            status_detail=refund.status,
            reason=refund.reason
        )
    
    except stripe.error.InvalidRequestError as e:
        return jsonify(error=f"Invalid request: {str(e)}"), 400
    except stripe.error.StripeError as e:
        return jsonify(error=f"Stripe error: {str(e)}"), 500
    except Exception as e:
        return jsonify(error=f"Server error: {str(e)}"), 500

@bp.route("/api/admin/refunds", methods=["GET"])
def list_refunds():
    """
    List recent refunds (admin only)
    """
    admin_token = os.getenv("ADMIN_TOKEN")
    auth_header = request.headers.get("Authorization", "")
    
    if not admin_token or auth_header != f"Bearer {admin_token}":
        return jsonify(error="unauthorized - admin access required"), 401
    
    try:
        limit = request.args.get("limit", 10, type=int)
        refunds = stripe.Refund.list(limit=limit)
        
        return jsonify(
            refunds=[
                {
                    "id": r.id,
                    "amount": r.amount / 100,
                    "currency": r.currency,
                    "status": r.status,
                    "reason": r.reason,
                    "created": r.created
                }
                for r in refunds.data
            ]
        )
    
    except Exception as e:
        return jsonify(error=str(e)), 500
