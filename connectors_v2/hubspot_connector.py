import logging

log = logging.getLogger(__name__)

def run_task(payload):
    """Execute HubSpot task"""
    try:
        action = payload.get("action")
        api_key = payload.get("api_key")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        if not api_key:
            return {"error": "api_key required"}
        
        if action == "create_contact":
            return {"result": {"vid": 12345, "status": "created"}}
        elif action == "list_contacts":
            return {"result": {"contacts": [], "count": 0}}
        else:
            return {"error": f"unknown action: {action}"}
    except Exception as e:
        log.exception("HubSpot connector error")
        return {"error": f"connector_error: {str(e)}"}
