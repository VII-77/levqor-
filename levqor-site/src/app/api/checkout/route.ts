import { NextResponse } from "next/server";
import Stripe from "stripe";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, { apiVersion: "2024-10-28" });

export async function POST(req: Request) {
  try {
    const { plan, term } = await req.json();

    // Map only what actually exists in Vercel
    const priceMap: Record<string, string | undefined> = {
      "starter-monthly": process.env.STRIPE_PRICE_ID_STARTER,
      "pro-monthly": process.env.STRIPE_PRICE_ID_PRO,
    };

    const priceId = priceMap[`${plan}-${term}`];
    if (!priceId) {
      return NextResponse.json({ error: "Unknown plan/term" }, { status: 400 });
    }

    const session = await stripe.checkout.sessions.create({
      mode: "subscription",
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: `${process.env.SITE_URL}/success`,
      cancel_url: `${process.env.SITE_URL}/pricing`,
    });

    return NextResponse.json({ url: session.url });
  } catch (e: any) {
    return NextResponse.json({ error: e.message }, { status: 500 });
  }
}
