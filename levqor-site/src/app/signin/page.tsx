"use client";
import { useState } from "react";
import { signIn } from "next-auth/react";

export default function SignIn(){
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);
  
  async function submit(e: React.FormEvent){
    e.preventDefault();
    await signIn("resend", { email, callbackUrl: "/dashboard" });
    setSubmitted(true);
  }
  
  return (
    <main className="p-8 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Sign in to Levqor</h1>
      
      {!submitted ? (
        <>
          <form onSubmit={submit} className="space-y-4">
            <div>
              <input 
                type="email" 
                className="border border-gray-300 p-3 w-full rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" 
                placeholder="you@example.com" 
                value={email} 
                onChange={e => setEmail(e.target.value)} 
                required
              />
            </div>
            <button 
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors" 
              type="submit"
            >
              Send magic link
            </button>
          </form>
          <p className="text-sm text-gray-600 mt-4">
            You'll receive an email from {process.env.NEXT_PUBLIC_AUTH_FROM || "no-reply@levqor.ai"}
          </p>
        </>
      ) : (
        <div className="text-center">
          <div className="text-4xl mb-4">📧</div>
          <h2 className="text-xl font-semibold mb-2">Check your email</h2>
          <p className="text-gray-600">A sign-in link has been sent to {email}</p>
        </div>
      )}
    </main>
  );
}
