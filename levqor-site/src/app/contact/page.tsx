export default function ContactPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">Contact Us</h1>
          <p className="text-xl text-gray-600">
            We&apos;re here to help. Reach out to our team.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-12">
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Email Support</h3>
            <a href="mailto:support@levqor.ai" className="text-blue-600 hover:underline font-medium">
              support@levqor.ai
            </a>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-8">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Documentation</h3>
            <a href="/docs" className="text-blue-600 hover:underline font-medium">
              View Documentation
            </a>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-8">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Enterprise Sales</h3>
            <a href="mailto:sales@levqor.ai" className="text-blue-600 hover:underline font-medium">
              sales@levqor.ai
            </a>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-8">
            <h3 className="text-lg font-bold text-gray-900 mb-4">System Status</h3>
            <a href="https://api.levqor.ai/status" className="text-blue-600 hover:underline font-medium">
              View Status
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
