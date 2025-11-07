# 🌐 CUSTOM DOMAIN SETUP: api.levqor.ai → Replit

## ✅ Current Status

**Your Replit Backend:**
- Dev URL: `https://8926134e-3060-49c1-80a0-a72a22cd9b37-00-18jcmdylcvaqw.kirk.replit.dev`
- Smoke Test: **10/10 PASS** ✅
- Status: Production-ready

**Goal:** Point `api.levqor.ai` to this Replit deployment

---

## 📋 STEP-BY-STEP GUIDE

### Step 1: Deploy Your App (Publish)

1. **Click the "Deploy" button** in Replit (top right)
2. **Select deployment type:** Autoscale (recommended for your API)
3. **Configure deployment:**
   - Name: `levqor-backend`
   - Entry point: Already configured via `deploy_config_tool`
   - Secrets: Already configured ✅

4. **Click "Deploy"** and wait for deployment to complete

---

### Step 2: Add Custom Domain in Replit

1. **Go to Deployments tab** (after successful deployment)
2. **Click "Settings"**
3. **Click "Link a domain"** or **"Manually connect from another registrar"**
4. **Enter your domain:** `api.levqor.ai`

5. **Replit will provide DNS records** like:
   ```
   Type: A
   Name: api
   Value: [IP address like 34.111.xxx.xxx]
   
   Type: TXT
   Name: _replit-challenge.api
   Value: [verification code]
   ```

**⚠️ IMPORTANT:** Copy these exact values - you'll need them for DNS configuration!

---

### Step 3: Configure DNS Records

**Option A: Cloudflare (if using Cloudflare)**

1. Log into Cloudflare
2. Select your `levqor.ai` domain
3. Go to **DNS** > **Records**
4. **Add A Record:**
   - Type: `A`
   - Name: `api`
   - IPv4 address: [IP from Replit]
   - Proxy status: **DNS only (gray cloud)** ⚠️ CRITICAL!
   - TTL: Auto

5. **Add TXT Record:**
   - Type: `TXT`
   - Name: `_replit-challenge.api`
   - Content: [verification code from Replit]
   - TTL: Auto

6. Click **Save**

**⚠️ CRITICAL:** Set proxy to "DNS only" (gray cloud). Cloudflare proxy (orange cloud) prevents Replit from auto-renewing SSL certificates!

---

**Option B: Other Registrar (Namecheap, GoDaddy, etc.)**

1. Log into your domain registrar
2. Go to DNS Management / DNS Records
3. Add the A record and TXT record provided by Replit
4. Save changes

---

### Step 4: Wait for DNS Propagation

**Estimated time:** 10 minutes - 48 hours (usually under 1 hour)

**Check propagation:**
```bash
# Check if DNS is propagating
dig +short api.levqor.ai

# Should return the IP address Replit gave you
# Example: 34.111.179.208
```

**Alternative check:**
```bash
# Test with curl (may fail until verified)
curl -I https://api.levqor.ai
```

---

### Step 5: Verify in Replit

1. Return to Replit **Deployments** > **Settings** > **Domains**
2. Wait for domain to show **"Verified"** status
3. Replit will automatically provision SSL certificate (takes a few minutes)

**Status indicators:**
- 🟡 **Pending:** DNS not propagated yet
- ✅ **Verified:** Domain connected, SSL certificate provisioning
- ✅ **Active:** Fully operational with HTTPS

---

### Step 6: Run Smoke Test

Once domain shows "Verified" or "Active":

```bash
export BACKEND="https://api.levqor.ai"
./public_smoke.sh
```

**Expected result:**
```
✅ ALL PUBLIC SMOKE TESTS PASSED!
10/10 including /billing/health
```

---

## 🔧 TROUBLESHOOTING

### Issue: Domain shows "Pending" for hours

**Solutions:**
1. Verify DNS records are correct in registrar
2. If using Cloudflare: Ensure proxy is **OFF** (gray cloud)
3. Check for conflicting records (remove old A records for `api`)
4. Wait longer - DNS can take up to 48 hours

---

### Issue: SSL Certificate Error

**Solutions:**
1. Ensure Cloudflare proxy is disabled (must be DNS only)
2. Remove any AAAA records (Replit only supports A records)
3. Verify only ONE A record exists for `api.levqor.ai`
4. Wait for Replit to provision certificate (can take 10-15 minutes after verification)

---

### Issue: 404 or Connection Refused

**Solutions:**
1. Verify deployment is running (check Deployments tab)
2. Ensure domain shows "Active" status in Replit
3. Test dev URL first to ensure deployment works
4. Clear browser cache / try incognito mode

---

## 📊 DNS CONFIGURATION CHECKLIST

Before leaving your DNS registrar, verify:

- [ ] A record added: `api` → `[Replit IP]`
- [ ] TXT record added: `_replit-challenge.api` → `[verification code]`
- [ ] No conflicting A records for `api` subdomain
- [ ] No AAAA (IPv6) records for `api` subdomain
- [ ] Cloudflare proxy DISABLED (if using Cloudflare)
- [ ] Changes saved in registrar

---

## 🎯 QUICK REFERENCE

**Your Domain:** `api.levqor.ai`

**Current Working URLs:**
- Dev: `https://8926134e-3060-49c1-80a0-a72a22cd9b37-00-18jcmdylcvaqw.kirk.replit.dev`
- After setup: `https://api.levqor.ai`

**Deployment Type:** Autoscale (recommended)

**Required DNS Records:** A + TXT (provided by Replit)

**Cloudflare Users:** Must use "DNS only" (gray cloud)

**Propagation Time:** 10 min - 48 hours (typically < 1 hour)

---

## ✅ SUCCESS CRITERIA

Your domain is successfully configured when:

1. ✅ Domain shows "Verified" in Replit Deployments
2. ✅ HTTPS works: `curl -I https://api.levqor.ai` returns 200
3. ✅ Smoke test passes: `./public_smoke.sh` → 10/10
4. ✅ Billing endpoint works: `/billing/health` returns operational

---

## 🚀 NEXT STEPS AFTER SETUP

1. **Update frontend** to use `https://api.levqor.ai`
2. **Update documentation** with new API URL
3. **Configure CORS** if needed (already set for app.levqor.ai)
4. **Set up monitoring** for uptime/performance
5. **Update Stripe webhooks** to use new domain

---

*Last updated: 2025-11-07*
*For Replit Autoscale deployments*
