"""
SLO Watchdog - Service Level Objective Monitor
Monitors API latency and triggers rollback if SLO breached
"""
import requests
import subprocess
import time
import os
from datetime import datetime

# SLO Configuration
SLO_LATENCY_THRESHOLD = float(os.getenv("SLO_LATENCY_THRESHOLD", "0.2"))  # 200ms
FAIL_THRESHOLD = int(os.getenv("SLO_FAIL_THRESHOLD", "3"))  # Failures before rollback
CHECK_ITERATIONS = int(os.getenv("SLO_CHECK_ITERATIONS", "5"))
CHECK_INTERVAL = int(os.getenv("SLO_CHECK_INTERVAL", "5"))  # seconds

def check_endpoint_latency(url: str = "http://localhost:5000/status") -> tuple:
    """
    Check endpoint latency
    
    Returns:
        (success: bool, latency: float)
    """
    try:
        response = requests.get(url, timeout=5)
        latency = response.elapsed.total_seconds()
        success = response.status_code == 200
        return success, latency
    except Exception as e:
        print(f"[!] Request failed: {e}")
        return False, 999.0

def trigger_rollback():
    """Trigger rollback to previous deployment"""
    rollback_script = "scripts/rollback_last_deploy.sh"
    
    if not os.path.exists(rollback_script):
        print(f"[!] Rollback script not found: {rollback_script}")
        print("[ℹ] Skipping rollback - manual intervention required")
        return False
    
    try:
        print(f"[⚠️] Triggering rollback via {rollback_script}")
        result = subprocess.run(
            ["bash", rollback_script],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("[✓] Rollback completed successfully")
            return True
        else:
            print(f"[!] Rollback failed: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"[!] Rollback error: {e}")
        return False

def send_slo_alert(failures: int, avg_latency: float):
    """Send Telegram alert for SLO breach"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        return
    
    message = f"""
🚨 SLO WATCHDOG ALERT

Service degradation detected!

Failures: {failures}/{CHECK_ITERATIONS}
Avg Latency: {avg_latency*1000:.0f}ms
SLO Target: {SLO_LATENCY_THRESHOLD*1000:.0f}ms

⏮️ Automatic rollback initiated.
"""
    
    try:
        requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={"chat_id": chat_id, "text": message.strip()},
            timeout=10
        )
    except Exception as e:
        print(f"[!] Failed to send Telegram alert: {e}")

def run_slo_check() -> dict:
    """
    Run SLO watchdog check
    
    Returns:
        dict with check results
    """
    print(f"[🔍] Starting SLO watchdog check")
    print(f"    Target: <{SLO_LATENCY_THRESHOLD*1000:.0f}ms")
    print(f"    Iterations: {CHECK_ITERATIONS}")
    print(f"    Fail threshold: {FAIL_THRESHOLD}")
    print()
    
    failures = 0
    latencies = []
    
    for i in range(CHECK_ITERATIONS):
        success, latency = check_endpoint_latency()
        latencies.append(latency)
        
        status = "✓" if success and latency <= SLO_LATENCY_THRESHOLD else "✗"
        
        if not success or latency > SLO_LATENCY_THRESHOLD:
            failures += 1
        
        print(f"  [{i+1}/{CHECK_ITERATIONS}] {status} {latency*1000:.0f}ms")
        
        if i < CHECK_ITERATIONS - 1:
            time.sleep(CHECK_INTERVAL)
    
    avg_latency = sum(latencies) / len(latencies)
    
    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "failures": failures,
        "total_checks": CHECK_ITERATIONS,
        "avg_latency_ms": avg_latency * 1000,
        "slo_threshold_ms": SLO_LATENCY_THRESHOLD * 1000,
        "slo_breached": failures >= FAIL_THRESHOLD,
        "rollback_triggered": False
    }
    
    print()
    print(f"[📊] Results: {failures}/{CHECK_ITERATIONS} failures, avg {avg_latency*1000:.0f}ms")
    
    if failures >= FAIL_THRESHOLD:
        print(f"[🚨] SLO BREACH: {failures} failures >= threshold {FAIL_THRESHOLD}")
        send_slo_alert(failures, avg_latency)
        
        rollback_success = trigger_rollback()
        result["rollback_triggered"] = rollback_success
    else:
        print(f"[✓] SLO within acceptable limits")
    
    return result

if __name__ == "__main__":
    import json
    result = run_slo_check()
    print()
    print(json.dumps(result, indent=2))
