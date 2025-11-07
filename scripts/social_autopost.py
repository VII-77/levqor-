import os
import requests
import sys

BUF_TOKEN = os.getenv("BUFFER_ACCESS_TOKEN")
if not BUF_TOKEN:
    print("[!] BUFFER_ACCESS_TOKEN not set - skipping social post")
    print("    Set this env var to enable automatic social media posting")
    sys.exit(0)

PROFILE_ID = os.getenv("BUFFER_PROFILE_ID")
if not PROFILE_ID:
    print("[!] BUFFER_PROFILE_ID not set - cannot determine target profile")
    sys.exit(1)

payload = {
    "text": "🚀 Levqor is live! Automate your workflows 10× faster → https://levqor.ai",
    "profile_ids": [PROFILE_ID],
    "now": True
}

try:
    r = requests.post(
        "https://api.bufferapp.com/1/updates/create.json",
        data=payload,
        headers={"Authorization": f"Bearer {BUF_TOKEN}"},
        timeout=10
    )
    print(f"[✓] Buffer post queued: HTTP {r.status_code}")
    if r.status_code == 200:
        print(f"[✓] Post scheduled successfully!")
    else:
        print(f"[!] Response: {r.text}")
except Exception as e:
    print(f"[!] Failed to post to Buffer: {e}")
    sys.exit(1)
