import TrustSection from '@/components/TrustSection';

export default function PricingPage() {
  const plans = [
    {
      name: 'Starter',
      price: '$29',
      period: '/month',
      features: ['100 workflow runs/month', 'Basic integrations', 'Email support', '1 team member'],
      cta: 'Start Free Trial'
    },
    {
      name: 'Professional',
      price: '$99',
      period: '/month',
      features: ['1,000 workflow runs/month', 'All integrations', 'Priority support', '5 team members', 'Advanced analytics'],
      cta: 'Start Free Trial',
      featured: true
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      period: '',
      features: ['Unlimited workflow runs', 'Custom integrations', '24/7 dedicated support', 'Unlimited team members', 'SLA & compliance'],
      cta: 'Contact Sales'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Simple, Transparent Pricing
          </h1>
          <p className="text-xl text-gray-600 mb-16">
            Choose the plan that fits your automation needs
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto mb-20">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`rounded-2xl p-8 ${
                plan.featured
                  ? 'bg-blue-600 text-white shadow-2xl scale-105'
                  : 'bg-white text-gray-900 shadow-lg'
              }`}
            >
              {plan.featured && (
                <div className="bg-blue-500 text-white text-sm font-bold px-3 py-1 rounded-full inline-block mb-4">
                  MOST POPULAR
                </div>
              )}
              <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
              <div className="mb-6">
                <span className="text-4xl font-bold">{plan.price}</span>
                <span className={plan.featured ? 'text-blue-100' : 'text-gray-500'}>
                  {plan.period}
                </span>
              </div>
              <ul className="space-y-4 mb-8">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start">
                    <svg
                      className={`w-5 h-5 mr-3 mt-0.5 flex-shrink-0 ${
                        plan.featured ? 'text-blue-200' : 'text-blue-600'
                      }`}
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
              <a
                href="/signin"
                className={`block w-full text-center py-3 px-6 rounded-lg font-semibold transition ${
                  plan.featured
                    ? 'bg-white text-blue-600 hover:bg-gray-100'
                    : 'bg-blue-600 text-white hover:bg-blue-700'
                }`}
              >
                {plan.cta}
              </a>
            </div>
          ))}
        </div>
      </div>
      
      <TrustSection />
    </div>
  );
}
