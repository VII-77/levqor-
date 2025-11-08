#!/bin/bash
set -e

echo "🚀 Deploying Levqor frontend to Vercel..."

# Navigate to frontend directory
cd /home/runner/workspace/levqor-site

# Clean build artifacts
echo "🧹 Cleaning build artifacts..."
rm -rf .next .vercel

# Deploy to Vercel with proper configuration
echo "📦 Deploying to Vercel..."
vercel \
  --token $VERCEL_TOKEN \
  --prod \
  --yes \
  --force \
  --name levqor \
  -e NEXTAUTH_URL=https://levqor.ai \
  -e NEXT_PUBLIC_API_URL=https://api.levqor.ai \
  -e AUTH_FROM_EMAIL=no-reply@levqor.ai \
  -e NEXT_PUBLIC_AUTH_FROM=no-reply@levqor.ai \
  -e RESEND_API_KEY=$RESEND_API_KEY \
  -e NEXTAUTH_SECRET=vTYc1NItPfyeaZzfpPQdIuQnbY4lrb6b0-eeqa9qlFo=

echo "✅ Deployment complete!"
echo ""
echo "Your site should be live at: https://levqor.ai"
echo "Wait 1-2 minutes for the deployment to propagate, then test:"
echo "  - https://levqor.ai (homepage)"
echo "  - https://levqor.ai/signin (sign-in page)"
echo "  - https://levqor.ai/dashboard (protected dashboard)"
