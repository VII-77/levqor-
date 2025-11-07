#!/usr/bin/env python3
"""
Phase-4 Secret Verification Script
Validates all enterprise security secrets are properly configured
"""

import os
import sys

def check_secret(name, required=False, validator=None):
    """Check if a secret exists and optionally validate its format"""
    value = os.environ.get(name, "").strip()
    
    if not value:
        status = "❌ MISSING" if required else "⚠️  NOT SET"
        return False, status, None
    
    if validator:
        valid, msg = validator(value)
        if not valid:
            return False, f"❌ INVALID: {msg}", len(value)
    
    return True, "✅ OK", len(value)

def validate_redis_url(url):
    """Validate Redis URL format"""
    if not url.startswith(('redis://', 'rediss://', 'unix://')):
        return False, "Must start with redis://, rediss://, or unix://"
    return True, None

def validate_sentry_dsn(dsn):
    """Validate Sentry DSN format"""
    if not dsn.startswith('https://'):
        return False, "Must start with https://"
    if '@' not in dsn or 'sentry.io' not in dsn:
        return False, "Invalid Sentry DSN format (should be https://...@....sentry.io/...)"
    return True, None

def validate_webhook_secret(secret):
    """Validate webhook secret format"""
    if len(secret) < 16:
        return False, "Too short (minimum 16 characters)"
    return True, None

def validate_stripe_webhook(secret):
    """Validate Stripe webhook secret"""
    if not secret.startswith('whsec_'):
        return False, "Must start with 'whsec_'"
    return True, None

print("=" * 70)
print("PHASE-4 SECRET VERIFICATION")
print("=" * 70)

secrets = {
    "HIGH PRIORITY": [
        ("STRIPE_WEBHOOK_SECRET", True, validate_stripe_webhook, 
         "Stripe webhook signature verification"),
        ("REDIS_URL", True, validate_redis_url, 
         "Async job queue and rate limiting"),
    ],
    "MEDIUM PRIORITY": [
        ("SLACK_SIGNING_SECRET", False, validate_webhook_secret, 
         "Slack webhook signature verification"),
    ],
    "LOW PRIORITY": [
        ("SENTRY_DSN", False, validate_sentry_dsn, 
         "Production error tracking (optional)"),
    ]
}

all_valid = True

for priority, items in secrets.items():
    print(f"\n{priority}")
    print("-" * 70)
    
    for name, required, validator, description in items:
        valid, status, length = check_secret(name, required, validator)
        
        if not valid:
            all_valid = False
        
        length_str = f" (length: {length})" if length else ""
        print(f"{name:30} {status}{length_str}")
        print(f"{'':30} → {description}")

print("\n" + "=" * 70)

if all_valid:
    print("✅ ALL SECRETS PROPERLY CONFIGURED")
    print("=" * 70)
    sys.exit(0)
else:
    print("❌ SOME SECRETS NEED ATTENTION")
    print("=" * 70)
    print("\nFIX INSTRUCTIONS:")
    print("-" * 70)
    
    # Check specific issues
    redis_url = os.environ.get("REDIS_URL", "").strip()
    if redis_url and not redis_url.startswith(('redis://', 'rediss://', 'unix://')):
        print("\n🔧 REDIS_URL Format Issue:")
        print("   Current format is invalid.")
        print("   Required format: redis://default:PASSWORD@HOST:PORT")
        print("   Example: redis://default:abc123@redis-12345.upstash.io:6379")
        print("   Or for TLS: rediss://default:PASSWORD@HOST:PORT")
    
    sentry_dsn = os.environ.get("SENTRY_DSN", "").strip()
    if sentry_dsn and len(sentry_dsn) < 50:
        print("\n🔧 SENTRY_DSN Format Issue:")
        print("   Current DSN appears too short (valid DSNs are 80+ characters).")
        print("   Required format: https://PUBLIC_KEY@o123456.ingest.sentry.io/PROJECT_ID")
        print("   Get it from: Sentry Dashboard → Settings → Client Keys (DSN)")
        print("   Note: Sentry is optional - you can leave it empty if not needed")
    
    stripe_webhook = os.environ.get("STRIPE_WEBHOOK_SECRET", "").strip()
    if stripe_webhook and not stripe_webhook.startswith('whsec_'):
        print("\n🔧 STRIPE_WEBHOOK_SECRET Format Issue:")
        print("   Must start with 'whsec_'")
        print("   Get it from: Stripe Dashboard → Developers → Webhooks")
        print("   Click your webhook endpoint → Copy 'Signing secret'")
    
    print("\n" + "=" * 70)
    sys.exit(1)
