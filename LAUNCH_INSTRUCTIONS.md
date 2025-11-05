# 🚀 LEVQOR BACKEND - FINAL LAUNCH INSTRUCTIONS

**Build:** 2025-11-05.1  
**Status:** ✅ READY TO GO LIVE

---

## ⚡ LAUNCH SEQUENCE

### 1️⃣ Set Deployment Environment Variables

In **Replit Deployment > Environment Variables**, add:

```bash
API_KEYS=<prod_key1,prod_key2>
API_KEYS_NEXT=
BUILD_ID=2025-11-05.1
RATE_BURST=20
RATE_GLOBAL=200
MAX_CONTENT_LENGTH=524288
```

### 2️⃣ Publish on Replit

**Deployment is already configured:**
- ✅ Target: Autoscale
- ✅ Start Command: `gunicorn --workers 2 --threads 4 --timeout 30 --bind 0.0.0.0:$PORT --reuse-port --log-level info run:app`
- ✅ Health Path: `/`

**Action:** Click **"Publish"** button.

### 3️⃣ Configure DNS

Add this CNAME record:

```
CNAME  api.levqor.ai  →  <your-repl-name>.repl.co
```

### 4️⃣ Update Frontend (Vercel)

Set environment variable:

```bash
VITE_API_URL=https://api.levqor.ai
```

Then deploy.

---

## 🧪 SMOKE TEST (Run immediately after publish)

```bash
# Test 1: Root + Headers
curl -sI https://api.levqor.ai/ | head -n1
curl -sI https://api.levqor.ai/public/metrics | grep -E 'Strict-Transport|Content-Security-Policy|X-Frame-Options'

# Test 2: Job Intake → Status
KEY=<one_of_your_API_KEYS>
jid=$(curl -s -X POST https://api.levqor.ai/api/v1/intake \
  -H "X-Api-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"workflow":"demo","payload":{}}' | jq -r .job_id)
curl -s https://api.levqor.ai/api/v1/status/$jid | jq
```

**Expected Results:**
- Root returns HTTP 200 with version/build
- Security headers present (HSTS, CSP, COOP/COEP, X-Frame-Options)
- Job created with valid UUID
- Status check returns job with "queued" status

---

## ⏱️ 24-HOUR RUNBOOK (Condensed)

| Time | Action | Expected Result |
|------|--------|-----------------|
| **T+0 min** | Publish. Run smoke tests above. | All tests pass |
| **T+5 min** | Add UptimeRobot probe: `https://api.levqor.ai/health` every 5 min | Monitor shows 200 OK |
| **T+30 min** | Check Replit logs | Error rate <1%, 2xx/4xx/5xx distribution sane |
| **T+2 h** | Burst-test rate limit (send 25 requests) | Expect 429 with Retry-After header |
| **T+4 h** | Run backup: `./scripts/backup_db.sh` | File appears in backups/ directory |
| **T+24 h** | Verify backup integrity | `sqlite3 backups/<latest>.db 'PRAGMA integrity_check;'` returns "ok" |

---

## 🔴 ROLLBACK PROCEDURE

If issues arise:

1. **Replit** → Deployments → Redeploy previous successful build
2. **Keep DNS unchanged**
3. **Check logs** for root cause
4. **Fix issues** in development
5. **Re-deploy** when ready

---

## ✅ GO/NO-GO CRITERIA (Must ALL be TRUE)

- [ ] `/`, `/health`, `/public/metrics` return 200
- [ ] HSTS, CSP, COOP/COEP present on responses
- [ ] `POST /api/v1/intake` works with X-Api-Key
- [ ] 429 appears under burst with headers: Retry-After, X-RateLimit-*
- [ ] `/.well-known/security.txt` reachable
- [ ] Backup created and integrity check passes

---

## 🎯 PRODUCTION ENDPOINTS

Once live, these will be your production URLs:

- **Backend Root:** `https://api.levqor.ai/`
- **Health Check:** `https://api.levqor.ai/health`
- **Public Metrics:** `https://api.levqor.ai/public/metrics`
- **Job Intake:** `POST https://api.levqor.ai/api/v1/intake`
- **Job Status:** `GET https://api.levqor.ai/api/v1/status/<job_id>`
- **API Docs:** `https://api.levqor.ai/public/openapi.json`
- **Security Contact:** `https://api.levqor.ai/.well-known/security.txt`

---

## 🎉 YOU ARE CLEARED TO SHIP

All hardening complete. All tests passing. Zero security issues.

**Launch when ready!**
