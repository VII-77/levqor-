# Levqor Monitoring & Error Tracking

## Error Tracking (Sentry)

### Setup
1. Create Sentry account: https://sentry.io
2. Create new project for Levqor
3. Copy DSN
4. Add to Replit Secrets: `SENTRY_DSN=https://...@sentry.io/...`

### Backend Integration
Sentry SDK is configured in `run.py`. When `SENTRY_DSN` is set:
- Automatic error capture
- Performance monitoring (10% sample rate)
- Request tracing

### Frontend Integration
Add to `levqor/frontend`:
```typescript
import * as Sentry from "@sentry/nextjs"

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 0.1,
})
```

## Uptime Monitoring

### BetterStack (Recommended)
1. Sign up: https://betterstack.com/uptime
2. Create monitor for `https://api.levqor.ai/health`
3. Add heartbeat endpoint
4. Set alert channels (email, Slack)

**Free tier:** 10 monitors, 1-min checks

### UptimeRobot (Alternative)
1. Sign up: https://uptimerobot.com
2. Add HTTP monitor: `https://api.levqor.ai/health`
3. Interval: 5 minutes
4. Alert contacts: Your email

**Free tier:** 50 monitors, 5-min checks

## Internal Health Checks

The system performs self-checks every 60 seconds:
```
GET /health      → {"ok": true}
GET /status      → {"status": "operational"}
GET /ready       → {"ready": true, "db": "ok"}
```

Failures logged to `logs/health.log`

## Logging

### Structured Logging
All logs are JSON-formatted for easy parsing:
```json
{
  "timestamp": "2025-11-06T20:00:00Z",
  "level": "INFO",
  "logger": "levqor",
  "message": "Request processed",
  "request_id": "abc123",
  "duration_ms": 45
}
```

### Log Rotation
- Max size: 10MB per file
- Backup count: 5 files
- Old logs compressed automatically

### Accessing Logs
```bash
# Recent logs
tail -f logs/levqor.log

# Search for errors
grep "ERROR" logs/levqor.log

# JSON query (if jq installed)
cat logs/levqor.log | jq 'select(.level=="ERROR")'
```

## Alerting

### Critical Alerts
- API downtime > 5 minutes
- Error rate > 5%
- Database connection failures
- Credit system failures

### Warning Alerts
- Response time > 2s (p95)
- Memory usage > 80%
- Disk usage > 90%

## Costs
- **Sentry:** Free tier (5K errors/month) or $26/month
- **BetterStack:** Free tier (10 monitors) or $20/month
- **UptimeRobot:** Free tier (50 monitors)

## Status: IMPLEMENTED (Config Ready)
- ✅ Configuration files created
- ✅ Internal health checks active
- ⏳ External services require API keys (user action)
