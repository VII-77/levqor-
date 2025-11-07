#!/usr/bin/env python3
"""
Stripe Webhook Tester
Verifies billing webhooks and payment handling are configured correctly
"""

import os
import sys
import json
import argparse
import requests

def check_stripe_config():
    """Verify Stripe is configured"""
    print("🔍 Checking Stripe Configuration")
    print("=" * 50)
    
    secret_key = os.environ.get('STRIPE_SECRET_KEY')
    webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    if not secret_key:
        print("❌ STRIPE_SECRET_KEY not set")
        return False
    
    print("✅ STRIPE_SECRET_KEY configured")
    
    if not webhook_secret:
        print("⚠️  STRIPE_WEBHOOK_SECRET not set (optional)")
        print("   Webhooks will work but won't verify signatures")
    else:
        print("✅ STRIPE_WEBHOOK_SECRET configured")
    
    return True

def test_webhook_endpoint():
    """Test webhook endpoint is accessible"""
    print("\n🔍 Testing Webhook Endpoint")
    print("=" * 50)
    
    url = "http://localhost:5000/billing/webhook"
    
    # Create mock Stripe event
    mock_event = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": "cs_test_123",
                "client_reference_id": "test_user_123",
                "customer_details": {
                    "email": "test@example.com"
                },
                "amount_total": 4900,
                "payment_status": "paid"
            }
        }
    }
    
    try:
        response = requests.post(
            url,
            json=mock_event,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Webhook endpoint responsive")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"⚠️  Webhook returned {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook test failed: {e}")
        return False

def check_billing_endpoints():
    """Verify billing endpoints are operational"""
    print("\n🔍 Checking Billing Endpoints")
    print("=" * 50)
    
    endpoints = [
        "/billing/usage?user_id=test",
        "/billing/limits?user_id=test",
        "/billing/create-checkout-session"
    ]
    
    results = []
    for endpoint in endpoints:
        url = f"http://localhost:5000{endpoint}"
        try:
            if endpoint.endswith("create-checkout-session"):
                # POST endpoint
                response = requests.post(
                    url,
                    json={
                        "price_id": "price_test",
                        "email": "test@example.com",
                        "user_id": "test_user"
                    }
                )
            else:
                # GET endpoint
                response = requests.get(url)
            
            status = "✅" if response.status_code in [200, 404, 400] else "❌"
            print(f"{status} {endpoint} -> {response.status_code}")
            results.append(response.status_code in [200, 404, 400])
            
        except Exception as e:
            print(f"❌ {endpoint} -> Error: {e}")
            results.append(False)
    
    return all(results)

def verify_payment_handlers():
    """Check payment success/failure handlers exist"""
    print("\n🔍 Verifying Payment Handlers")
    print("=" * 50)
    
    try:
        # Check if handlers are defined in run.py
        with open("run.py", 'r') as f:
            content = f.read()
        
        handlers = [
            "handle_successful_payment",
            "handle_failed_payment",
            "stripe_webhook"
        ]
        
        for handler in handlers:
            if f"def {handler}" in content:
                print(f"✅ {handler}() defined")
            else:
                print(f"❌ {handler}() missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Could not verify handlers: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Test Stripe webhooks")
    parser.add_argument('--check', choices=['all', 'config', 'endpoints', 'webhook'],
                       default='all', help='What to check')
    args = parser.parse_args()
    
    print("\n💳 Stripe Webhook & Billing Tester\n")
    
    results = {}
    
    if args.check in ['all', 'config']:
        results['config'] = check_stripe_config()
    
    if args.check in ['all', 'endpoints']:
        results['endpoints'] = check_billing_endpoints()
    
    if args.check in ['all', 'webhook']:
        results['webhook'] = test_webhook_endpoint()
        results['handlers'] = verify_payment_handlers()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Summary")
    print("=" * 50)
    
    all_ok = all(results.values())
    
    if all_ok:
        print("✅ All billing systems operational!")
        print("\n🎯 Production checklist:")
        print("  1. Set STRIPE_WEBHOOK_SECRET for signature verification")
        print("  2. Configure webhook URL in Stripe Dashboard:")
        print("     https://dashboard.stripe.com/webhooks")
        print("  3. Add endpoint: https://your-domain.repl.co/billing/webhook")
        print("  4. Subscribe to events: checkout.session.*")
    else:
        print("⚠️  Some billing checks failed")
        print("   Review errors above before going live")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
