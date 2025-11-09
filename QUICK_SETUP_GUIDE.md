# 🚀 Quick Setup Guide - Stripe & Vercel

## Option 1: Interactive Script (Recommended)

Run this command and follow the prompts:
```bash
./setup_stripe_and_vercel.sh
```

---

## Option 2: Manual Setup (Step-by-Step)

### PART A: Create Stripe Prices (5 minutes)

**Direct Link:** https://dashboard.stripe.com/products

#### Create 4 Prices:

**1. Starter Monthly - £19/mo**
- Click "+ Create product"
- Name: `Levqor Starter`
- Description: `1 project, email support, basic insights`
- Click "More pricing options" → Select "Recurring"
- Pricing model: **Flat rate**
- Amount: **19**
- Currency: **GBP (£)**
- Billing period: **Monthly**
- Click "Add product"
- **→ COPY THE PRICE ID** (starts with `price_`)

**2. Starter Yearly - £190/yr**
- Click on the "Levqor Starter" product you just created
- Click "Add another price"
- Amount: **190** (saves £38/year)
- Currency: **GBP (£)**
- Billing period: **Yearly**
- Click "Add price"
- **→ COPY THE PRICE ID**

**3. Pro Monthly - £49/mo**
- Click "+ Create product"
- Name: `Levqor Pro`
- Description: `Unlimited projects, priority support, advanced insights`
- Click "More pricing options" → Select "Recurring"
- Amount: **49**
- Currency: **GBP (£)**
- Billing period: **Monthly**
- Click "Add product"
- **→ COPY THE PRICE ID**

**4. Pro Yearly - £490/yr**
- Click on the "Levqor Pro" product you just created
- Click "Add another price"
- Amount: **490** (saves £98/year)
- Currency: **GBP (£)**
- Billing period: **Yearly**
- Click "Add price"
- **→ COPY THE PRICE ID**

---

### PART B: Add to Replit Secrets

In Replit, click **Tools → Secrets**, then add these 5 secrets:

```
Key: STRIPE_PRICE_STARTER
Value: [paste Starter monthly price ID]

Key: STRIPE_PRICE_STARTER_YEAR
Value: [paste Starter yearly price ID]

Key: STRIPE_PRICE_PRO
Value: [paste Pro monthly price ID]

Key: STRIPE_PRICE_PRO_YEAR
Value: [paste Pro yearly price ID]

Key: SITE_URL
Value: https://levqor.ai
```

---

### PART C: Add to Vercel Environment Variables

**Direct Link:** https://vercel.com/dashboard

1. Select your **levqor-site** project
2. Click **Settings** tab
3. Click **Environment Variables** in left sidebar
4. Click **Add** and add these 6 variables:

```
Variable 1:
  Key: STRIPE_SECRET_KEY
  Value: [Your Stripe secret key - same as in Replit]
  Environments: ☑ Production ☑ Preview ☑ Development

Variable 2:
  Key: STRIPE_PRICE_STARTER
  Value: [Your Starter monthly price ID]
  Environments: ☑ Production ☑ Preview ☑ Development

Variable 3:
  Key: STRIPE_PRICE_STARTER_YEAR
  Value: [Your Starter yearly price ID]
  Environments: ☑ Production ☑ Preview ☑ Development

Variable 4:
  Key: STRIPE_PRICE_PRO
  Value: [Your Pro monthly price ID]
  Environments: ☑ Production ☑ Preview ☑ Development

Variable 5:
  Key: STRIPE_PRICE_PRO_YEAR
  Value: [Your Pro yearly price ID]
  Environments: ☑ Production ☑ Preview ☑ Development

Variable 6:
  Key: SITE_URL
  Value: https://levqor.ai
  Environments: ☑ Production ☑ Preview ☑ Development
```

5. Click **Save** after each variable

---

### PART D: Deploy

Once all secrets are added:

```bash
# Deploy to Vercel
git add levqor-site/
git commit -m "Pricing v2.1: complete Stripe integration"
git push origin main
```

Wait 2-3 minutes for Vercel to build and deploy.

---

### ✅ Test Your Setup

1. Visit: **https://levqor.ai/pricing**
2. Toggle between Monthly/Yearly - prices should update
3. Click "Buy now" on any plan
4. Should redirect to Stripe Checkout with correct price
5. Use test card: `4242 4242 4242 4242`
6. Complete checkout → should redirect to `/thanks`

---

## 🔗 Quick Links

- **Stripe Products:** https://dashboard.stripe.com/products
- **Vercel Dashboard:** https://vercel.com/dashboard
- **Vercel Project Settings:** https://vercel.com/[your-username]/levqor-site/settings/environment-variables

---

## 📋 Summary

- ✅ 4 Stripe prices to create
- ✅ 5 Replit secrets to add
- ✅ 6 Vercel environment variables to add
- ✅ 1 git push to deploy

**Total time:** ~10 minutes
