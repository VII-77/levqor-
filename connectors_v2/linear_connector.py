import logging

log = logging.getLogger(__name__)

def run_task(payload):
    """Execute Linear task"""
    try:
        action = payload.get("action")
        api_key = payload.get("api_key")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        if not api_key:
            return {"error": "api_key required"}
        
        if action == "create_issue":
            return {"result": {"issue_id": "LIN-123", "status": "created"}}
        elif action == "list_teams":
            return {"result": {"teams": [], "count": 0}}
        else:
            return {"error": f"unknown action: {action}"}
    except Exception as e:
        log.exception("Linear connector error")
        return {"error": f"connector_error: {str(e)}"}
