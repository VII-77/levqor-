# ✅ Levqor 3-Tier Pricing - Setup Complete

**Status:** Stripe configured, code updated, ready to deploy  
**Date:** November 10, 2025

---

## 🎯 What Was Done

### ✅ Stripe Products Created

| Product | Monthly | Yearly |
|---------|---------|--------|
| **Levqor Starter** | £19/mo | £190/yr (save £38) |
| **Levqor Pro** | £49/mo | £490/yr (save £98) |
| **Levqor Business** | £149/mo | £1490/yr (save £298) |

**Add-ons created (not yet in checkout):**
- Extra Seat: £10/mo
- Priority Support: £99/mo

---

## 📋 Environment Variables to Add

**Go to:** https://vercel.com/vii-77s-projects/levqor-site/settings/environment-variables

**Add these 6 core variables to Production:**

```
STRIPE_PRICE_STARTER=price_1SRtpZBNwdcDOF992dQ9yf82
STRIPE_PRICE_STARTER_YEAR=price_1SRtpZBNwdcDOF99XoBQH7mg
STRIPE_PRICE_PRO=price_1SRtpZBNwdcDOF990z9ov1QT
STRIPE_PRICE_PRO_YEAR=price_1SRtpaBNwdcDOF99LF9fgL6E
STRIPE_PRICE_BUSINESS=price_1SRtpaBNwdcDOF99fIM8ywkl
STRIPE_PRICE_BUSINESS_YEAR=price_1SRtpaBNwdcDOF998gShL2Bl
```

**Optional (for future add-on support):**

```
STRIPE_PRICE_ADDON_SEAT=price_1SRtpaBNwdcDOF99IHUlZDja
STRIPE_PRICE_ADDON_SUPPORT=price_1SRtpaBNwdcDOF99YPqeRxlV
```

---

## 🚀 Deploy to Production

### Option 1: Automated Script

Run in your Shell terminal:

```bash
./deploy-3-tier.sh
```

### Option 2: Manual Steps

1. **Commit and push:**
   ```bash
   cd ~/workspace/levqor-site
   git add src/app/api/checkout/route.ts
   git commit -m "Pricing: add Business tier + clean Stripe IDs, static env mapping"
   git push origin main
   ```

2. **Add environment variables:**
   - Go to Vercel → Settings → Environment Variables
   - Add the 6 core STRIPE_PRICE_* variables shown above
   - Set environment to "Production"
   - Click "Save"

3. **Redeploy:**
   - Go to Vercel → Deployments
   - Click "Redeploy" on the latest deployment
   - OR click "Deploy" button (top right) → Select "main"

---

## 🧪 Verification Tests

After deployment completes (2-3 minutes), test all endpoints:

```bash
# Starter Monthly
curl -s https://levqor.ai/api/checkout?plan=starter&term=monthly

# Pro Yearly  
curl -s https://levqor.ai/api/checkout?plan=pro&term=yearly

# Business Monthly
curl -s https://levqor.ai/api/checkout?plan=business&term=monthly
```

**Expected response format:**
```json
{
  "ok": true,
  "url": "https://checkout.stripe.com/c/pay/cs_test_...",
  "plan": "starter",
  "term": "monthly"
}
```

---

## 📦 Code Changes

**File:** `levqor-site/src/app/api/checkout/route.ts`

**Key Features:**
- ✅ 3-tier pricing support (Starter, Pro, Business)
- ✅ Monthly and yearly billing options
- ✅ Clean MAP-based price lookup
- ✅ Static environment variable references
- ✅ POST and GET handlers
- ✅ Consistent error handling with `{ ok: false, error: "..." }`
- ✅ Simplified Stripe session creation

---

## 🎨 Next Steps for Frontend

To display the Business tier on your pricing page, update:

**File:** `levqor-site/src/app/pricing/page.tsx`

Add a third pricing card:

```typescript
{
  title: "Business",
  price: billingCycle === "monthly" ? "£149" : "£1490",
  period: billingCycle === "monthly" ? "/month" : "/year",
  features: [
    "Everything in Pro",
    "Unlimited workflows",
    "Advanced analytics",
    "Priority support",
    "Custom integrations",
    "SLA guarantee"
  ],
  cta: "Start Business",
  href: `/api/checkout?plan=business&term=${billingCycle === "monthly" ? "monthly" : "yearly"}`
}
```

---

## ✅ Checklist

- [x] Archive old Stripe products
- [x] Create 3 new products (Starter, Pro, Business)
- [x] Create 6 prices (3 × 2 billing terms)
- [x] Create 2 add-on products
- [x] Update checkout route to support all 3 tiers
- [x] Generate environment variable configuration
- [ ] **Add environment variables to Vercel**
- [ ] **Commit and push code**
- [ ] **Redeploy site**
- [ ] **Verify all 3 tiers work**
- [ ] Update pricing page frontend (optional)

---

**Your 3-tier pricing is configured in Stripe and the code is ready. Just add the env vars and redeploy!** 🚀
