export async function logEvent(type: string, payload: any) {
  try {
    const backendBase = process.env.NEXT_PUBLIC_BACKEND_BASE;
    if (!backendBase) {
      console.warn('Backend base URL not configured');
      return;
    }

    let ref = null;
    if (typeof window !== 'undefined') {
      const storedRef = localStorage.getItem('levqor_ref');
      if (storedRef) {
        try {
          ref = JSON.parse(storedRef);
        } catch (e) {
          console.warn('Failed to parse stored ref');
        }
      }
    }

    await fetch(`${backendBase}/api/v1/metrics/track`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        type,
        payload,
        ref,
      }),
    });
  } catch (error) {
    console.error('Failed to log event:', error);
  }
}
