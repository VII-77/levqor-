# 🚀 Two-Tier Pricing Deployment Guide

## ✅ What's Been Implemented

1. **Two pricing tiers:**
   - **Starter**: £19/month (1 project, email support, basic insights, 100 runs/month)
   - **Pro**: £49/month (unlimited projects, priority support, advanced insights, 1,000 runs/month)

2. **Stripe Checkout API** at `/api/checkout`
   - Handles subscription creation via Stripe
   - Redirects to `/thanks` on success
   - Returns to `/pricing` on cancel

3. **Thank you page** at `/thanks`
   - Confirmation after successful checkout

## 🔧 Setup Required (One-Time)

### Step 1: Create Stripe Price IDs

Run this helper to see instructions:
```bash
./scripts/setup_stripe_prices.sh
```

Or follow these steps manually:

1. **Go to Stripe Dashboard**: https://dashboard.stripe.com/products

2. **Create Starter Plan:**
   - Click "Add product"
   - Name: `Levqor Starter`
   - Description: `1 project, email support, basic insights, 100 workflow runs/month`
   - Pricing Model: `Recurring`
   - Price: `£19 GBP / month`
   - Click "Save product"
   - **Copy the Price ID** (looks like `price_1ABC...`)

3. **Create Pro Plan:**
   - Click "Add product"
   - Name: `Levqor Pro`
   - Description: `Unlimited projects, priority support, advanced insights, 1,000 workflow runs/month`
   - Pricing Model: `Recurring`
   - Price: `£49 GBP / month`
   - Click "Save product"
   - **Copy the Price ID** (looks like `price_1XYZ...`)

### Step 2: Add Secrets to Replit

In the Replit Secrets panel (Tools → Secrets), add:

```
STRIPE_PRICE_STARTER=price_1ABC...  (your Starter price ID)
STRIPE_PRICE_PRO=price_1XYZ...      (your Pro price ID)
SITE_URL=https://levqor.ai          (your frontend URL)
```

## 📦 Deploy to Vercel

Once secrets are added, deploy:

```bash
# Stage the new files
git add levqor-site/src/app/page.tsx \
        levqor-site/src/app/pricing/page.tsx \
        levqor-site/src/app/thanks/page.tsx \
        levqor-site/src/app/api/checkout/route.ts \
        levqor-site/package.json \
        levqor-site/package-lock.json

# Commit
git commit -m "Add two-tier pricing (Starter £19, Pro £49) with Stripe Checkout"

# Push to deploy
git push origin main
```

**Important**: After deploying, add the same 3 secrets to Vercel:
1. Go to: https://vercel.com/your-project/settings/environment-variables
2. Add `STRIPE_PRICE_STARTER`, `STRIPE_PRICE_PRO`, and `SITE_URL`
3. Redeploy if needed

## ✅ Testing

After deployment:

1. **Visit pricing page**: https://levqor.ai/pricing
2. **Click "Buy now"** on either plan
3. **Should redirect** to Stripe Checkout
4. **Use test card**: `4242 4242 4242 4242` (any future date, any CVC)
5. **Complete checkout**
6. **Verify redirect** to https://levqor.ai/thanks

## 🔍 Troubleshooting

**Error: "Unknown plan"**
→ Check that `STRIPE_PRICE_STARTER` and `STRIPE_PRICE_PRO` are set in Vercel

**Error: "Stripe API error"**
→ Verify `STRIPE_SECRET_KEY` is set in Vercel and matches your Stripe account

**Checkout page doesn't load**
→ Check Vercel deployment logs for errors

## 📊 Files Changed

- `levqor-site/src/app/page.tsx` - Simplified homepage (756B)
- `levqor-site/src/app/pricing/page.tsx` - Two-tier pricing (2.1KB)
- `levqor-site/src/app/thanks/page.tsx` - Success page (900B)
- `levqor-site/src/app/api/checkout/route.ts` - Stripe Checkout API (1.2KB)
- `levqor-site/package.json` - Added `stripe` dependency
