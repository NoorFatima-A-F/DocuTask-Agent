import React, { useState, useEffect } from 'react';
import { Clock } from 'lucide-react';

interface LatencyClockProps {
  isRunning: boolean;
  finalLatencyMs?: number;
}

export const LatencyClock: React.FC<LatencyClockProps> = ({
  isRunning,
  finalLatencyMs,
}) => {
  const [elapsedMs, setElapsedMs] = useState<number>(finalLatencyMs || 0);

  useEffect(() => {
    if (!isRunning) {
      if (finalLatencyMs) setElapsedMs(finalLatencyMs);
      return;
    }

    const start = performance.now();
    const timer = setInterval(() => {
      setElapsedMs(Math.round(performance.now() - start));
    }, 50);

    return () => clearInterval(timer);
  }, [isRunning, finalLatencyMs]);

  const seconds = (elapsedMs / 1000).toFixed(2);

  return (
    <div className="flex items-center gap-2 font-mono text-xs px-2.5 py-1 rounded-md bg-slate-900 border border-slate-800 text-slate-300">
      <Clock className={`w-3.5 h-3.5 ${isRunning ? 'text-cyan-400 animate-spin' : 'text-slate-400'}`} />
      <span>LATENCY:</span>
      <strong className={isRunning ? 'text-cyan-300' : 'text-emerald-400'}>
        {seconds}s ({elapsedMs}ms)
      </strong>
    </div>
  );
};
