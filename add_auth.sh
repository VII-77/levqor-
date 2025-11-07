# === ADD AUTH (NEXTAUTH + RESEND MAGIC LINK) ===
set -euo pipefail
FRONT=levqor-site
cd "$FRONT"

# 0) Ensure deps
npm i next-auth @auth/core @auth/prisma-adapter react-hook-form --save
# If you don't use Prisma, we’ll go email-only (no DB)

# 1) Env vars for Vercel (you must paste values when prompted)
vercel env add NEXTAUTH_URL production   # https://levqor.ai
vercel env add NEXTAUTH_SECRET production # openssl rand -hex 32
vercel env add RESEND_API_KEY production  # re_xxx
vercel env add NEXT_PUBLIC_API_URL production  # https://api.levqor.ai

# 2) App Router auth routes
mkdir -p src/app/api/auth/[...nextauth]
cat > src/app/api/auth/[...nextauth]/route.ts <<'TS'
import NextAuth from "next-auth"
import Email from "next-auth/providers/email"
import { Resend } from "resend"

export const authOptions = {
  providers: [
    Email({
      sendVerificationRequest: async ({ identifier, url }) => {
        const resend = new Resend(process.env.RESEND_API_KEY!)
        await resend.emails.send({
          from: "no-reply@levqor.ai",
          to: identifier,
          subject: "Sign in to Levqor",
          html: `<p>Click to sign in: <a href="${url}">${url}</a></p>`
        })
      }
    })
  ],
  session: { strategy: "jwt", maxAge: 60 * 60 }, // 1h
  secret: process.env.NEXTAUTH_SECRET
}
const handler = NextAuth(authOptions as any)
export { handler as GET, handler as POST }
TS

# 3) Sign-in page
mkdir -p src/app/signin
cat > src/app/signin/page.tsx <<'TS'
"use client";
import { signIn } from "next-auth/react"
import { useState } from "react"

export default function SignIn() {
  const [email, setEmail] = useState("")
  async function submit(e:any){ e.preventDefault(); await signIn("email",{ email, callbackUrl:"/dashboard" }) }
  return (
    <main className="p-8 max-w-md mx-auto">
      <h1 className="text-2xl font-bold">Sign in</h1>
      <form onSubmit={submit} className="mt-4 space-y-3">
        <input className="border p-2 w-full" type="email" placeholder="you@example.com" value={email} onChange={e=>setEmail(e.target.value)} required/>
        <button className="border px-3 py-2" type="submit">Send magic link</button>
      </form>
      <p className="text-sm opacity-70 mt-3">You’ll receive an email from no-reply@levqor.ai</p>
    </main>
  )
}
TS

# 4) Protected dashboard
mkdir -p src/app/dashboard
cat > src/app/dashboard/page.tsx <<'TS'
import { auth } from "next-auth"
export const dynamic = "force-dynamic";
export default async function Dashboard(){
  const session = await auth()
  if(!session) { return <main className="p-8"><h1>Unauthorized</h1><a href="/signin">Sign in</a></main> }
  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <p>Welcome, {(session.user as any)?.email || "user"}.</p>
      <p className="opacity-70">API: {process.env.NEXT_PUBLIC_API_URL}</p>
    </main>
  )
}
TS

# 5) NextAuth helper for App Router
mkdir -p src/auth
cat > src/auth/index.ts <<'TS'
export { auth } from "next-auth"
TS

# 6) Middleware to protect /dashboard
cat > src/middleware.ts <<'TS'
export { default } from "next-auth/middleware"
export const config = { matcher: ["/dashboard"] }
TS

# 7) Add link to navbar/home if missing
HOMEPAGE=$(rg -l "export default function Home|metadata|page" src/app || true | head -1)
[ -n "$HOMEPAGE" ] && grep -q "/signin" "$HOMEPAGE" || \
  awk '1; /<main|<header|<nav/{print "<p style=\"margin-top:16px\"><a href=\"/signin\">Sign in</a> · <a href=\"/dashboard\">Dashboard</a></p>"}' "$HOMEPAGE" > "$HOMEPAGE.tmp" && mv "$HOMEPAGE.tmp" "$HOMEPAGE"

# 8) Deploy
vercel --prod --confirm --name levqor

echo "✅ Auth deployed. Test https://levqor.ai/signin (check Resend logs for emails)."