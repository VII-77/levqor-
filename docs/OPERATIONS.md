# Operations Runbook

## Overview
This runbook provides on-call procedures, rollback steps, and incident communication templates for Levqor production operations.

## System Architecture

### Components
- **API Server**: Flask + Gunicorn on Replit Autoscale
- **Database**: PostgreSQL (Neon-backed)
- **Queue**: Redis + RQ (optional, graceful degradation to sync mode)
- **Monitoring**: Prometheus metrics + Sentry (optional)
- **Email**: Resend.com
- **Payments**: Stripe

### Feature Flags
All Phase-4 features are controlled by environment variables:
- `NEW_QUEUE_ENABLED=true|false` - Async queue system
- `SECURITY_HEADERS_ENABLED=true|false` - Security headers
- `RATELIMIT_ENABLED=true|false` - Rate limiting
- `WEBHOOK_VERIFY_ALL=true|false` - Webhook signature verification
- `ABUSE_GUARDS_ENABLED=true|false` - Abuse controls

## Health Checks

### Quick Status Check
```bash
curl https://your-domain.com/ops/uptime
```

Expected response:
```json
{
  "status": "operational",
  "services": {
    "api": "operational",
    "database": "operational"
  },
  "response_time_ms": 0.03,
  "version": "1.0.0"
}
```

### Queue Health Check
```bash
curl https://your-domain.com/ops/queue_health
```

### Metrics Endpoint
```bash
curl https://your-domain.com/metrics
```

## Common Incidents

### 1. High Error Rate

**Symptoms:**
- `/metrics` shows `error_rate_total` increasing
- Sentry alerts firing

**Investigation:**
1. Check `/ops/uptime` - is database healthy?
2. Check `/ops/queue_health` - is queue backed up?
3. Review Sentry for error patterns
4. Check `logs/errors.jsonl` for recent errors

**Resolution:**
- If database slow: Check query performance
- If queue backed up: Increase workers or disable queue temporarily
- If external service down: Check connector status

### 2. Rate Limiting Issues

**Symptoms:**
- Users reporting 429 errors
- Legitimate traffic being blocked

**Quick Fix:**
```bash
# Disable rate limiting temporarily
export RATELIMIT_ENABLED=false
# Restart application
```

**Long-term Fix:**
- Adjust rate limits in `middleware/ratelimit.py`
- Upgrade affected users to Pro plan

### 3. Queue/DLQ Overflow

**Symptoms:**
- `/ops/queue_health` shows high `dlq` count
- Jobs not processing

**Investigation:**
```bash
curl -X POST https://your-domain.com/ops/dlq/retry -H "Authorization: Bearer YOUR_ADMIN_KEY"
```

**Resolution:**
1. Check DLQ for poison messages
2. Fix underlying issue (e.g., API key rotation)
3. Retry DLQ jobs
4. If persistent: Disable queue temporarily

### 4. Database Connection Exhaustion

**Symptoms:**
- "too many connections" errors
- Database timeouts

**Immediate Action:**
```bash
# Reduce Gunicorn workers
export GUNICORN_WORKERS=1
# Restart application
```

**Long-term Fix:**
- Implement connection pooling
- Scale database resources

### 5. Webhook Verification Failures

**Symptoms:**
- Stripe/Slack webhooks returning 401
- Payment confirmations not sending

**Quick Fix:**
```bash
# Temporarily disable strict verification
export WEBHOOK_VERIFY_ALL=false
# Restart application
```

**Proper Fix:**
- Verify `STRIPE_WEBHOOK_SECRET` is correct
- Check webhook signature format
- Review webhook logs

## Rollback Procedures

### Emergency Rollback (All Phase-4 Features)

**Step 1: Disable All Flags**
```bash
export NEW_QUEUE_ENABLED=false
export SECURITY_HEADERS_ENABLED=false
export RATELIMIT_ENABLED=false
export WEBHOOK_VERIFY_ALL=false
export ABUSE_GUARDS_ENABLED=false
```

**Step 2: Restart Application**
```bash
# In Replit: Click "Stop" then "Run"
# Or via CLI:
pkill gunicorn
# Workflows will auto-restart
```

**Step 3: Verify Rollback**
```bash
curl https://your-domain.com/ops/uptime
curl https://your-domain.com/ops/queue_health
# Should show mode: "sync"
```

### Selective Rollback

**Disable Queue Only:**
```bash
export NEW_QUEUE_ENABLED=false
```

**Disable Rate Limiting Only:**
```bash
export RATELIMIT_ENABLED=false
```

**Disable Webhook Verification:**
```bash
export WEBHOOK_VERIFY_ALL=false
```

## Incident Communication Templates

### Status Page Update (Minor Incident)
```
[Investigating] API Performance Degradation

We're investigating reports of slow API responses. The system remains operational and all data is safe. We'll update this status as we learn more.

Posted: [TIME] UTC
```

### Status Page Update (Major Incident)
```
[Identified] Payment Processing Delays

We've identified an issue affecting payment confirmations. Payments are being processed successfully, but confirmation emails may be delayed. We're working on a fix.

Workaround: Check your Stripe dashboard for payment status.

Posted: [TIME] UTC
Next update: 30 minutes
```

### Resolution Announcement
```
[Resolved] Payment Processing Delays

The issue affecting payment confirmations has been resolved. All delayed emails have been sent. We're monitoring closely to ensure stability.

Root cause: Webhook signature verification misconfiguration
Fix: Updated STRIPE_WEBHOOK_SECRET and restarted services

Posted: [TIME] UTC
```

### Email to Affected Users
```
Subject: Brief Service Disruption - Resolved

Hi [Name],

We experienced a brief service disruption on [DATE] from [START] to [END] UTC that may have affected [FEATURE].

What happened:
- [Brief description]

What we did:
- [Resolution steps]

What we're doing to prevent this:
- [Prevention measures]

We apologize for any inconvenience. If you experienced any issues, please contact support@levqor.com.

Best,
The Levqor Team
```

## Backup & Recovery

### Manual Backup
```bash
python3 db/backup.py
```

### Restore Drill
```bash
python3 db/restore_verify.py
```

Expected output:
```
PARITY:100%
RTO: 15.3 minutes
```

### Actual Restore (DANGEROUS)
```bash
# Only in emergency with approval
psql -h $PGHOST -p $PGPORT -U $PGUSER -d $PGDATABASE < db/backups/pg/backup_TIMESTAMP.sql
```

## Monitoring Checklist

### Daily (Automated)
- ✅ Database backup @ 03:00 UTC
- ✅ Restore verification weekly
- ✅ Metrics collection

### Weekly (Manual)
- ✅ Review error logs
- ✅ Check DLQ for recurring failures
- ✅ Audit abuse control blocks
- ✅ Review Sentry trends

### Monthly
- ✅ Rotate API keys
- ✅ Update dependencies
- ✅ Review and tune rate limits
- ✅ Capacity planning

## Escalation

### L1: On-Call Engineer
- Health check failures
- Rate limit adjustments
- Queue management

### L2: Senior Engineer
- Database issues
- Security incidents
- Architecture changes

### L3: CTO/Founder
- Data breaches
- Legal/compliance
- Major outages (>1 hour)

## Contact Information
- **Support Email**: support@levqor.com
- **On-Call**: [PagerDuty/Phone]
- **Status Page**: status.levqor.com
- **Sentry**: sentry.io/levqor
- **Metrics**: your-domain.com/metrics

## Useful Commands

```bash
# Check all feature flags
env | grep ENABLED

# View recent errors
tail -100 logs/errors.jsonl | jq

# Count requests by endpoint (if logging configured)
grep "GET /" logs/app.log | wc -l

# Monitor queue depth
watch -n 5 'curl -s http://localhost:5000/ops/queue_health | jq .depth'

# Test rate limiting
for i in {1..100}; do curl http://localhost:5000/api/v1/status; done
```

## Post-Incident Review Template

1. **Timeline**: What happened and when?
2. **Impact**: How many users affected? Revenue impact?
3. **Root Cause**: Technical details
4. **Resolution**: What fixed it?
5. **Prevention**: How do we prevent recurrence?
6. **Action Items**: Specific tasks with owners

---

*Last Updated: 2025-11-07*
*Version: 4.0*
