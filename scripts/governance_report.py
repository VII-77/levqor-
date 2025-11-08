"""
Weekly Governance Report - Sends comprehensive HTML summary email.
Includes SLO breaches, costs, users, incidents, and feature flags.
"""
import os
import sys
import json
import sqlite3
import logging
import requests
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("levqor.governance")

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RECEIVING_EMAIL = os.getenv("RECEIVING_EMAIL", "ops@levqor.ai")

def get_week_summary() -> dict:
    """Gather all metrics for the weekly report"""
    conn = sqlite3.connect("levqor.db")
    c = conn.cursor()
    
    week_ago = datetime.now() - timedelta(days=7)
    week_ts = int(week_ago.timestamp())
    
    # User metrics
    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM users WHERE created_at > ?", [week_ts])
    new_users = c.fetchone()[0]
    
    # Growth events
    c.execute("SELECT COUNT(*) FROM growth_events WHERE event='signup' AND ts > ?", [week_ts])
    signups = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM growth_events WHERE event='paid' AND ts > ?", [week_ts])
    conversions = c.fetchone()[0]
    
    # Feature flags
    c.execute("SELECT key, value FROM feature_flags")
    flags = {k: v for k, v in c.fetchall()}
    
    # Discounts
    now = int(datetime.now().timestamp())
    c.execute("SELECT COUNT(*) FROM discounts WHERE active=1 AND expires_ts > ?", [now])
    active_discounts = c.fetchone()[0]
    
    # KV metrics
    c.execute("SELECT key, value FROM kv WHERE key LIKE '%_30d'")
    kv_metrics = {k: v for k, v in c.fetchall()}
    
    conn.close()
    
    return {
        "period": f"{week_ago.strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}",
        "users": {
            "total": total_users,
            "new_this_week": new_users
        },
        "growth": {
            "signups": signups,
            "conversions": conversions,
            "conversion_rate": round((conversions / max(signups, 1)) * 100, 2)
        },
        "feature_flags": flags,
        "active_discounts": active_discounts,
        "kv_metrics": kv_metrics
    }

def build_html_report(summary: dict) -> str:
    """Build HTML email body"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; border-radius: 8px; padding: 30px; }}
            h1 {{ color: #1a1a1a; margin-top: 0; }}
            h2 {{ color: #4a4a4a; border-bottom: 2px solid #e0e0e0; padding-bottom: 8px; }}
            .metric {{ display: inline-block; margin: 10px 20px 10px 0; }}
            .metric-label {{ font-size: 12px; color: #666; text-transform: uppercase; }}
            .metric-value {{ font-size: 28px; font-weight: bold; color: #2563eb; }}
            .flag {{ padding: 4px 8px; border-radius: 4px; font-size: 12px; display: inline-block; margin: 4px; }}
            .flag-true {{ background: #10b981; color: white; }}
            .flag-false {{ background: #e5e7eb; color: #374151; }}
            .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Levqor Weekly Governance Report</h1>
            <p style="color: #666;">{summary['period']}</p>
            
            <h2>👥 User Metrics</h2>
            <div class="metric">
                <div class="metric-label">Total Users</div>
                <div class="metric-value">{summary['users']['total']}</div>
            </div>
            <div class="metric">
                <div class="metric-label">New This Week</div>
                <div class="metric-value">{summary['users']['new_this_week']}</div>
            </div>
            
            <h2>📈 Growth</h2>
            <div class="metric">
                <div class="metric-label">Signups</div>
                <div class="metric-value">{summary['growth']['signups']}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Conversions</div>
                <div class="metric-value">{summary['growth']['conversions']}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Conversion Rate</div>
                <div class="metric-value">{summary['growth']['conversion_rate']}%</div>
            </div>
            
            <h2>🎛️ Feature Flags</h2>
            <div>
    """
    
    for flag, value in summary['feature_flags'].items():
        flag_class = "flag-true" if value.lower() == "true" else "flag-false"
        html += f'<span class="flag {flag_class}">{flag}: {value}</span>'
    
    html += f"""
            </div>
            
            <h2>💰 Financial</h2>
            <div class="metric">
                <div class="metric-label">Active Discounts</div>
                <div class="metric-value">{summary['active_discounts']}</div>
            </div>
    """
    
    # Add KV metrics if available
    if summary['kv_metrics']:
        html += "<h2>📊 KV Metrics (30d)</h2><ul>"
        for key, value in summary['kv_metrics'].items():
            html += f"<li><strong>{key}:</strong> {value}</li>"
        html += "</ul>"
    
    html += """
            <div class="footer">
                <p>Generated automatically by Levqor Governance Reporter</p>
                <p>Backend: <a href="https://api.levqor.ai">api.levqor.ai</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def send_governance_report():
    """Send weekly governance report via Resend"""
    if not RESEND_API_KEY:
        logger.warning("RESEND_API_KEY not set - skipping governance report")
        print("⚠️ GOVERNANCE_REPORT=skipped (no RESEND_API_KEY)")
        return False
    
    try:
        # Gather metrics
        summary = get_week_summary()
        html_body = build_html_report(summary)
        
        # Send via Resend
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": "Levqor Governance <governance@levqor.ai>",
                "to": [RECEIVING_EMAIL],
                "subject": f"📊 Weekly Governance Report - {datetime.now().strftime('%Y-%m-%d')}",
                "html": html_body
            },
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            logger.info(f"✅ Governance report sent to {RECEIVING_EMAIL}")
            print(f"✅ GOVERNANCE_REPORT=ok (sent to {RECEIVING_EMAIL})")
            return True
        else:
            logger.error(f"Failed to send report: {response.status_code} {response.text}")
            print(f"❌ GOVERNANCE_REPORT=failed ({response.status_code})")
            return False
            
    except Exception as e:
        logger.error(f"Governance report error: {e}")
        print(f"❌ STEP FAILED: GOVERNANCE_REPORT - {e}")
        return False

if __name__ == "__main__":
    success = send_governance_report()
    sys.exit(0 if success else 1)
