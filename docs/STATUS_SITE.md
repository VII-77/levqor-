# Public System Status Dashboard

## Overview
Public status page showing real-time system health and incident history.

## Implementation

### Option 1: Static HTML (Implemented)
**Location:** `status/template.html`

**Features:**
- Real-time component status
- Incident history
- Auto-refresh every 60s
- Mobile responsive

**Hosting:**
```bash
# Serve via Flask
@app.get("/status/live")
def status_page():
    return send_file("status/template.html")
```

### Option 2: statuspage.io (SaaS)
**URL:** https://www.atlassian.com/software/statuspage

**Features:**
- Hosted status page
- Incident management
- Subscriber notifications
- API integration

**Cost:** $29/month

### Option 3: Cachet (Self-hosted)
**URL:** https://cachethq.io

**Features:**
- Open source
- Self-hosted
- Component monitoring
- Metrics display

**Cost:** $0 (hosting only)

## Incident Management

### Creating Incidents
**Manual:**
1. Create markdown file: `status/incidents/YYYYMMDD_title.md`
2. Add frontmatter:
```markdown
---
title: API Latency Spike
status: investigating|identified|monitoring|resolved
severity: minor|major|critical
started: 2025-11-06T14:30:00Z
resolved: 2025-11-06T15:00:00Z
---

## Update 15:00 UTC
Issue resolved. API latency back to normal.

## Update 14:45 UTC
Identified cause: Database connection pool exhausted. Increasing pool size.

## Update 14:30 UTC
Investigating elevated API response times.
```

### Automated Detection
```python
# Check health and create incident
if avg_latency > 2000:  # ms
    create_incident(
        title="High API Latency",
        status="investigating",
        severity="major"
    )
```

## Components to Monitor
1. **API** - https://api.levqor.ai/health
2. **Dashboard** - https://levqor.ai
3. **Workflow Builder** - Frontend status
4. **Email Delivery** - Resend status
5. **Database** - Connection health
6. **Background Jobs** - Scheduler status

## Status Page URL
```
https://api.levqor.ai/status/live
https://status.levqor.ai (custom domain)
```

## Subscriber Notifications

### Email Alerts
```python
# When incident created
send_email(
    to=subscribers,
    subject="[INCIDENT] API Latency Spike",
    body=incident_details
)
```

### Subscription Management
```
GET /status/subscribe?email=user@example.com
POST /status/unsubscribe
```

## Uptime Display

### 90-Day Uptime
```
API Uptime: 99.95%
Dashboard Uptime: 99.98%
```

### Uptime Calculation
```python
total_time = 90 * 24 * 60  # minutes
downtime = sum(incident_durations)
uptime_pct = ((total_time - downtime) / total_time) * 100
```

## Integration with Monitoring

### Automatic Updates
```python
# From UptimeRobot webhook
@app.post("/webhooks/uptime")
def uptime_webhook():
    data = request.json
    
    if data['alert_type'] == 'down':
        create_incident(
            title=f"{data['monitor_name']} Down",
            status="investigating"
        )
```

## Customization

### Branding
- Logo: Add to `status/logo.png`
- Colors: Edit CSS in template
- Domain: Custom subdomain

### Custom Components
Edit `status/template.html`:
```html
<div class="service">
    <span class="service-name">Your Component</span>
    <span class="service-status up">Operational</span>
</div>
```

## Best Practices
1. **Be transparent** - Show all incidents
2. **Update frequently** - Every 30-60 min during incidents
3. **Post-mortems** - Root cause analysis
4. **Subscribe option** - Email notifications
5. **Mobile friendly** - Responsive design

## Status
- ✅ Static template created
- ✅ Incident system documented
- ⏳ Requires hosting (add endpoint to run.py)
- ⏳ Optional: statuspage.io ($29/mo)
