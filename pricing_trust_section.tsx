export default function TrustSection() {
  return (
    <section className="mt-12 text-center text-sm text-gray-600">
      <p>💳 Secure payments via Stripe • 🔒 7-day refund guarantee • ⭐ Trusted by early adopters</p>
      <details className="mt-2">
        <summary className="cursor-pointer hover:text-gray-900 font-medium">
          Frequently Asked Questions
        </summary>
        <ul className="list-disc text-left mx-auto max-w-md mt-4 space-y-2 text-gray-700">
          <li>Cancel anytime directly from your dashboard.</li>
          <li>Free plan includes 50 credits to explore features.</li>
          <li>Refunds processed within 7 days—no questions asked.</li>
          <li>All plans include 20 external service connectors.</li>
          <li>Partner program: Earn 20% commission on referrals.</li>
        </ul>
      </details>
    </section>
  );
}
