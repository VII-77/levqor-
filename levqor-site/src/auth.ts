import NextAuth, { NextAuthConfig } from "next-auth"
import Resend from "next-auth/providers/resend"
import Google from "next-auth/providers/google"
import AzureAD from "next-auth/providers/azure-ad"

const DENYLIST = ['mailinator.com', 'tempmail.com', 'guerrillamail.com', 'temp-mail.org'];

async function sendAuditEvent(event: string, email: string, userAgent?: string, ip?: string) {
  try {
    await fetch('https://api.levqor.ai/audit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        event,
        email,
        user_agent: userAgent,
        ip,
        ts: Date.now()
      })
    }).catch(() => {});
  } catch (err) {
    // Fire-and-forget
  }
}

export const authOptions: NextAuthConfig = {
  providers: [
    Resend({
      apiKey: process.env.RESEND_API_KEY,
      from: process.env.AUTH_FROM_EMAIL || "no-reply@levqor.ai",
    }),
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID || "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
      allowDangerousEmailAccountLinking: true,
    }),
    AzureAD({
      clientId: process.env.MICROSOFT_CLIENT_ID || "",
      clientSecret: process.env.MICROSOFT_CLIENT_SECRET || "",
      allowDangerousEmailAccountLinking: true,
    }),
  ],
  pages: {
    signIn: '/signin',
  },
  session: { 
    strategy: "jwt",
    maxAge: 60 * 60,
  },
  callbacks: {
    async signIn({ user, account, profile }) {
      const email = user.email || '';
      const domain = email.split('@')[1];
      
      if (DENYLIST.includes(domain)) {
        return false;
      }
      
      return true;
    },
  },
  events: {
    async signIn(message) {
      const email = message.user.email || 'unknown';
      await sendAuditEvent('sign_in', email, undefined, undefined);
    },
    async signOut(message) {
      const email = (message as any).token?.email || 'unknown';
      await sendAuditEvent('sign_out', email, undefined, undefined);
    },
  },
};

export const { handlers, signIn, signOut, auth } = NextAuth(authOptions);
