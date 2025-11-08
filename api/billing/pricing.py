"""
Billing API: Adaptive pricing model endpoint
"""
from flask import Blueprint, jsonify, request
from services.pricing_model import suggest_price
import logging

logger = logging.getLogger("levqor.billing")
bp = Blueprint("pricing_model", __name__)


@bp.get("/billing/pricing/model")
def pricing_model():
    """
    GET /billing/pricing/model
    
    Query params:
        runs: Monthly job runs (default: 0)
        p95: P95 latency in ms (default: 120)
        oc: OpenAI costs (default: 0)
        ic: Infrastructure costs (default: 20)
        rf: Refunds (default: 0)
    
    Returns suggested pricing with rationale
    """
    try:
        runs = int(float(request.args.get("runs", "0")))
        p95 = float(request.args.get("p95", "120"))
        oc = float(request.args.get("oc", "0"))
        ic = float(request.args.get("ic", "20"))
        rf = float(request.args.get("rf", "0"))
        
        price, rationale = suggest_price(runs, p95, oc, ic, rf)
        
        return jsonify({
            "status": "ok",
            "price": price,
            "rationale": rationale
        })
    
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid pricing request: {e}")
        return jsonify({
            "status": "error",
            "error": "bad_request",
            "message": "Invalid parameter format"
        }), 400
    
    except Exception as e:
        logger.exception("Pricing model error")
        return jsonify({
            "status": "error",
            "error": "internal_error"
        }), 500
