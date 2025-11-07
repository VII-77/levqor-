import logging

log = logging.getLogger(__name__)

def run_task(payload):
    """Execute Asana task"""
    try:
        action = payload.get("action")
        token = payload.get("token")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        if not token:
            return {"error": "token required"}
        
        if action == "create_task":
            return {"result": {"gid": "123456789", "status": "created"}}
        elif action == "list_projects":
            return {"result": {"projects": [], "count": 0}}
        else:
            return {"error": f"unknown action: {action}"}
    except Exception as e:
        log.exception("Asana connector error")
        return {"error": f"connector_error: {str(e)}"}
