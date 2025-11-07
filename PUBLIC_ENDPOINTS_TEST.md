# LEVQOR PUBLIC ENDPOINTS

## 🌐 Base URL
```
https://workspace-vii7cc.replit.app
```

## 📍 Endpoint Tests

### 1. Health Check
**Endpoint**: `/status`  
**Purpose**: Quick health check (200 OK = healthy)

**Test:**
```bash
curl -fsS https://workspace-vii7cc.replit.app/status
```

**Expected Response:**
```json
{"status":"pass"}
```

---

### 2. System Uptime
**Endpoint**: `/ops/uptime`  
**Purpose**: Detailed system health with response time metrics

**Test:**
```bash
curl -fsS https://workspace-vii7cc.replit.app/ops/uptime
```

**Expected Response:**
```json
{
  "response_time_ms": 3.15,
  "services": {
    "api": "operational",
    "database": "operational"
  },
  "status": "operational",
  "timestamp": 1762527164.7359462,
  "version": "1.0.0"
}
```

---

### 3. Queue Health
**Endpoint**: `/ops/queue_health`  
**Purpose**: Check async queue system status

**Test:**
```bash
curl -fsS https://workspace-vii7cc.replit.app/ops/queue_health
```

**Expected Response:**
```json
{
  "depth": 0,
  "dlq": 0,
  "mode": "sync",
  "queue_available": true,
  "retry": 0
}
```

---

### 4. Billing/Stripe Health
**Endpoint**: `/billing/health`  
**Purpose**: Verify Stripe integration and account balance

**Test:**
```bash
curl -fsS https://workspace-vii7cc.replit.app/billing/health
```

**Expected Response:**
```json
{
  "available": [
    {
      "amount": 0,
      "currency": "gbp",
      "source_types": {
        "card": 0
      }
    }
  ],
  "pending": [
    {
      "amount": -23,
      "currency": "gbp",
      "source_types": {
        "card": -23
      }
    }
  ],
  "status": "operational",
  "stripe": true
}
```

---

## 🧪 Quick Test Script

```bash
#!/bin/bash
BASE_URL="https://workspace-vii7cc.replit.app"

echo "Testing Levqor Public Endpoints..."
echo ""

echo "1. Health Check:"
curl -fsS "$BASE_URL/status"
echo ""
echo ""

echo "2. System Uptime:"
curl -fsS "$BASE_URL/ops/uptime" | python3 -m json.tool
echo ""

echo "3. Queue Health:"
curl -fsS "$BASE_URL/ops/queue_health" | python3 -m json.tool
echo ""

echo "4. Billing Health:"
curl -fsS "$BASE_URL/billing/health" | python3 -m json.tool
echo ""

echo "✅ All tests complete!"
```

---

## 📊 Endpoint Summary

| Endpoint | Purpose | Response Time | Status |
|----------|---------|---------------|--------|
| `/status` | Quick health check | <5ms | ✅ |
| `/ops/uptime` | System metrics | <10ms | ✅ |
| `/ops/queue_health` | Queue status | <10ms | ✅ |
| `/billing/health` | Stripe integration | <50ms | ✅ |

---

## 🔧 Troubleshooting

**Connection Refused:**
- Backend may be sleeping (Replit auto-sleep)
- Visit the homepage first to wake it up
- Wait 10 seconds and retry

**500 Internal Server Error:**
- Check application logs
- Verify secrets are configured
- Check `/ops/uptime` for service status

**404 Not Found:**
- Verify endpoint URL is correct
- Check for trailing slashes

---

*Last Updated: 2025-11-07*
