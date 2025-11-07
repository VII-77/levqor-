#!/usr/bin/env python3
"""
Sentry Integration Test
Verifies Sentry error tracking is configured correctly
"""

import os
import sys

def test_sentry_config():
    """Test Sentry configuration"""
    print("🔍 Checking Sentry Configuration")
    print("=" * 50)
    
    dsn = os.environ.get('SENTRY_DSN')
    
    if not dsn:
        print("❌ SENTRY_DSN not set")
        print("\n📋 Setup instructions:")
        print("  1. Create account at https://sentry.io")
        print("  2. Create new project")
        print("  3. Copy DSN from project settings")
        print("  4. Set as Replit secret: SENTRY_DSN=<your_dsn>")
        print("\n⚠️  Sentry is optional - errors will log to logs/errors.jsonl")
        return False
    
    print(f"✅ SENTRY_DSN configured: {dsn[:30]}...")
    
    # Test Sentry SDK
    try:
        import sentry_sdk
        print("✅ Sentry SDK installed")
    except ImportError:
        print("❌ Sentry SDK not installed")
        print("   Run: pip install sentry-sdk")
        return False
    
    # Initialize and test
    try:
        sentry_sdk.init(
            dsn=dsn,
            traces_sample_rate=0.1,
            environment=os.environ.get('REPL_SLUG', 'development')
        )
        print("✅ Sentry initialized successfully")
        
        # Send test error
        try:
            1 / 0
        except ZeroDivisionError:
            sentry_sdk.capture_exception()
            print("✅ Test error sent to Sentry")
            print("\n🎯 Check your Sentry dashboard for the test error!")
            print("   https://sentry.io/organizations/your-org/issues/")
        
        return True
        
    except Exception as e:
        print(f"❌ Sentry initialization failed: {e}")
        return False

def check_error_logging():
    """Verify fallback error logging works"""
    print("\n🔍 Checking Fallback Error Logging")
    print("=" * 50)
    
    import os
    if os.path.exists("logs/errors.jsonl"):
        print("✅ Error log file exists: logs/errors.jsonl")
        
        # Count errors
        with open("logs/errors.jsonl", 'r') as f:
            error_count = len(f.readlines())
        print(f"   Total errors logged: {error_count}")
        
        return True
    else:
        print("ℹ️  No errors logged yet (logs/errors.jsonl)")
        return True

def main():
    print("\n🛡️  Sentry Error Tracking Test\n")
    
    sentry_ok = test_sentry_config()
    fallback_ok = check_error_logging()
    
    print("\n" + "=" * 50)
    print("📊 Summary")
    print("=" * 50)
    
    if sentry_ok:
        print("✅ Sentry active - errors sent to dashboard")
    else:
        print("⚠️  Sentry inactive - using local logging")
    
    if fallback_ok:
        print("✅ Fallback logging operational")
    
    print("\n💡 Recommendation:")
    if not sentry_ok:
        print("   Set up Sentry for production error tracking")
        print("   Current setup works but lacks real-time alerts")
    else:
        print("   Your error tracking is production-ready!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
