import NextAuth from "next-auth"
import Resend from "next-auth/providers/resend"

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Resend({
      apiKey: process.env.RESEND_API_KEY,
      from: process.env.AUTH_FROM_EMAIL || "no-reply@levqor.ai",
    }),
  ],
  pages: {
    signIn: '/signin',
  },
  session: { 
    strategy: "jwt",
    maxAge: 60 * 60,
  },
})
