"use client";
import { useState } from "react";

type Term = "monthly" | "yearly";
type Tier = "free" | "starter" | "pro" | "business";

const plans = {
  free: {
    monthly: 0,
    yearly: 0,
    workflows: 2,
    runs: "200",
    speed: "Standard",
    users: 1,
    connectors: "Core only",
    aiCredits: "200",
    support: "Community",
    features: ["2 workflows", "200 runs/mo", "1 user", "Core connectors", "200 AI credits", "Community support"]
  },
  starter: {
    monthly: 19,
    yearly: 190,
    workflows: 10,
    runs: "5,000",
    speed: "Fast",
    users: 1,
    connectors: "Core + Beta",
    aiCredits: "2,500",
    support: "Email",
    features: ["10 workflows", "5,000 runs/mo", "1 user", "Core + Beta connectors", "2,500 AI credits", "Email support"]
  },
  pro: {
    monthly: 49,
    yearly: 490,
    workflows: 50,
    runs: "25,000",
    speed: "Faster",
    users: 3,
    connectors: "All (incl. Beta)",
    aiCredits: "10,000",
    support: "Priority",
    trial: true,
    features: ["50 workflows", "25,000 runs/mo", "3 users", "All connectors", "10,000 AI credits", "Priority support", "7-day free trial"]
  },
  business: {
    monthly: 149,
    yearly: 1490,
    workflows: 200,
    runs: "100,000",
    speed: "Fastest",
    users: 10,
    connectors: "All + SSO",
    aiCredits: "40,000",
    support: "4-hr SLA",
    trial: true,
    features: ["200 workflows", "100,000 runs/mo", "10 users", "All connectors + SSO", "40,000 AI credits", "4-hour SLA", "7-day free trial"]
  }
};

const availableConnectors = ["Gmail", "Google Sheets", "Slack", "Discord", "Notion", "Webhooks", "Stripe"];
const comingSoonConnectors = [
  { name: "Salesforce", eta: "Q4 2025" },
  { name: "HubSpot", eta: "Q4 2025" },
  { name: "Shopify", eta: "Q1 2026" },
  { name: "Xero", eta: "Q1 2026" },
  { name: "QuickBooks", eta: "Q1 2026" },
  { name: "Zendesk", eta: "Q1 2026" },
  { name: "MS Teams", eta: "Q1 2026" }
];

function Card({
  tier, title, price, per, features, badge, trial, term
}: { tier: Tier; title: string; price: number; per: string; features: string[]; badge?: string; trial?: boolean; term: Term }) {
  
  const handleClick = async () => {
    if (tier === "free") {
      window.location.href = "/dashboard";
      return;
    }
    
    try {
      const response = await fetch("/api/checkout", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ plan: tier, term })
      });
      const data = await response.json();
      if (data.url) {
        window.location.href = data.url;
      }
    } catch (err) {
      console.error("Checkout error:", err);
    }
  };

  return (
    <div className="rounded-2xl border p-6 shadow grid gap-4 bg-white hover:shadow-lg transition-shadow">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold">{title}</h3>
        {badge && <span className="text-xs rounded-full px-3 py-1 bg-black text-white font-medium">{badge}</span>}
      </div>
      <div className="text-3xl font-bold">
        £{price}
        <span className="text-base font-normal text-gray-600">/{per}</span>
      </div>
      {trial && <div className="text-sm text-green-600 font-medium">✓ 7-day free trial</div>}
      <ul className="text-sm space-y-2 flex-1">
        {features.map((f, i) => (
          <li key={i} className="flex items-start gap-2">
            <span className="text-green-600">✓</span>
            <span>{f}</span>
          </li>
        ))}
      </ul>
      <button
        onClick={handleClick}
        className="rounded-xl border border-black bg-black text-white px-4 py-2 hover:bg-gray-800 transition-colors font-medium"
      >
        {tier === "free" ? "Start for Free" : trial ? "Start 7-Day Trial" : "Upgrade"}
      </button>
    </div>
  );
}

function NotifyModal({ connector, eta, onClose }: { connector: string; eta: string; onClose: () => void }) {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await fetch("/api/notify-coming-soon", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ email, connector })
      });
      setSubmitted(true);
      setTimeout(() => onClose(), 2000);
    } catch (err) {
      console.error("Notify error:", err);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-white rounded-2xl p-6 max-w-md w-full mx-4" onClick={(e) => e.stopPropagation()}>
        {submitted ? (
          <div className="text-center py-4">
            <div className="text-4xl mb-3">✓</div>
            <p className="font-medium">Thanks! We'll notify you when {connector} is ready.</p>
          </div>
        ) : (
          <>
            <h3 className="text-xl font-semibold mb-2">Notify me: {connector}</h3>
            <p className="text-sm text-gray-600 mb-4">Expected: {eta}</p>
            <form onSubmit={handleSubmit} className="space-y-4">
              <input
                type="email"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-4 py-2 border rounded-xl focus:outline-none focus:ring-2 focus:ring-black"
              />
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={onClose}
                  className="flex-1 px-4 py-2 border rounded-xl hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-black text-white rounded-xl hover:bg-gray-800"
                >
                  Notify Me
                </button>
              </div>
            </form>
          </>
        )}
      </div>
    </div>
  );
}

export default function PricingPage() {
  const [term, setTerm] = useState<Term>("monthly");
  const [notifyModal, setNotifyModal] = useState<{ connector: string; eta: string } | null>(null);

  return (
    <main className="mx-auto max-w-6xl p-6">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-3">Simple, transparent pricing</h1>
        <p className="text-gray-600">Choose the plan that fits your automation needs</p>
      </div>

      {/* Monthly/Yearly Toggle */}
      <div className="flex items-center justify-center gap-3 mb-8">
        <button
          className={"px-6 py-2 rounded-xl border font-medium transition-colors " + (term === "monthly" ? "bg-black text-white" : "hover:bg-gray-50")}
          onClick={() => setTerm("monthly")}
        >
          Monthly
        </button>
        <button
          className={"px-6 py-2 rounded-xl border font-medium transition-colors " + (term === "yearly" ? "bg-black text-white" : "hover:bg-gray-50")}
          onClick={() => setTerm("yearly")}
        >
          Yearly
        </button>
        {term === "yearly" && (
          <span className="text-sm text-green-600 font-medium bg-green-50 px-3 py-1 rounded-full">
            Save 2 months
          </span>
        )}
      </div>

      {/* Pricing Cards */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-12">
        <Card
          tier="free"
          title="Free"
          price={0}
          per={term === "yearly" ? "yr" : "mo"}
          features={plans.free.features}
          term={term}
        />
        <Card
          tier="starter"
          title="Starter"
          price={term === "yearly" ? plans.starter.yearly : plans.starter.monthly}
          per={term === "yearly" ? "yr" : "mo"}
          features={plans.starter.features}
          term={term}
        />
        <Card
          tier="pro"
          title="Pro"
          price={term === "yearly" ? plans.pro.yearly : plans.pro.monthly}
          per={term === "yearly" ? "yr" : "mo"}
          features={plans.pro.features}
          badge="Most Popular"
          trial={plans.pro.trial}
          term={term}
        />
        <Card
          tier="business"
          title="Business"
          price={term === "yearly" ? plans.business.yearly : plans.business.monthly}
          per={term === "yearly" ? "yr" : "mo"}
          features={plans.business.features}
          badge="Best Value"
          trial={plans.business.trial}
          term={term}
        />
      </div>

      {/* Feature Comparison Table */}
      <div className="mb-12 overflow-x-auto">
        <h2 className="text-2xl font-bold mb-6 text-center">Compare Plans</h2>
        <table className="w-full border-collapse bg-white rounded-2xl overflow-hidden shadow">
          <thead className="bg-gray-50">
            <tr>
              <th className="text-left p-4 font-semibold">Feature</th>
              <th className="text-center p-4 font-semibold">Free</th>
              <th className="text-center p-4 font-semibold">Starter</th>
              <th className="text-center p-4 font-semibold">Pro</th>
              <th className="text-center p-4 font-semibold">Business</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            <tr>
              <td className="p-4">Workflows</td>
              <td className="text-center p-4">{plans.free.workflows}</td>
              <td className="text-center p-4">{plans.starter.workflows}</td>
              <td className="text-center p-4">{plans.pro.workflows}</td>
              <td className="text-center p-4">{plans.business.workflows}</td>
            </tr>
            <tr className="bg-gray-50">
              <td className="p-4">Runs per month</td>
              <td className="text-center p-4">{plans.free.runs}</td>
              <td className="text-center p-4">{plans.starter.runs}</td>
              <td className="text-center p-4">{plans.pro.runs}</td>
              <td className="text-center p-4">{plans.business.runs}</td>
            </tr>
            <tr>
              <td className="p-4">Speed</td>
              <td className="text-center p-4">{plans.free.speed}</td>
              <td className="text-center p-4">{plans.starter.speed}</td>
              <td className="text-center p-4">{plans.pro.speed}</td>
              <td className="text-center p-4">{plans.business.speed}</td>
            </tr>
            <tr className="bg-gray-50">
              <td className="p-4">Users</td>
              <td className="text-center p-4">{plans.free.users}</td>
              <td className="text-center p-4">{plans.starter.users}</td>
              <td className="text-center p-4">{plans.pro.users}</td>
              <td className="text-center p-4">{plans.business.users}</td>
            </tr>
            <tr>
              <td className="p-4">Connectors</td>
              <td className="text-center p-4 text-sm">{plans.free.connectors}</td>
              <td className="text-center p-4 text-sm">{plans.starter.connectors}</td>
              <td className="text-center p-4 text-sm">{plans.pro.connectors}</td>
              <td className="text-center p-4 text-sm">{plans.business.connectors}</td>
            </tr>
            <tr className="bg-gray-50">
              <td className="p-4">AI Credits</td>
              <td className="text-center p-4">{plans.free.aiCredits}</td>
              <td className="text-center p-4">{plans.starter.aiCredits}</td>
              <td className="text-center p-4">{plans.pro.aiCredits}</td>
              <td className="text-center p-4">{plans.business.aiCredits}</td>
            </tr>
            <tr>
              <td className="p-4">Support</td>
              <td className="text-center p-4">{plans.free.support}</td>
              <td className="text-center p-4">{plans.starter.support}</td>
              <td className="text-center p-4">{plans.pro.support}</td>
              <td className="text-center p-4">{plans.business.support}</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Connectors Section */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6 text-center">Connectors</h2>
        <div className="bg-white rounded-2xl p-6 shadow mb-6">
          <h3 className="font-semibold mb-3 text-green-600">✓ Available Now</h3>
          <div className="flex flex-wrap gap-2">
            {availableConnectors.map((c) => (
              <span key={c} className="px-3 py-1 bg-green-50 text-green-700 rounded-full text-sm font-medium">
                {c}
              </span>
            ))}
          </div>
        </div>
        <div className="bg-white rounded-2xl p-6 shadow">
          <h3 className="font-semibold mb-3 text-orange-600">⏳ Coming Soon</h3>
          <div className="flex flex-wrap gap-2">
            {comingSoonConnectors.map((c) => (
              <button
                key={c.name}
                onClick={() => setNotifyModal(c)}
                className="px-3 py-1 bg-orange-50 text-orange-700 rounded-full text-sm font-medium hover:bg-orange-100 transition-colors"
              >
                {c.name} • {c.eta}
              </button>
            ))}
          </div>
          <p className="text-sm text-gray-600 mt-3">Click any connector to get notified when it's ready</p>
        </div>
      </div>

      {/* Trust Strip */}
      <div className="bg-blue-50 rounded-2xl p-6 mb-12 text-center">
        <div className="flex flex-wrap justify-center gap-6 text-sm">
          <div className="flex items-center gap-2">
            <span className="text-blue-600">✓</span>
            <span>Cancel anytime, prorated</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-blue-600">✓</span>
            <span>7-day trial on Pro & Business</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-blue-600">✓</span>
            <span>GDPR compliant</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-blue-600">✓</span>
            <span>Encryption at rest</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-blue-600">✓</span>
            <span>SLA on Business plan</span>
          </div>
        </div>
      </div>

      {/* FAQ */}
      <div className="border-t pt-8">
        <h2 className="text-2xl font-bold mb-6 text-center">Frequently Asked Questions</h2>
        <div className="space-y-4 max-w-3xl mx-auto">
          <details className="bg-white rounded-xl p-4 shadow">
            <summary className="cursor-pointer font-medium">What happens after the trial?</summary>
            <p className="mt-2 text-sm text-gray-600">
              Pro and Business plans include a 7-day free trial. You won't be charged until the trial ends. Cancel anytime during the trial with no charge.
            </p>
          </details>
          <details className="bg-white rounded-xl p-4 shadow">
            <summary className="cursor-pointer font-medium">Can I switch plans later?</summary>
            <p className="mt-2 text-sm text-gray-600">
              Yes! You can upgrade or downgrade at any time. Changes are prorated automatically.
            </p>
          </details>
          <details className="bg-white rounded-xl p-4 shadow">
            <summary className="cursor-pointer font-medium">Do you offer refunds?</summary>
            <p className="mt-2 text-sm text-gray-600">
              We offer a 7-day refund window for first-time purchases if you're not satisfied.
            </p>
          </details>
          <details className="bg-white rounded-xl p-4 shadow">
            <summary className="cursor-pointer font-medium">How do invoices work?</summary>
            <p className="mt-2 text-sm text-gray-600">
              Stripe automatically sends invoices to your email after each payment. You can access all past invoices in your billing portal.
            </p>
          </details>
          <details className="bg-white rounded-xl p-4 shadow">
            <summary className="cursor-pointer font-medium">What are add-ons?</summary>
            <p className="mt-2 text-sm text-gray-600">
              Add-ons let you extend your plan: Extra Runs Pack (+25k runs, £29), AI Credits Pack (+10k tokens, £9), Priority SLA for Pro (+£39). Contact us to add them to your subscription.
            </p>
          </details>
        </div>
      </div>

      {/* Notify Modal */}
      {notifyModal && (
        <NotifyModal
          connector={notifyModal.connector}
          eta={notifyModal.eta}
          onClose={() => setNotifyModal(null)}
        />
      )}

      {/* VAT Notice */}
      <div className="mt-8 text-xs text-center text-gray-500">
        <p>Prices exclude VAT where applicable. VAT is calculated automatically at checkout.</p>
        <p className="mt-1">Have a promo code? Enter it on the Stripe checkout page.</p>
      </div>
    </main>
  );
}
