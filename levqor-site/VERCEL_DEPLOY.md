# Deploy levqor-site to Vercel

## Method 1: Vercel Dashboard (Easiest)

1. **Push to GitHub** (if not already):
   ```bash
   git add levqor-site/
   git commit -m "Add levqor-site public landing"
   git push
   ```

2. **Import to Vercel**:
   - Go to https://vercel.com/new
   - Import your repository
   - Framework Preset: **Next.js**
   - Root Directory: **levqor-site**
   - Click **Deploy**

3. **Configure Domain**:
   - Go to Project Settings → Domains
   - Add custom domain: `levqor.ai`
   - Update DNS: `CNAME levqor.ai → cname.vercel-dns.com`

4. **Environment Variables** (Optional):
   ```
   NEXT_PUBLIC_PLAUSIBLE_DOMAIN=levqor.ai
   NEXT_PUBLIC_API_URL=https://api.levqor.ai
   ```

---

## Method 2: CLI Deploy (From Local Machine)

1. **Install Vercel CLI** (on your local machine):
   ```bash
   npm install -g vercel
   ```

2. **Login**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   cd levqor-site
   vercel --prod
   ```

---

## Method 3: CLI from Replit (Using Token)

1. **Get Vercel Token**:
   - Go to https://vercel.com/account/tokens
   - Create new token
   - Copy the token

2. **Deploy with Token**:
   ```bash
   cd levqor-site
   VERCEL_TOKEN=your_token_here vercel --prod --token=$VERCEL_TOKEN
   ```

---

## Post-Deployment Checklist

✅ Verify all routes work:
- https://levqor.ai/
- https://levqor.ai/blog
- https://levqor.ai/contact
- https://levqor.ai/privacy
- https://levqor.ai/terms

✅ Check SEO:
- View page source, confirm OpenGraph tags
- Test sharing on Twitter/LinkedIn
- Submit sitemap to Google Search Console

✅ Test Analytics (if configured):
- Check Plausible dashboard
- Verify page view events

---

## Build Output

Your site is already optimized:
- **10 static routes** (all pre-rendered)
- **87 kB** total JavaScript
- **Mobile responsive**
- **SEO optimized**

Deploy time: ~2 minutes on Vercel ⚡
