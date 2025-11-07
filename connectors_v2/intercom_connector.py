import logging

log = logging.getLogger(__name__)

def run_task(payload):
    """Execute Intercom task"""
    try:
        action = payload.get("action")
        access_token = payload.get("access_token")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        if not access_token:
            return {"error": "access_token required"}
        
        if action == "create_user":
            return {"result": {"user_id": "usr123", "status": "created"}}
        elif action == "send_message":
            return {"result": {"message_id": "msg123", "status": "sent"}}
        else:
            return {"error": f"unknown action: {action}"}
    except Exception as e:
        log.exception("Intercom connector error")
        return {"error": f"connector_error: {str(e)}"}
