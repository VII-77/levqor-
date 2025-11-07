#!/bin/bash
# === LEVQOR COMPLETE AUTH DEPLOYMENT ===
set -euo pipefail

echo "🚀 Levqor Frontend Deployment with NextAuth + Resend"
echo "===================================================="
echo ""

# Check prerequisites
if [ -z "${VERCEL_TOKEN:-}" ]; then
  echo "❌ ERROR: VERCEL_TOKEN not set"
  echo "   Add your Vercel token to Replit Secrets"
  exit 1
fi

if [ -z "${RESEND_API_KEY:-}" ]; then
  echo "❌ ERROR: RESEND_API_KEY not set"
  echo "   Add your Resend API key to Replit Secrets"
  exit 1
fi

cd levqor-site

echo "✅ Environment variables configured"
echo "   - VERCEL_TOKEN: present"
  echo "   - RESEND_API_KEY: present"
echo ""

# Install Vercel CLI if needed
if ! command -v vercel &> /dev/null; then
  echo "📦 Installing Vercel CLI..."
  npm install -g vercel
fi

# Read NEXTAUTH_SECRET from .env.production
NEXTAUTH_SECRET=$(grep '^NEXTAUTH_SECRET=' .env.production | cut -d'=' -f2)

echo "📋 Deployment Configuration:"
echo "   - Domain: levqor.ai"
echo "   - API URL: https://api.levqor.ai"
echo "   - Email from: no-reply@levqor.ai"
echo ""

# Build first to catch any errors
echo "🔨 Building Next.js application..."
npm run build

# Deploy to Vercel
echo ""
echo "🚀 Deploying to Vercel..."
vercel --token "$VERCEL_TOKEN" \
  --prod \
  --yes \
  --name "levqor" \
  -e NEXTAUTH_URL=https://levqor.ai \
  -e NEXTAUTH_SECRET="$NEXTAUTH_SECRET" \
  -e RESEND_API_KEY="$RESEND_API_KEY" \
  -e AUTH_FROM_EMAIL=no-reply@levqor.ai \
  -e NEXT_PUBLIC_AUTH_FROM=no-reply@levqor.ai \
  -e NEXT_PUBLIC_API_URL=https://api.levqor.ai

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "🌐 Your site: https://levqor.ai"
echo ""
echo "🧪 Test the authentication flow:"
echo "   1. Visit https://levqor.ai/signin"
echo "   2. Enter your email address"
echo "   3. Check your email for the magic link"
echo "   4. Click the link to access /dashboard"
echo ""
echo "📊 Monitor:"
echo "   - Vercel Dashboard: https://vercel.com/dashboard"
echo "   - Resend Dashboard: https://resend.com/emails"
