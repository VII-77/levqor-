import { NextResponse } from "next/server";

export function GET() {
  return NextResponse.json({
    sees: {
      STRIPE_PRICE_STARTER: !!process.env.STRIPE_PRICE_STARTER,
      STRIPE_PRICE_STARTER_YEAR: !!process.env.STRIPE_PRICE_STARTER_YEAR,
      STRIPE_PRICE_PRO: !!process.env.STRIPE_PRICE_PRO,
      STRIPE_PRICE_PRO_YEAR: !!process.env.STRIPE_PRICE_PRO_YEAR,
      STRIPE_PRICE_BUSINESS: !!process.env.STRIPE_PRICE_BUSINESS,
      STRIPE_PRICE_BUSINESS_YEAR: !!process.env.STRIPE_PRICE_BUSINESS_YEAR,
      STRIPE_PRICE_ID_STARTER: !!process.env.STRIPE_PRICE_ID_STARTER,
      STRIPE_PRICE_ID_PRO: !!process.env.STRIPE_PRICE_ID_PRO,
      STRIPE_PRICE_ID_BUSINESS: !!process.env.STRIPE_PRICE_ID_BUSINESS,
      SITE_URL: !!process.env.SITE_URL,
      STRIPE_SECRET_KEY: !!process.env.STRIPE_SECRET_KEY,
    }
  });
}
