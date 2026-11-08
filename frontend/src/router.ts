import { useEffect, useState } from 'react';

/** Minimal History-API router; the backend serves index.html for these paths. */
export type Route =
  | { name: 'home' }
  | { name: 'job'; jobId: string }
  | { name: 'reviews' }
  | { name: 'review'; extractionId: string }
  | { name: 'notFound' };

export function parseRoute(pathname: string): Route {
  const parts = pathname.replace(/\/+$/, '').split('/').filter(Boolean);
  if (parts.length === 0) return { name: 'home' };
  if (parts[0] === 'jobs' && parts.length === 2) return { name: 'job', jobId: parts[1] };
  if (parts[0] === 'reviews' && parts.length === 1) return { name: 'reviews' };
  if (parts[0] === 'reviews' && parts.length === 2) return { name: 'review', extractionId: parts[1] };
  return { name: 'notFound' };
}

export function navigate(path: string): void {
  window.history.pushState({}, '', path);
  window.dispatchEvent(new PopStateEvent('popstate'));
}

export function useRoute(): Route {
  const [route, setRoute] = useState(() => parseRoute(window.location.pathname));
  useEffect(() => {
    const onPop = () => setRoute(parseRoute(window.location.pathname));
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, []);
  return route;
}
