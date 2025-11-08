export default function Testimonials() {
  const testimonials = [
    {
      quote: "Levqor cut our manual workflow time by 80%. It's like having an extra team member working 24/7.",
      author: "Sarah Chen",
      role: "Head of Operations, TechStart"
    },
    {
      quote: "The AI-driven automation is incredible. It learns from our patterns and optimizes itself.",
      author: "Marcus Rodriguez",
      role: "CTO, InnoVentures"
    },
    {
      quote: "Best investment we made this year. ROI was positive within the first month.",
      author: "Emily Watson",
      role: "CEO, CloudBase"
    }
  ];

  return (
    <section className="py-20 bg-gradient-to-br from-blue-50 to-indigo-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">
          Loved by Teams Worldwide
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((item, i) => (
            <div key={i} className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition">
              <div className="flex gap-1 mb-4">
                {[...Array(5)].map((_, i) => (
                  <svg key={i} className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              <p className="text-gray-700 mb-4 italic">&ldquo;{item.quote}&rdquo;</p>
              <div>
                <p className="font-semibold text-gray-900">{item.author}</p>
                <p className="text-sm text-gray-500">{item.role}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
