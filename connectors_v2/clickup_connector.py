import logging

log = logging.getLogger(__name__)

def run_task(payload):
    """Execute ClickUp task"""
    try:
        action = payload.get("action")
        api_key = payload.get("api_key")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        if not api_key:
            return {"error": "api_key required"}
        
        if action == "create_task":
            return {"result": {"task_id": "task123", "status": "created"}}
        elif action == "list_spaces":
            return {"result": {"spaces": [], "count": 0}}
        else:
            return {"error": f"unknown action: {action}"}
    except Exception as e:
        log.exception("ClickUp connector error")
        return {"error": f"connector_error: {str(e)}"}
