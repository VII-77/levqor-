#!/usr/bin/env python3
"""Test Levqor email system"""

import notifier

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🧪 TESTING LEVQOR EMAIL SYSTEM")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print()

print("Sending test email via notifier.alert()...")
code, resp = notifier.alert(
    "Levqor Email Test",
    "This is an automated test from Levqor backend.\n\nIf you receive this, your email system is working!"
)

print(f"Response Code: {code}")
print(f"Response: {resp}")
print()

if code == 200:
    print("✅ SUCCESS - Email sent!")
    print("Check your inbox (including spam folder)")
else:
    print("❌ FAILED - Check logs/email_test.log for details")

print()
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
