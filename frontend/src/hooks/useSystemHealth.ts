import { useQuery } from '@tanstack/react-query';

export interface SystemHealthData {
  isOnline: boolean;
  statusText: string;
  activeWorkers: number;
  queueDepth: number;
  service: string;
  lastChecked: string;
}

export function useSystemHealth() {
  return useQuery<SystemHealthData>({
    queryKey: ['systemHealth'],
    queryFn: async () => {
      try {
        const res = await fetch('/api/v1/health', {
          headers: { 'Accept': 'application/json' },
        });

        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }

        const data = await res.json();
        return {
          isOnline: true,
          statusText: data.data?.status || 'HEALTHY',
          activeWorkers: 1,
          queueDepth: 0,
          service: data.data?.service || 'DocuTask Agent Platform',
          lastChecked: new Date().toLocaleTimeString(),
        };
      } catch {
        return {
          isOnline: false,
          statusText: 'OFFLINE',
          activeWorkers: 0,
          queueDepth: 0,
          service: 'FastAPI Backend',
          lastChecked: new Date().toLocaleTimeString(),
        };
      }
    },
    refetchInterval: 5000,
    retry: false,
    staleTime: 4000,
  });
}
