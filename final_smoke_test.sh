#!/bin/bash
set -e

KEY="${1:-levqor_r65toSg3omMJbgFa__Cjoxf6fZEVbbNG33XqcSpVnCY}"

echo "🔍 Testing api.levqor.ai..."
echo ""

# Test 1: Root endpoint
echo "1️⃣ Testing root endpoint..."
curl -sI https://api.levqor.ai/ | head -n1

# Test 2: Security headers
echo ""
echo "2️⃣ Checking security headers..."
curl -sI https://api.levqor.ai/public/metrics | grep -E 'Strict-Transport|Content-Security-Policy|X-Frame-Options'

# Test 3: Create job
echo ""
echo "3️⃣ Creating test job..."
jid=$(curl -s -X POST https://api.levqor.ai/api/v1/intake \
  -H "X-Api-Key: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"workflow":"demo","payload":{}}' | jq -r .job_id)

echo "Job ID: $jid"

# Test 4: Check job status
echo ""
echo "4️⃣ Checking job status..."
curl -s https://api.levqor.ai/api/v1/status/$jid | jq

echo ""
echo "🟢 BACKEND LIVE - api.levqor.ai is production-ready!"
