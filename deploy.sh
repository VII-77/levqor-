set -e

echo "1) Create performance indexes…"
cat > db/indexes.sql <<'SQL'
CREATE INDEX IF NOT EXISTS ix_users_email          ON users(email);
CREATE INDEX IF NOT EXISTS ix_supp_hash            ON suppression(hash);
CREATE INDEX IF NOT EXISTS ix_conv_user_created    ON partner_conversions(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS ix_conv_code_created    ON partner_conversions(partner_code, created_at DESC);
SQL

if [ -n "$DATABASE_URL" ]; then
  echo "Detected Postgres. Applying indexes…"
  psql "$DATABASE_URL" -f db/indexes.sql >/dev/null
else
  echo "Applying indexes to SQLite…"
  sqlite3 levqor.db < db/indexes.sql
  sqlite3 levqor.db "VACUUM; ANALYZE;"
fi
echo "✓ Indexes applied"

echo "2) Tighten SLO and enable spend guard…"
export SLO_LATENCY_MS=150
export DAILY_SPEND_LIMIT=${DAILY_SPEND_LIMIT:-50}
echo "SLO_LATENCY_MS=$SLO_LATENCY_MS  DAILY_SPEND_LIMIT=$DAILY_SPEND_LIMIT"

echo "3) Light caching for safe endpoints (runtime env only)…"
export SAFE_CACHE_TTL=60

echo "4) Quick health checks…"
bash verify_v6_0.sh
bash verify_v5_3.sh
bash verify_v5_2.sh

echo "5) Run guards…"
python3 monitors/slo_watchdog.py || true
python3 monitors/spend_guard.py  || true

echo "6) Backup with checksum (optional but recommended)…"
bash scripts/backup_cycle.sh || true

echo "----------------------------------------------"
echo "ALL SET. READY TO DEPLOY."
echo "Next: Click the Replit “Deploy” button."
echo "Post-deploy: open /status and /ops/uptime."
echo "----------------------------------------------"
