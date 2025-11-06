#!/usr/bin/env python3
"""Verify Resend domain status"""

import os
import requests

API_KEY = os.getenv("RESEND_API_KEY")
BASE = "https://api.resend.com"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("🔍 Checking Resend domain verification status...")
print()

response = requests.get(f"{BASE}/domains", headers=headers, timeout=10)

if response.status_code == 200:
    domains = response.json().get("data", [])
    levqor_domain = None
    
    for d in domains:
        if d.get("name") == "levqor.ai":
            levqor_domain = d
            break
    
    if levqor_domain:
        status = levqor_domain.get("status", "unknown")
        print(f"Domain: levqor.ai")
        print(f"Status: {status}")
        print(f"Region: {levqor_domain.get('region', 'unknown')}")
        print()
        
        if status == "verified":
            print("✅ DOMAIN VERIFIED!")
            print()
            print("You can now send emails. Run:")
            print("  python3 test_email.py")
        else:
            print("⏳ Domain not verified yet")
            print()
            print("Make sure you added all DNS records to Cloudflare.")
            print("DNS propagation can take 5-30 minutes.")
            print()
            print("Check status: https://resend.com/domains")
    else:
        print("❌ Domain levqor.ai not found in Resend")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
