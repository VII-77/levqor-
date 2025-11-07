import logging

log = logging.getLogger(__name__)

def run_task(payload):
    """
    Execute Airtable task
    
    Args:
        payload (dict): {action, api_key, base_id, params}
    
    Returns:
        dict: {"result": data} or {"error": message}
    """
    try:
        action = payload.get("action")
        api_key = payload.get("api_key")
        base_id = payload.get("base_id")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        if not api_key:
            return {"error": "api_key required"}
        if not base_id and action != "list_bases":
            return {"error": "base_id required"}
        
        if action == "list_records":
            table_name = params.get("table_name", "Table 1")
            return {"result": {"records": [], "table": table_name, "status": "stub_ok"}}
        
        elif action == "create_record":
            return {"result": {"id": "rec123456789", "status": "created"}}
        
        elif action == "update_record":
            return {"result": {"id": params.get("record_id"), "status": "updated"}}
        
        else:
            return {"error": f"unknown action: {action}"}
    
    except Exception as e:
        log.exception("Airtable connector error")
        return {"error": f"connector_error: {str(e)}"}
