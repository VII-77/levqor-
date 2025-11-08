import Link from 'next/link';

export default function DashboardTiles() {
  const tiles = [
    {
      title: 'Create Your First Workflow',
      description: 'Set up automated tasks in minutes with our visual builder',
      action: 'Get Started',
      href: '/workflows/new',
      icon: '⚡'
    },
    {
      title: 'Browse Templates',
      description: 'Choose from 100+ pre-built workflow templates',
      action: 'Explore',
      href: '/templates',
      icon: '📋'
    },
    {
      title: 'Connect Integrations',
      description: 'Connect to 50+ apps and services',
      action: 'View Integrations',
      href: '/integrations',
      icon: '🔌'
    }
  ];

  return (
    <div className="grid md:grid-cols-3 gap-6">
      {tiles.map((tile, i) => (
        <div key={i} className="bg-white rounded-lg border-2 border-gray-200 p-6 hover:border-blue-500 transition group">
          <div className="text-4xl mb-4">{tile.icon}</div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">{tile.title}</h3>
          <p className="text-gray-600 mb-4">{tile.description}</p>
          <Link
            href={tile.href}
            className="inline-flex items-center text-blue-600 font-semibold hover:text-blue-700 group-hover:gap-2 transition-all"
          >
            {tile.action}
            <svg className="w-5 h-5 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        </div>
      ))}
    </div>
  );
}
