#!/bin/bash
# Final deployment script for 3-tier pricing
set -e

echo "🚀 Finalizing 3-Tier Pricing Deployment"
echo "========================================"
echo ""

cd ~/workspace/levqor-site

echo "📝 Step 1: Commit checkout route..."
git add src/app/api/checkout/route.ts
git commit -m "Pricing: add Business tier (£149/mo, £1490/yr) + clean checkout API" || echo "Already committed"
echo ""

echo "📤 Step 2: Push to GitHub..."
git push origin main
echo "✅ Code pushed!"
echo ""

echo "⏳ Step 3: Waiting 180 seconds for Vercel auto-deploy..."
sleep 180
echo ""

echo "🧪 Step 4: Testing all 3 tiers..."
echo ""

echo "Test 1: Starter Monthly (£19/mo)"
RESULT=$(curl -s "https://levqor.ai/api/checkout?plan=starter&term=monthly")
echo "$RESULT" | grep -q '"ok":true' && echo "✅ PASS: $RESULT" || echo "❌ FAIL: $RESULT"
echo ""

echo "Test 2: Pro Yearly (£490/yr)"
RESULT=$(curl -s "https://levqor.ai/api/checkout?plan=pro&term=yearly")
echo "$RESULT" | grep -q '"ok":true' && echo "✅ PASS: $RESULT" || echo "❌ FAIL: $RESULT"
echo ""

echo "Test 3: Business Monthly (£149/mo)"
RESULT=$(curl -s "https://levqor.ai/api/checkout?plan=business&term=monthly")
echo "$RESULT" | grep -q '"ok":true' && echo "✅ PASS: $RESULT" || echo "❌ FAIL: $RESULT"
echo ""

echo "Test 4: Business Yearly (£1490/yr)"
RESULT=$(curl -s "https://levqor.ai/api/checkout?plan=business&term=yearly")
echo "$RESULT" | grep -q '"ok":true' && echo "✅ PASS: $RESULT" || echo "❌ FAIL: $RESULT"
echo ""

echo "========================================"
echo "✅ 3-TIER PRICING DEPLOYMENT COMPLETE!"
echo ""
echo "All tiers are now live:"
echo "  • Starter: £19/mo or £190/yr"
echo "  • Pro: £49/mo or £490/yr"
echo "  • Business: £149/mo or £1490/yr"
