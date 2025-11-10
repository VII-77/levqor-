#!/bin/bash

echo "═══════════════════════════════════════"
echo "CHECKOUT API TESTS"
echo "═══════════════════════════════════════"
echo ""

BASE_URL="${1:-https://levqor.ai}"

echo "Testing against: $BASE_URL"
echo ""

test_checkout() {
  local plan=$1
  local term=$2
  echo "Testing: $plan ($term)..."
  
  response=$(curl -s -X POST "$BASE_URL/api/checkout" \
    -H "content-type: application/json" \
    --data "{\"plan\":\"$plan\",\"term\":\"$term\"}")
  
  url=$(echo "$response" | jq -r '.url // empty')
  
  if [[ "$url" =~ ^https://checkout.stripe.com ]]; then
    echo "  ✅ PASS - Got Stripe URL"
  else
    echo "  ❌ FAIL - Response: $response"
    return 1
  fi
}

test_addons() {
  local plan=$1
  local term=$2
  echo "Testing: $plan ($term) with add-ons..."
  
  response=$(curl -s -X POST "$BASE_URL/api/checkout" \
    -H "content-type: application/json" \
    --data "{\"plan\":\"$plan\",\"term\":\"$term\",\"addons\":[\"runs_25k\",\"ai_10k\"]}")
  
  url=$(echo "$response" | jq -r '.url // empty')
  
  if [[ "$url" =~ ^https://checkout.stripe.com ]]; then
    echo "  ✅ PASS - Got Stripe URL with add-ons"
  else
    echo "  ❌ FAIL - Response: $response"
    return 1
  fi
}

echo "1. Core Plan Tests"
echo "──────────────────"
test_checkout "starter" "monthly"
test_checkout "starter" "yearly"
test_checkout "pro" "monthly"
test_checkout "pro" "yearly"
test_checkout "business" "monthly"
test_checkout "business" "yearly"

echo ""
echo "2. Add-ons Tests"
echo "──────────────────"
test_addons "pro" "monthly"
test_addons "business" "yearly"

echo ""
echo "3. GET Support (Legacy)"
echo "──────────────────"
response=$(curl -s "$BASE_URL/api/checkout?plan=starter&term=monthly")
url=$(echo "$response" | jq -r '.url // empty')
if [[ "$url" =~ ^https://checkout.stripe.com ]]; then
  echo "  ✅ PASS - GET method works"
else
  echo "  ❌ FAIL - Response: $response"
fi

echo ""
echo "═══════════════════════════════════════"
echo "Tests complete!"
echo "═══════════════════════════════════════"
