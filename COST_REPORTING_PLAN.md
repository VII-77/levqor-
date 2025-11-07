# 📊 COST REPORTING SYSTEM - PLANNING

Based on your cron schedules, you want:

## Scheduling Requirements

### Daily Report (09:00 London time)
```cron
0 9 * * * python3 scripts/daily_cost_report.py >> logs/daily.log 2>&1
```
- Runs every day at 09:00 Europe/London
- Logs to `logs/daily.log`
- Generates daily cost metrics

### Weekly Email Summary (Sunday 09:00 London time)  
```cron
0 9 * * SUN python3 scripts/daily_cost_report.py --email >> logs/weekly_summary.log 2>&1
```
- Runs every Sunday at 09:00 Europe/London
- Sends email summary
- Logs to `logs/weekly_summary.log`

---

## Implementation Options

### Option 1: APScheduler (Recommended for Replit)
Since you're on Replit Autoscale (always running), use APScheduler with timezone support:

```python
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = BackgroundScheduler(timezone='Europe/London')

# Daily report at 09:00 London time
scheduler.add_job(
    daily_cost_report,
    CronTrigger(hour=9, minute=0, timezone='Europe/London'),
    id='daily_cost_report'
)

# Weekly email on Sunday at 09:00 London time
scheduler.add_job(
    weekly_email_summary,
    CronTrigger(day_of_week='sun', hour=9, minute=0, timezone='Europe/London'),
    id='weekly_email_summary'
)

scheduler.start()
```

**Pros:**
- Handles DST automatically (09:00 London = 09:00 always)
- Already running in your Flask app
- No external cron needed
- Works perfectly on Replit Autoscale

### Option 2: System Cron (Not Available on Replit)
Traditional cron jobs don't work on Replit Autoscale.

---

## What Needs to Be Built

### 1. Cost Tracking Module
- Track API calls (OpenAI, external services)
- Track compute costs
- Track database operations
- Store metrics in PostgreSQL

### 2. Daily Report Script
**`scripts/daily_cost_report.py`**
- Calculate yesterday's costs
- Generate summary report
- Store in database
- Optionally print to logs

### 3. Email Functionality
- Weekly summary email
- Cost breakdown by service
- Alerts for anomalies
- Uses RESEND_API_KEY (you have this)

### 4. Database Schema
```sql
CREATE TABLE cost_metrics (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    service VARCHAR(100),
    cost_usd DECIMAL(10,2),
    usage_count INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Questions for You

1. **Do you want me to implement this cost reporting system?**
   - Daily cost tracking
   - Weekly email summaries
   - APScheduler integration

2. **What costs should we track?**
   - OpenAI API calls?
   - Database operations?
   - External service calls?
   - Compute time?

3. **Email recipients?**
   - Use RECEIVING_EMAIL secret?
   - Or different email for reports?

4. **Cost thresholds?**
   - Daily spending limit alerts?
   - Weekly budget warnings?

---

## Current Status

✅ You have RESEND_API_KEY for sending emails
✅ You have PostgreSQL database for storing metrics
✅ Backend is on Autoscale (perfect for APScheduler)
⏳ Need to build cost tracking
⏳ Need to build reporting scripts
⏳ Need to add APScheduler integration

---

**Ready to implement when you confirm!** 🚀
