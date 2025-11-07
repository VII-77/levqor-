"""
Telegram Alert System
Sends notifications for critical events and monitoring alerts
"""
import os
import requests
from typing import Optional
from datetime import datetime

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ALERT_TIMEOUT = int(os.getenv("TELEGRAM_TIMEOUT", "10"))

def send_alert(
    message: str,
    parse_mode: str = "Markdown",
    disable_notification: bool = False
) -> dict:
    """
    Send Telegram alert message
    
    Args:
        message: Alert message text
        parse_mode: Message formatting (Markdown or HTML)
        disable_notification: Send silently without notification
    
    Returns:
        dict with status and details
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return {
            "success": False,
            "error": "Telegram not configured (missing BOT_TOKEN or CHAT_ID)"
        }
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": parse_mode,
        "disable_notification": disable_notification
    }
    
    try:
        response = requests.post(url, data=payload, timeout=ALERT_TIMEOUT)
        result = response.json()
        
        if result.get("ok"):
            return {
                "success": True,
                "message_id": result["result"]["message_id"],
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            return {
                "success": False,
                "error": result.get("description", "Unknown error")
            }
    
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timeout"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def send_critical_alert(title: str, details: str):
    """Send high-priority critical alert"""
    message = f"""
🚨 *CRITICAL ALERT*

*{title}*

{details}

_Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}_
"""
    return send_alert(message.strip(), disable_notification=False)

def send_warning(title: str, details: str):
    """Send warning alert"""
    message = f"""
⚠️ *WARNING*

*{title}*

{details}

_Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}_
"""
    return send_alert(message.strip(), disable_notification=True)

def send_info(title: str, details: str):
    """Send informational alert"""
    message = f"""
ℹ️ *INFO*

*{title}*

{details}

_Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}_
"""
    return send_alert(message.strip(), disable_notification=True)

def send_success(title: str, details: str):
    """Send success notification"""
    message = f"""
✅ *SUCCESS*

*{title}*

{details}

_Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}_
"""
    return send_alert(message.strip(), disable_notification=True)

# Pre-configured alert templates
def alert_system_down():
    """Alert when system goes down"""
    return send_critical_alert(
        "System Down",
        "Application is not responding. Immediate action required."
    )

def alert_high_error_rate(rate: float):
    """Alert when error rate is high"""
    return send_warning(
        "High Error Rate",
        f"Current error rate: {rate:.1f}%\nThreshold exceeded."
    )

def alert_backup_failed(error: str):
    """Alert when backup fails"""
    return send_critical_alert(
        "Backup Failed",
        f"Database backup failed:\n{error}"
    )

def alert_spend_limit_exceeded(actual: float, limit: float):
    """Alert when spend limit is exceeded"""
    return send_critical_alert(
        "Spend Limit Exceeded",
        f"Daily spend: ${actual:.2f}\nLimit: ${limit:.2f}\n\nBilling has been paused."
    )

def alert_payout_processed(partner_code: str, amount: float):
    """Notify when payout is processed"""
    return send_success(
        "Payout Processed",
        f"Partner: {partner_code}\nAmount: ${amount:.2f}"
    )

if __name__ == "__main__":
    # Test alert
    alert_message = os.getenv("ALERT_MESSAGE", "Levqor test alert - system operational")
    result = send_info("Test Alert", alert_message)
    
    if result["success"]:
        print(f"[✓] Alert sent successfully (ID: {result['message_id']})")
    else:
        print(f"[✗] Alert failed: {result['error']}")
