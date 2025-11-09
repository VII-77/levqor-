import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';

export const runtime = 'edge';
export const dynamic = 'force-dynamic';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-10-29.clover',
});

export async function POST(req: NextRequest) {
  try {
    const rawBody = await req.text();
    const sig = req.headers.get('stripe-signature') || '';
    const secret = process.env.STRIPE_WEBHOOK_SECRET!;
    
    let event: Stripe.Event;

    try {
      event = stripe.webhooks.constructEvent(rawBody, sig, secret);
    } catch (err: any) {
      console.error('Webhook signature verification failed:', err.message);
      return new NextResponse(JSON.stringify({ error: 'Invalid signature', detail: err?.message }), { status: 400 });
    }

    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object as Stripe.Checkout.Session;
        console.log('Checkout completed:', {
          customer: session.customer,
          subscription: session.subscription,
          amount: session.amount_total,
        });
        break;
      }
      case 'customer.subscription.created':
      case 'customer.subscription.updated': {
        const subscription = event.data.object as Stripe.Subscription;
        console.log('Subscription event:', event.type, {
          id: subscription.id,
          status: subscription.status,
          customer: subscription.customer,
        });
        break;
      }
      case 'customer.subscription.deleted': {
        const subscription = event.data.object as Stripe.Subscription;
        console.log('Subscription cancelled:', {
          id: subscription.id,
          customer: subscription.customer,
        });
        break;
      }
      default:
        console.log('Unhandled event type:', event.type);
    }
    
    return NextResponse.json({ received: true });
  } catch (e: any) {
    console.error('Webhook handler error:', e);
    return new NextResponse(JSON.stringify({ error: 'handler_failed', detail: e?.message }), { status: 500 });
  }
}

export async function GET() {
  return NextResponse.json({ ok: true, route: '/api/stripe/webhook' });
}
