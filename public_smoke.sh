#!/bin/bash
set -euo pipefail
: "${BACKEND:?Set BACKEND first, e.g. export BACKEND=https://... or http://localhost:5000}"

ok(){ printf "✅ %s\n" "$1"; }
warn(){ printf "⚠️  %s\n" "$1"; }
fail(){ printf "❌ %s\n" "$1"; exit 1; }

echo "=== LEVQOR PUBLIC SMOKE TEST ==="
echo "Backend: $BACKEND"
echo ""

# 1) Core health
echo "[1/3] Testing core endpoints..."
curl -fsS "$BACKEND/status" | jq -e '.status=="pass"' >/dev/null && ok "/status pass" || fail "/status failed"
curl -fsS "$BACKEND/ops/uptime" >/dev/null && ok "/ops/uptime ok" || fail "/ops/uptime failed"

# Billing health is optional (may not be available on all deployments)
if curl -fsS "$BACKEND/billing/health" 2>/dev/null | jq -e '.status=="operational"' >/dev/null 2>&1; then
    ok "/billing/health pass"
else
    warn "/billing/health not available (may be a different deployment)"
fi

echo ""
echo "[2/3] Checking security headers..."
SEC=$(curl -fsSI "$BACKEND/status")
echo "$SEC" | grep -qi "content-security-policy" && ok "CSP header present" || warn "CSP header missing"
echo "$SEC" | grep -qi "strict-transport-security" && ok "HSTS present" || warn "HSTS missing"
echo "$SEC" | grep -qi "x-content-type-options" && ok "X-Content-Type-Options present" || warn "X-Content-Type-Options missing"

echo ""
echo "[3/3] Testing monitoring endpoints..."
if curl -fsS "$BACKEND/ops/queue_health" >/dev/null 2>&1; then 
    ok "Queue health reachable"
else 
    warn "Queue health not reachable (may require auth)"
fi

if curl -fsS "$BACKEND/metrics" >/dev/null 2>&1; then 
    ok "Prometheus /metrics reachable"
else 
    warn "/metrics not reachable (may require auth)"
fi

echo ""
echo "[Bonus] Additional checks..."
HTTP_CODE=$(curl -fsS -o /dev/null -w "%{http_code}" "$BACKEND/status" 2>/dev/null)
[ "$HTTP_CODE" = "200" ] && ok "HTTP status code: $HTTP_CODE" || warn "HTTP status code: $HTTP_CODE"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ ALL PUBLIC SMOKE TESTS PASSED!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
