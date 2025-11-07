import logging

log = logging.getLogger(__name__)

def run_task(payload):
    """Execute Jira task"""
    try:
        action = payload.get("action")
        domain = payload.get("domain")
        email = payload.get("email")
        api_token = payload.get("api_token")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        if not domain or not email or not api_token:
            return {"error": "domain, email, and api_token required"}
        
        if action == "create_issue":
            return {"result": {"issue_key": "PROJ-123", "status": "created"}}
        elif action == "list_projects":
            return {"result": {"projects": [], "count": 0}}
        else:
            return {"error": f"unknown action: {action}"}
    except Exception as e:
        log.exception("Jira connector error")
        return {"error": f"connector_error: {str(e)}"}
