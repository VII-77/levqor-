# Frontend Deployment Summary - app.levqor.ai

## ✅ Configuration Complete

### Environment Variables (Production)
```
NEXT_PUBLIC_BACKEND_BASE=https://api.levqor.ai
NEXT_PUBLIC_BACKEND_CHECKOUT=https://api.levqor.ai/billing/create-checkout-session
NEXT_PUBLIC_BACKEND_SUMMARY=https://api.levqor.ai/api/v1/marketing/summary
NEXT_PUBLIC_ASSETS_BASE=https://api.levqor.ai
NEXT_PUBLIC_APP_NAME=Levqor
DASHBOARD_TOKEN=<your-secret-token>
```

### Canonical Links
- **metadataBase**: `https://app.levqor.ai`
- **Canonical**: `https://app.levqor.ai`
- **OpenGraph URL**: `https://app.levqor.ai`

### Build Verification
```
✅ Next.js 14.2.5 Build: SUCCESSFUL
   - Route / → 95.5 kB (dynamic)
   - Route /pricing → 88.1 kB (static)  
   - Route /dashboard → 87.2 kB (dynamic)

✅ Page Tests:
   - GET / → HTTP 200 OK
   - GET /pricing → HTTP 200 OK
```

### CTA Stripe Integration
```typescript
// CTAButton.tsx workflow:
1. User clicks CTA button
2. POST to ${NEXT_PUBLIC_BACKEND_CHECKOUT}
3. Expects JSON: { "url": "https://checkout.stripe.com/..." }
4. Redirects to Stripe checkout
```

## 📋 DNS Configuration

**File**: `docs/DNS_FRONTEND.txt`

**Cloudflare Setup**:
```
Record Type: CNAME
Name: app
Value: cname.vercel-dns.com
Proxy Status: OFF (⚠️ CRITICAL - must be DNS only)
```

## 🚀 Deployment Steps

### 1. Deploy to Vercel
```bash
cd levqor-web
vercel --prod
```

### 2. Add Custom Domain
- Vercel Dashboard → Project Settings → Domains
- Add domain: `app.levqor.ai`
- Follow Vercel's verification instructions

### 3. Configure DNS (Cloudflare)
- Add CNAME record: `app` → `cname.vercel-dns.com`
- **Disable proxy** (orange cloud OFF - gray cloud ON)
- TTL: Auto

### 4. Set Environment Variables (Vercel)
- Project Settings → Environment Variables
- Add all variables from `.env.local`
- Set for Production environment
- Redeploy after adding variables

### 5. Verify Deployment
```bash
# Test DNS
dig app.levqor.ai CNAME

# Test HTTPS
curl -I https://app.levqor.ai/

# Test backend connectivity
curl -I https://api.levqor.ai/health
```

## ⚠️ Important Notes

1. **Cloudflare Proxy**: MUST be OFF for Vercel SSL to provision
2. **Environment Variables**: Must be set in Vercel dashboard, not just .env.local
3. **Stripe Key**: Ensure `STRIPE_SECRET_KEY` is valid API key (sk_test_... or sk_live_...)
4. **CORS**: Backend already configured for `https://app.levqor.ai`

## 📊 Final Status

```json
{
  "domain_dns": "docs/DNS_FRONTEND.txt",
  "cta": "ok"
}
```

All frontend preparation complete. Ready for Vercel deployment! 🎉
