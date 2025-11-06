'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { logEvent } from '@/utils/metrics';

export default function PageViewTracker() {
  const pathname = usePathname();

  useEffect(() => {
    if (pathname) {
      logEvent('page_view', { path: pathname });
    }
  }, [pathname]);

  return null;
}
