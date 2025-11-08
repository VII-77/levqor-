#!/bin/bash
set -e

echo "🔎 VERIFYING LEVQOR v6.5..."
FAIL=0

function check() {
    if eval "$1" >/dev/null 2>&1; then
        echo "✅ $2"
    else
        echo "❌ $2"
        FAIL=1
    fi
}

echo ""
echo "=== FILE STRUCTURE CHECKS ==="
check "test -f monitors/ai_insights.py" "AI Insights module present"
check "test -f monitors/runbooks.py" "Runbooks module present"
check "test -f api/admin/insights.py" "Insights API present"
check "test -f api/admin/runbooks.py" "Runbooks API present"
check "test -f api/admin/postmortem.py" "Postmortem API present"
check "test -f db/migrations/007_insights.sql" "Migration file present"
check "test -f levqor-site/src/app/insights/page.tsx" "Frontend insights page present"
check "test -f levqor-site/src/app/admin/insights/page.tsx" "Admin insights page present"

echo ""
echo "=== DATABASE CHECKS ==="
check "sqlite3 levqor.db 'SELECT name FROM sqlite_master WHERE type=\"table\" AND name=\"incidents\"' | grep incidents" "incidents table exists" || python3 -c "import sqlite3; c=sqlite3.connect('levqor.db'); print('✅ incidents table exists' if c.execute('SELECT name FROM sqlite_master WHERE type=\"table\" AND name=\"incidents\"').fetchone() else exit(1))"
check "sqlite3 levqor.db 'SELECT name FROM sqlite_master WHERE type=\"table\" AND name=\"feature_flags\"' | grep feature_flags" "feature_flags table exists" || python3 -c "import sqlite3; c=sqlite3.connect('levqor.db'); print('✅ feature_flags table exists' if c.execute('SELECT name FROM sqlite_master WHERE type=\"table\" AND name=\"feature_flags\"').fetchone() else exit(1))"

echo ""
echo "=== API ENDPOINT CHECKS ==="
check "curl -sf https://api.levqor.ai/status" "Backend health check"
check "curl -sf https://api.levqor.ai/api/admin/anomaly/explain?latency_ms=100 | grep latency_ms" "Anomaly API working"
check "curl -sf https://api.levqor.ai/api/admin/runbooks | grep runbooks" "Runbooks API working"
check "curl -sf https://api.levqor.ai/api/admin/brief/weekly | grep summary" "Weekly brief API working"
check "curl -sf -X POST https://api.levqor.ai/api/admin/incidents/summarize -H 'Content-Type: application/json' -d '{\"type\":\"test\"}' | grep summary" "Incident summarize API working"

echo ""
echo "=== FRONTEND CHECKS ==="
check "curl -sf https://levqor.ai/insights | grep -i insights" "Frontend insights page accessible"
check "curl -sf https://levqor.ai/admin/insights | grep -i insights" "Admin insights page accessible"

echo ""
if [ $FAIL -eq 0 ]; then
    echo "🎯 All v6.5 checks passed!"
    exit 0
else
    echo "⚠️ Some checks failed"
    exit 1
fi
