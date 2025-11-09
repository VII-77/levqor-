#!/usr/bin/env python3
"""
Create Stripe products and prices for Levqor pricing plans.
This script creates:
- Levqor Starter: £19/mo and £190/yr
- Levqor Pro: £49/mo and £490/yr
"""

import os
import stripe

# Initialize Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

if not stripe.api_key:
    print("❌ STRIPE_SECRET_KEY not found in environment variables")
    exit(1)

print("🔧 Creating Stripe products and prices...")
print("=" * 60)

# Store price IDs
price_ids = {}

# Create Levqor Starter Product
print("\n1️⃣  Creating Levqor Starter product...")
try:
    # Check if product already exists
    existing_products = stripe.Product.list(limit=100)
    starter_product = next((p for p in existing_products.data if p.name == "Levqor Starter"), None)
    
    if starter_product:
        print(f"   ✓ Product already exists: {starter_product.id}")
        product_starter = starter_product
    else:
        product_starter = stripe.Product.create(
            name="Levqor Starter",
            description="1 project, email support, basic insights"
        )
        print(f"   ✓ Created product: {product_starter.id}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Create Starter Monthly Price (£19/mo)
print("\n2️⃣  Creating Starter Monthly price (£19/mo)...")
try:
    price_starter_monthly = stripe.Price.create(
        product=product_starter.id,
        unit_amount=1900,  # £19.00 in pence
        currency="gbp",
        recurring={"interval": "month"},
        nickname="Starter Monthly"
    )
    price_ids['STRIPE_PRICE_STARTER'] = price_starter_monthly.id
    print(f"   ✓ Created price: {price_starter_monthly.id}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Create Starter Yearly Price (£190/yr)
print("\n3️⃣  Creating Starter Yearly price (£190/yr)...")
try:
    price_starter_yearly = stripe.Price.create(
        product=product_starter.id,
        unit_amount=19000,  # £190.00 in pence (2 months free!)
        currency="gbp",
        recurring={"interval": "year"},
        nickname="Starter Yearly"
    )
    price_ids['STRIPE_PRICE_STARTER_YEAR'] = price_starter_yearly.id
    print(f"   ✓ Created price: {price_starter_yearly.id}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Create Levqor Pro Product
print("\n4️⃣  Creating Levqor Pro product...")
try:
    pro_product = next((p for p in existing_products.data if p.name == "Levqor Pro"), None)
    
    if pro_product:
        print(f"   ✓ Product already exists: {pro_product.id}")
        product_pro = pro_product
    else:
        product_pro = stripe.Product.create(
            name="Levqor Pro",
            description="Unlimited projects, priority support, advanced insights + runbooks"
        )
        print(f"   ✓ Created product: {product_pro.id}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Create Pro Monthly Price (£49/mo)
print("\n5️⃣  Creating Pro Monthly price (£49/mo)...")
try:
    price_pro_monthly = stripe.Price.create(
        product=product_pro.id,
        unit_amount=4900,  # £49.00 in pence
        currency="gbp",
        recurring={"interval": "month"},
        nickname="Pro Monthly"
    )
    price_ids['STRIPE_PRICE_PRO'] = price_pro_monthly.id
    print(f"   ✓ Created price: {price_pro_monthly.id}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Create Pro Yearly Price (£490/yr)
print("\n6️⃣  Creating Pro Yearly price (£490/yr)...")
try:
    price_pro_yearly = stripe.Price.create(
        product=product_pro.id,
        unit_amount=49000,  # £490.00 in pence (2 months free!)
        currency="gbp",
        recurring={"interval": "year"},
        nickname="Pro Yearly"
    )
    price_ids['STRIPE_PRICE_PRO_YEAR'] = price_pro_yearly.id
    print(f"   ✓ Created price: {price_pro_yearly.id}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Print summary
print("\n" + "=" * 60)
print("✅ SUCCESS! All prices created.")
print("=" * 60)
print("\n📋 ADD THESE TO REPLIT SECRETS:\n")
for key, value in price_ids.items():
    print(f"{key}={value}")

print("\nSITE_URL=https://levqor.ai")

print("\n" + "=" * 60)
print("📋 ADD THESE TO VERCEL ENVIRONMENT VARIABLES TOO:")
print("=" * 60)
print("Same 5 values above + STRIPE_SECRET_KEY")
print("\n✅ Done! Now add these secrets and deploy.")
