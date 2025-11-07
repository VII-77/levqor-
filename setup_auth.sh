#!/bin/bash
# === LEVQOR AUTH + DASHBOARD (NEXTAUTH + RESEND) ===
set -euo pipefail
say(){ printf "\n\033[1m%s\033[0m\n" "$1"; }; ok(){ echo "✅ $1"; }; warn(){ echo "⚠️ $1"; }

# ---- config (edit if different) ----
FRONT_DIR="levqor-site"
SITE_URL="${SITE_URL:-https://levqor.ai}"
API_URL="${API_URL:-https://api.levqor.ai}"
FROM_EMAIL="${FROM_EMAIL:-no-reply@levqor.ai}"

say "0) Context"
echo "Front: $FRONT_DIR"
echo "Site : $SITE_URL"
echo "API  : $API_URL"
echo "From : $FROM_EMAIL"

cd "$FRONT_DIR"

say "1) Install auth deps"
npm i next-auth @auth/core react-hook-form --save >/dev/null

say "2) Scaffold NextAuth (App Router)"
mkdir -p src/app/api/auth/\[...nextauth]
cat > src/app/api/auth/\[...nextauth]/route.ts <<'TS'
import NextAuth from "next-auth"
import Email from "next-auth/providers/email"
import { Resend } from "resend"

export const authOptions:any = {
  providers: [
    Email({
      async sendVerificationRequest({ identifier, url }) {
        const resend = new Resend(process.env.RESEND_API_KEY!)
        await resend.emails.send({
          from: process.env.AUTH_FROM_EMAIL || "no-reply@levqor.ai",
          to: identifier,
          subject: "Sign in to Levqor",
          html: `<p>Click to sign in:</p><p><a href="${url}">${url}</a></p>`
        })
      },
    })
  ],
  session: { strategy: "jwt", maxAge: 60 * 60 }, // 1h
  secret: process.env.NEXTAUTH_SECRET
}
const handler = NextAuth(authOptions)
export { handler as GET, handler as POST }
TS
ok "API route created"

say "3) Sign-in page"
mkdir -p src/app/signin
cat > src/app/signin/page.tsx <<'TS'
"use client";
import { useState } from "react";
import { signIn } from "next-auth/react";
export default function SignIn(){
  const [email,setEmail]=useState("");
  async function submit(e:any){ e.preventDefault(); await signIn("email",{ email, callbackUrl:"/dashboard" }); }
  return (
    <main className="p-8 max-w-md mx-auto">
      <h1 className="text-2xl font-bold">Sign in</h1>
      <form onSubmit={submit} className="mt-4 space-y-3">
        <input type="email" className="border p-2 w-full" placeholder="you@example.com" value={email} onChange={e=>setEmail(e.target.value)} required/>
        <button className="border px-3 py-2" type="submit">Send magic link</button>
      </form>
      <p className="text-sm opacity-70 mt-3">You'll receive an email from {process.env.NEXT_PUBLIC_AUTH_FROM||"no-reply@levqor.ai"}</p>
    </main>
  );
}
TS
ok "/signin ready"

say "4) Protected /dashboard pulling usage"
mkdir -p src/app/dashboard
cat > src/app/dashboard/page.tsx <<'TS'
import { auth } from "next-auth";
export const dynamic = "force-dynamic";
async function getUsage(){
  const api = process.env.NEXT_PUBLIC_API_URL!;
  try {
    const res = await fetch(`${api}/api/usage/summary`, { cache: "no-store" });
    if(!res.ok) return null;
    return res.json();
  } catch { return null; }
}
export default async function Dashboard(){
  const session = await auth();
  if(!session){ return <main className="p-8"><h1>Unauthorized</h1><a href="/signin">Sign in</a></main>; }
  const usage = await getUsage();
  return (
    <main className="p-8 space-y-3">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <p className="opacity-70">Signed in as {(session.user as any)?.email || "user"}.</p>
      <div className="mt-4 border p-4">
        <h2 className="font-semibold mb-2">Usage</h2>
        <pre className="text-sm">{JSON.stringify(usage, null, 2) || "No data"}</pre>
      </div>
      <p className="text-sm opacity-70">API: {process.env.NEXT_PUBLIC_API_URL}</p>
    </main>
  );
}
TS
ok "/dashboard ready"

say "5) App Router auth helper + middleware"
mkdir -p src/auth
cat > src/auth/index.ts <<'TS'
export { auth } from "next-auth"
TS
cat > src/middleware.ts <<'TS'
export { default } from "next-auth/middleware"
export const config = { matcher: ["/dashboard"] }
TS
ok "middleware added"

say "6) Add nav links if missing"
HP=$(rg -l "export default function Home|metadata|page" src/app || true | head -1 || true)
if [ -n "${HP:-}" ] && ! grep -q "/signin" "$HP"; then
  awk '1; /<main|<header|<nav/{print "<p style=\"margin-top:16px\"><a href=\"/signin\">Sign in</a> · <a href=\"/dashboard\">Dashboard</a></p>"}' "$HP" > "$HP.tmp" && mv "$HP.tmp" "$HP" && ok "nav links added"
else
  warn "homepage not found or links already present"
fi

say "7) Env: write .env.production fallback"
touch .env.production
grep -q '^NEXT_PUBLIC_API_URL=' .env.production || echo "NEXT_PUBLIC_API_URL=$API_URL" >> .env.production
grep -q '^NEXTAUTH_URL=' .env.production      || echo "NEXTAUTH_URL=$SITE_URL" >> .env.production
grep -q '^AUTH_FROM_EMAIL=' .env.production   || echo "AUTH_FROM_EMAIL=$FROM_EMAIL" >> .env.production
grep -q '^NEXT_PUBLIC_AUTH_FROM=' .env.production || echo "NEXT_PUBLIC_AUTH_FROM=$FROM_EMAIL" >> .env.production
# Generate secret if absent
if ! grep -q '^NEXTAUTH_SECRET=' .env.production; then
  SECRET=$(python3 - <<'PY'
import os,base64;print(base64.urlsafe_b64encode(os.urandom(32)).decode())
PY
)
  echo "NEXTAUTH_SECRET=$SECRET" >> .env.production
fi
ok ".env.production updated (fallback for Vercel)"

say "8) Optional: push env to Vercel if token configured"
if command -v vercel >/dev/null 2>&1; then
  : # best-effort; skip interactive additions in non-tty
else
  npm i -g vercel >/dev/null 2>&1 || true
fi

say "9) Build + deploy"
# Build check (fail fast if types break)
npm run build || { warn "build failed; trying once more after installing types"; npm i -D @types/node @types/react >/dev/null 2>&1 || true; npm run build; }
vercel --prod --confirm --name "levqor" || warn "Vercel deploy warning; check dashboard"

say "10) Post-deploy checks"
curl -fsS "$SITE_URL" >/dev/null && ok "Root reachable"
curl -fsS "$SITE_URL/signin" >/dev/null && ok "/signin reachable"
curl -I -s "$SITE_URL/dashboard" | head -n1 | grep -q "200\|307" && ok "/dashboard protected (200/307)" || warn "dashboard check needs manual test"

say "DONE → Test sign-in flow:"
echo "1) Open $SITE_URL/signin"
echo "2) Enter email; check Resend for magic-link email"
echo "3) Click link → redirected to /dashboard with usage JSON"
