# === LEVQOR LIVE VERIFY + REPAIR ===
set -euo pipefail
say(){ printf "\n\033[1m%s\033[0m\n" "$1"; }; ok(){ echo "✅ $1"; }; warn(){ echo "⚠️  $1"; }; fail(){ echo "❌ $1"; exit 1; }

# Vars
BACKEND_URL="${BACKEND_URL:-https://api.levqor.ai}"
FRONTEND_URL="${FRONTEND_URL:-https://levqor.ai}"
FRONTEND_DIR="${FRONTEND_DIR:-levqor-site}"
VERCEL_PROJ="${VERCEL_PROJ:-levqor}"

say "1) DNS + SSL sanity"
echo "Backend:  $BACKEND_URL"
echo "Frontend: $FRONTEND_URL"
dig +short api.levqor.ai || warn "api.levqor.ai has no DNS result"
dig +short levqor.ai     || warn "levqor.ai has no DNS result"
curl -sI "$FRONTEND_URL" | head -n1 || warn "frontend not reachable yet"
curl -sI "$BACKEND_URL/status" | head -n1 || warn "/status not reachable yet"

say "2) Backend health"
curl -fsS "$BACKEND_URL/status" | jq -e '.status=="pass"' >/dev/null && ok "/status pass" || fail "Backend /status not pass"
curl -fsS "$BACKEND_URL/ops/uptime" >/dev/null && ok "/ops/uptime ok" || warn "uptime warn"
curl -fsS "$BACKEND_URL/billing/health" >/dev/null && ok "billing ok" || warn "billing warn (check STRIPE_* secrets)"
curl -fsS "$BACKEND_URL/ops/queue_health" >/dev/null && ok "queue ok" || warn "queue warn"
curl -fsS "$BACKEND_URL/metrics" >/dev/null && ok "metrics ok" || warn "metrics warn"

say "3) Frontend → backend wiring"
cd "$FRONTEND_DIR"
# Ensure Vercel CLI
command -v vercel >/dev/null || npm i -g vercel >/dev/null 2>&1 || true
# Ensure API URL set for Vercel
if ! vercel env ls 2>/dev/null | grep -q NEXT_PUBLIC_API_URL; then
  echo "NEXT_PUBLIC_API_URL not set; adding…"
  printf "https://api.levqor.ai\n" | vercel env add NEXT_PUBLIC_API_URL production || true
fi
# Ensure .env.production fallback
grep -q '^NEXT_PUBLIC_API_URL=' .env.production 2>/dev/null || echo "NEXT_PUBLIC_API_URL=$BACKEND_URL" >> .env.production

# Minimal routes if missing
mkdir -p src/app 2>/dev/null || true
if ! ls -1 src/app 2>/dev/null | grep -E 'signin|login|dashboard' >/dev/null 2>&1; then
  say "No signin/dashboard pages. Adding placeholders."
  mkdir -p src/app/{signin,dashboard}
  cat > src/app/signin/page.tsx <<'TS'
export default function SignIn(){return(<main className="p-8"><h1>Sign in</h1><p>Placeholder auth UI.</p></main>);}
TS
  cat > src/app/dashboard/page.tsx <<'TS'
export default function Dashboard(){return(<main className="p-8"><h1>Dashboard</h1><p>Placeholder dashboard.</p></main>);}
TS
  ok "Placeholders added"
fi

say "4) Redeploy frontend"
vercel --prod --confirm --name "$VERCEL_PROJ" || warn "Vercel deploy warning (check dashboard)"

say "5) Public smoke test"
cd - >/dev/null
[ -f public_smoke.sh ] || fail "public_smoke.sh missing"
BACKEND="$BACKEND_URL" ./public_smoke.sh || fail "Smoke test failed"
ok "Smoke test passed"

say "6) Frontend route checks"
curl -fsS "$FRONTEND_URL"            >/dev/null && ok "root ok" || warn "root warn"
curl -fsS "$FRONTEND_URL/pricing"    >/dev/null && ok "/pricing ok" || warn "pricing missing"
curl -fsS "$FRONTEND_URL/signin"     >/dev/null && ok "/signin ok" || warn "signin missing"
curl -fsS "$FRONTEND_URL/dashboard"  >/dev/null && ok "/dashboard ok" || warn "dashboard missing"

say "DONE. If warnings remain: fix DNS (Cloudflare CNAME to Vercel), set Vercel env NEXT_PUBLIC_API_URL=https://api.levqor.ai, and ensure Stripe secrets on backend."