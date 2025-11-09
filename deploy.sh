#!/bin/bash
# Levqor Stripe Checkout - Deploy Script
# Run this to push code and verify deployment

set -e

echo "🚀 Deploying Levqor Stripe Checkout Fix"
echo "========================================"
echo ""

cd ~/workspace/levqor-site

echo "📤 Step 1: Pushing code to GitHub..."
git push origin main
echo "✅ Code pushed!"
echo ""

echo "⏳ Step 2: Waiting 180 seconds for Vercel to deploy..."
sleep 180
echo "✅ Wait complete!"
echo ""

echo "🧪 Step 3: Testing endpoints..."
echo ""

echo "Test 1: Starter Monthly"
RESULT1=$(curl -s -X POST https://levqor.ai/api/checkout \
  -H 'content-type: application/json' \
  --data '{"plan":"starter","term":"monthly"}')
echo "$RESULT1"
echo ""

echo "Test 2: Pro Monthly"
RESULT2=$(curl -s -X POST https://levqor.ai/api/checkout \
  -H 'content-type: application/json' \
  --data '{"plan":"pro","term":"monthly"}')
echo "$RESULT2"
echo ""

echo "Test 3: Starter Yearly"
RESULT3=$(curl -s -X POST https://levqor.ai/api/checkout \
  -H 'content-type: application/json' \
  --data '{"plan":"starter","term":"yearly"}')
echo "$RESULT3"
echo ""

echo "Test 4: Pro Yearly"
RESULT4=$(curl -s -X POST https://levqor.ai/api/checkout \
  -H 'content-type: application/json' \
  --data '{"plan":"pro","term":"yearly"}')
echo "$RESULT4"
echo ""

echo "========================================"
if [[ "$RESULT1" == *"checkout.stripe.com"* ]]; then
  echo "✅ SUCCESS! Stripe checkout is working!"
else
  echo "❌ FAILED! Check logs above for errors"
fi
