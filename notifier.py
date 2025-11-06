import os
import requests
from datetime import datetime

API_KEY = os.getenv("RESEND_API_KEY")
BASE = "https://api.resend.com"

def send_email(to, subject, text, from_addr="no-reply@levqor.ai"):
    """Send email via Resend API"""
    if not API_KEY:
        return 500, "RESEND_API_KEY not configured"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "from": f"Levqor <{from_addr}>",
        "to": [to],
        "subject": subject,
        "text": text
    }
    
    try:
        r = requests.post(f"{BASE}/emails", json=data, headers=headers, timeout=10)
        log_email(to, subject, r.status_code, r.text)
        return r.status_code, r.text
    except Exception as e:
        log_email(to, subject, 0, f"Error: {str(e)}")
        return 500, f"Error: {str(e)}"

def alert(subj, msg):
    """Send alert to support@levqor.ai"""
    return send_email("support@levqor.ai", subj, msg)

def billing(subj, msg):
    """Send billing notification to billing@levqor.ai"""
    return send_email("billing@levqor.ai", subj, msg)

def security(subj, msg):
    """Send security alert to security@levqor.ai"""
    return send_email("security@levqor.ai", subj, msg)

def log_email(to, subject, status_code, response):
    """Log email send attempts"""
    timestamp = datetime.utcnow().isoformat()
    log_entry = f"[{timestamp}] To: {to} | Subject: {subject} | Status: {status_code} | Response: {response[:100]}\n"
    
    try:
        with open("logs/email_test.log", "a") as f:
            f.write(log_entry)
    except:
        pass
