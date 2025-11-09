import Link from "next/link"

export default function ThanksPage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center text-center space-y-6 px-4">
      <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
        <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
        </svg>
      </div>
      <h1 className="text-4xl font-bold">Thank you for subscribing!</h1>
      <p className="max-w-md text-gray-600">
        Your subscription is now active. Check your email for login details and next steps.
      </p>
      <Link href="/dashboard" className="px-6 py-3 bg-black text-white rounded-lg hover:bg-gray-800 transition">
        Go to Dashboard
      </Link>
    </main>
  )
}
