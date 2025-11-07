/**
 * Testimonials Section Component
 * Social proof and refund policy for marketing pages
 */

import React from 'react'

interface Testimonial {
  quote: string
  author: string
  role: string
  verified?: boolean
}

const testimonials: Testimonial[] = [
  {
    quote: "Levqor transformed our workflow automation. We saved 20+ hours per week!",
    author: "Sarah Chen",
    role: "Operations Manager",
    verified: true
  },
  {
    quote: "The AI-powered integrations are incredibly intuitive. Setup took minutes, not hours.",
    author: "Marcus Rodriguez",
    role: "Tech Lead",
    verified: true
  },
  {
    quote: "Best automation platform we've used. The partner program is a game-changer.",
    author: "Emily Thompson",
    role: "Verified Partner",
    verified: true
  }
]

export default function TestimonialsSection() {
  return (
    <section className="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 py-16 px-6 rounded-2xl shadow-lg">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            What our users say
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Join thousands of teams automating their workflows with Levqor
          </p>
        </div>

        {/* Testimonials Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {testimonials.map((testimonial, index) => (
            <div
              key={index}
              className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md hover:shadow-xl transition-shadow duration-300"
            >
              <div className="flex items-start mb-4">
                <svg
                  className="w-10 h-10 text-blue-500 opacity-50"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z" />
                </svg>
              </div>
              
              <p className="text-gray-700 dark:text-gray-300 mb-4 italic">
                "{testimonial.quote}"
              </p>
              
              <div className="flex items-center justify-between border-t pt-4">
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white">
                    {testimonial.author}
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {testimonial.role}
                  </p>
                </div>
                
                {testimonial.verified && (
                  <div className="flex items-center text-green-600 dark:text-green-400">
                    <svg className="w-5 h-5 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fillRule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                        clipRule="evenodd"
                      />
                    </svg>
                    <span className="text-xs font-medium">Verified</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Trust Badges & Refund Policy */}
        <div className="bg-blue-50 dark:bg-blue-900/20 border-2 border-blue-200 dark:border-blue-800 rounded-xl p-8 text-center">
          <div className="flex flex-wrap justify-center items-center gap-8 mb-6">
            {/* Trust Badge: 7-Day Refund */}
            <div className="flex items-center gap-2">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="font-semibold text-gray-800 dark:text-gray-200">
                7-Day Money-Back Guarantee
              </span>
            </div>

            {/* Trust Badge: Secure */}
            <div className="flex items-center gap-2">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <span className="font-semibold text-gray-800 dark:text-gray-200">
                Enterprise-Grade Security
              </span>
            </div>

            {/* Trust Badge: Support */}
            <div className="flex items-center gap-2">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              <span className="font-semibold text-gray-800 dark:text-gray-200">
                24/7 Customer Support
              </span>
            </div>
          </div>

          <p className="text-sm text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Try Levqor risk-free for 7 days. If you're not completely satisfied, we'll refund your 
            purchase—no questions asked. Cancel anytime with just one click.
          </p>
        </div>
      </div>
    </section>
  )
}

/**
 * USAGE:
 * 
 * In your marketing page (e.g., app/page.tsx):
 * 
 * import TestimonialsSection from '@/components/TestimonialsSection'
 * 
 * export default function HomePage() {
 *   return (
 *     <main>
 *       {/* ... other sections ... *\/}
 *       <TestimonialsSection />
 *       {/* ... more sections ... *\/}
 *     </main>
 *   )
 * }
 */
