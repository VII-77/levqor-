export default function Logos() {
  const logos = ['Acme Corp', 'TechStart', 'InnoVentures', 'CloudBase', 'DataFlow', 'AutoMate'];

  return (
    <section className="py-12 bg-white border-y border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <p className="text-center text-sm font-semibold text-gray-500 uppercase tracking-wide mb-8">
          Trusted by leading teams
        </p>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8 items-center">
          {logos.map((name) => (
            <div key={name} className="flex justify-center">
              <div className="text-2xl font-bold text-gray-300 hover:text-gray-400 transition">
                {name}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
