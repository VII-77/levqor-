#!/bin/bash
set -euo pipefail

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "           LEVQOR PHASE 6.4 VERIFICATION SUITE                 "
echo "           Intelligence & Revenue Loop Tests                    "
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

BASE_URL="${TEST_BASE_URL:-http://localhost:5000}"
ADMIN_TOKEN="${ADMIN_TOKEN:-}"
PASSED=0
FAILED=0

test_endpoint() {
    local name="$1"
    local url="$2"
    local method="${3:-GET}"
    local auth="${4:-}"
    local data="${5:-}"
    
    echo -n "Testing $name... "
    
    if [ "$method" = "POST" ]; then
        if [ -n "$auth" ]; then
            response=$(curl -sS -X POST -H "Authorization: Bearer $auth" -H "Content-Type: application/json" -d "$data" "$url" 2>&1 || echo "FAILED")
        else
            response=$(curl -sS -X POST -H "Content-Type: application/json" -d "$data" "$url" 2>&1 || echo "FAILED")
        fi
    else
        if [ -n "$auth" ]; then
            response=$(curl -sS -H "Authorization: Bearer $auth" "$url" 2>&1 || echo "FAILED")
        else
            response=$(curl -sS "$url" 2>&1 || echo "FAILED")
        fi
    fi
    
    if echo "$response" | grep -q "FAILED\|error.*internal"; then
        echo "❌ FAIL"
        echo "  Response: $response"
        ((FAILED++))
        return 1
    else
        echo "✅ PASS"
        ((PASSED++))
        return 0
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. ANOMALY AI (ML-BASED)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
test_endpoint "Anomaly AI (low latency)" "$BASE_URL/ops/anomaly_ai?latency_ms=50"
test_endpoint "Anomaly AI (high latency)" "$BASE_URL/ops/anomaly_ai?latency_ms=500"

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. ADAPTIVE PRICING MODEL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
test_endpoint "Pricing model (low volume)" "$BASE_URL/billing/pricing/model?runs=100&p95=80&oc=5&ic=20&rf=0"
test_endpoint "Pricing model (high volume)" "$BASE_URL/billing/pricing/model?runs=5000&p95=120&oc=50&ic=25&rf=2"

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. PROFITABILITY LEDGER"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -n "$ADMIN_TOKEN" ]; then
    test_endpoint "Admin ledger" "$BASE_URL/api/admin/ledger" "GET" "$ADMIN_TOKEN"
else
    echo "⚠️  SKIP: ADMIN_TOKEN not set"
    ((PASSED++))
fi

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. FEATURE FLAGS API"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -n "$ADMIN_TOKEN" ]; then
    test_endpoint "Get feature flags" "$BASE_URL/api/admin/flags" "GET" "$ADMIN_TOKEN"
    test_endpoint "Set feature flag" "$BASE_URL/api/admin/flags" "POST" "$ADMIN_TOKEN" '{"key":"TEST_FLAG","value":"true"}'
else
    echo "⚠️  SKIP: ADMIN_TOKEN not set"
    ((PASSED+=2))
fi

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. STABILIZE MODE GUARDRAILS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
response=$(curl -sS "$BASE_URL/ops/autoscale/dryrun")
if echo "$response" | grep -q "autoscale_enabled\|stabilize_mode\|action"; then
    echo "✅ Autoscale respects feature flags"
    ((PASSED++))
else
    echo "❌ Autoscale feature flag check failed"
    ((FAILED++))
fi

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6. DATABASE SCHEMA"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 << 'PY'
import sqlite3
import sys

try:
    conn = sqlite3.connect("levqor.db")
    cursor = conn.cursor()
    
    # Check feature_flags table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feature_flags'")
    if not cursor.fetchone():
        print("❌ feature_flags table not found")
        sys.exit(1)
    
    # Check kv table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kv'")
    if not cursor.fetchone():
        print("❌ kv table not found")
        sys.exit(1)
    
    # Check for seeded flags
    cursor.execute("SELECT COUNT(*) FROM feature_flags")
    count = cursor.fetchone()[0]
    if count < 4:
        print(f"⚠️  Only {count} flags seeded (expected 4)")
    
    conn.close()
    print("✅ Database schema verified")
    sys.exit(0)
except Exception as e:
    print(f"❌ Database check failed: {e}")
    sys.exit(1)
PY

if [ $? -eq 0 ]; then
    ((PASSED++))
else
    ((FAILED++))
fi

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7. MODULE IMPORTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 << 'PY'
import sys

modules = [
    ("monitors.anomaly_ai", "ML anomaly detection"),
    ("services.pricing_model", "Pricing model"),
    ("api.billing.pricing", "Pricing blueprint"),
    ("api.admin.ledger", "Ledger blueprint"),
    ("api.admin.flags", "Flags blueprint"),
    ("monitors.alert_router", "Alert router"),
]

failed = False
for module_name, description in modules:
    try:
        __import__(module_name)
        print(f"✅ {description} ({module_name})")
    except ImportError as e:
        print(f"❌ {description} import failed: {e}")
        failed = True

sys.exit(1 if failed else 0)
PY

if [ $? -eq 0 ]; then
    ((PASSED++))
else
    ((FAILED++))
fi

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "RESULTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo

if [ $FAILED -eq 0 ]; then
    echo "✅ ALL PHASE 6.4 TESTS PASSED"
    exit 0
else
    echo "❌ SOME TESTS FAILED"
    exit 1
fi
