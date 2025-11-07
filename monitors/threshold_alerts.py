import requests
import os
import sys

THR = {"error_rate": 1.0, "queue_depth": 10}

try:
    m = requests.get("http://localhost:5000/metrics", timeout=5).text
except Exception as e:
    print(f"[!] Failed to fetch metrics: {e}")
    sys.exit(1)

alerts = []
for k, v in THR.items():
    try:
        val = float(m.split(k)[1].split()[0])
        if val > v:
            alerts.append(f"{k}>{v} ({val})")
    except:
        pass

if alerts:
    msg = "⚠️ Levqor Alert: " + ", ".join(alerts)
    print(msg)
    
    if os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"):
        try:
            requests.post(
                f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage",
                data={"chat_id": os.getenv('TELEGRAM_CHAT_ID'), "text": msg},
                timeout=10
            )
            print("[✓] Alert sent via Telegram")
        except Exception as e:
            print(f"[!] Failed to send Telegram alert: {e}")
else:
    print("[✓] All metrics within thresholds")
