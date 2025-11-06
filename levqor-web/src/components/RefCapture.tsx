'use client';

import { useEffect } from 'react';

export default function RefCapture() {
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const params = new URLSearchParams(window.location.search);
    const utmSource = params.get('utm_source');
    const utmMedium = params.get('utm_medium');
    const utmCampaign = params.get('utm_campaign');
    const ref = params.get('ref');

    if (utmSource || utmMedium || utmCampaign || ref) {
      const refData = {
        utm_source: utmSource,
        utm_medium: utmMedium,
        utm_campaign: utmCampaign,
        ref: ref,
        timestamp: Date.now(),
      };

      localStorage.setItem('levqor_ref', JSON.stringify(refData));
    }
  }, []);

  return null;
}
