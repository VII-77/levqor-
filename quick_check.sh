#!/bin/bash
echo "═══════════════════════════════════════════════════════"
echo "🔍 CHECKING API STATUS"
echo "═══════════════════════════════════════════════════════"
echo ""

# Check DNS
echo "1️⃣ DNS Resolution:"
dns=$(dig api.levqor.ai +short 2>/dev/null | head -1)
if [ -n "$dns" ]; then
  echo "   ✅ api.levqor.ai → $dns"
else
  echo "   ❌ DNS not resolved yet"
fi
echo ""

# Test direct Replit URL
echo "2️⃣ Direct Replit URL (https://levqor-backend.replit.app):"
result=$(curl -s https://levqor-backend.replit.app/ 2>&1)
if echo "$result" | grep -q "levqor-backend"; then
  echo "   ✅ Backend is working!"
else
  echo "   ❌ Backend not responding"
fi
echo ""

# Test custom domain
echo "3️⃣ Custom Domain (https://api.levqor.ai):"
result2=$(curl -s https://api.levqor.ai/ 2>&1)
if echo "$result2" | grep -q "levqor-backend"; then
  echo "   ✅ Custom domain is LIVE!"
  echo ""
  echo "🟢 READY TO RUN: ./final_smoke_test.sh"
else
  echo "   ⏳ Custom domain not ready yet"
  echo ""
  echo "ACTION NEEDED:"
  echo "- Go to Replit → Deployments → Domains"
  echo "- Click 'Verify' on api.levqor.ai"
  echo "- Wait for 'Verified ✅' status"
  echo "- Then run: ./final_smoke_test.sh"
fi
echo ""
echo "═══════════════════════════════════════════════════════"
