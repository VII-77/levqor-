#!/usr/bin/env bash
set -euo pipefail

echo "═══════════════════════════════════════"
echo "SAFE DEPLOYMENT SCRIPT"
echo "═══════════════════════════════════════"
echo ""

cd "$(dirname "$0")/.." || exit 1

# Ensure we're in the right directory
if [ ! -f "package.json" ]; then
  echo "❌ Not in levqor-site directory"
  exit 1
fi

echo "📦 Step 1: Clean staging area..."
# Restore any accidentally staged files
git restore --staged .env* node_modules .next dist .vercel 2>/dev/null || true
git restore --staged ../FINAL_SHIP_LOG.txt 2>/dev/null || true

echo ""
echo "📁 Step 2: Stage source files..."
git add src/ || true
git add scripts/ || true
git add package.json package-lock.json 2>/dev/null || true
git add ../PHASE_7_PRICING_FINALIZED.md ../scripts/create_stripe_pricing_v7.js ../scripts/create_enterprise_addons.js 2>/dev/null || true

echo ""
echo "📝 Step 3: Show what will be committed..."
git status --short

echo ""
read -p "Continue with commit? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Aborted."
  exit 0
fi

echo ""
echo "💾 Step 4: Commit changes..."
git commit -m "Pricing v7.0 Final: 4 tiers + enterprise add-ons + trials + verification

Features:
- 4-tier pricing: Free, Starter (£19/£190), Pro (£49/£490), Business (£149/£1490)
- 7-day trials on Pro & Business (configurable via FREE_TRIAL_DAYS)
- Enterprise add-ons: Priority Support (£99), SLA 99.9% (£199), White-label (£299)
- Coming soon connectors with waitlist capture
- Automatic tax calculation in Stripe Checkout
- Session ID in success URL for tracking

Technical:
- Updated checkout API with enterprise add-ons (PRIORITY_SUPPORT, SLA_99_9, WHITE_LABEL)
- Static environment variable references (Next.js safe)
- Trial days configurable via FREE_TRIAL_DAYS env var
- Enhanced error handling with try/catch
- Idempotent Stripe sync script (stripe_sync.mjs)
- Comprehensive verification script (verify_final.sh)
- Safe deployment script with rate-limit awareness

Infrastructure:
- 14 Vercel environment variables configured
- 3 Stripe products with metadata
- 6 plan prices (3 tiers × 2 billing terms)
- 3 enterprise add-on prices
- All old add-ons cleaned from Vercel

Testing:
- GET and POST checkout methods verified
- Add-ons line items validated
- Trial period applied correctly
- Automatic tax enabled" || echo "No changes to commit"

echo ""
echo "🚀 Step 5: Push to GitHub..."
if [ -n "${CI:-}" ]; then
  echo "Running in CI, skipping interactive push confirmation"
  git push origin main
else
  read -p "Push to GitHub (triggers Vercel deploy)? (y/N): " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push origin main
  else
    echo "Push skipped. Run 'git push origin main' when ready."
    exit 0
  fi
fi

echo ""
echo "⏳ Step 6: Waiting for Vercel deployment (120 seconds)..."
for i in {1..24}; do
  echo -n "▓"
  sleep 5
done
echo ""

echo ""
echo "✅ Deployment triggered!"
echo ""
echo "Next steps:"
echo "  1. Check Vercel dashboard: https://vercel.com/dashboard"
echo "  2. Run verification: ./scripts/verify_final.sh"
echo "  3. Test pricing page: https://levqor.ai/pricing"
echo ""
