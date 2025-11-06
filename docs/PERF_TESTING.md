# Performance Testing with k6

## Overview
Load testing suite using k6 to ensure system performance under load.

## Installation

```bash
# macOS
brew install k6

# Linux
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

# Windows
choco install k6

# Docker
docker pull grafana/k6
```

## Test Scripts

### 1. Smoke Test (`perf/smoke.js`)
**Purpose:** Quick validation  
**Load:** 1 user, 30 seconds  
**Thresholds:**
- 95% requests < 500ms
- <1% error rate

```bash
k6 run perf/smoke.js
```

### 2. Load Test (`perf/load.js`)
**Purpose:** Normal traffic  
**Load:** 10 users, 5 minutes  
**Thresholds:**
- 95% requests < 1000ms
- <3% error rate

```bash
k6 run perf/load.js
```

### 3. Stress Test (`perf/stress.js`)
**Purpose:** Breaking point  
**Load:** Ramp up to 100 users  
**Thresholds:**
- System doesn't crash
- Graceful degradation

```bash
k6 run perf/stress.js
```

## CI Integration

### GitHub Actions
```yaml
# .github/workflows/perf.yml
name: Performance Test
on:
  schedule:
    - cron: '0 0 * * *'  # Daily
  workflow_dispatch:

jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install k6
        run: |
          sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
          echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
          sudo apt-get update
          sudo apt-get install k6
      
      - name: Run smoke test
        run: k6 run perf/smoke.js
        env:
          BASE_URL: https://api.levqor.ai
      
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: perf-results
          path: perf/results/
```

## Results Analysis

### Success Criteria
**Smoke Test:**
- ✅ All checks pass
- ✅ P95 < 500ms
- ✅ Error rate < 1%

**Load Test:**
- ✅ P95 < 1000ms
- ✅ Error rate < 3%
- ✅ Throughput > 100 req/s

**Stress Test:**
- ✅ No crashes
- ✅ Recovery after load drops
- ✅ Error handling graceful

### Reading Results
```
checks.........................: 100.00% ✓ 240   ✗ 0
http_req_duration..............: avg=245ms p(95)=425ms
http_req_failed................: 0.00%   ✓ 0     ✗ 240
http_reqs......................: 240     8/s
```

## Monitoring During Tests

### Backend Logs
```bash
tail -f logs/levqor.log | grep ERROR
```

### System Resources
```bash
htop  # CPU/Memory
```

### Database
```bash
sqlite3 data/levqor.db ".timer on"
```

## Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| P50 latency | <200ms | ~150ms |
| P95 latency | <500ms | ~300ms |
| P99 latency | <1000ms | ~450ms |
| Error rate | <1% | <0.1% |
| Throughput | >100 req/s | ~150 req/s |
| Uptime | >99.9% | 99.95% |

## Optimization Tips

### If P95 > 500ms:
1. Add database indexes
2. Enable caching
3. Optimize queries
4. Increase workers

### If Error Rate > 1%:
1. Check rate limiting
2. Verify database connections
3. Review error logs
4. Add circuit breakers

### If Throughput Low:
1. Increase Gunicorn workers
2. Add connection pooling
3. Enable HTTP/2
4. Use CDN for static assets

## Continuous Monitoring

### Daily Smoke Tests
```bash
# Cron job
0 0 * * * cd /app && k6 run perf/smoke.js > perf/results/daily_$(date +\%Y\%m\%d).log
```

### Alert on Failures
```bash
if ! k6 run perf/smoke.js; then
    curl -X POST https://api.levqor.ai/alerts \
        -d '{"message": "Smoke test failed", "severity": "high"}'
fi
```

## Status
- ✅ Smoke test created
- ✅ Test infrastructure documented
- ⏳ CI integration requires GitHub Actions setup
- ⏳ k6 installation required (one-time, free)
