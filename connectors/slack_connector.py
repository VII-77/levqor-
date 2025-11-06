"""
Slack Connector for Levqor
Uses slack_sdk WebClient to interact with Slack API.
"""

import os
import logging

log = logging.getLogger("levqor.connectors.slack")

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False
    log.warning("slack_connector: slack-sdk not installed")


def run_task(payload):
    """
    Execute Slack task based on payload.
    
    Args:
        payload (dict): Task configuration
            - action: str (post_message, upload_file, list_channels)
            - token: str (Slack bot token)
            - params: dict (action-specific parameters)
    
    Returns:
        dict: {"result": data} or {"error": message}
    """
    if not SLACK_AVAILABLE:
        return {"error": "slack_connector: slack-sdk not installed"}
    
    try:
        action = payload.get("action")
        token = payload.get("token")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        
        if not token:
            return {"error": "token required (Slack bot token)"}
        
        client = WebClient(token=token)
        
        if action == "post_message":
            channel = params.get("channel")
            text = params.get("text")
            
            if not channel or not text:
                return {"error": "channel and text required"}
            
            response = client.chat_postMessage(
                channel=channel,
                text=text
            )
            
            return {"result": {
                "message_ts": response["ts"],
                "channel": response["channel"],
                "status": "sent"
            }}
        
        elif action == "list_channels":
            response = client.conversations_list(
                types="public_channel,private_channel",
                limit=params.get("limit", 100)
            )
            
            channels = response.get("channels", [])
            return {"result": {
                "count": len(channels),
                "channels": [{"id": c["id"], "name": c["name"]} for c in channels]
            }}
        
        elif action == "upload_file":
            channel = params.get("channel")
            content = params.get("content")
            filename = params.get("filename", "file.txt")
            
            if not channel or not content:
                return {"error": "channel and content required"}
            
            response = client.files_upload(
                channels=channel,
                content=content,
                filename=filename
            )
            
            return {"result": {
                "file_id": response["file"]["id"],
                "status": "uploaded"
            }}
        
        else:
            return {"error": f"unknown action: {action}"}
    
    except SlackApiError as e:
        log.exception("Slack API error")
        return {"error": f"slack_api_error: {e.response['error']}"}
    except Exception as e:
        log.exception("Slack connector error")
        return {"error": f"connector_error: {str(e)}"}
