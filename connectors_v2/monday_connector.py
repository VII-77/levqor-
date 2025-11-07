import logging

log = logging.getLogger(__name__)

def run_task(payload):
    """Execute Monday.com task"""
    try:
        action = payload.get("action")
        api_key = payload.get("api_key")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        if not api_key:
            return {"error": "api_key required"}
        
        if action == "create_item":
            return {"result": {"item_id": "123456", "status": "created"}}
        elif action == "list_boards":
            return {"result": {"boards": [], "count": 0}}
        else:
            return {"error": f"unknown action: {action}"}
    except Exception as e:
        log.exception("Monday connector error")
        return {"error": f"connector_error: {str(e)}"}
