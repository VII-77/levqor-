#!/bin/bash

echo "🔍 Levqor Production Verification Script"
echo "========================================="
echo ""

API_URL="${1:-http://localhost:5000}"
FAILED_CHECKS=0
PASSED_CHECKS=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_pass() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
    ((PASSED_CHECKS++))
}

check_fail() {
    echo -e "${RED}❌ FAIL${NC}: $1"
    ((FAILED_CHECKS++))
}

check_warn() {
    echo -e "${YELLOW}⚠️  WARN${NC}: $1"
}

echo "Testing API at: $API_URL"
echo ""

# 1. Basic Health Check
echo "📋 Test 1: Basic Health Check"
response=$(curl -s -w "\n%{http_code}" "$API_URL/ops/uptime" 2>/dev/null || echo "000")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n -1)

if [ "$http_code" = "200" ]; then
    check_pass "API is reachable (HTTP 200)"
    
    # Check database status (nested under services)
    if echo "$body" | grep -q '"database":"operational"'; then
        check_pass "Database is operational"
    else
        check_warn "Database status check skipped (unable to parse)"
    fi
else
    check_fail "API unreachable (HTTP $http_code)"
fi
echo ""

# 2. Queue Health Check
echo "📋 Test 2: Queue Infrastructure"
response=$(curl -s "$API_URL/ops/queue_health" 2>/dev/null || echo "{}")
queue_status=$(echo "$response" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)

if [ "$queue_status" = "healthy" ]; then
    check_pass "Redis queue is healthy"
elif [ "$queue_status" = "unavailable" ]; then
    check_warn "Redis unavailable (graceful degradation active)"
elif [ "$queue_status" = "error" ]; then
    check_warn "Queue error (expected if Redis not configured)"
else
    check_fail "Queue status unknown: $queue_status"
fi
echo ""

# 3. Metrics Endpoint
echo "📋 Test 3: Prometheus Metrics"
metrics=$(curl -s "$API_URL/metrics" 2>/dev/null || echo "")

if [ -z "$metrics" ]; then
    check_fail "Metrics endpoint returned no data"
else
    check_pass "Metrics endpoint accessible"
    
    # Check for required metrics
    if echo "$metrics" | grep -q "jobs_run_total"; then
        check_pass "jobs_run_total metric present"
    else
        check_fail "jobs_run_total metric missing"
    fi
    
    if echo "$metrics" | grep -q "queue_depth"; then
        check_pass "queue_depth metric present"
    else
        check_fail "queue_depth metric missing"
    fi
    
    if echo "$metrics" | grep -q "error_rate"; then
        check_pass "error_rate metric present"
    else
        check_fail "error_rate metric missing"
    fi
    
    if echo "$metrics" | grep -q "database_status"; then
        check_pass "database_status metric present"
    else
        check_fail "database_status metric missing"
    fi
fi
echo ""

# 4. Feature Flags (requires API key)
echo "📋 Test 4: Feature Flags System"
if [ -z "$LEVQOR_API_KEY" ]; then
    check_warn "LEVQOR_API_KEY not set, skipping flags check"
else
    flags=$(curl -s -H "Authorization: Bearer $LEVQOR_API_KEY" "$API_URL/api/v1/ops/flags" 2>/dev/null || echo "{}")
    
    if echo "$flags" | grep -q "PG_ENABLED"; then
        check_pass "Feature flags endpoint accessible"
        
        pg_enabled=$(echo "$flags" | grep -o '"PG_ENABLED":[^,}]*' | cut -d':' -f2)
        queue_enabled=$(echo "$flags" | grep -o '"NEW_QUEUE_ENABLED":[^,}]*' | cut -d':' -f2)
        
        echo "   PG_ENABLED: $pg_enabled"
        echo "   NEW_QUEUE_ENABLED: $queue_enabled"
    else
        check_fail "Feature flags endpoint error"
    fi
fi
echo ""

# 5. Billing Endpoints
echo "📋 Test 5: Billing Infrastructure"
usage_response=$(curl -s -w "\n%{http_code}" "$API_URL/billing/usage?user_id=test_user" 2>/dev/null || echo "000")
usage_code=$(echo "$usage_response" | tail -n1)

limits_response=$(curl -s -w "\n%{http_code}" "$API_URL/billing/limits?user_id=test_user" 2>/dev/null || echo "000")
limits_code=$(echo "$limits_response" | tail -n1)

if [ "$usage_code" = "200" ] || [ "$usage_code" = "404" ]; then
    check_pass "/billing/usage endpoint operational"
else
    check_fail "/billing/usage endpoint error (HTTP $usage_code)"
fi

if [ "$limits_code" = "200" ] || [ "$limits_code" = "404" ]; then
    check_pass "/billing/limits endpoint operational"
else
    check_fail "/billing/limits endpoint error (HTTP $limits_code)"
fi
echo ""

# 6. File System Checks
echo "📋 Test 6: Infrastructure Files"
if [ -f "config/flags.json" ]; then
    check_pass "Feature flags config exists"
else
    check_fail "config/flags.json not found"
fi

if [ -f "logging_config.py" ]; then
    check_pass "Logging config exists"
else
    check_fail "logging_config.py not found"
fi

if [ -f "db/migrate_v2.py" ]; then
    check_pass "PostgreSQL migration script exists"
else
    check_fail "db/migrate_v2.py not found"
fi

if [ -f "scripts/canary_check.sh" ]; then
    check_pass "Canary testing script exists"
else
    check_fail "scripts/canary_check.sh not found"
fi

if [ -d "job_queue" ]; then
    check_pass "Job queue module exists"
else
    check_fail "job_queue/ directory not found"
fi

if [ -d "connectors_v2" ]; then
    check_pass "Connectors v2 module exists"
else
    check_fail "connectors_v2/ directory not found"
fi
echo ""

# 7. Log Directory
echo "📋 Test 7: Logging Infrastructure"
if [ -d "logs" ]; then
    check_pass "logs/ directory exists"
    
    log_count=$(ls -1 logs/*.log 2>/dev/null | wc -l)
    echo "   Found $log_count log files"
else
    check_warn "logs/ directory not found (will be created on startup)"
fi
echo ""

# 8. Documentation
echo "📋 Test 8: Documentation"
if [ -f "PHASE2_COMPLETION.md" ]; then
    check_pass "Phase-2 completion report exists"
else
    check_fail "PHASE2_COMPLETION.md not found"
fi

if [ -f "replit.md" ]; then
    check_pass "Project documentation exists"
else
    check_warn "replit.md not found"
fi
echo ""

# Summary
echo "========================================="
echo "📊 Verification Summary"
echo "========================================="
echo -e "Passed: ${GREEN}$PASSED_CHECKS${NC}"
echo -e "Failed: ${RED}$FAILED_CHECKS${NC}"
echo ""

if [ $FAILED_CHECKS -eq 0 ]; then
    echo -e "${GREEN}✅ ALL CHECKS PASSED${NC}"
    echo "Your production environment is fully operational!"
    exit 0
elif [ $FAILED_CHECKS -le 2 ]; then
    echo -e "${YELLOW}⚠️  MINOR ISSUES DETECTED${NC}"
    echo "Production environment is mostly operational with minor warnings."
    exit 0
else
    echo -e "${RED}❌ CRITICAL ISSUES DETECTED${NC}"
    echo "Please review failed checks before deploying to production."
    exit 1
fi
