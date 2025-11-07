"""
Spend Guard - Automatic Cost Protection
Monitors Stripe spending and pauses billing if daily limit exceeded
"""
import os
import requests
import json
from datetime import datetime

# Configuration
DAILY_SPEND_LIMIT = float(os.getenv("DAILY_SPEND_LIMIT", "50.0"))
BILLING_FLAGS_FILE = "config/billing_flags.json"

def get_stripe_balance() -> dict:
    """Fetch current Stripe balance"""
    stripe_key = os.getenv("STRIPE_SECRET_KEY")
    if not stripe_key:
        return {"error": "STRIPE_SECRET_KEY not configured"}
    
    try:
        response = requests.get(
            "https://api.stripe.com/v1/balance",
            auth=(stripe_key, ""),
            timeout=10
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def calculate_daily_spend(balance_data: dict) -> float:
    """Calculate total pending spend"""
    if "error" in balance_data:
        return 0.0
    
    pending = balance_data.get("pending", [])
    total_pending = sum(item["amount"] for item in pending) / 100  # Convert cents to dollars
    
    return abs(total_pending)  # Pending is negative for outgoing

def update_billing_flags(enabled: bool):
    """Update billing flags configuration"""
    os.makedirs("config", exist_ok=True)
    
    flags = {
        "BILLING_ENABLED": enabled,
        "updated_at": datetime.utcnow().isoformat(),
        "spend_limit": DAILY_SPEND_LIMIT
    }
    
    with open(BILLING_FLAGS_FILE, "w") as f:
        json.dump(flags, f, indent=2)

def check_spend_guard() -> dict:
    """
    Check if spending is within limits
    
    Returns:
        dict with status and details
    """
    print(f"[🛡️] Running spend guard check (limit: ${DAILY_SPEND_LIMIT})")
    
    balance_data = get_stripe_balance()
    if "error" in balance_data:
        print(f"[!] Error fetching Stripe balance: {balance_data['error']}")
        return {
            "status": "error",
            "error": balance_data["error"]
        }
    
    daily_spend = calculate_daily_spend(balance_data)
    
    result = {
        "status": "ok",
        "daily_spend": daily_spend,
        "limit": DAILY_SPEND_LIMIT,
        "within_limit": daily_spend <= DAILY_SPEND_LIMIT,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if daily_spend > DAILY_SPEND_LIMIT:
        print(f"[🚨] ALERT: Daily spend ${daily_spend:.2f} exceeds limit ${DAILY_SPEND_LIMIT}")
        print(f"[⏸️] Pausing billing to prevent overcharge")
        
        update_billing_flags(enabled=False)
        
        result["status"] = "limit_exceeded"
        result["action"] = "billing_paused"
        
        # Send Telegram alert if configured
        send_spend_alert(daily_spend, DAILY_SPEND_LIMIT)
    else:
        print(f"[✓] Spend within limit: ${daily_spend:.2f} / ${DAILY_SPEND_LIMIT}")
        update_billing_flags(enabled=True)
        result["action"] = "none"
    
    return result

def send_spend_alert(actual: float, limit: float):
    """Send Telegram alert for spend limit breach"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        return
    
    message = f"""
🚨 SPEND GUARD ALERT

Daily spend limit exceeded!
Actual: ${actual:.2f}
Limit: ${limit:.2f}

⏸️ Billing has been automatically paused.

Review your Stripe dashboard and adjust DAILY_SPEND_LIMIT if needed.
"""
    
    try:
        requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={"chat_id": chat_id, "text": message.strip()},
            timeout=10
        )
    except Exception as e:
        print(f"[!] Failed to send Telegram alert: {e}")

if __name__ == "__main__":
    result = check_spend_guard()
    print(f"\n[📊] Result: {json.dumps(result, indent=2)}")
