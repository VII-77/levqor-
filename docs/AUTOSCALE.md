# Levqor Autoscaling Configuration

## Overview
Levqor runs on Replit Autoscale with automatic cold start detection and health monitoring.

## Configuration

### Cold Start Detection
The system detects cold starts when response time exceeds 3000ms and can fallback to a local worker pool.

**Config:** `config/scale.json`

### Health Monitoring

**Internal Ping:**
- Checks `/health`, `/status`, `/ready` every 60 seconds
- Logs failures to `logs/health.log`
- Auto-restarts on consecutive failures

**External Monitoring (UptimeRobot):**
1. Create account at https://uptimerobot.com
2. Add monitors:
   - `https://api.levqor.ai/health` (every 5 min)
   - `https://api.levqor.ai/status` (every 10 min)
3. Configure alert contacts

### Deployment Settings
- **Platform:** Replit Autoscale
- **Workers:** 2 (configurable via `GUNICORN_WORKERS`)
- **Threads:** 4 per worker (`GUNICORN_THREADS`)
- **Timeout:** 30s (`GUNICORN_TIMEOUT`)

## Scaling Behavior
- **Auto-scale:** Based on request load
- **Cold starts:** <3s typical, <5s worst case
- **Fallback:** Local worker pool activates if cold starts exceed threshold

## Monitoring
Check scaling metrics:
```bash
curl https://api.levqor.ai/metrics
```

## Costs
- Replit Autoscale: Pay per compute time
- UptimeRobot: Free tier (50 monitors)
- No additional infrastructure needed
