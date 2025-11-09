import { NextResponse } from 'next/server';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, { apiVersion: '2024-11-20.acacia' });

export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const plan = searchParams.get('plan');
    
    const priceId = plan === 'pro'
      ? process.env.STRIPE_PRICE_PRO
      : process.env.STRIPE_PRICE_STARTER;

    if (!priceId) {
      return NextResponse.json({ error: 'Unknown plan' }, { status: 400 });
    }

    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: `${process.env.SITE_URL || 'https://levqor.ai'}/thanks?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.SITE_URL || 'https://levqor.ai'}/pricing`,
      allow_promotion_codes: true,
      billing_address_collection: 'auto',
      automatic_tax: { enabled: true },
    });

    return NextResponse.redirect(session.url!, 303);
  } catch (e: any) {
    console.error('Stripe checkout error:', e);
    return NextResponse.json({ error: e.message ?? 'checkout_error' }, { status: 500 });
  }
}
