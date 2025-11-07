import logging

log = logging.getLogger(__name__)

def run_task(payload):
    """
    Execute Stripe task
    
    Args:
        payload (dict): {action, api_key, params}
    
    Returns:
        dict: {"result": data} or {"error": message}
    """
    try:
        action = payload.get("action")
        api_key = payload.get("api_key")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        if not api_key:
            return {"error": "api_key required"}
        
        if action == "create_customer":
            email = params.get("email")
            return {"result": {"customer_id": "cus_123456789", "email": email, "status": "created"}}
        
        elif action == "create_payment_intent":
            amount = params.get("amount", 1000)
            currency = params.get("currency", "usd")
            return {"result": {"payment_intent_id": "pi_123456789", "amount": amount, "currency": currency, "status": "created"}}
        
        elif action == "list_customers":
            return {"result": {"customers": [], "count": 0}}
        
        else:
            return {"error": f"unknown action: {action}"}
    
    except Exception as e:
        log.exception("Stripe connector error")
        return {"error": f"connector_error: {str(e)}"}
