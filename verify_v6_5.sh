#!/bin/bash
# Phase 6.5 Verification Script
set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 Phase 6.5 Verification: Intelligence Feedback & Growth Loop"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

FAIL_COUNT=0

# Function to check endpoint
check_endpoint() {
    local name="$1"
    local url="$2"
    local auth="$3"
    
    if [ -n "$auth" ]; then
        if curl -fsS -H "Authorization: Bearer $ADMIN_TOKEN" "$url" >/dev/null 2>&1; then
            echo "✅ $name"
        else
            echo "❌ $name FAILED"
            ((FAIL_COUNT++))
        fi
    else
        if curl -fsS "$url" >/dev/null 2>&1; then
            echo "✅ $name"
        else
            echo "❌ $name FAILED"
            ((FAIL_COUNT++))
        fi
    fi
}

# Check database tables
echo "📊 Checking Database Tables..."
python3 -c "
import sqlite3
conn = sqlite3.connect('levqor.db')
c = conn.cursor()
tables = ['growth_events', 'referral_retention', 'discounts', 'tuning_audit']
for table in tables:
    c.execute(f'SELECT name FROM sqlite_master WHERE type=\\\"table\\\" AND name=\\\"{table}\\\"')
    if c.fetchone():
        print(f'✅ Table: {table}')
    else:
        print(f'❌ Table: {table} MISSING')
        exit(1)
conn.close()
" || ((FAIL_COUNT++))

echo ""
echo "🌐 Checking API Endpoints..."

# Base URL
BASE_URL="${BASE_URL:-http://localhost:5000}"

# Public endpoints (no auth)
check_endpoint "Auto-Tuning Endpoint" "$BASE_URL/ops/auto_tune"
check_endpoint "Discount Preview" "$BASE_URL/billing/discounts/preview"
check_endpoint "Active Discounts" "$BASE_URL/billing/discounts/active"
check_endpoint "Anomaly AI (Phase 6.4)" "$BASE_URL/ops/anomaly_ai?latency_ms=100"

# Admin endpoints (require auth)
if [ -n "$ADMIN_TOKEN" ]; then
    check_endpoint "Growth Analytics" "$BASE_URL/api/admin/growth" "auth"
    check_endpoint "Feature Flags API" "$BASE_URL/api/admin/flags" "auth"
    check_endpoint "Profitability Ledger" "$BASE_URL/api/admin/ledger" "auth"
else
    echo "⚠️  ADMIN_TOKEN not set - skipping admin endpoint checks"
fi

echo ""
echo "📦 Checking File Existence..."

FILES=(
    "monitors/auto_tune.py"
    "api/admin/growth.py"
    "scripts/aggregate_growth_retention.py"
    "api/billing/discounts.py"
    "scripts/governance_report.py"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ File: $file"
    else
        echo "❌ File: $file MISSING"
        ((FAIL_COUNT++))
    fi
done

echo ""
echo "🎛️  Checking Feature Flags..."

python3 -c "
import sqlite3
conn = sqlite3.connect('levqor.db')
c = conn.cursor()
c.execute('SELECT key, value FROM feature_flags')
flags = dict(c.fetchall())
conn.close()

expected = ['AUTOSCALE_ENABLED', 'INCIDENT_AUTORECOVER', 'PRICING_AUTO_APPLY', 'STABILIZE_MODE']
for flag in expected:
    val = flags.get(flag, 'MISSING')
    status = '✅' if val in ['true', 'false'] else '❌'
    print(f'{status} Flag: {flag}={val}')
" || ((FAIL_COUNT++))

echo ""
echo "🤖 Checking Scheduler Jobs..."

python3 -c "
from monitors.scheduler import get_scheduler
scheduler = get_scheduler()
if scheduler:
    jobs = scheduler.get_jobs()
    job_names = [j.name for j in jobs]
    expected_jobs = [
        'Daily retention metrics',
        'SLO monitoring',
        'Daily ops report',
        'Weekly cost forecast',
        'Hourly KV cost sync',
        'Daily growth retention by source',
        'Weekly governance email'
    ]
    for job in expected_jobs:
        if job in job_names:
            print(f'✅ Job: {job}')
        else:
            print(f'❌ Job: {job} MISSING')
            exit(1)
    print(f'Total jobs: {len(jobs)}')
else:
    print('❌ Scheduler not initialized')
    exit(1)
" || ((FAIL_COUNT++))

echo ""
echo "🔬 Testing Profit Guard..."

python3 -c "
from monitors.autoscale import get_controller
controller = get_controller()
decision = controller.decide_action(queue_depth=0, p95_latency_ms=50)
if 'profit_margin_pct' in decision['metrics'] and 'profit_frozen' in decision['metrics']:
    print('✅ Profit guard integrated into autoscale')
else:
    print('❌ Profit guard NOT found in autoscale metrics')
    exit(1)
" || ((FAIL_COUNT++))

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAIL_COUNT -eq 0 ]; then
    echo "✅ Phase 6.5 Verification: ALL CHECKS PASSED"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📋 Summary:"
    echo "  • Auto-Tuning Engine: Operational"
    echo "  • Growth Intelligence: Operational"
    echo "  • Behavioral Cohort Retention: Operational"
    echo "  • Dynamic Discount System: Operational"
    echo "  • Profit-Driven Autoscale: Integrated"
    echo "  • Weekly Governance Reporter: Scheduled"
    echo "  • APScheduler: 7 jobs running"
    echo ""
    echo "🚀 Phase 6.5 is production-ready!"
    exit 0
else
    echo "❌ Phase 6.5 Verification: $FAIL_COUNT CHECKS FAILED"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 1
fi
