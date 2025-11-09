export default function PricingPage() {
  const card = (title: string, price: string, features: string[], planKey: 'starter' | 'pro') => (
    <div className="max-w-sm rounded-2xl shadow-lg p-8 border border-gray-200 hover:shadow-xl transition">
      <h3 className="text-2xl font-semibold mb-2">{title}</h3>
      <p className="text-4xl font-bold my-4">
        £{price}
        <span className="text-lg font-normal text-gray-500">/mo</span>
      </p>
      <ul className="text-sm space-y-3 mb-6 text-gray-600">
        {features.map((f, i) => (
          <li key={i} className="flex items-start">
            <svg className="w-5 h-5 mr-2 text-green-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
            {f}
          </li>
        ))}
      </ul>
      <a
        className="block w-full text-center px-6 py-3 rounded-lg bg-black text-white font-medium hover:bg-gray-800 transition"
        href={`/api/checkout?plan=${planKey}`}
      >
        Buy now
      </a>
    </div>
  );

  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-4 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-3">Simple, Transparent Pricing</h1>
        <p className="text-gray-600">Choose the plan that fits your automation needs</p>
      </div>
      <div className="grid gap-8 md:grid-cols-2 max-w-4xl">
        {card('Starter', '19', [
          '1 project',
          'Email support',
          'Basic insights',
          '100 workflow runs/month'
        ], 'starter')}
        {card('Pro', '49', [
          'Unlimited projects',
          'Priority support',
          'Advanced insights + runbooks',
          '1,000 workflow runs/month'
        ], 'pro')}
      </div>
      <p className="text-sm text-gray-500 mt-8">
        Need enterprise? <a href="/contact" className="underline hover:text-gray-700">Contact us</a>
      </p>
    </main>
  );
}
