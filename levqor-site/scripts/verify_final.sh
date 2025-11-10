#!/usr/bin/env bash
set -euo pipefail

APP="${1:-https://levqor.ai}"
API="${2:-https://api.levqor.ai}"

echo "═══════════════════════════════════════"
echo "FINAL VERIFICATION"
echo "═══════════════════════════════════════"
echo ""
echo "App:  $APP"
echo "API:  $API"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

pass=0
fail=0

check() {
  local name="$1"
  local cmd="$2"
  echo -n "  $name... "
  if eval "$cmd" &>/dev/null; then
    echo -e "${GREEN}✓${NC}"
    ((pass++))
  else
    echo -e "${RED}✗${NC}"
    ((fail++))
  fi
}

echo "1. Frontend Pages"
echo "─────────────────────────────"
check "Homepage" "curl -sf $APP -o /dev/null"
check "Pricing page" "curl -sf $APP/pricing -o /dev/null"
check "Sign-in page" "curl -sf $APP/signin -o /dev/null"
check "Dashboard (redirect)" "curl -sf $APP/dashboard -o /dev/null || curl -sI $APP/dashboard | grep -q '30[12]'"

echo ""
echo "2. API Health"
echo "─────────────────────────────"
check "API Status" "curl -sf $API/status -o /dev/null"
check "API Uptime" "curl -sf $API/ops/uptime -o /dev/null"
check "API Health" "curl -sf $API/health -o /dev/null"

echo ""
echo "3. Checkout API (GET)"
echo "─────────────────────────────"
check "Starter Monthly" "curl -sf '$APP/api/checkout?plan=starter&term=monthly' | grep -q 'url'"
check "Pro Yearly" "curl -sf '$APP/api/checkout?plan=pro&term=yearly' | grep -q 'url'"
check "Business Monthly" "curl -sf '$APP/api/checkout?plan=business&term=monthly' | grep -q 'url'"

echo ""
echo "4. Checkout API (POST)"
echo "─────────────────────────────"
check "Starter POST" "curl -sf -X POST '$APP/api/checkout' -H 'content-type: application/json' --data '{\"plan\":\"starter\",\"term\":\"monthly\"}' | grep -q 'url'"
check "Pro POST with trial" "curl -sf -X POST '$APP/api/checkout' -H 'content-type: application/json' --data '{\"plan\":\"pro\",\"term\":\"yearly\"}' | grep -q 'url'"
check "Business POST" "curl -sf -X POST '$APP/api/checkout' -H 'content-type: application/json' --data '{\"plan\":\"business\",\"term\":\"monthly\"}' | grep -q 'url'"

echo ""
echo "5. Add-ons Support"
echo "─────────────────────────────"
check "Business + Priority Support" "curl -sf -X POST '$APP/api/checkout' -H 'content-type: application/json' --data '{\"plan\":\"business\",\"term\":\"monthly\",\"addons\":[\"PRIORITY_SUPPORT\"]}' | grep -q 'url'"
check "Pro + SLA 99.9%" "curl -sf -X POST '$APP/api/checkout' -H 'content-type: application/json' --data '{\"plan\":\"pro\",\"term\":\"yearly\",\"addons\":[\"SLA_99_9\"]}' | grep -q 'url'"

echo ""
echo "6. Detailed Checkout Response"
echo "─────────────────────────────"
echo "Sample response (Business + White-label):"
curl -sf -X POST "$APP/api/checkout" \
  -H 'content-type: application/json' \
  --data '{"plan":"business","term":"yearly","addons":["WHITE_LABEL"]}' \
  | jq '.' 2>/dev/null || echo "No jq installed, raw response shown"

echo ""
echo "═══════════════════════════════════════"
echo "RESULTS"
echo "═══════════════════════════════════════"
echo -e "${GREEN}Passed: $pass${NC}"
echo -e "${RED}Failed: $fail${NC}"

if [ $fail -eq 0 ]; then
  echo ""
  echo "✅ All checks passed!"
  exit 0
else
  echo ""
  echo "❌ Some checks failed. Review the output above."
  exit 1
fi
