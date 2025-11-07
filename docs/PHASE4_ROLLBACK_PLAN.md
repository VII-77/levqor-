# Phase-4 Hardening Rollback Plan

## Overview
This document provides procedures for rolling back Phase-4 Hardening features if issues are encountered in production.

## Quick Rollback (All Features)

### Emergency Shutdown
If Phase-4 features are causing critical issues:

```bash
# Disable all Phase-4 features immediately
export NEW_QUEUE_ENABLED=false
export SECURITY_HEADERS_ENABLED=false
export RATELIMIT_ENABLED=false
export WEBHOOK_VERIFY_ALL=false
export ABUSE_GUARDS_ENABLED=false

# Restart application
# In Replit: Click "Stop" then "Run"
# Workflows will auto-restart with flags disabled
```

### Verification After Rollback
```bash
# Check queue mode
curl http://localhost:5000/ops/queue_health
# Should show: {"mode": "sync", "queue_available": false}

# Verify no security headers
curl -I http://localhost:5000/
# Should NOT see: X-Frame-Options, Content-Security-Policy

# Test rate limiting disabled
for i in {1..100}; do curl http://localhost:5000/api/v1/status/test; done
# Should NOT return 429 errors
```

## Selective Rollback by Feature

### 1. Queue System

**Disable:**
```bash
export NEW_QUEUE_ENABLED=false
```

**Impact:**
- Jobs execute synchronously
- No DLQ functionality
- Idempotency checks disabled
- Slower response for heavy jobs

**Verification:**
```bash
curl http://localhost:5000/ops/queue_health
# Expected: {"mode": "sync"}
```

### 2. Security Headers

**Disable:**
```bash
export SECURITY_HEADERS_ENABLED=false
```

**Impact:**
- Removes CSP, HSTS, X-Frame-Options
- Slightly reduced XSS/clickjacking protection
- No functional impact on API

**Verification:**
```bash
curl -I http://localhost:5000/ | grep -i "x-frame"
# Should return empty (no header)
```

### 3. Rate Limiting

**Disable:**
```bash
export RATELIMIT_ENABLED=false
```

**Impact:**
- No per-key or per-IP limits
- Potential for abuse
- Increased server load risk

**Verification:**
```bash
# Make 100 rapid requests
for i in {1..100}; do curl -s http://localhost:5000/api/v1/status/test; done
# Should NOT return 429 errors
```

### 4. Webhook Verification

**Disable:**
```bash
export WEBHOOK_VERIFY_ALL=false
```

**Impact:**
- Webhooks accepted without signature verification
- Reduced security for inbound webhooks
- Stripe/Slack webhooks still process

**Verification:**
```bash
# Test webhook without signature
curl -X POST http://localhost:5000/webhooks/stripe/test -d '{}'
# Should NOT return 401 Unauthorized
```

### 5. Abuse Controls

**Disable:**
```bash
export ABUSE_GUARDS_ENABLED=false
```

**Impact:**
- No device binding for free plans
- No referral fraud detection
- Potential for account sharing abuse

**Verification:**
```bash
# Check abuse metrics
curl http://localhost:5000/metrics | grep abuse
# Counters may exist but guards are disabled
```

## Rollback Triggers

### Critical Issues (Immediate Rollback)
- **Service Outage**: API returns 5xx errors >5%
- **Data Loss**: Database corruption detected
- **Security Breach**: Unauthorized access detected
- **Performance Degradation**: P95 latency >1000ms

### Warning Signs (Selective Rollback)
- **Queue Backlog**: DLQ depth >100
- **Rate Limit False Positives**: Legitimate users blocked
- **Webhook Failures**: Payment confirmations not sending
- **High Error Rate**: Sentry alerts >10/min

## Known Issues & Workarounds

### Issue: Redis Connection Failed
**Symptoms:** Queue health shows "error" mode
**Rollback:** `export NEW_QUEUE_ENABLED=false`
**Workaround:** Check REDIS_URL environment variable, or operate in sync mode

### Issue: CSP Blocking Resources
**Symptoms:** Frontend not loading scripts/styles
**Rollback:** `export SECURITY_HEADERS_ENABLED=false`
**Workaround:** Update CSP directives to allow required domains

### Issue: Rate Limiting Too Aggressive
**Symptoms:** Legitimate API calls returning 429
**Rollback:** `export RATELIMIT_ENABLED=false`
**Workaround:** Adjust limits in `middleware/ratelimit.py`

### Issue: Stripe Webhook Signature Mismatch
**Symptoms:** Payment webhooks returning 401
**Rollback:** `export WEBHOOK_VERIFY_ALL=false`
**Workaround:** Verify STRIPE_WEBHOOK_SECRET matches Stripe dashboard

## Rollback Procedures by Environment

### Development (Replit)
1. Update environment variables in Secrets tab
2. Click "Stop" button
3. Click "Run" button
4. Verify with health checks

### Production (Deployed)
1. Access deployment settings
2. Update environment variables
3. Trigger redeployment or restart
4. Monitor metrics for 5 minutes
5. Run smoke tests

## Post-Rollback Checklist

- [ ] Verify API health: `/ops/uptime` returns 200
- [ ] Check error rate: Sentry dashboard
- [ ] Monitor queue: `/ops/queue_health`
- [ ] Test key endpoints: `/api/v1/status/test`
- [ ] Verify metrics: `/metrics`
- [ ] Check backups: Recent backup exists
- [ ] Review logs: No new errors in last 5 minutes
- [ ] Notify stakeholders: Status update sent

## Communication Templates

### Internal Notification
```
Subject: Phase-4 Rollback - [FEATURE]

We've rolled back [FEATURE] due to [REASON].

Impact: [DESCRIBE]
Rollback completed: [TIME]
Current status: [OPERATIONAL/DEGRADED]
ETA for fix: [TIMEFRAME]

Monitoring closely. Will update in 30 minutes.
```

### Customer Notification (if needed)
```
Subject: Brief Service Interruption - Resolved

We experienced a brief service issue affecting [FEATURE] from [START] to [END] UTC.

The issue has been resolved by temporarily disabling an enhancement while we investigate.

All core functionality is operating normally. Your data is safe.

We apologize for any inconvenience.
```

## Gradual Re-enablement

After rolling back, re-enable features gradually:

### Week 1: Testing
- Enable in development environment only
- Run full test suite
- Monitor for 3 days

### Week 2: Canary
- Enable for 10% of traffic using `CANARY_MODE=true`
- Monitor metrics closely
- If stable for 48 hours, proceed

### Week 3: Full Rollout
- Enable for 50% of traffic
- Monitor for 24 hours
- Enable for 100%

## Permanent Removal (Last Resort)

If a feature is permanently deprecated:

1. **Code Removal:**
   ```bash
   git rm queue/worker.py queue/tasks.py
   git rm middleware/ratelimit.py
   # etc.
   ```

2. **Documentation Update:**
   - Update replit.md
   - Remove from feature lists
   - Archive related docs

3. **Cleanup:**
   - Remove environment variables
   - Delete unused database tables
   - Remove test files

4. **Communication:**
   - Notify all stakeholders
   - Update changelog
   - Document reasons

## Contact & Escalation

- **L1 (On-Call)**: Feature flag rollbacks, health checks
- **L2 (Engineering Lead)**: Code rollbacks, database issues
- **L3 (CTO)**: Security breaches, data loss

**Emergency Contact:** [PHONE/PAGERDUTY]

---

## Appendix: Feature Flag Reference

| Flag | Default | Purpose | Rollback Impact |
|------|---------|---------|----------------|
| `NEW_QUEUE_ENABLED` | false | Async job queue | Sync execution |
| `SECURITY_HEADERS_ENABLED` | false | CSP, HSTS, etc. | Headers removed |
| `RATELIMIT_ENABLED` | false | API rate limiting | No limits |
| `WEBHOOK_VERIFY_ALL` | false | Signature verification | Signatures ignored |
| `ABUSE_GUARDS_ENABLED` | false | Fraud detection | Guards disabled |

All flags use environment variables with graceful degradation built-in.

---

*Last Updated: 2025-11-07*
*Version: 4.0*
*Status: PRODUCTION READY*
