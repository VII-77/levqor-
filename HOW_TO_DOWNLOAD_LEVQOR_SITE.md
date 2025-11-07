# 📥 HOW TO DOWNLOAD levqor-site FROM REPLIT

## ✅ THE FOLDER IS READY!

I've prepared the `levqor-site` folder for download. It's clean and ready to deploy!

---

## 🎯 DOWNLOAD FROM REPLIT

### Method 1: Download Folder Directly (Easiest)

**In Replit:**

1. Look at the **left sidebar** (file tree)
2. Find the **`levqor-site`** folder
3. **Right-click** on `levqor-site`
4. Click **"Download as zip"**
5. Save to your computer
6. **Unzip** the downloaded file

**That's it!** You now have the folder on your computer.

---

### Method 2: Create Clean ZIP (No Dependencies)

**In Replit Shell, run:**

```bash
cd levqor-site
zip -r ../levqor-site-clean.zip . -x "node_modules/*" ".next/*" ".vercel/*"
cd ..
```

Then:
1. Find `levqor-site-clean.zip` in the file tree
2. Right-click → Download
3. Unzip on your computer

**Why this method?** Creates smaller ZIP without `node_modules` (265MB → ~2MB)

---

## 🚀 AFTER DOWNLOADING

**On your computer, open Terminal and run:**

```bash
# Navigate to the folder
cd ~/Downloads/levqor-site
# (or wherever you unzipped it)

# Install dependencies
npm install

# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy!
vercel --prod
```

**Then:**
1. Add domain `levqor.ai` in Vercel dashboard
2. Update DNS in Cloudflare
3. Wait for verification
4. Done! ✅

---

## 📚 GUIDES INCLUDED IN THE FOLDER

When you download `levqor-site`, you'll find these guides:

1. **`README.md`** - Overview of the site
2. **`DEPLOY_FROM_COMPUTER.md`** - Step-by-step deployment guide
3. **`VERCEL_DEPLOY.md`** - Alternative deployment methods
4. **`DEPLOYMENT.md`** - Quick reference

**Start with `DEPLOY_FROM_COMPUTER.md`** - it has everything you need!

---

## ✅ WHAT'S IN THE FOLDER

```
levqor-site/
├── README.md                    ← Start here
├── DEPLOY_FROM_COMPUTER.md      ← Full deployment guide
├── src/                         ← Next.js source code
├── content/                     ← Blog posts (Markdown)
├── package.json                 ← Dependencies
├── vercel.json                  ← Vercel config (ready!)
└── next.config.js               ← Next.js settings
```

**Size:** ~265MB with node_modules, ~2MB without

---

## 🎯 QUICK START AFTER DOWNLOAD

**5-minute deploy:**

```bash
cd levqor-site
npm install
vercel --prod
```

Then add domain in Vercel dashboard → Update DNS → Done!

---

## 💡 COMPLETE INSTRUCTIONS

**I've also created:**
- **`DOWNLOAD_AND_DEPLOY.md`** (in root) - Complete download & deploy walkthrough

**Read that for the full end-to-end process!**

---

*Your site is 100% ready to deploy - just download and run `vercel --prod`!* 🚀
