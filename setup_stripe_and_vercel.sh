#!/bin/bash
# Interactive setup for Stripe Prices & Vercel Environment Variables

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   LEVQOR PRICING SETUP - Stripe & Vercel Configuration    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Stripe Setup
echo "═══════════════════════════════════════════════════════════════"
echo "STEP 1: CREATE STRIPE PRICES"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Open this link in your browser:"
echo "👉 https://dashboard.stripe.com/products"
echo ""
echo "You need to create 4 prices. Follow these steps for each:"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣  STARTER - MONTHLY (£19/mo)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   • Click 'Create product'"
echo "   • Name: Levqor Starter"
echo "   • Description: 1 project, email support, basic insights"
echo "   • Click 'More pricing options' → Select 'Recurring'"
echo "   • Pricing model: Flat rate"
echo "   • Amount: 19"
echo "   • Currency: GBP (£)"
echo "   • Billing period: Monthly"
echo "   • Click 'Add product'"
echo "   • COPY THE PRICE ID (starts with price_)"
echo ""
read -p "Paste the Starter Monthly Price ID here: " STRIPE_PRICE_STARTER
echo "✅ Saved: STRIPE_PRICE_STARTER=$STRIPE_PRICE_STARTER"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣  STARTER - YEARLY (£190/yr - 2 months free!)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   • Go back to the 'Levqor Starter' product you just created"
echo "   • Click 'Add another price'"
echo "   • Pricing model: Flat rate"
echo "   • Amount: 190  (saves £38/year = 2 months free)"
echo "   • Currency: GBP (£)"
echo "   • Billing period: Yearly"
echo "   • Click 'Add price'"
echo "   • COPY THE PRICE ID"
echo ""
read -p "Paste the Starter Yearly Price ID here: " STRIPE_PRICE_STARTER_YEAR
echo "✅ Saved: STRIPE_PRICE_STARTER_YEAR=$STRIPE_PRICE_STARTER_YEAR"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣  PRO - MONTHLY (£49/mo)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   • Click 'Create product'"
echo "   • Name: Levqor Pro"
echo "   • Description: Unlimited projects, priority support, advanced insights"
echo "   • Click 'More pricing options' → Select 'Recurring'"
echo "   • Pricing model: Flat rate"
echo "   • Amount: 49"
echo "   • Currency: GBP (£)"
echo "   • Billing period: Monthly"
echo "   • Click 'Add product'"
echo "   • COPY THE PRICE ID"
echo ""
read -p "Paste the Pro Monthly Price ID here: " STRIPE_PRICE_PRO
echo "✅ Saved: STRIPE_PRICE_PRO=$STRIPE_PRICE_PRO"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4️⃣  PRO - YEARLY (£490/yr - 2 months free!)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   • Go back to the 'Levqor Pro' product you just created"
echo "   • Click 'Add another price'"
echo "   • Pricing model: Flat rate"
echo "   • Amount: 490  (saves £98/year = 2 months free)"
echo "   • Currency: GBP (£)"
echo "   • Billing period: Yearly"
echo "   • Click 'Add price'"
echo "   • COPY THE PRICE ID"
echo ""
read -p "Paste the Pro Yearly Price ID here: " STRIPE_PRICE_PRO_YEAR
echo "✅ Saved: STRIPE_PRICE_PRO_YEAR=$STRIPE_PRICE_PRO_YEAR"
echo ""

# Step 2: Add to Replit Secrets
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "STEP 2: ADD SECRETS TO REPLIT"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "I'll show you the commands to add these secrets to Replit."
echo "Copy and paste each line into the Replit Secrets panel:"
echo ""
echo "Key: STRIPE_PRICE_STARTER"
echo "Value: $STRIPE_PRICE_STARTER"
echo ""
echo "Key: STRIPE_PRICE_STARTER_YEAR"
echo "Value: $STRIPE_PRICE_STARTER_YEAR"
echo ""
echo "Key: STRIPE_PRICE_PRO"
echo "Value: $STRIPE_PRICE_PRO"
echo ""
echo "Key: STRIPE_PRICE_PRO_YEAR"
echo "Value: $STRIPE_PRICE_PRO_YEAR"
echo ""
echo "Key: SITE_URL"
echo "Value: https://levqor.ai"
echo ""
read -p "Press ENTER once you've added all 5 secrets to Replit..."
echo "✅ Replit secrets configured!"

# Step 3: Add to Vercel
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "STEP 3: ADD ENVIRONMENT VARIABLES TO VERCEL"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Open this link to add environment variables to Vercel:"
echo "👉 https://vercel.com/dashboard"
echo ""
echo "1. Select your Levqor project"
echo "2. Click 'Settings' tab"
echo "3. Click 'Environment Variables' in left sidebar"
echo "4. Add these 6 variables (click 'Add' for each):"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat << VARS

Variable 1:
  Key: STRIPE_SECRET_KEY
  Value: [Your Stripe secret key from Replit secrets]
  Environments: ✓ Production ✓ Preview ✓ Development

Variable 2:
  Key: STRIPE_PRICE_STARTER
  Value: $STRIPE_PRICE_STARTER
  Environments: ✓ Production ✓ Preview ✓ Development

Variable 3:
  Key: STRIPE_PRICE_STARTER_YEAR
  Value: $STRIPE_PRICE_STARTER_YEAR
  Environments: ✓ Production ✓ Preview ✓ Development

Variable 4:
  Key: STRIPE_PRICE_PRO
  Value: $STRIPE_PRICE_PRO
  Environments: ✓ Production ✓ Preview ✓ Development

Variable 5:
  Key: STRIPE_PRICE_PRO_YEAR
  Value: $STRIPE_PRICE_PRO_YEAR
  Environments: ✓ Production ✓ Preview ✓ Development

Variable 6:
  Key: SITE_URL
  Value: https://levqor.ai
  Environments: ✓ Production ✓ Preview ✓ Development

VARS
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Press ENTER once you've added all 6 variables to Vercel..."
echo "✅ Vercel environment variables configured!"

# Summary
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    🎉 SETUP COMPLETE! 🎉                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "✅ 4 Stripe prices created"
echo "✅ 5 secrets added to Replit"
echo "✅ 6 environment variables added to Vercel"
echo ""
echo "Next steps:"
echo "1. Deploy your changes: git push origin main"
echo "2. Wait 2-3 minutes for Vercel to build"
echo "3. Test at: https://levqor.ai/pricing"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Your Price IDs (save these for reference):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STRIPE_PRICE_STARTER=$STRIPE_PRICE_STARTER"
echo "STRIPE_PRICE_STARTER_YEAR=$STRIPE_PRICE_STARTER_YEAR"
echo "STRIPE_PRICE_PRO=$STRIPE_PRICE_PRO"
echo "STRIPE_PRICE_PRO_YEAR=$STRIPE_PRICE_PRO_YEAR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
