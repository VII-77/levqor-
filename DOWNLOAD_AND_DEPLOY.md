# 📥 DOWNLOAD & DEPLOY LEVQOR-SITE

## 🎯 YOUR MISSION

Download the `levqor-site` folder from Replit → Deploy to Vercel from your computer

**Time:** 15 minutes total

---

## STEP 1: Download from Replit (2 minutes)

### Method A: Download Specific Folder (Easiest)

1. **In Replit file tree** (left sidebar):
   - Find the `levqor-site` folder
   - Right-click on `levqor-site`
   - Click **"Download as zip"**
   - Save to your computer

2. **Unzip the folder:**
   - Find the downloaded `levqor-site.zip`
   - Unzip it to a location you can find
   - Example: `~/Downloads/levqor-site/`

---

### Method B: Use Replit Shell

In the Replit shell:

```bash
# Create a clean ZIP (without node_modules)
cd levqor-site
zip -r ../levqor-site-clean.zip . -x "node_modules/*" ".next/*" ".vercel/*"
cd ..
```

Then download `levqor-site-clean.zip` from the file tree.

---

## STEP 2: Install Vercel CLI (1 minute)

Open **Terminal** (Mac/Linux) or **Command Prompt** (Windows) on your computer:

```bash
npm install -g vercel
```

**Don't have Node.js?** Download from https://nodejs.org

---

## STEP 3: Deploy to Vercel (5 minutes)

### Navigate to the folder:

```bash
cd ~/Downloads/levqor-site
# Or wherever you unzipped it
```

### Install dependencies:

```bash
npm install
```

### Login to Vercel:

```bash
vercel login
```

This opens your browser - follow the login prompts.

### Deploy!

```bash
vercel --prod
```

**Answer the prompts:**
- Set up and deploy? → **Yes**
- Which scope? → **Your account name**
- Link to existing project? → **No**
- Project name? → **levqor-site** (or anything you want)
- In which directory? → **./** (press Enter)
- Override settings? → **No** (press Enter)

**Wait 1-2 minutes...**

✅ **Success!** Vercel gives you a URL like `levqor-site-xyz.vercel.app`

---

## STEP 4: Add Custom Domain (3 minutes)

### In Vercel Dashboard:

1. Go to https://vercel.com/dashboard
2. Click your project: **levqor-site**
3. Go to **Settings** → **Domains**
4. Click **"Add"**
5. Enter: `levqor.ai`
6. Click **"Add"**

Vercel shows you DNS instructions - **COPY THEM!**

Example:
```
Type: A
Name: @
Value: 76.76.21.21
```

---

## STEP 5: Configure Cloudflare DNS (4 minutes)

### In Cloudflare:

1. Log in to https://dash.cloudflare.com
2. Select domain: **levqor.ai**
3. Go to **DNS** → **Records**

### Add root domain record:

**If Vercel gave you an A record:**
- Type: `A`
- Name: `@`
- IPv4: `76.76.21.21` (from Vercel)
- Proxy: **DNS only** ⚠️ (gray cloud, NOT orange)
- TTL: Auto

**If Vercel gave you a CNAME:**
- Type: `CNAME`
- Name: `@`
- Target: `cname.vercel-dns.com`
- Proxy: **DNS only** ⚠️ (gray cloud)
- TTL: Auto

### Keep your API subdomain (don't change):
```
Type: A
Name: api
Value: [Replit IP]
Proxy: DNS only ✅
```

### Click **Save**

---

## STEP 6: Wait & Verify (1-30 minutes)

### In Vercel:
- Go to Settings → Domains
- Wait for `levqor.ai` to show **"Valid Configuration"**
- Usually takes 1-5 minutes
- Can take up to 1 hour for full DNS propagation

### Vercel automatically:
- ✅ Provisions SSL certificate
- ✅ Configures HTTPS
- ✅ Sets up global CDN

---

## STEP 7: Test! 🎉

**Visit in browser:**

✅ https://levqor.ai → Your marketing site  
✅ https://api.levqor.ai → Your backend API (still working)

---

## ✅ SUCCESS CHECKLIST

After completing all steps:

- [ ] Downloaded levqor-site folder
- [ ] Installed Vercel CLI
- [ ] Logged into Vercel
- [ ] Deployed with `vercel --prod`
- [ ] Added domain in Vercel
- [ ] Updated DNS in Cloudflare
- [ ] Domain shows "Valid Configuration"
- [ ] https://levqor.ai loads marketing site
- [ ] https://api.levqor.ai still works

---

## 🎁 WHAT YOU'LL HAVE

```
✅ https://levqor.ai
   → Marketing website (Vercel)
   → Homepage, features, pricing, blog
   → Professional landing page
   → Auto SSL, global CDN

✅ https://api.levqor.ai
   → Backend API (Replit)
   → All endpoints working
   → Stripe, monitoring, automation
```

**Complete platform live!** 🚀

---

## 🔧 TROUBLESHOOTING

### Can't download folder from Replit

**Fix:**
- Use Method B (create ZIP via shell)
- Or download entire project and extract `levqor-site` folder

---

### "command not found: vercel"

**Fix:**
```bash
# Use npx instead:
npx vercel --prod

# Or reinstall:
npm install -g vercel
```

---

### "Invalid Configuration" in Vercel

**Fix:**
- Cloudflare proxy must be **DNS only** (gray cloud)
- Wait longer (can take 1 hour)
- Remove any conflicting DNS records
- Check DNS records match Vercel's instructions exactly

---

### Build fails

**Fix:**
```bash
# Test locally:
cd levqor-site
npm install
npm run build

# If works, redeploy:
vercel --prod
```

---

## 💡 NEED HELP?

**Check these files in levqor-site folder:**
- `DEPLOY_FROM_COMPUTER.md` - Detailed deployment guide
- `README.md` - Site overview
- `VERCEL_DEPLOY.md` - Alternative deployment methods

---

**Total time: 15-20 minutes**  
**Your site is ready to deploy!** 🎉
