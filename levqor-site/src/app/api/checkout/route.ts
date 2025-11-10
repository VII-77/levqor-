import { NextResponse } from 'next/server';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY as string, { apiVersion: '2025-10-29.clover' });

type Plan = 'starter' | 'pro' | 'business';
type Term = 'monthly' | 'yearly';

const MAP: Record<Plan, Record<Term, string | undefined>> = {
  starter: {
    monthly: process.env.STRIPE_PRICE_STARTER,
    yearly: process.env.STRIPE_PRICE_STARTER_YEAR,
  },
  pro: {
    monthly: process.env.STRIPE_PRICE_PRO,
    yearly: process.env.STRIPE_PRICE_PRO_YEAR,
  },
  business: {
    monthly: process.env.STRIPE_PRICE_BUSINESS,
    yearly: process.env.STRIPE_PRICE_BUSINESS_YEAR,
  },
};

const ADDONS: Record<string, string | undefined> = {
  runs_25k: process.env.STRIPE_ADDON_RUNS_25K,
  ai_10k: process.env.STRIPE_ADDON_AI_10K,
  sla_pro: process.env.STRIPE_ADDON_SLA_PRO,
};

async function createCheckout(priceId: string, plan: Plan, addons?: string[]) {
  const lineItems: Stripe.Checkout.SessionCreateParams.LineItem[] = [
    { price: priceId, quantity: 1 }
  ];

  if (addons && addons.length > 0) {
    for (const addon of addons) {
      const addonPriceId = ADDONS[addon];
      if (addonPriceId) {
        lineItems.push({ price: addonPriceId, quantity: 1 });
      }
    }
  }

  const sessionParams: Stripe.Checkout.SessionCreateParams = {
    mode: 'subscription',
    line_items: lineItems,
    success_url: `${process.env.SITE_URL}/dashboard?checkout=success`,
    cancel_url: `${process.env.SITE_URL}/pricing?checkout=cancelled`,
  };

  if (plan === 'pro' || plan === 'business') {
    sessionParams.subscription_data = {
      trial_period_days: 7,
    };
  }

  const session = await stripe.checkout.sessions.create(sessionParams);
  return session.url;
}

function pickPrice(planRaw: string | null, termRaw: string | null) {
  const plan = (planRaw || 'starter').toLowerCase() as Plan;
  const term = (termRaw || 'monthly').toLowerCase() as Term;
  if (!['starter', 'pro', 'business'].includes(plan)) return { error: 'invalid_plan' };
  if (!['monthly', 'yearly'].includes(term)) return { error: 'invalid_term' };
  const priceId = MAP[plan][term];
  if (!priceId) return { error: 'price_not_configured' };
  return { plan, term, priceId };
}

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const plan = searchParams.get('plan');
  const term = searchParams.get('term');
  const pick = pickPrice(plan, term);
  if ('error' in pick) return NextResponse.json({ ok: false, error: pick.error }, { status: 400 });
  const url = await createCheckout(pick.priceId, pick.plan);
  return NextResponse.json({ ok: true, url, plan: pick.plan, term: pick.term });
}

export async function POST(req: Request) {
  const body = await req.json().catch(() => ({}));
  const pick = pickPrice(body?.plan ?? null, body?.term ?? null);
  if ('error' in pick) return NextResponse.json({ ok: false, error: pick.error }, { status: 400 });
  
  const addons = Array.isArray(body?.addons) ? body.addons : undefined;
  const url = await createCheckout(pick.priceId, pick.plan, addons);
  
  return NextResponse.json({ ok: true, url, plan: pick.plan, term: pick.term });
}
