#!/usr/bin/env node
const Stripe = require('stripe');
const fs = require('fs');

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

async function main() {
  console.log('═══════════════════════════════════════');
  console.log('PHASE 1: STRIPE PRICING V7.0');
  console.log('═══════════════════════════════════════\n');

  console.log('🧹 Step 1: Archive old Levqor products...');
  const products = await stripe.products.list({ limit: 100, active: true });
  for (const product of products.data) {
    if (product.name && product.name.toLowerCase().includes('levqor')) {
      console.log(`  Archiving: ${product.name} (${product.id})`);
      const prices = await stripe.prices.list({ product: product.id, active: true });
      for (const price of prices.data) {
        await stripe.prices.update(price.id, { active: false });
      }
      await stripe.products.update(product.id, { active: false });
    }
  }
  console.log('✅ Old products archived\n');

  console.log('📦 Step 2: Create new products with trials...');
  
  // Starter (no trial)
  const pStarter = await stripe.products.create({
    name: 'Levqor Starter',
    active: true,
    metadata: { project: 'levqor', tier: 'starter' }
  });
  console.log(`  ✅ Starter: ${pStarter.id}`);

  // Pro (with trial)
  const pPro = await stripe.products.create({
    name: 'Levqor Pro',
    active: true,
    metadata: { project: 'levqor', tier: 'pro', trial_days: '7' }
  });
  console.log(`  ✅ Pro: ${pPro.id}`);

  // Business (with trial)
  const pBusiness = await stripe.products.create({
    name: 'Levqor Business',
    active: true,
    metadata: { project: 'levqor', tier: 'business', trial_days: '7' }
  });
  console.log(`  ✅ Business: ${pBusiness.id}`);

  // Add-ons
  const pRunsPack = await stripe.products.create({
    name: 'Extra Runs Pack (+25k)',
    active: true,
    metadata: { project: 'levqor', type: 'addon' }
  });
  console.log(`  ✅ Add-on: Extra Runs: ${pRunsPack.id}`);

  const pAIPack = await stripe.products.create({
    name: 'AI Credits Pack (+10k)',
    active: true,
    metadata: { project: 'levqor', type: 'addon' }
  });
  console.log(`  ✅ Add-on: AI Credits: ${pAIPack.id}`);

  const pSLAPro = await stripe.products.create({
    name: 'Priority SLA for Pro',
    active: true,
    metadata: { project: 'levqor', type: 'addon' }
  });
  console.log(`  ✅ Add-on: SLA: ${pSLAPro.id}\n`);

  console.log('💰 Step 3: Create prices...');
  
  // Starter prices
  const priceStarterMonth = await stripe.prices.create({
    product: pStarter.id,
    currency: 'gbp',
    unit_amount: 1900,
    recurring: { interval: 'month' }
  });
  console.log(`  Starter Monthly: ${priceStarterMonth.id}`);

  const priceStarterYear = await stripe.prices.create({
    product: pStarter.id,
    currency: 'gbp',
    unit_amount: 19000,
    recurring: { interval: 'year' }
  });
  console.log(`  Starter Yearly: ${priceStarterYear.id}`);

  // Pro prices (with trial metadata)
  const priceProMonth = await stripe.prices.create({
    product: pPro.id,
    currency: 'gbp',
    unit_amount: 4900,
    recurring: { interval: 'month', trial_period_days: 7 }
  });
  console.log(`  Pro Monthly (7d trial): ${priceProMonth.id}`);

  const priceProYear = await stripe.prices.create({
    product: pPro.id,
    currency: 'gbp',
    unit_amount: 49000,
    recurring: { interval: 'year', trial_period_days: 7 }
  });
  console.log(`  Pro Yearly (7d trial): ${priceProYear.id}`);

  // Business prices (with trial)
  const priceBusMonth = await stripe.prices.create({
    product: pBusiness.id,
    currency: 'gbp',
    unit_amount: 14900,
    recurring: { interval: 'month', trial_period_days: 7 }
  });
  console.log(`  Business Monthly (7d trial): ${priceBusMonth.id}`);

  const priceBusYear = await stripe.prices.create({
    product: pBusiness.id,
    currency: 'gbp',
    unit_amount: 149000,
    recurring: { interval: 'year', trial_period_days: 7 }
  });
  console.log(`  Business Yearly (7d trial): ${priceBusYear.id}`);

  // Add-on prices
  const priceRunsPack = await stripe.prices.create({
    product: pRunsPack.id,
    currency: 'gbp',
    unit_amount: 2900,
    recurring: { interval: 'month' }
  });
  console.log(`  Extra Runs Pack: ${priceRunsPack.id}`);

  const priceAIPack = await stripe.prices.create({
    product: pAIPack.id,
    currency: 'gbp',
    unit_amount: 900,
    recurring: { interval: 'month' }
  });
  console.log(`  AI Credits Pack: ${priceAIPack.id}`);

  const priceSLAPro = await stripe.prices.create({
    product: pSLAPro.id,
    currency: 'gbp',
    unit_amount: 3900,
    recurring: { interval: 'month' }
  });
  console.log(`  Priority SLA: ${priceSLAPro.id}\n`);

  console.log('📝 Step 4: Generate Vercel environment variables...');
  const envVars = `
# Core Plans (6 variables)
STRIPE_PRICE_STARTER=${priceStarterMonth.id}
STRIPE_PRICE_STARTER_YEAR=${priceStarterYear.id}
STRIPE_PRICE_PRO=${priceProMonth.id}
STRIPE_PRICE_PRO_YEAR=${priceProYear.id}
STRIPE_PRICE_BUSINESS=${priceBusMonth.id}
STRIPE_PRICE_BUSINESS_YEAR=${priceBusYear.id}

# Add-ons (3 variables)
STRIPE_ADDON_RUNS_25K=${priceRunsPack.id}
STRIPE_ADDON_AI_10K=${priceAIPack.id}
STRIPE_ADDON_SLA_PRO=${priceSLAPro.id}
  `.trim();

  console.log(envVars);
  fs.writeFileSync('/tmp/vercel_env_v7.txt', envVars);
  
  // Save individual price IDs for automated Vercel update
  const priceIds = {
    STRIPE_PRICE_STARTER: priceStarterMonth.id,
    STRIPE_PRICE_STARTER_YEAR: priceStarterYear.id,
    STRIPE_PRICE_PRO: priceProMonth.id,
    STRIPE_PRICE_PRO_YEAR: priceProYear.id,
    STRIPE_PRICE_BUSINESS: priceBusMonth.id,
    STRIPE_PRICE_BUSINESS_YEAR: priceBusYear.id,
    STRIPE_ADDON_RUNS_25K: priceRunsPack.id,
    STRIPE_ADDON_AI_10K: priceAIPack.id,
    STRIPE_ADDON_SLA_PRO: priceSLAPro.id,
  };
  fs.writeFileSync('/tmp/price_ids.json', JSON.stringify(priceIds, null, 2));
  
  console.log('\n✅ All Stripe products and prices created!');
  console.log('\n📊 Summary:');
  console.log('  • 3 tiers: Starter, Pro, Business');
  console.log('  • 6 plan prices (3 × 2 billing terms)');
  console.log('  • 3 add-on prices');
  console.log('  • Pro & Business include 7-day trials');
  console.log('\nNext: Update Vercel environment variables');
}

main().catch(console.error);
