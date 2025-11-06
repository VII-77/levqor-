"""
Gmail Connector for Levqor
Uses Google API Python Client to interact with Gmail API.
"""

import os
import logging

log = logging.getLogger("levqor.connectors.gmail")

try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False
    log.warning("gmail_connector: google-api-python-client not installed")


def run_task(payload):
    """
    Execute Gmail task based on payload.
    
    Args:
        payload (dict): Task configuration
            - action: str (list_labels, send_email, list_messages)
            - credentials: dict (OAuth2 credentials)
            - params: dict (action-specific parameters)
    
    Returns:
        dict: {"result": data} or {"error": message}
    """
    if not GMAIL_AVAILABLE:
        return {"error": "gmail_connector: google-api-python-client not installed"}
    
    try:
        action = payload.get("action")
        creds_data = payload.get("credentials")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        
        if not creds_data:
            return {"error": "credentials required (OAuth2 token)"}
        
        creds = Credentials.from_authorized_user_info(creds_data)
        service = build("gmail", "v1", credentials=creds)
        
        if action == "list_labels":
            results = service.users().labels().list(userId="me").execute()
            labels = results.get("labels", [])
            return {"result": {"labels": [l["name"] for l in labels]}}
        
        elif action == "list_messages":
            max_results = params.get("max_results", 10)
            query = params.get("query", "")
            results = service.users().messages().list(
                userId="me", 
                maxResults=max_results,
                q=query
            ).execute()
            messages = results.get("messages", [])
            return {"result": {"count": len(messages), "messages": messages}}
        
        elif action == "send_email":
            to = params.get("to")
            subject = params.get("subject")
            body = params.get("body")
            
            if not to or not subject:
                return {"error": "to and subject required"}
            
            from email.mime.text import MIMEText
            from base64 import urlsafe_b64encode
            
            message = MIMEText(body or "")
            message["to"] = to
            message["subject"] = subject
            raw = urlsafe_b64encode(message.as_bytes()).decode()
            
            sent = service.users().messages().send(
                userId="me", 
                body={"raw": raw}
            ).execute()
            
            return {"result": {"message_id": sent.get("id"), "status": "sent"}}
        
        else:
            return {"error": f"unknown action: {action}"}
    
    except HttpError as e:
        log.exception("Gmail API error")
        return {"error": f"gmail_api_error: {str(e)}"}
    except Exception as e:
        log.exception("Gmail connector error")
        return {"error": f"connector_error: {str(e)}"}
