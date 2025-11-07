#!/bin/bash
# === PUBLIC SMOKE TESTS FOR LEVQOR ===
# Tests all public endpoints to verify system health
# Usage: BACKEND=https://api.levqor.ai ./public_smoke.sh

set -euo pipefail

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
ok() { echo -e "${GREEN}✅ $1${NC}"; }
fail() { echo -e "${RED}❌ $1${NC}"; exit 1; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
say() { echo -e "\n${YELLOW}=== $1 ===${NC}"; }

# Backend URL
BACKEND="${BACKEND:-https://api.levqor.ai}"
echo "Testing backend: $BACKEND"
echo ""

FAILED=0

# Test helper
test_endpoint() {
    local name="$1"
    local url="$2"
    local expected_status="${3:-200}"
    local check_json="${4:-true}"
    
    echo -n "Testing $name... "
    
    response=$(curl -s -w "\n%{http_code}" "$url" 2>&1)
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" != "$expected_status" ]; then
        echo -e "${RED}FAIL${NC} (HTTP $http_code, expected $expected_status)"
        echo "Response: $body"
        FAILED=$((FAILED + 1))
        return 1
    fi
    
    if [ "$check_json" = "true" ]; then
        if ! echo "$body" | jq . >/dev/null 2>&1; then
            echo -e "${RED}FAIL${NC} (Invalid JSON)"
            echo "Response: $body"
            FAILED=$((FAILED + 1))
            return 1
        fi
    fi
    
    echo -e "${GREEN}OK${NC}"
    return 0
}

# ===== Core Endpoints =====
say "Core Endpoints"

test_endpoint "Root (/)" "$BACKEND/" 200 true
test_endpoint "Health (/health)" "$BACKEND/health" 200 true
test_endpoint "Status (/status)" "$BACKEND/status" 200 true

# ===== Operations Endpoints =====
say "Operations Endpoints"

test_endpoint "Uptime (/ops/uptime)" "$BACKEND/ops/uptime" 200 true
test_endpoint "Queue Health (/ops/queue_health)" "$BACKEND/ops/queue_health" 200 true
test_endpoint "Billing Health (/billing/health)" "$BACKEND/billing/health" 200 true

# Verify uptime response structure
uptime_response=$(curl -fsS "$BACKEND/ops/uptime")
if echo "$uptime_response" | jq -e '.uptime_seconds' >/dev/null 2>&1; then
    ok "Uptime contains uptime_seconds field"
else
    fail "Uptime missing uptime_seconds field"
fi

# Verify queue_health response structure
queue_response=$(curl -fsS "$BACKEND/ops/queue_health")
if echo "$queue_response" | jq -e '.queue_stats' >/dev/null 2>&1; then
    ok "Queue health contains queue_stats field"
else
    fail "Queue health missing queue_stats field"
fi

# Verify billing_health response structure
billing_response=$(curl -fsS "$BACKEND/billing/health")
if echo "$billing_response" | jq -e '.healthy' >/dev/null 2>&1; then
    ok "Billing health contains healthy field"
    
    # Check if Stripe is configured
    is_healthy=$(echo "$billing_response" | jq -r '.healthy')
    if [ "$is_healthy" = "true" ]; then
        ok "Stripe credentials are configured"
    else
        warn "Stripe credentials not fully configured"
    fi
else
    fail "Billing health missing healthy field"
fi

# ===== Public Content =====
say "Public Content"

test_endpoint "Metrics (/public/metrics)" "$BACKEND/public/metrics" 200 true
test_endpoint "OpenAPI (/public/openapi.json)" "$BACKEND/public/openapi.json" 200 true

# ===== API v1 Endpoints (Status Check) =====
say "API v1 Endpoints"

# Create a test job
echo -n "Creating test job... "
job_response=$(curl -fsS -X POST "$BACKEND/api/v1/intake" \
    -H "Content-Type: application/json" \
    -H "X-Api-Key: test-key" \
    -d '{
        "workflow": "test-workflow",
        "payload": {"test": true},
        "callback_url": "https://example.com/callback",
        "priority": "normal"
    }' 2>&1 || echo '{"error": "no_auth"}')

if echo "$job_response" | jq -e '.job_id' >/dev/null 2>&1; then
    job_id=$(echo "$job_response" | jq -r '.job_id')
    echo -e "${GREEN}OK${NC} (job_id: $job_id)"
    
    # Check job status
    test_endpoint "Job Status (/api/v1/status/$job_id)" "$BACKEND/api/v1/status/$job_id" 200 true
else
    # Expected to fail without valid API key in production
    warn "Job creation skipped (API key required in production)"
fi

# ===== Summary =====
echo ""
say "Summary"

if [ $FAILED -eq 0 ]; then
    ok "All smoke tests passed! 🎉"
    echo ""
    echo "Backend is healthy and operational:"
    echo "  - All core endpoints responding"
    echo "  - Operations monitoring active"
    echo "  - Billing integration checked"
    echo "  - Public content served"
    exit 0
else
    fail "$FAILED test(s) failed"
fi
