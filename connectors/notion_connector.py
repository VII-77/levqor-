"""
Notion Connector for Levqor
Uses requests library to interact with Notion API.
"""

import os
import logging

log = logging.getLogger("levqor.connectors.notion")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    log.warning("notion_connector: requests library not installed")


def run_task(payload):
    """
    Execute Notion task based on payload.
    
    Args:
        payload (dict): Task configuration
            - action: str (list_databases, query_database, create_page, search)
            - token: str (Notion integration token)
            - params: dict (action-specific parameters)
    
    Returns:
        dict: {"result": data} or {"error": message}
    """
    if not REQUESTS_AVAILABLE:
        return {"error": "notion_connector: requests library not installed"}
    
    try:
        action = payload.get("action")
        token = payload.get("token")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        
        if not token:
            return {"error": "token required (Notion integration token)"}
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        if action == "search":
            query = params.get("query", "")
            data = {
                "query": query,
                "filter": {"property": "object", "value": "page"}
            }
            resp = requests.post(
                "https://api.notion.com/v1/search",
                json=data,
                headers=headers,
                timeout=10
            )
            resp.raise_for_status()
            results = resp.json()
            return {"result": {
                "count": len(results.get("results", [])),
                "pages": results.get("results", [])
            }}
        
        elif action == "query_database":
            database_id = params.get("database_id")
            if not database_id:
                return {"error": "database_id required"}
            
            page_size = params.get("page_size", 10)
            data = {"page_size": page_size}
            
            resp = requests.post(
                f"https://api.notion.com/v1/databases/{database_id}/query",
                json=data,
                headers=headers,
                timeout=10
            )
            resp.raise_for_status()
            results = resp.json()
            return {"result": {
                "count": len(results.get("results", [])),
                "has_more": results.get("has_more", False),
                "results": results.get("results", [])
            }}
        
        elif action == "create_page":
            database_id = params.get("database_id")
            properties = params.get("properties", {})
            
            if not database_id:
                return {"error": "database_id required"}
            
            data = {
                "parent": {"database_id": database_id},
                "properties": properties
            }
            
            resp = requests.post(
                "https://api.notion.com/v1/pages",
                json=data,
                headers=headers,
                timeout=10
            )
            resp.raise_for_status()
            page = resp.json()
            return {"result": {"page_id": page.get("id"), "status": "created"}}
        
        else:
            return {"error": f"unknown action: {action}"}
    
    except requests.exceptions.RequestException as e:
        log.exception("Notion API error")
        return {"error": f"notion_api_error: {str(e)}"}
    except Exception as e:
        log.exception("Notion connector error")
        return {"error": f"connector_error: {str(e)}"}
