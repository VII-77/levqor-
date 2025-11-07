# Levqor Marketing Site

**Professional Next.js 14 marketing website for Levqor AI automation platform.**

---

## 🚀 Quick Deploy to Vercel

This site is production-ready! Deploy in 5 minutes:

```bash
npm install -g vercel
vercel --prod
```

Then add custom domain `levqor.ai` in Vercel dashboard.

**See `DEPLOY_FROM_COMPUTER.md` for complete instructions.**

---

## 📦 What's Included

- ✅ Professional homepage with hero section
- ✅ Features showcase
- ✅ Pricing page  
- ✅ Blog system (Markdown-based)
- ✅ Legal pages (Privacy Policy, Terms of Service)
- ✅ SEO optimized with OpenGraph tags
- ✅ Mobile responsive design
- ✅ Security headers (CSP, HSTS, COOP)
- ✅ Fast performance

---

## 🛠️ Local Development

```bash
npm install
npm run dev
```

Open http://localhost:5000

---

## 📋 Environment Variables (Optional)

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=https://api.levqor.ai
NEXT_PUBLIC_PLAUSIBLE_DOMAIN=levqor.ai
```

---

## 🌐 Deployment

**Recommended:** Vercel (optimized for Next.js)

1. Deploy: `vercel --prod`
2. Add domain: `levqor.ai` in Vercel dashboard
3. Configure DNS in Cloudflare

**See full guide:** `DEPLOY_FROM_COMPUTER.md`

---

## 📁 Structure

```
levqor-site/
├── src/
│   ├── app/          # Next.js app router pages
│   └── components/   # React components
├── content/          # Blog posts (Markdown)
├── public/           # Static assets
└── vercel.json       # Vercel configuration
```

---

## 🎯 Production URLs

After deployment:

- **Marketing Site:** https://levqor.ai
- **Backend API:** https://api.levqor.ai
- **API Docs:** https://api.levqor.ai/public/docs

---

## 🔧 Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** CSS Modules
- **Deployment:** Vercel
- **Blog:** Markdown files

---

**Ready to deploy!** See `DEPLOY_FROM_COMPUTER.md` for step-by-step instructions.
