#!/usr/bin/env node
const Stripe = require('stripe');
const fs = require('fs');

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

async function main() {
  console.log('== 1) Archive old Levqor products ==');
  const products = await stripe.products.list({ limit: 100, active: true });
  for (const product of products.data) {
    if (product.name && product.name.toLowerCase().includes('levqor')) {
      console.log(`Archiving product: ${product.name} (${product.id})`);
      const prices = await stripe.prices.list({ product: product.id, active: true });
      for (const price of prices.data) {
        await stripe.prices.update(price.id, { active: false });
        console.log(`  - Archived price: ${price.id}`);
      }
      await stripe.products.update(product.id, { active: false });
    }
  }

  console.log('\n== 2) Create new products ==');
  const pStarter = await stripe.products.create({
    name: 'Levqor Starter',
    active: true,
    metadata: { project: 'levqor' }
  });
  console.log(`✅ Created Starter: ${pStarter.id}`);

  const pPro = await stripe.products.create({
    name: 'Levqor Pro',
    active: true,
    metadata: { project: 'levqor' }
  });
  console.log(`✅ Created Pro: ${pPro.id}`);

  const pBusiness = await stripe.products.create({
    name: 'Levqor Business',
    active: true,
    metadata: { project: 'levqor' }
  });
  console.log(`✅ Created Business: ${pBusiness.id}`);

  const pSeat = await stripe.products.create({
    name: 'Levqor Add-on: Extra Seat',
    active: true,
    metadata: { project: 'levqor' }
  });
  console.log(`✅ Created Extra Seat: ${pSeat.id}`);

  const pSupport = await stripe.products.create({
    name: 'Levqor Add-on: Priority Support',
    active: true,
    metadata: { project: 'levqor' }
  });
  console.log(`✅ Created Priority Support: ${pSupport.id}`);

  console.log('\n== 3) Create prices (GBP, recurring) ==');
  
  console.log('Creating Starter prices...');
  const priceStarterMonth = await stripe.prices.create({
    product: pStarter.id,
    currency: 'gbp',
    unit_amount: 1900,
    recurring: { interval: 'month' },
    active: true
  });
  console.log(`  Monthly (£19): ${priceStarterMonth.id}`);

  const priceStarterYear = await stripe.prices.create({
    product: pStarter.id,
    currency: 'gbp',
    unit_amount: 19000,
    recurring: { interval: 'year' },
    active: true
  });
  console.log(`  Yearly (£190): ${priceStarterYear.id}`);

  console.log('Creating Pro prices...');
  const priceProMonth = await stripe.prices.create({
    product: pPro.id,
    currency: 'gbp',
    unit_amount: 4900,
    recurring: { interval: 'month' },
    active: true
  });
  console.log(`  Monthly (£49): ${priceProMonth.id}`);

  const priceProYear = await stripe.prices.create({
    product: pPro.id,
    currency: 'gbp',
    unit_amount: 49000,
    recurring: { interval: 'year' },
    active: true
  });
  console.log(`  Yearly (£490): ${priceProYear.id}`);

  console.log('Creating Business prices...');
  const priceBusMonth = await stripe.prices.create({
    product: pBusiness.id,
    currency: 'gbp',
    unit_amount: 14900,
    recurring: { interval: 'month' },
    active: true
  });
  console.log(`  Monthly (£149): ${priceBusMonth.id}`);

  const priceBusYear = await stripe.prices.create({
    product: pBusiness.id,
    currency: 'gbp',
    unit_amount: 149000,
    recurring: { interval: 'year' },
    active: true
  });
  console.log(`  Yearly (£1490): ${priceBusYear.id}`);

  console.log('Creating Add-on prices...');
  const priceSeatMonth = await stripe.prices.create({
    product: pSeat.id,
    currency: 'gbp',
    unit_amount: 1000,
    recurring: { interval: 'month' },
    active: true
  });
  console.log(`  Extra Seat (£10/mo): ${priceSeatMonth.id}`);

  const priceSupportMonth = await stripe.prices.create({
    product: pSupport.id,
    currency: 'gbp',
    unit_amount: 9900,
    recurring: { interval: 'month' },
    active: true
  });
  console.log(`  Priority Support (£99/mo): ${priceSupportMonth.id}`);

  console.log('\n== 4) Generate Vercel environment variables ==');
  const envVars = `
# ===== Paste these into Vercel (Production) =====
# Core checkout (3 tiers × 2 terms)
STRIPE_PRICE_STARTER=${priceStarterMonth.id}
STRIPE_PRICE_STARTER_YEAR=${priceStarterYear.id}
STRIPE_PRICE_PRO=${priceProMonth.id}
STRIPE_PRICE_PRO_YEAR=${priceProYear.id}
STRIPE_PRICE_BUSINESS=${priceBusMonth.id}
STRIPE_PRICE_BUSINESS_YEAR=${priceBusYear.id}

# Optional add-ons (not used by /api/checkout yet)
STRIPE_PRICE_ADDON_SEAT=${priceSeatMonth.id}
STRIPE_PRICE_ADDON_SUPPORT=${priceSupportMonth.id}
`.trim();

  console.log(envVars);
  fs.writeFileSync('/tmp/vercel_env_vars.txt', envVars);
  
  console.log('\n✅ All Stripe products and prices created successfully!');
  console.log('\nNext steps:');
  console.log('1. Copy the environment variables above');
  console.log('2. Add them to Vercel: https://vercel.com/vii-77s-projects/levqor-site/settings/environment-variables');
  console.log('3. Redeploy the site');
}

main().catch(console.error);
