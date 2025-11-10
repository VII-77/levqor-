#!/usr/bin/env node
import Stripe from 'stripe';
import { writeFileSync } from 'fs';

const DRY_RUN = process.env.DRY_RUN === "false" ? false : true;
const stripeKey = process.env.STRIPE_SECRET_KEY || process.env.VERCEL_STRIPE_SECRET_KEY || "";

if (!stripeKey) {
  console.error("❌ Missing STRIPE_SECRET_KEY");
  process.exit(1);
}

const stripe = new Stripe(stripeKey, { apiVersion: "2025-10-29.clover" });
const currency = "gbp";

const plans = [
  { key: "STARTER", name: "Levqor Starter", monthly: 1900, yearly: 19000 },
  { key: "PRO", name: "Levqor Pro", monthly: 4900, yearly: 49000 },
  { key: "BUSINESS", name: "Levqor Business", monthly: 14900, yearly: 149000 },
];

const addons = [
  { key: "ADDON_PRIORITY_SUPPORT", name: "Priority Support", amount: 9900 },
  { key: "ADDON_SLA_99_9", name: "SLA 99.9%", amount: 19900 },
  { key: "ADDON_WHITE_LABEL", name: "White-label", amount: 29900 },
];

function envName(base) {
  return `STRIPE_PRICE_${base}`;
}

function envYear(base) {
  return `STRIPE_PRICE_${base}_YEAR`;
}

async function ensureProduct(name) {
  const list = await stripe.products.list({ limit: 100, active: true });
  let found = list.data.find(p => p.name === name);
  
  if (!found && !DRY_RUN) {
    console.log(`  Creating product: ${name}`);
    found = await stripe.products.create({ name, active: true });
  } else if (!found) {
    console.log(`  [DRY RUN] Would create product: ${name}`);
  } else {
    console.log(`  ✓ Found product: ${name} (${found.id})`);
  }
  
  return found;
}

async function ensurePrice(productId, unit_amount, interval) {
  const prices = await stripe.prices.list({ product: productId, active: true, limit: 100 });
  let p = prices.data.find(x => 
    x.unit_amount === unit_amount && 
    x.currency === currency && 
    x.recurring?.interval === interval
  );
  
  if (!p && !DRY_RUN) {
    console.log(`    Creating price: £${unit_amount / 100}/${interval}`);
    p = await stripe.prices.create({
      currency,
      unit_amount,
      product: productId,
      recurring: { interval }
    });
  } else if (!p) {
    console.log(`    [DRY RUN] Would create price: £${unit_amount / 100}/${interval}`);
  } else {
    console.log(`    ✓ Found price: £${unit_amount / 100}/${interval} (${p.id})`);
  }
  
  return p;
}

(async () => {
  console.log('═══════════════════════════════════════');
  console.log(`STRIPE SYNC ${DRY_RUN ? '(DRY RUN)' : '(LIVE)'}`);
  console.log('═══════════════════════════════════════\n');

  const results = {};

  // Plans
  console.log('📦 Syncing Plans...');
  for (const plan of plans) {
    console.log(`\n${plan.name}:`);
    const prod = await ensureProduct(plan.name);
    results[plan.key] = { product: prod?.id || null };

    if (prod) {
      const pm = await ensurePrice(prod.id, plan.monthly, "month");
      const py = await ensurePrice(prod.id, plan.yearly, "year");
      results[plan.key].monthly = pm?.id || null;
      results[plan.key].yearly = py?.id || null;
    }
  }

  // Add-ons
  console.log('\n📦 Syncing Add-ons...');
  for (const ad of addons) {
    console.log(`\n${ad.name}:`);
    const prod = await ensureProduct(ad.name);
    const price = prod ? await ensurePrice(prod.id, ad.amount, "month") : null;
    results[ad.key] = { product: prod?.id || null, monthly: price?.id || null };
  }

  console.log('\n═══════════════════════════════════════');
  console.log('RESULTS');
  console.log('═══════════════════════════════════════\n');
  console.log(JSON.stringify({ DRY_RUN, results }, null, 2));

  if (!DRY_RUN) {
    // Generate environment variable script
    let envScript = '# Vercel Environment Variables\n';
    
    for (const plan of plans) {
      if (results[plan.key].monthly) {
        envScript += `\nvercel env add STRIPE_PRICE_${plan.key} production --token "$VERCEL_TOKEN" <<< "${results[plan.key].monthly}"`;
      }
      if (results[plan.key].yearly) {
        envScript += `\nvercel env add STRIPE_PRICE_${plan.key}_YEAR production --token "$VERCEL_TOKEN" <<< "${results[plan.key].yearly}"`;
      }
    }
    
    for (const ad of addons) {
      if (results[ad.key].monthly) {
        envScript += `\nvercel env add STRIPE_PRICE_${ad.key} production --token "$VERCEL_TOKEN" <<< "${results[ad.key].monthly}"`;
      }
    }
    
    writeFileSync('/tmp/stripe_env_setup.sh', envScript);
    console.log('\n✅ Environment setup script saved to /tmp/stripe_env_setup.sh');
  } else {
    console.log('\n💡 To create these products/prices, run:');
    console.log('   DRY_RUN=false node scripts/stripe_sync.mjs');
  }
})().catch(err => {
  console.error('❌ Error:', err.message);
  process.exit(1);
});
