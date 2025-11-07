# 🌐 WHY levqor.ai SHOWS "NOT FOUND"

## 🔍 THE ISSUE

**What's happening:**
- ✅ `api.levqor.ai` → Works perfectly! (your Flask backend)
- ❌ `levqor.ai` → Returns 404 "Not Found"

**Why?**
You only configured the **api** subdomain, not the **root** domain.

---

## 📊 WHAT YOU HAVE

You built **TWO separate applications:**

### 1. Backend API ✅ DEPLOYED
- **URL:** `api.levqor.ai`
- **Type:** Flask backend
- **Purpose:** API endpoints
- **Status:** Working perfectly!

### 2. Marketing Site ❌ NOT DEPLOYED
- **Should be:** `levqor.ai`
- **Type:** Next.js website
- **Location:** `levqor-site/` folder in your project
- **Status:** Built but not deployed

---

## ✅ THE SOLUTION

You need to deploy your marketing site to the root domain.

### Option 1: Deploy to Vercel (Recommended - 15 min)

**What is Vercel?**
Free hosting platform perfect for Next.js sites (the company that makes Next.js)

**Steps:**

1. **Sign up at vercel.com** (free)

2. **Import your levqor-site project**
   - Click "New Project"
   - Connect your code (can upload folder)
   - Vercel auto-detects Next.js
   - Click "Deploy"

3. **Add custom domain**
   - In Vercel project settings
   - Go to "Domains"
   - Add `levqor.ai`
   - Vercel gives you DNS records

4. **Update Cloudflare DNS**
   - Keep: `api` → Replit (already working)
   - Add: `@` (root) → Vercel (new)

**Result:**
- `levqor.ai` → Your marketing site
- `api.levqor.ai` → Your backend (unchanged)

---

### Option 2: Simple Redirect (5 minutes)

**Quick fix to make root domain work immediately**

**Steps in Cloudflare:**

1. Go to **Rules** → **Redirect Rules**
2. Click "Create Rule"
3. Configure:
   - **Name:** "Root to API"
   - **When:** Hostname equals `levqor.ai`
   - **Then:** Redirect to `https://api.levqor.ai`
   - **Status:** 301 (Permanent)
4. Click Save

**Result:**
Visiting `levqor.ai` automatically redirects to `api.levqor.ai`

---

### Option 3: Simple HTML Landing Page

**Create basic homepage**

1. Create simple HTML file
2. Deploy to Cloudflare Pages (free)
3. Point root domain to it

---

## 🎯 MY RECOMMENDATION

**Deploy levqor-site to Vercel** because:

✅ You already built a professional Next.js marketing site  
✅ Vercel is free for your use case  
✅ Takes 15 minutes  
✅ Automatic SSL, global CDN  
✅ Professional setup  

Your `levqor-site/` folder has:
- Homepage with hero section
- Features page
- Pricing
- Blog
- Legal pages
- SEO optimization

**It's ready to go!** Just needs to be deployed.

---

## 📋 WHAT YOUR DNS SHOULD LOOK LIKE

**Current (API only):**
```
api.levqor.ai    A    [Replit IP]        ✅ Working
```

**After fixing root domain:**
```
api.levqor.ai    A       [Replit IP]         ✅ Backend API
levqor.ai        CNAME   cname.vercel.com    ✅ Marketing site
```

---

## 🎁 FINAL SETUP

After deploying the marketing site:

```
https://levqor.ai
  → Marketing website (Vercel)
  → Homepage, features, pricing, blog
  ✅ Professional landing page

https://api.levqor.ai  
  → Backend API (Replit)
  → All your endpoints working
  ✅ Already operational!
```

---

## ❓ WHAT DO YOU WANT TO DO?

**Choose one:**

1. **Deploy marketing site to Vercel** (recommended)
   - I can help prepare the levqor-site folder

2. **Create simple redirect** (quick fix)
   - Just redirect levqor.ai → api.levqor.ai

3. **Create basic landing page** (custom HTML)
   - Simple "Coming Soon" or info page

Let me know which option you prefer!

---

*Your API is working perfectly - we just need to put something at the root domain!*
