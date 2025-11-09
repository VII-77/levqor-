import Link from "next/link"

export default function Pricing() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center text-center space-y-8 px-4">
      <h1 className="text-4xl font-bold">Pricing</h1>
      <div className="border rounded-xl p-8 w-80 shadow-lg bg-white">
        <h2 className="text-2xl font-semibold">Pro Plan</h2>
        <p className="text-gray-600 mt-2">£19/month • Cancel anytime</p>
        <p className="mt-4 text-sm text-gray-500">Access to all automation features and AI tools.</p>
        <a href="https://buy.stripe.com/" className="mt-6 inline-block bg-black text-white px-5 py-3 rounded-lg hover:bg-gray-800 transition">
          Subscribe
        </a>
      </div>
      <p className="text-sm text-gray-400 mt-6">
        Need a custom setup? <Link href="/contact" className="underline hover:text-gray-600">Contact us</Link>
      </p>
    </main>
  )
}
