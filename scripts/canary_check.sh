#!/bin/bash
set -e

echo "🐤 Canary deployment health check"
echo "=================================="

API_URL="${1:-http://localhost:5000}"
THRESHOLD_ERROR_RATE=5.0
THRESHOLD_P95_MS=500

echo "Testing API: $API_URL"

check_health() {
    echo -n "⏳ Health check... "
    response=$(curl -s -w "\n%{http_code}" "$API_URL/ops/uptime" || echo "000")
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" = "200" ]; then
        echo "✅ PASS (200 OK)"
        return 0
    else
        echo "❌ FAIL (HTTP $http_code)"
        return 1
    fi
}

check_queue() {
    echo -n "⏳ Queue health... "
    response=$(curl -s "$API_URL/ops/queue_health" || echo "{}")
    status=$(echo "$response" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    
    if [ "$status" = "healthy" ] || [ "$status" = "unavailable" ]; then
        echo "✅ PASS ($status)"
        return 0
    else
        echo "❌ FAIL ($status)"
        return 1
    fi
}

check_metrics() {
    echo -n "⏳ Metrics check... "
    response=$(curl -s "$API_URL/metrics" || echo "")
    
    if [ -z "$response" ]; then
        echo "❌ FAIL (no response)"
        return 1
    fi
    
    error_rate=$(echo "$response" | grep "error_rate" | awk '{print $2}')
    
    if [ -z "$error_rate" ]; then
        echo "⚠️  WARN (no error_rate metric)"
        return 0
    fi
    
    if (( $(echo "$error_rate > $THRESHOLD_ERROR_RATE" | bc -l) )); then
        echo "❌ FAIL (error_rate: ${error_rate}% > ${THRESHOLD_ERROR_RATE}%)"
        return 1
    else
        echo "✅ PASS (error_rate: ${error_rate}%)"
        return 0
    fi
}

check_database() {
    echo -n "⏳ Database connectivity... "
    response=$(curl -s "$API_URL/ops/uptime" || echo "{}")
    db_status=$(echo "$response" | grep -o '"database":"[^"]*"' | cut -d'"' -f4)
    
    if [ "$db_status" = "operational" ]; then
        echo "✅ PASS"
        return 0
    else
        echo "❌ FAIL ($db_status)"
        return 1
    fi
}

main() {
    checks_passed=0
    checks_total=4
    
    check_health && ((checks_passed++)) || true
    check_queue && ((checks_passed++)) || true
    check_metrics && ((checks_passed++)) || true
    check_database && ((checks_passed++)) || true
    
    echo ""
    echo "=================================="
    echo "Results: $checks_passed/$checks_total checks passed"
    
    if [ $checks_passed -eq $checks_total ]; then
        echo "✅ All canary checks PASSED - deployment is healthy"
        exit 0
    elif [ $checks_passed -ge 3 ]; then
        echo "⚠️  Most canary checks passed - deployment acceptable with warnings"
        exit 0
    else
        echo "❌ CRITICAL: Canary checks FAILED - rollback recommended"
        echo ""
        echo "To rollback:"
        echo "  1. Revert feature flags in config/flags.json"
        echo "  2. Restart workflows: npm run restart"
        echo "  3. Check logs: tail -f logs/*.log"
        exit 1
    fi
}

main
