#!/bin/bash
set -e

cd levqor-site

echo "🚀 Deploying Levqor to Vercel..."

# Install Vercel CLI if needed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Build
echo "🔨 Building Next.js app..."
npm run build

# Deploy
echo "☁️  Deploying to production..."
vercel --prod --yes --name levqor \
  -e NEXTAUTH_URL=https://levqor.ai \
  -e NEXT_PUBLIC_API_URL=https://api.levqor.ai \
  -e AUTH_FROM_EMAIL=no-reply@levqor.ai \
  -e NEXT_PUBLIC_AUTH_FROM=no-reply@levqor.ai \
  -e RESEND_API_KEY="$RESEND_API_KEY" \
  -e NEXTAUTH_SECRET=vTYc1NItPfyeaZzfpPQdIuQnbY4lrb6b0-eeqa9qlFo=

echo ""
echo "✅ DEPLOY COMPLETE!"
echo ""
echo "Frontend:  https://levqor.ai"
echo "Sign-in:   https://levqor.ai/signin"
echo "Dashboard: https://levqor.ai/dashboard"
echo ""
echo "Next: Open /signin, enter email, click magic link"
