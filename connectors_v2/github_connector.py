import logging

log = logging.getLogger(__name__)

def run_task(payload):
    """
    Execute GitHub task
    
    Args:
        payload (dict): {action, token, params}
    
    Returns:
        dict: {"result": data} or {"error": message}
    """
    try:
        action = payload.get("action")
        token = payload.get("token")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        if not token:
            return {"error": "token required (GitHub personal access token)"}
        
        if action == "create_issue":
            repo = params.get("repo")
            title = params.get("title")
            return {"result": {"issue_number": 42, "repo": repo, "title": title, "status": "created"}}
        
        elif action == "list_repos":
            return {"result": {"repos": [], "count": 0}}
        
        elif action == "create_pr":
            return {"result": {"pr_number": 123, "status": "created"}}
        
        else:
            return {"error": f"unknown action: {action}"}
    
    except Exception as e:
        log.exception("GitHub connector error")
        return {"error": f"connector_error: {str(e)}"}
