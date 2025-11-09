# 🚀 START HERE - Super Easy Setup (10 Minutes)

Follow these 3 simple parts. Each step has exactly what to click and what to copy/paste.

---

## 📦 PART 1: Create Stripe Prices (5 minutes)

### Click this link to open Stripe:
👉 **https://dashboard.stripe.com/products**

Now follow these 4 mini-steps:

---

### 🟦 PRICE 1 of 4: Starter Monthly (£19)

1. Click the blue **"+ Create product"** button (top right)
2. Fill in the form:
   - **Name:** Copy this → `Levqor Starter`
   - **Description:** Copy this → `1 project, email support, basic insights`
3. Under the price section:
   - Click **"More pricing options"**
   - Select **"Recurring"** (the circular radio button)
   - **Pricing model:** Select "Flat rate" from dropdown
   - **Amount:** Type `19`
   - **Currency:** Select `GBP (£)` from dropdown
   - **Billing period:** Select **"Monthly"** from dropdown
4. Click the blue **"Add product"** button at bottom
5. **IMPORTANT:** You'll see a Price ID that looks like `price_1ABC...`
   - Click the **copy icon** next to it (or select and Ctrl+C / Cmd+C)
   - Open a text file and paste it with label: `STARTER_MONTHLY=price_...`

✅ **Success:** You should see "Levqor Starter" in your products list

---

### 🟦 PRICE 2 of 4: Starter Yearly (£190)

1. **Don't** create a new product - click on **"Levqor Starter"** you just created
2. Click **"Add another price"** button
3. Fill in:
   - **Pricing model:** Flat rate
   - **Amount:** Type `190` (this gives 2 months free!)
   - **Currency:** GBP (£)
   - **Billing period:** Select **"Yearly"** from dropdown
4. Click **"Add price"**
5. **Copy the new Price ID** and save it as: `STARTER_YEARLY=price_...`

✅ **Success:** Levqor Starter now shows 2 prices (£19/mo and £190/yr)

---

### 🟦 PRICE 3 of 4: Pro Monthly (£49)

1. Go back to products list (click "Products" in left sidebar)
2. Click **"+ Create product"** again
3. Fill in:
   - **Name:** `Levqor Pro`
   - **Description:** `Unlimited projects, priority support, advanced insights`
4. Under price:
   - Click **"More pricing options"** → **"Recurring"**
   - **Amount:** `49`
   - **Currency:** GBP (£)
   - **Billing period:** **"Monthly"**
5. Click **"Add product"**
6. **Copy the Price ID** and save: `PRO_MONTHLY=price_...`

✅ **Success:** You now have 2 products (Starter and Pro)

---

### 🟦 PRICE 4 of 4: Pro Yearly (£490)

1. Click on **"Levqor Pro"** product
2. Click **"Add another price"**
3. Fill in:
   - **Amount:** `490` (2 months free!)
   - **Currency:** GBP (£)
   - **Billing period:** **"Yearly"**
4. Click **"Add price"**
5. **Copy the Price ID** and save: `PRO_YEARLY=price_...`

✅ **Success:** All done with Stripe! You should have 4 price IDs saved.

---

## 🔐 PART 2: Add to Replit Secrets (2 minutes)

### In Replit (this window):

1. Look at the **left sidebar**
2. Click **"Tools"** (wrench icon)
3. Click **"Secrets"**
4. You'll see a form with "Key" and "Value" fields

### Add these 5 secrets one by one:

**Secret 1:**
- Key: `STRIPE_PRICE_STARTER`
- Value: [Paste your STARTER_MONTHLY price ID from Part 1]
- Click "Add new secret"

**Secret 2:**
- Key: `STRIPE_PRICE_STARTER_YEAR`
- Value: [Paste your STARTER_YEARLY price ID]
- Click "Add new secret"

**Secret 3:**
- Key: `STRIPE_PRICE_PRO`
- Value: [Paste your PRO_MONTHLY price ID]
- Click "Add new secret"

**Secret 4:**
- Key: `STRIPE_PRICE_PRO_YEAR`
- Value: [Paste your PRO_YEARLY price ID]
- Click "Add new secret"

**Secret 5:**
- Key: `SITE_URL`
- Value: `https://levqor.ai`
- Click "Add new secret"

✅ **Success:** You should see 5 new secrets in the list

---

## 🌐 PART 3: Add to Vercel (3 minutes)

### Click this link to open Vercel:
👉 **https://vercel.com/dashboard**

1. **Find your project** - Look for "levqor-site" or similar in the list
2. **Click on your project name**
3. At the top, click the **"Settings"** tab
4. In the left sidebar, click **"Environment Variables"**

### Add these 6 variables (one at a time):

For each variable:
- Click **"Add New"** or **"New Variable"** button
- Fill in Key and Value
- **Check ALL THREE boxes:** Production, Preview, Development
- Click "Save"

---

**Variable 1:**
```
Key: STRIPE_SECRET_KEY
Value: [Go to Replit Secrets and copy the value of STRIPE_SECRET_KEY]
☑ Production  ☑ Preview  ☑ Development
```

**Variable 2:**
```
Key: STRIPE_PRICE_STARTER
Value: [Your STARTER_MONTHLY price ID from Part 1]
☑ Production  ☑ Preview  ☑ Development
```

**Variable 3:**
```
Key: STRIPE_PRICE_STARTER_YEAR
Value: [Your STARTER_YEARLY price ID from Part 1]
☑ Production  ☑ Preview  ☑ Development
```

**Variable 4:**
```
Key: STRIPE_PRICE_PRO
Value: [Your PRO_MONTHLY price ID from Part 1]
☑ Production  ☑ Preview  ☑ Development
```

**Variable 5:**
```
Key: STRIPE_PRICE_PRO_YEAR
Value: [Your PRO_YEARLY price ID from Part 1]
☑ Production  ☑ Preview  ☑ Development
```

**Variable 6:**
```
Key: SITE_URL
Value: https://levqor.ai
☑ Production  ☑ Preview  ☑ Development
```

✅ **Success:** You should see 6 environment variables listed

---

## 🚀 FINAL STEP: Deploy (1 minute)

Come back to this Replit window and paste these commands in the **Shell** at the bottom:

```bash
# Remove any locks
rm -f .git/index.lock

# Add your changes
git add levqor-site/

# Save your changes
git commit -m "Add Stripe pricing with monthly/yearly plans"

# Deploy to Vercel (automatic)
git push origin main
```

✅ **Success:** You'll see "Everything up-to-date" or upload progress

**Wait 2-3 minutes** for Vercel to rebuild your site.

---

## 🎉 TEST YOUR PRICING PAGE

After 2-3 minutes, visit:
👉 **https://levqor.ai/pricing**

**What you should see:**
- ✅ Two buttons at top: "Monthly" and "Yearly"
- ✅ Two pricing cards: "Starter" and "Pro"
- ✅ When you click "Monthly", prices show £19 and £49
- ✅ When you click "Yearly", prices show £190 and £490
- ✅ Click any "Buy now" button → Should redirect to Stripe checkout

**Test checkout (use test card):**
- Card number: `4242 4242 4242 4242`
- Expiry: Any future date (like `12/25`)
- CVC: Any 3 digits (like `123`)
- Complete checkout → Should redirect to thank you page

---

## ❓ Need Help?

**Problem: "Price IDs don't work"**
→ Double-check you copied them correctly from Stripe (should start with `price_`)

**Problem: "Checkout doesn't load"**
→ Make sure all 6 variables are in Vercel with all 3 environments checked

**Problem: "Page not updating"**
→ Wait the full 2-3 minutes for Vercel to finish building

---

## ✅ Checklist

- [ ] Created 4 Stripe prices
- [ ] Added 5 secrets to Replit
- [ ] Added 6 variables to Vercel
- [ ] Ran git commands
- [ ] Waited 2-3 minutes
- [ ] Tested at levqor.ai/pricing

**When all checked, you're done! 🎉**
