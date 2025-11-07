# === LEVQOR LIVE TRIAGE & FIX ===
set -euo pipefail

say(){ printf "\n\033[1m%s\033[0m\n" "$1"; }
ok(){  printf "✅ %s\n" "$1"; }
warn(){ printf "⚠️  %s\n" "$1"; }
fail(){ printf "❌ %s\n" "$1"; exit 1; }

# -------- 0) Inputs --------
: "${BACKEND_URL:=https://api.levqor.ai}"   # change if needed
: "${FRONTEND_DIR:=levqor-site}"           # Next.js project directory
: "${VERCEL_PROJ:=levqor}"                 # Vercel project name

say "0) Context"
echo "Backend:  $BACKEND_URL"
echo "Frontend: $FRONTEND_DIR (Vercel proj: $VERCEL_PROJ)"

# -------- 1) Backend quick health --------
say "1) Backend health"
if ! curl -fsS "$BACKEND_URL/status" | jq -e '.status=="pass"' >/dev/null ; then
  warn "/status not pass; collecting diagnostics"
  curl -iS "$BACKEND_URL/status" || true
fi
curl -fsS "$BACKEND_URL/ops/uptime" >/dev/null && ok "uptime ok" || warn "uptime endpoint issue"
curl -fsS "$BACKEND_URL/ops/queue_health" >/dev/null && ok "queue health ok" || warn "queue health warn"
if ! curl -fsS "$BACKEND_URL/billing/health" | jq . >/dev/null ; then
  warn "billing/health failing → checking secrets locally (STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET)"
fi

# -------- 2) Backend env sanity (secrets present?) --------
say "2) Backend required secrets present?"
req=(JWT_SECRET STRIPE_SECRET_KEY STRIPE_WEBHOOK_SECRET RESEND_API_KEY)
missing=()
for k in "${req[@]}"; do
  v=$(python3 - <<PY
import os;print("SET" if os.getenv("$k") else "")
PY
)
  [ "$v" = "SET" ] && ok "$k set" || { warn "$k missing"; missing+=("$k"); }
done
[ ${#missing[@]} -eq 0 ] || echo "Missing: ${missing[*]}"

# -------- 3) Backend logs snapshot --------
say "3) Backend last 200 log lines"
tail -n 200 logs/*.log 2>/dev/null || echo "no local logs; using platform logs only"

# -------- 4) Frontend wiring check --------
say "4) Frontend → backend wiring"
cd "$FRONTEND_DIR"
if ! command -v npx >/dev/null 2>&1; then npm i -g npm@latest >/dev/null 2>&1 || true; fi
if ! grep -R "NEXT_PUBLIC_API_URL" -n . >/dev/null 2>&1 ; then
  warn "NEXT_PUBLIC_API_URL not used in codebase; creating fallback .env"
fi

# ensure .env.production has API URL
mkdir -p .; touch .env.production
if ! grep -q "NEXT_PUBLIC_API_URL=" .env.production; then
  echo "NEXT_PUBLIC_API_URL=$BACKEND_URL" >> .env.production
  ok "Set NEXT_PUBLIC_API_URL in .env.production"
else
  sed -i.bak "s|^NEXT_PUBLIC_API_URL=.*|NEXT_PUBLIC_API_URL=$BACKEND_URL|" .env.production && ok "Updated NEXT_PUBLIC_API_URL"
fi

# -------- 5) Frontend route inventory (do we even have auth UI?) --------
say "5) Frontend route inventory"
routes=$(ls -1 src/app 2>/dev/null || ls -1 app 2>/dev/null || true)
echo "$routes"
if ! ls -1 {src/,}app 2>/dev/null | grep -E '(login|signin|auth|dashboard)' >/dev/null 2>&1 ; then
  warn "No auth or dashboard routes in the frontend. This explains missing sign-in."
  echo "Creating minimal placeholder /signin and /dashboard pages..."
  mkdir -p src/app/signin src/app/dashboard 2>/dev/null || mkdir -p app/signin app/dashboard
  cat > src/app/signin/page.tsx <<'TS' 2>/dev/null || cat > app/signin/page.tsx <<'TS'
export const dynamic = "force-static";
export default function SignIn() {
  return (
    <main className="p-8 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold">Sign in</h1>
      <p className="mt-2 text-sm opacity-80">Auth UI not wired yet. This placeholder confirms routing.</p>
      <a className="mt-6 inline-block underline" href="/">← Back home</a>
    </main>
  );
}
TS
  cat > src/app/dashboard/page.tsx <<'TS' 2>/dev/null || cat > app/dashboard/page.tsx <<'TS'
export const dynamic = "force-static";
export default function Dashboard() {
  return (
    <main className="p-8 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <p className="mt-2 text-sm opacity-80">Placeholder dashboard. Backend at NEXT_PUBLIC_API_URL.</p>
      <a className="mt-6 inline-block underline" href="/">← Back home</a>
    </main>
  );
}
TS
  ok "Placeholder pages created (/signin, /dashboard)"
fi

# -------- 6) Frontend redeploy to Vercel --------
say "6) Frontend redeploy"
if ! command -v vercel >/dev/null 2>&1; then npm i -g vercel >/dev/null 2>&1; fi
vercel --prod --confirm --name "$VERCEL_PROJ" || warn "Vercel deploy returned warning; check dashboard"

# -------- 7) Public verification (frontend + backend) --------
say "7) Public verification"
cd -
[ -f public_smoke.sh ] || fail "public_smoke.sh missing in backend root"
BACKEND="$BACKEND_URL" ./public_smoke.sh || fail "Public smoke failed"
ok "Public smoke passed"

say "DONE. If auth still missing, it’s because the frontend never had real auth pages. Placeholders now exist; we can wire real auth next."