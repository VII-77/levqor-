export default function TermsPage() {
  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">Terms of Service</h1>
        <p className="text-gray-500 mb-12">Last updated: {new Date().toLocaleDateString()}</p>
        
        <div className="prose prose-lg max-w-none text-gray-700 space-y-8">
          <section>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Agreement to Terms</h2>
            <p>
              By accessing or using Levqor, you agree to be bound by these Terms of Service.
            </p>
          </section>

          <section>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Acceptable Use</h2>
            <p>You agree not to:</p>
            <ul className="list-disc list-inside space-y-2 mt-4">
              <li>Violate any laws or regulations</li>
              <li>Infringe on intellectual property rights</li>
              <li>Attempt to gain unauthorized access to systems</li>
              <li>Exceed rate limits or abuse API endpoints</li>
            </ul>
          </section>

          <section>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Billing and Payments</h2>
            <p>
              Subscriptions are billed monthly or annually in advance. All fees are non-refundable except as required by law.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
