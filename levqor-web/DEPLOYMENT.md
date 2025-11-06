# Deployment Guide for Levqor Frontend

## Quick Start

The Next.js frontend has been built successfully and is ready to deploy.

## Deployment Options

### Option 1: Vercel (Recommended)

Vercel is the creators of Next.js and provides the best deployment experience.

**Steps:**

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy from the `levqor-web/` directory:
```bash
cd levqor-web
vercel --prod
```

4. Follow the prompts to:
   - Link to existing project or create new one
   - Configure environment variables (copy from .env.local)
   - Deploy

**Environment Variables to Set in Vercel:**
```
NEXT_PUBLIC_BACKEND_BASE=https://api.levqor.ai
NEXT_PUBLIC_BACKEND_CHECKOUT=https://api.levqor.ai/billing/create-checkout-session
NEXT_PUBLIC_BACKEND_SUMMARY=https://api.levqor.ai/api/v1/marketing/summary
NEXT_PUBLIC_ASSETS_BASE=https://api.levqor.ai
NEXT_PUBLIC_APP_NAME=Levqor
```

Optional analytics (leave empty if not using):
```
NEXT_PUBLIC_PLAUSIBLE_DOMAIN=
NEXT_PUBLIC_HEAP_ID=
```

### Option 2: Netlify

1. Install Netlify CLI:
```bash
npm i -g netlify-cli
```

2. Build and deploy:
```bash
cd levqor-web
netlify deploy --prod --dir=.next
```

### Option 3: Docker

Create a Dockerfile:
```dockerfile
FROM node:20-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000
ENV PORT 3000

CMD ["node", "server.js"]
```

Build and run:
```bash
docker build -t levqor-web .
docker run -p 3000:3000 levqor-web
```

### Option 4: Manual Server Deployment

1. Copy the `levqor-web/` folder to your server
2. Install dependencies: `npm install`
3. Build: `npm run build`
4. Start: `npm run start`

Make sure to set the environment variables on your server.

## Custom Domain Configuration

### Vercel
1. Go to your project settings
2. Add custom domain under "Domains"
3. Follow DNS configuration instructions

### Netlify
1. Go to Domain settings
2. Add custom domain
3. Update DNS records as instructed

## Post-Deployment Checklist

- [ ] Verify frontend loads at deployed URL
- [ ] Test landing page (/)
- [ ] Test pricing page (/pricing)
- [ ] Click "Start Free Trial" button - should redirect to Stripe checkout
- [ ] Verify newsletter signup form works
- [ ] Check live stats widget displays data
- [ ] Verify OpenGraph meta tags (view page source)
- [ ] Test on mobile devices
- [ ] Configure custom domain (if applicable)
- [ ] Set up SSL certificate (usually automatic)
- [ ] Update backend CORS if needed to allow frontend domain

## Troubleshooting

### Build Errors
- Ensure all environment variables are set
- Check Node.js version is 18+
- Clear `.next` folder and rebuild

### Runtime Errors
- Verify backend API is accessible from deployed location
- Check browser console for CORS errors
- Ensure environment variables are properly set in deployment platform

### Performance
- Enable ISR (Incremental Static Regeneration) for `/` and `/pricing`
- Configure CDN caching headers
- Optimize images if replacing og-image.jpg

## Monitoring

Once deployed, monitor:
- Page load times
- API response times from backend
- Error rates in browser console
- Analytics (if Plausible/Heap configured)
