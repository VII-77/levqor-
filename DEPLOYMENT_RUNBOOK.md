# Levqor Backend - Production Deployment Runbook
**Date:** November 5, 2025  
**Build:** 2025-11-05.1  
**Status:** ✅ READY TO SHIP

---

## ✅ PRE-DEPLOYMENT CHECKLIST COMPLETE

- [x] All 12 hardening deltas implemented
- [x] Architect review passed (zero security issues)
- [x] Deployment configuration set (Autoscale)
- [x] Database backup created: `backups/levqor-2025-11-05-205112.db`
- [x] All production tests passing

---

## 🚀 DEPLOYMENT STEPS

### Step 1: Configure Deployment Environment Variables

In Replit Deployment Settings, add these secrets:

```bash
# Required
API_KEYS=<your-production-keys-comma-separated>

# For first deployment, leave empty
API_KEYS_NEXT=

# Build tracking
BUILD_ID=2025-11-05.1

# Optional (already have defaults in code)
RATE_BURST=20
RATE_GLOBAL=200
MAX_CONTENT_LENGTH=524288
```

### Step 2: Publish on Replit

**Deployment is already configured:**
- ✅ Target: Autoscale
- ✅ Start Command: `gunicorn --workers 2 --threads 4 --timeout 30 --bind 0.0.0.0:5000 --reuse-port --log-level info run:app`
- ✅ Health Check Path: `/`

**Action:** Click the **"Publish"** button in Replit.

### Step 3: DNS Configuration

Set up these DNS records with your provider:

```
A     levqor.ai       -> 76.76.21.21
CNAME www.levqor.ai   -> cname.vercel-dns.com
CNAME api.levqor.ai   -> <your-repl-name>.repl.co
```

### Step 4: Frontend Environment (Vercel)

Set these environment variables in Vercel:

```bash
VITE_API_URL=https://api.levqor.ai
VITE_CHECKOUT_LINK_PILOT=<stripe-test-link>
VITE_CHECKOUT_LINK_PRO=<stripe-test-link>
```

Then deploy frontend.

---

## 🧪 SMOKE TESTS

Run these immediately after deployment:

### Test 1: Root Endpoint + Headers
```bash
# Should return: HTTP/2 200
curl -sI https://api.levqor.ai/ | head -n1

# Should show: Strict-Transport-Security, Content-Security-Policy, X-Frame-Options
curl -sI https://api.levqor.ai/public/metrics | grep -E 'Strict-Transport|Content-Security-Policy|X-Frame-Options'
```

### Test 2: Job Intake → Status
```bash
# Replace with one of your API_KEYS
KEY=<your-production-key>

# Create job and get job_id
jid=$(curl -s -X POST https://api.levqor.ai/api/v1/intake \
  -H "X-Api-Key: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"workflow":"demo","payload":{}}' | jq -r .job_id)

# Check status (should return job with "queued" status)
curl -s https://api.levqor.ai/api/v1/status/$jid | jq
```

### Test 3: Rate Limiting
```bash
# Send 25 rapid requests - should see some 429 responses
for i in $(seq 1 25); do
  curl -s -o /dev/null -w "%{http_code} " \
    -H "X-Api-Key: $KEY" \
    -H "Content-Type: application/json" \
    -d '{"workflow":"test","payload":{}}' \
    https://api.levqor.ai/api/v1/intake
done
echo ""
```

---

## 💾 BACKUP VERIFICATION

**Latest backup created:** `backups/levqor-2025-11-05-205112.db`

Verify backup integrity (run locally or in dev environment):
```bash
sqlite3 backups/levqor-2025-11-05-205112.db "PRAGMA integrity_check;"
# Should output: ok
```

**Backup schedule:** Run `./scripts/backup_db.sh` before major changes or weekly.

---

## 🔑 API KEY ROTATION SCHEDULE

**Today (Day 0):**
- API_KEYS set with production keys
- API_KEYS_NEXT left empty

**T+30 days (First rotation):**
1. Generate new keys
2. Set `API_KEYS_NEXT=<new-keys>`
3. Deploy (both old and new keys work)
4. Update clients to use new keys
5. After all clients migrated: move new keys to `API_KEYS`, clear `API_KEYS_NEXT`
6. Deploy again

See `API_KEY_ROTATION.md` for detailed procedure.

---

## 📋 COMPLIANCE CHECKLIST

- [ ] Add ICO registration number to Privacy Policy (`public/legal/privacy.html`)
- [ ] Verify footer links on frontend:
  - Privacy Policy → `/legal/privacy`
  - Terms of Service → `/legal/terms`
  - Cookie Notice → `/legal/cookies`
  - FAQ → `/faq`
  - API Documentation → `/public/openapi.json`
  - Security Contact → `/.well-known/security.txt`

---

## ⏱️ 24-HOUR MONITORING RUNBOOK

### Hour 0: Launch
- [x] Publish deployment
- [ ] Run all smoke tests above
- [ ] Verify all tests pass

### Hour 1: Monitoring Setup
- [ ] Configure UptimeRobot: `https://api.levqor.ai/health` every 5 minutes
- [ ] Set up alert channels (email/Slack)

### Hours 2-24: Active Monitoring
- [ ] Watch Replit deployment logs
- [ ] Monitor error rate (target: <1%)
- [ ] Check rate-limit frequency
- [ ] Verify security headers on random requests

### Day 1 End: Validation
- [ ] Run rate-limit burst test (expect 429s)
- [ ] **Restore Drill:** 
  - Copy latest backup to new Repl
  - Boot server
  - Run integrity check
  - Verify data present

---

## ✅ SUCCESS CRITERIA

**All of these must pass:**
1. ✅ Smoke tests return expected results
2. ✅ Security headers present on all responses
3. ✅ Rate limiting triggers at 20 requests/minute
4. ✅ Error rate < 1% over 24 hours
5. ✅ Health check uptime > 99%
6. ✅ Backup restore drill successful
7. ✅ No leaked API keys in logs
8. ✅ All compliance links accessible

---

## 🎉 LEVQOR IS LIVE

When all checks pass, your production backend is operational.

**Quick Reference Links:**
- Backend: `https://api.levqor.ai`
- Health: `https://api.levqor.ai/health`
- Metrics: `https://api.levqor.ai/public/metrics`
- API Docs: `https://api.levqor.ai/public/openapi.json`
- Security: `https://api.levqor.ai/.well-known/security.txt`

**Support Contacts:**
- Security issues: security@levqor.ai (per security.txt)
- Operations: ops@levqor.ai
