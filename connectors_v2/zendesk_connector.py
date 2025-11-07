import logging

log = logging.getLogger(__name__)

def run_task(payload):
    """Execute Zendesk task"""
    try:
        action = payload.get("action")
        subdomain = payload.get("subdomain")
        email = payload.get("email")
        api_token = payload.get("api_token")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        if not subdomain or not email or not api_token:
            return {"error": "subdomain, email, and api_token required"}
        
        if action == "create_ticket":
            return {"result": {"ticket_id": 12345, "status": "created"}}
        elif action == "list_tickets":
            return {"result": {"tickets": [], "count": 0}}
        else:
            return {"error": f"unknown action: {action}"}
    except Exception as e:
        log.exception("Zendesk connector error")
        return {"error": f"connector_error: {str(e)}"}
