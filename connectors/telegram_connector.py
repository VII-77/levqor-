"""
Telegram Connector for Levqor
Uses python-telegram-bot library to interact with Telegram Bot API.
"""

import os
import logging

log = logging.getLogger("levqor.connectors.telegram")

try:
    import asyncio
    from telegram import Bot
    from telegram.error import TelegramError
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    log.warning("telegram_connector: python-telegram-bot not installed")


def run_task(payload):
    """
    Execute Telegram task based on payload.
    
    Args:
        payload (dict): Task configuration
            - action: str (send_message, get_updates, send_photo)
            - token: str (Telegram bot token)
            - params: dict (action-specific parameters)
    
    Returns:
        dict: {"result": data} or {"error": message}
    """
    if not TELEGRAM_AVAILABLE:
        return {"error": "telegram_connector: python-telegram-bot not installed"}
    
    try:
        action = payload.get("action")
        token = payload.get("token")
        params = payload.get("params", {})
        
        if not action:
            return {"error": "action required"}
        
        if not token:
            return {"error": "token required (Telegram bot token)"}
        
        bot = Bot(token=token)
        
        if action == "send_message":
            chat_id = params.get("chat_id")
            text = params.get("text")
            
            if not chat_id or not text:
                return {"error": "chat_id and text required"}
            
            async def _send():
                message = await bot.send_message(chat_id=chat_id, text=text)
                return message
            
            message = asyncio.run(_send())
            return {"result": {
                "message_id": message.message_id,
                "chat_id": message.chat.id,
                "status": "sent"
            }}
        
        elif action == "get_me":
            async def _get_me():
                user = await bot.get_me()
                return user
            
            user = asyncio.run(_get_me())
            return {"result": {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name
            }}
        
        elif action == "get_updates":
            limit = params.get("limit", 10)
            
            async def _get_updates():
                updates = await bot.get_updates(limit=limit)
                return updates
            
            updates = asyncio.run(_get_updates())
            return {"result": {
                "count": len(updates),
                "updates": [{"update_id": u.update_id} for u in updates]
            }}
        
        else:
            return {"error": f"unknown action: {action}"}
    
    except TelegramError as e:
        log.exception("Telegram API error")
        return {"error": f"telegram_api_error: {str(e)}"}
    except Exception as e:
        log.exception("Telegram connector error")
        return {"error": f"connector_error: {str(e)}"}
