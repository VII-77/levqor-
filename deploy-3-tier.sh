#!/bin/bash
# Deploy Levqor 3-Tier Pricing
set -e

echo "🚀 Deploying Levqor 3-Tier Pricing"
echo "===================================="
echo ""

cd ~/workspace/levqor-site

echo "📝 Step 1: Commit checkout route updates..."
git add src/app/api/checkout/route.ts
git commit -m "Pricing: add Business tier + clean Stripe IDs, static env mapping" || echo "Already committed"
echo ""

echo "📤 Step 2: Push to GitHub..."
git push origin main
echo "✅ Pushed!"
echo ""

echo "⚠️  Step 3: MANUAL ACTION REQUIRED"
echo "=================================="
echo ""
echo "Add these environment variables to Vercel Production:"
cat /tmp/vercel_env_vars.txt
echo ""
echo "Go to: https://vercel.com/vii-77s-projects/levqor-site/settings/environment-variables"
echo ""
echo "Then redeploy from: https://vercel.com/vii-77s-projects/levqor-site/deployments"
echo ""
echo "After Vercel redeploys, run these tests:"
echo ""
echo '  curl -s https://levqor.ai/api/checkout?plan=starter&term=monthly'
echo '  curl -s https://levqor.ai/api/checkout?plan=pro&term=yearly'
echo '  curl -s https://levqor.ai/api/checkout?plan=business&term=monthly'
echo ""
echo "Expected: {\"ok\":true,\"url\":\"https://checkout.stripe.com/...\"}"
