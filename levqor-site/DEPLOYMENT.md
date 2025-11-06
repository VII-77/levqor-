# Levqor.ai Landing Site - Vercel Deployment

## Quick Deploy

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Deploy to Vercel:
   ```bash
   cd /home/runner/workspace/levqor-site
   vercel --prod
   ```

3. Set environment variables in Vercel dashboard:
   - `NEXT_PUBLIC_PLAUSIBLE_DOMAIN=levqor.ai` (if using Plausible analytics)
   - `NEXT_PUBLIC_API_URL=https://api.levqor.ai`

4. Configure custom domain `levqor.ai` in Vercel dashboard

## DNS Configuration for Cloudflare

### A Record (Alternative)
- Type: `A`
- Name: `@`
- Value: `76.76.21.21` (Vercel's IP)
- TTL: Auto

### CNAME Records (Recommended)
- Type: `CNAME`
- Name: `@`
- Value: `cname.vercel-dns.com.`
- TTL: Auto

- Type: `CNAME`
- Name: `www`
- Value: `cname.vercel-dns.com.`
- TTL: Auto

## Post-Deployment

1. Verify site loads at https://levqor.ai
2. Check SEO: sitemap.xml, robots.txt
3. Verify Plausible analytics (if configured)
4. Test all pages: /, /contact, /privacy, /terms
5. Test responsive design on mobile devices

## Features Included

- ✅ Landing page with demo video placeholder
- ✅ Contact page with email addresses
- ✅ Privacy policy
- ✅ Terms of service
- ✅ SEO (metadata, OpenGraph, Twitter Cards)
- ✅ Sitemap.xml
- ✅ Robots.txt
- ✅ Plausible analytics support (optional)
- ✅ Mobile responsive
