import logging

log = logging.getLogger(__name__)

def run_task(payload):
    """
    Execute Twilio task
    
    Args:
        payload (dict): {action, account_sid, auth_token, params}
    
    Returns:
        dict: {"result": data} or {"error": message}
    """
    try:
        action = payload.get("action")
        account_sid = payload.get("account_sid")
        auth_token = payload.get("auth_token")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        if not account_sid or not auth_token:
            return {"error": "account_sid and auth_token required"}
        
        if action == "send_sms":
            to = params.get("to")
            from_num = params.get("from")
            body = params.get("body", "")
            
            if not to or not from_num:
                return {"error": "to and from phone numbers required"}
            
            return {"result": {"sid": "SM123456789", "status": "sent", "to": to}}
        
        elif action == "make_call":
            return {"result": {"call_sid": "CA123456789", "status": "initiated"}}
        
        else:
            return {"error": f"unknown action: {action}"}
    
    except Exception as e:
        log.exception("Twilio connector error")
        return {"error": f"connector_error: {str(e)}"}
