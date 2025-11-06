#!/usr/bin/env python3
"""Setup Resend domain and get DNS records"""

import os
import requests
import json

API_KEY = os.getenv("RESEND_API_KEY")
BASE = "https://api.resend.com"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🔧 RESEND DOMAIN SETUP")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print()

# Step 1: Add domain
print("1️⃣ Adding levqor.ai domain to Resend...")
response = requests.post(
    f"{BASE}/domains",
    json={"name": "levqor.ai"},
    headers=headers,
    timeout=10
)

if response.status_code == 201 or response.status_code == 200:
    domain_data = response.json()
    print("✅ Domain added successfully!")
    print()
    
    # Step 2: Get DNS records
    print("2️⃣ Fetching DNS records...")
    domain_id = domain_data.get("id")
    
    records = domain_data.get("records", [])
    
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📋 DNS RECORDS TO ADD IN CLOUDFLARE:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    
    dns_output = []
    for record in records:
        rec_type = record.get("type", "TXT")
        name = record.get("name", "")
        value = record.get("value", "")
        print(f"Type:  {rec_type}")
        print(f"Name:  {name}")
        print(f"Value: {value}")
        print()
        dns_output.append(f"{rec_type}  {name}  {value}")
    
    # Update DNS file
    with open("docs/LEVQOR_EMAIL_DNS.txt", "w") as f:
        f.write("╔═══════════════════════════════════════════════════════════╗\n")
        f.write("║        LEVQOR EMAIL DNS RECORDS FOR CLOUDFLARE            ║\n")
        f.write("╚═══════════════════════════════════════════════════════════╝\n\n")
        f.write("ADD THESE RECORDS IN CLOUDFLARE DNS:\n")
        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n")
        
        for record in records:
            rec_type = record.get("type", "TXT")
            name = record.get("name", "")
            value = record.get("value", "")
            f.write(f"Type:  {rec_type}\n")
            f.write(f"Name:  {name}\n")
            f.write(f"Value: {value}\n")
            f.write(f"TTL:   Auto\n\n")
        
        f.write("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        f.write("CLOUDFLARE EMAIL ROUTING (FREE INBOUND):\n")
        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n")
        f.write("1. Go to Cloudflare → levqor.ai → Email → Email Routing\n")
        f.write("2. Click 'Enable Email Routing'\n")
        f.write("3. Add forwarding rules:\n\n")
        f.write("   support@levqor.ai  → (your Gmail)\n")
        f.write("   billing@levqor.ai  → (your Gmail)\n")
        f.write("   security@levqor.ai → (your Gmail)\n")
        f.write("   no-reply@levqor.ai → (your Gmail)\n\n")
        f.write("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        f.write("NEXT STEPS:\n")
        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n")
        f.write("1. Add ALL DNS records above to Cloudflare\n")
        f.write("2. Wait 5-10 minutes for DNS propagation\n")
        f.write("3. Run: python3 verify_resend.py\n")
        f.write("4. Once verified, run: python3 test_email.py\n\n")
    
    print("✅ DNS records saved to docs/LEVQOR_EMAIL_DNS.txt")
    print()
    print("📝 NEXT STEPS:")
    print("   1. Open docs/LEVQOR_EMAIL_DNS.txt")
    print("   2. Add all DNS records to Cloudflare")
    print("   3. Wait 5-10 minutes")
    print("   4. Run: python3 verify_resend.py")
    
elif response.status_code == 422:
    error_data = response.json()
    if "already exists" in str(error_data):
        print("ℹ️  Domain already exists in Resend")
        print()
        print("Fetching existing domain details...")
        
        # Get domain list
        list_response = requests.get(f"{BASE}/domains", headers=headers, timeout=10)
        if list_response.status_code == 200:
            domains = list_response.json().get("data", [])
            levqor_domain = None
            for d in domains:
                if d.get("name") == "levqor.ai":
                    levqor_domain = d
                    break
            
            if levqor_domain:
                print(f"Status: {levqor_domain.get('status', 'unknown')}")
                print(f"Region: {levqor_domain.get('region', 'unknown')}")
                print()
                
                records = levqor_domain.get("records", [])
                if records:
                    print("DNS RECORDS:")
                    for record in records:
                        print(f"  {record.get('type')} {record.get('name')} = {record.get('value')}")
    else:
        print(f"❌ Error: {error_data}")
else:
    print(f"❌ Failed: {response.status_code}")
    print(response.text)

print()
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
