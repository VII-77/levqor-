export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">Privacy Policy</h1>
        <p className="text-gray-500 mb-12">Last updated: {new Date().toLocaleDateString()}</p>
        
        <div className="prose prose-lg max-w-none text-gray-700 space-y-8">
          <section>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Introduction</h2>
            <p>
              Levqor is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information.
            </p>
          </section>

          <section>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Information We Collect</h2>
            <ul className="list-disc list-inside space-y-2">
              <li>Email address and account information</li>
              <li>Workflow execution logs and metrics</li>
              <li>Billing and payment information</li>
              <li>System performance data</li>
            </ul>
          </section>

          <section>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Data Security</h2>
            <p>
              We implement industry-standard security measures including encryption in transit and at rest, regular security audits, and access controls.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
