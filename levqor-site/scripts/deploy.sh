#!/bin/bash

echo "═══════════════════════════════════════"
echo "DEPLOYMENT SCRIPT - Pricing V7.0"
echo "═══════════════════════════════════════"
echo ""

cd "$(dirname "$0")/.." || exit 1

echo "📦 Step 1: Stage changes..."
git add src/app/pricing/page.tsx
git add src/app/api/checkout/route.ts
git add src/app/api/notify-coming-soon/
git add scripts/

echo ""
echo "📝 Step 2: Commit changes..."
git commit -m "v7.0: Competitive pricing with 4 tiers, trials, add-ons, coming-soon notify

- 4-tier pricing: Free, Starter, Pro, Business
- 7-day trials on Pro & Business
- 3 add-ons: Extra Runs, AI Credits, Priority SLA
- Coming soon connectors with notify waitlist
- Updated checkout API with trial support
- Feature comparison table
- Trust elements (GDPR, encryption, SLA)
- Comprehensive FAQ section
- All prices static-env safe for Next.js"

echo ""
echo "🚀 Step 3: Push to GitHub..."
git push origin main

echo ""
echo "⏳ Step 4: Waiting for Vercel deployment (2 minutes)..."
sleep 120

echo ""
echo "✅ Deployment complete!"
echo ""
echo "═══════════════════════════════════════"
echo "NEXT STEPS"
echo "═══════════════════════════════════════"
echo ""
echo "1. Verify deployment:"
echo "   https://vercel.com/dashboard"
echo ""
echo "2. Test endpoints:"
echo "   ./scripts/test_checkout.sh"
echo ""
echo "3. View pricing page:"
echo "   https://levqor.ai/pricing"
echo ""
echo "═══════════════════════════════════════"
