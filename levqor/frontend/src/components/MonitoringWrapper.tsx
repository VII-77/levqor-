'use client';

import { useEffect } from 'react';
import dynamic from 'next/dynamic';

const SupportWidget = dynamic(() => import('./SupportWidget'), { ssr: false });

const ENABLE_ERROR_REPORTER = process.env.NEXT_PUBLIC_ENABLE_ERROR_REPORTER !== 'false';
const HAS_SENTRY = !!process.env.SENTRY_DSN;
const ENABLE_SUPPORT_WIDGET = process.env.NEXT_PUBLIC_ENABLE_SUPPORT_WIDGET !== 'false';
const HAS_CRISP = !!process.env.NEXT_PUBLIC_CRISP_WEBSITE_ID;

export default function MonitoringWrapper() {
  useEffect(() => {
    if (!HAS_SENTRY && ENABLE_ERROR_REPORTER) {
      import('@/lib/errorReporter').then(({ errorReporter }) => {
        errorReporter.init();
      });
    }
  }, []);

  const showSupportWidget = !HAS_CRISP && ENABLE_SUPPORT_WIDGET;

  return (
    <>
      {showSupportWidget && <SupportWidget />}
    </>
  );
}
