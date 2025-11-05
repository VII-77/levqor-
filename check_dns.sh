#!/bin/bash
echo "🔍 Checking api.levqor.ai DNS status..."
echo ""

# Check DNS
nslookup api.levqor.ai 8.8.8.8 | grep -A2 "Name:" || echo "❌ DNS not propagated yet"

echo ""
echo "🌐 Testing endpoint..."

# Test endpoint
response=$(curl -s -m 5 https://api.levqor.ai/ 2>&1)
if echo "$response" | grep -q "levqor-backend"; then
  echo "✅ api.levqor.ai is LIVE!"
  echo "$response" | jq
else
  echo "⏳ Waiting for DNS to propagate..."
fi
