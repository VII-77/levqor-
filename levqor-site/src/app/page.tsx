import Link from "next/link"

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center text-center space-y-6 px-4">
      <h1 className="text-5xl font-bold">Automate Smarter with Levqor</h1>
      <p className="max-w-xl text-gray-500">
        AI-powered automation for modern businesses. Start free, scale fast.
      </p>
      <div className="flex space-x-4">
        <Link href="/pricing" className="px-6 py-3 bg-black text-white rounded-lg hover:bg-gray-800 transition">
          View Plans
        </Link>
        <Link href="/contact" className="px-6 py-3 border border-black rounded-lg hover:bg-gray-50 transition">
          Contact Us
        </Link>
      </div>
    </main>
  )
}
