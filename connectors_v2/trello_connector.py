import logging

log = logging.getLogger(__name__)

def run_task(payload):
    """Execute Trello task"""
    try:
        action = payload.get("action")
        api_key = payload.get("api_key")
        token = payload.get("token")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        if not api_key or not token:
            return {"error": "api_key and token required"}
        
        if action == "create_card":
            return {"result": {"card_id": "abc123", "status": "created"}}
        elif action == "list_boards":
            return {"result": {"boards": [], "count": 0}}
        else:
            return {"error": f"unknown action: {action}"}
    except Exception as e:
        log.exception("Trello connector error")
        return {"error": f"connector_error: {str(e)}"}
