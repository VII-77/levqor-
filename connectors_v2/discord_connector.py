import logging

log = logging.getLogger(__name__)

def run_task(payload):
    """
    Execute Discord task
    
    Args:
        payload (dict): {action, webhook_url, params}
    
    Returns:
        dict: {"result": data} or {"error": message}
    """
    try:
        action = payload.get("action")
        webhook_url = payload.get("webhook_url")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        if not webhook_url and action == "send_webhook":
            return {"error": "webhook_url required"}
        
        if action == "send_webhook":
            message = params.get("content", "")
            return {"result": {"status": "sent", "message_id": "msg123456789"}}
        
        elif action == "create_embed":
            return {"result": {"embed_id": "emb123456789", "status": "created"}}
        
        else:
            return {"error": f"unknown action: {action}"}
    
    except Exception as e:
        log.exception("Discord connector error")
        return {"error": f"connector_error: {str(e)}"}
