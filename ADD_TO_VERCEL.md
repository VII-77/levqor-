# 🌐 Add Environment Variables to Vercel

## Quick Link
👉 **https://vercel.com/dashboard**

---

## Steps

1. **Open Vercel** and select your **levqor-site** project
2. Click **Settings** tab (top navigation)
3. Click **Environment Variables** (left sidebar)
4. Click **Add New** button

---

## Add These 6 Variables

For each variable below:
- Click "Add New" 
- Enter Key and Value
- **Check all 3 boxes:** ☑ Production ☑ Preview ☑ Development
- Click "Save"

---

### Variable 1: STRIPE_SECRET_KEY
```
Key: STRIPE_SECRET_KEY
Value: [Copy from Replit Secrets - your sk_live_... or sk_test_... key]
☑ Production  ☑ Preview  ☑ Development
```

### Variable 2: STRIPE_PRICE_STARTER
```
Key: STRIPE_PRICE_STARTER
Value: price_1SRVexBNwdcDOF999Z60rAxx
☑ Production  ☑ Preview  ☑ Development
```

### Variable 3: STRIPE_PRICE_STARTER_YEAR
```
Key: STRIPE_PRICE_STARTER_YEAR
Value: price_1SRVexBNwdcDOF99K23wFq5b
☑ Production  ☑ Preview  ☑ Development
```

### Variable 4: STRIPE_PRICE_PRO
```
Key: STRIPE_PRICE_PRO
Value: price_1SRVexBNwdcDOF99mKJiXeRZ
☑ Production  ☑ Preview  ☑ Development
```

### Variable 5: STRIPE_PRICE_PRO_YEAR
```
Key: STRIPE_PRICE_PRO_YEAR
Value: price_1SRVexBNwdcDOF99aLTW8cCJ
☑ Production  ☑ Preview  ☑ Development
```

### Variable 6: SITE_URL
```
Key: SITE_URL
Value: https://levqor.ai
☑ Production  ☑ Preview  ☑ Development
```

---

## After Adding All Variables

Once all 6 variables are saved in Vercel, deploy:

```bash
git add levqor-site/
git commit -m "Pricing v2.1: monthly+yearly plans with Stripe integration"
git push origin main
```

Vercel will automatically deploy (2-3 minutes).

---

## Test After Deployment

Visit: **https://levqor.ai/pricing**

You should see:
- ✅ Monthly/Yearly toggle
- ✅ Starter £19/mo or £190/yr
- ✅ Pro £49/mo or £490/yr
- ✅ "Buy now" buttons redirect to Stripe Checkout

---

✅ **You're done!**
