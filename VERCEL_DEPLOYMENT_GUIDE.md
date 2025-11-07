# 🚀 DEPLOY levqor-site TO VERCEL

## ✅ YOUR SITE IS READY!

**Location:** `levqor-site/` folder  
**Framework:** Next.js 14  
**Status:** Built and ready to deploy  

---

## 📋 STEP-BY-STEP DEPLOYMENT

### Step 1: Sign Up / Log In to Vercel

1. Go to **https://vercel.com**
2. Click **"Sign Up"** (or Log In if you have an account)
3. Choose **"Continue with GitHub"** (recommended)
   - Or use Email if you prefer

**Why GitHub?** Makes deploying updates super easy later!

---

### Step 2: Import Your Project

**Method A: Using GitHub (Recommended)**

1. **Upload levqor-site to GitHub:**
   - Create new repository on GitHub
   - Name it: `levqor-site` or `levqor-marketing`
   - Upload the `levqor-site/` folder contents

2. **In Vercel:**
   - Click **"Add New..."** → **"Project"**
   - Click **"Import Git Repository"**
   - Select your GitHub repository
   - Click **"Import"**

**Method B: Direct Upload (Easier, but no auto-updates)**

1. **Create ZIP file of levqor-site:**
   ```bash
   cd levqor-site
   zip -r levqor-site.zip . -x "node_modules/*" ".next/*" ".vercel/*"
   ```

2. **In Vercel:**
   - Use Vercel CLI (see below)

**Method C: Using Vercel CLI (Quick)**

```bash
# Install Vercel CLI
npm i -g vercel

# Go to your site folder
cd levqor-site

# Deploy!
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Scope: Your account
# - Link to existing project? No
# - Project name: levqor-site
# - Directory: ./ (current)
# - Override settings? No

# After deployment, set production domain:
vercel --prod
```

---

### Step 3: Configure Project Settings

**Vercel auto-detects Next.js!** But verify:

- **Framework Preset:** Next.js ✅ (auto-detected)
- **Build Command:** `npm run build` ✅ (auto)
- **Output Directory:** `.next` ✅ (auto)
- **Install Command:** `npm install` ✅ (auto)

**Click "Deploy"** and wait 1-2 minutes!

---

### Step 4: Add Custom Domain (levqor.ai)

After successful deployment:

1. **In Vercel Project:**
   - Go to **Settings** → **Domains**
   - Click **"Add"**
   - Enter: `levqor.ai`
   - Click **"Add"**

2. **Vercel will show DNS instructions:**
   ```
   Type: A
   Name: @
   Value: 76.76.21.21
   
   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   ```
   
   **OR** (depending on your setup):
   ```
   Type: CNAME
   Name: @
   Value: cname.vercel-dns.com
   ```

3. **Copy these values!** You'll add them to Cloudflare next.

---

### Step 5: Configure DNS in Cloudflare

1. **Log into Cloudflare**
2. **Select domain:** levqor.ai
3. **Go to:** DNS → Records

4. **Add/Update records for ROOT domain:**

   **Option A: If Vercel gave you A record:**
   - Type: `A`
   - Name: `@` (root)
   - IPv4: `76.76.21.21` (Vercel IP)
   - Proxy: **DNS only** (gray cloud) ⚠️
   - TTL: Auto

   **Option B: If Vercel gave you CNAME:**
   - Type: `CNAME`
   - Name: `@` (root)
   - Target: `cname.vercel-dns.com`
   - Proxy: **DNS only** (gray cloud) ⚠️
   - TTL: Auto

5. **Keep your existing API subdomain:**
   ```
   Type: A
   Name: api
   Value: [Your Replit IP]
   Proxy: DNS only ✅ (already configured)
   ```

6. **Add www subdomain (optional):**
   - Type: `CNAME`
   - Name: `www`
   - Target: `cname.vercel-dns.com`
   - Proxy: DNS only

7. **Click Save**

---

### Step 6: Wait for Verification

**In Vercel:**
- Go back to Settings → Domains
- Wait for `levqor.ai` to show **"Valid Configuration"**
- Usually takes 1-5 minutes
- Can take up to 1 hour for DNS propagation

**Vercel will automatically:**
- ✅ Provision SSL certificate
- ✅ Configure HTTPS
- ✅ Set up global CDN

---

### Step 7: Test Your Site!

Once verified, test:

```bash
curl -I https://levqor.ai
# Should return 200 OK

curl -I https://api.levqor.ai
# Should still work (backend)
```

**Or just visit in browser:**
- https://levqor.ai → Your marketing site ✅
- https://api.levqor.ai → Your backend API ✅

---

## ✅ SUCCESS CHECKLIST

After deployment:

- [ ] Vercel deployment successful
- [ ] Domain added in Vercel
- [ ] DNS records added in Cloudflare
- [ ] Domain shows "Valid Configuration" in Vercel
- [ ] SSL certificate active
- [ ] https://levqor.ai loads marketing site
- [ ] https://api.levqor.ai still works (backend)

---

## 🎁 FINAL SETUP

**What you'll have:**

```
https://levqor.ai
  → Marketing site (Vercel)
  → Homepage, features, pricing, blog
  → Next.js 14, auto-deployed
  
https://api.levqor.ai
  → Backend API (Replit)
  → All endpoints working
  → Stripe, monitoring, automation
  
https://www.levqor.ai (optional)
  → Redirects to levqor.ai
```

---

## 🔧 TROUBLESHOOTING

### "Invalid Configuration" in Vercel

**Fix:**
- Check DNS records in Cloudflare are correct
- Ensure Cloudflare proxy is **OFF** (gray cloud)
- Wait longer (can take up to 1 hour)
- Remove any conflicting DNS records

---

### SSL Certificate Error

**Fix:**
- Cloudflare proxy must be **DNS only**
- Remove AAAA records if any exist
- Wait for Vercel to provision cert (5-10 min)

---

### Site not loading

**Fix:**
- Check deployment logs in Vercel
- Verify build was successful
- Try: `vercel --prod` to redeploy
- Clear browser cache

---

## 💡 QUICK COMMANDS

**Deploy updates:**
```bash
cd levqor-site
vercel --prod
```

**Check deployment:**
```bash
vercel ls
```

**View logs:**
```bash
vercel logs [deployment-url]
```

---

## 📚 WHAT'S IN YOUR MARKETING SITE

Your `levqor-site` includes:

- ✅ Professional homepage with hero section
- ✅ Features showcase
- ✅ Pricing page
- ✅ Blog system (Markdown-based)
- ✅ Legal pages (Privacy, Terms)
- ✅ SEO optimized
- ✅ Mobile responsive
- ✅ Security headers
- ✅ Fast performance

**It's production-ready!**

---

## 🎊 AFTER DEPLOYMENT

**Update your documentation:**
- Main site: https://levqor.ai
- API docs: https://api.levqor.ai/public/docs
- Status: https://api.levqor.ai/status

**Next steps:**
- Add Google Analytics (if needed)
- Set up monitoring (Vercel Analytics)
- Connect to GitHub for auto-deployments
- Add blog posts

---

*Estimated total time: 15-20 minutes*  
*Your site is ready - just needs to be deployed!* 🚀
