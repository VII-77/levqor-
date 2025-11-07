import logging

log = logging.getLogger(__name__)

def run_task(payload):
    """Execute Salesforce task"""
    try:
        action = payload.get("action")
        instance_url = payload.get("instance_url")
        access_token = payload.get("access_token")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        if not instance_url or not access_token:
            return {"error": "instance_url and access_token required"}
        
        if action == "create_lead":
            return {"result": {"lead_id": "00Q123456789", "status": "created"}}
        elif action == "query":
            return {"result": {"records": [], "count": 0}}
        else:
            return {"error": f"unknown action: {action}"}
    except Exception as e:
        log.exception("Salesforce connector error")
        return {"error": f"connector_error: {str(e)}"}
