"""
Smart alert router - sends alerts to Slack, Telegram, and/or Email
"""
import os
import requests
import logging

logger = logging.getLogger("levqor.alerts")


def send_alert(level, message):
    """
    Send alert to configured channels (Slack, Telegram, Email).
    
    Args:
        level: Alert level (info, warning, error, critical)
        message: Alert message text
    
    Returns:
        dict: Status of each channel
    """
    results = {}
    payload = f"[{level.upper()}] {message}"
    
    # Slack webhook
    slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
    if slack_webhook:
        try:
            response = requests.post(
                slack_webhook,
                json={"text": payload},
                timeout=5
            )
            results["slack"] = "sent" if response.status_code == 200 else "failed"
        except Exception as e:
            logger.error(f"Slack alert failed: {e}")
            results["slack"] = "failed"
    
    # Telegram bot
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat = os.getenv("TELEGRAM_CHAT_ID")
    
    if telegram_token and telegram_chat:
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{telegram_token}/sendMessage",
                data={
                    "chat_id": telegram_chat,
                    "text": payload
                },
                timeout=5
            )
            results["telegram"] = "sent" if response.status_code == 200 else "failed"
        except Exception as e:
            logger.error(f"Telegram alert failed: {e}")
            results["telegram"] = "failed"
    
    # Email via Resend (if configured)
    resend_key = os.getenv("RESEND_API_KEY")
    receiving_email = os.getenv("RECEIVING_EMAIL")
    
    if resend_key and receiving_email:
        try:
            response = requests.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {resend_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "from": "alerts@levqor.ai",
                    "to": receiving_email,
                    "subject": f"[{level.upper()}] Levqor Alert",
                    "text": message
                },
                timeout=10
            )
            results["email"] = "sent" if response.status_code == 200 else "failed"
        except Exception as e:
            logger.error(f"Email alert failed: {e}")
            results["email"] = "failed"
    
    logger.info(f"Alert sent ({level}): {message} - Results: {results}")
    
    return results
