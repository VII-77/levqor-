"""
Daily Cost + Uptime Report
Sends daily operational metrics via Telegram
"""
import os
import requests
import datetime
import json

def generate_report():
    """Generate daily operational report"""
    report_lines = [
        "📊 LEVQOR DAILY REPORT",
        f"Date: {datetime.date.today().isoformat()}",
        ""
    ]
    
    # Stripe balance
    try:
        stripe_key = os.getenv("STRIPE_SECRET_KEY")
        if stripe_key:
            response = requests.get(
                "https://api.stripe.com/v1/balance",
                auth=(stripe_key, ""),
                timeout=10
            )
            balance_data = response.json()
            
            if "available" in balance_data and balance_data["available"]:
                amount = balance_data["available"][0]["amount"] / 100
                currency = balance_data["available"][0]["currency"].upper()
                report_lines.append(f"💰 Stripe Balance: {amount:.2f} {currency}")
            
            if "pending" in balance_data and balance_data["pending"]:
                pending = sum(p["amount"] for p in balance_data["pending"]) / 100
                report_lines.append(f"⏳ Pending: {pending:.2f} {currency}")
        else:
            report_lines.append("⚠️ Stripe: API key not configured")
    
    except Exception as e:
        report_lines.append(f"⚠️ Stripe: {str(e)}")
    
    report_lines.append("")
    
    # System metrics
    try:
        metrics = requests.get("http://localhost:5000/metrics", timeout=5).text
        
        # Extract uptime
        for line in metrics.splitlines():
            if "uptime_seconds" in line and not line.startswith("#"):
                uptime_seconds = float(line.split()[-1])
                uptime_hours = uptime_seconds / 3600
                uptime_days = uptime_hours / 24
                if uptime_days >= 1:
                    report_lines.append(f"⏰ Uptime: {uptime_days:.1f} days")
                else:
                    report_lines.append(f"⏰ Uptime: {uptime_hours:.1f} hours")
                break
        
        # Extract error rate
        for line in metrics.splitlines():
            if line.startswith("error_rate "):
                error_rate = float(line.split()[-1])
                if error_rate > 0:
                    report_lines.append(f"⚠️ Error Rate: {error_rate:.2%}")
                else:
                    report_lines.append("✅ Error Rate: 0%")
                break
        
        # Extract queue depth
        for line in metrics.splitlines():
            if line.startswith("queue_depth "):
                queue_depth = int(float(line.split()[-1]))
                report_lines.append(f"📦 Queue Depth: {queue_depth}")
                break
    
    except Exception as e:
        report_lines.append(f"⚠️ Metrics: {str(e)}")
    
    report_lines.append("")
    
    # Database stats
    try:
        import sqlite3
        conn = sqlite3.connect('levqor.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        report_lines.append(f"👥 Total Users: {user_count}")
        
        cursor.execute("SELECT COUNT(*) FROM partners")
        partner_count = cursor.fetchone()[0]
        report_lines.append(f"🤝 Active Partners: {partner_count}")
        
        cursor.execute("SELECT SUM(pending_commission) FROM partners")
        pending = cursor.fetchone()[0] or 0
        report_lines.append(f"💵 Pending Commissions: ${pending:.2f}")
        
        conn.close()
    
    except Exception as e:
        report_lines.append(f"⚠️ Database: {str(e)}")
    
    return "\n".join(report_lines)

def send_telegram_alert(message):
    """Send message via Telegram"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("[ℹ] Telegram not configured - skipping alert")
        return False
    
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={"chat_id": chat_id, "text": message},
            timeout=10
        )
        
        if response.status_code == 200:
            print("[✓] Telegram alert sent successfully")
            return True
        else:
            print(f"[!] Telegram API error: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"[!] Failed to send Telegram alert: {e}")
        return False

if __name__ == "__main__":
    report = generate_report()
    print(report)
    print()
    
    # Send via Telegram if configured
    send_telegram_alert(report)
