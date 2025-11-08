export default function DocsPage() {
  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <h1 className="text-5xl font-bold text-gray-900 mb-8">Documentation</h1>
        
        <div className="prose prose-lg max-w-none">
          <section className="mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Getting Started</h2>
            <p className="text-gray-600 mb-4">
              Welcome to Levqor! This guide will help you get started with building powerful automation workflows.
            </p>
            
            <h3 className="text-2xl font-bold text-gray-900 mt-8 mb-3">Quick Start</h3>
            <ol className="list-decimal list-inside space-y-2 text-gray-700">
              <li>Sign up for a free account</li>
              <li>Connect your first integration</li>
              <li>Create your first workflow</li>
              <li>Test and deploy</li>
            </ol>
          </section>

          <section className="mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">API Reference</h2>
            <p className="text-gray-600 mb-4">
              Integrate Levqor into your applications using our REST API.
            </p>
            
            <div className="bg-gray-50 rounded-lg p-6 mb-4">
              <h4 className="font-mono text-sm font-bold text-gray-900 mb-2">Base URL</h4>
              <code className="text-blue-600">https://api.levqor.ai/api/v1</code>
            </div>

            <h3 className="text-2xl font-bold text-gray-900 mt-8 mb-3">Authentication</h3>
            <p className="text-gray-600 mb-4">
              All API requests require an API key passed in the <code className="bg-gray-100 px-2 py-1 rounded">X-Api-Key</code> header.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
