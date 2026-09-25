import React from 'react';
import { ConfidenceTier } from '../../types/extraction';

interface StatusBadgeProps {
  status?: string;
  confidence?: number;
  tier?: ConfidenceTier;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  confidence,
  tier,
  size = 'md',
  className = '',
}) => {
  const sizeClasses = {
    sm: 'text-[10px] px-1.5 py-0.2',
    md: 'text-xs px-2 py-0.5',
    lg: 'text-xs px-2.5 py-1',
  }[size];

  if (confidence !== undefined) {
    const pct = (confidence * 100).toFixed(1);
    let colorClass = 'bg-emerald-950/40 text-emerald-400 border-emerald-800/50';
    if (confidence < 0.70) {
      colorClass = 'bg-rose-950/40 text-rose-400 border-rose-800/50';
    } else if (confidence < 0.90) {
      colorClass = 'bg-amber-950/40 text-amber-400 border-amber-800/50';
    }

    return (
      <span
        className={`inline-flex items-center gap-1 font-mono font-medium rounded border ${sizeClasses} ${colorClass} ${className}`}
      >
        <span className="w-1.5 h-1.5 rounded-full bg-current" />
        {pct}%
      </span>
    );
  }

  if (tier) {
    const tierStyles: Record<ConfidenceTier, string> = {
      HIGH: 'bg-emerald-950/40 text-emerald-400 border-emerald-800/50',
      MEDIUM: 'bg-amber-950/40 text-amber-400 border-amber-800/50',
      LOW: 'bg-rose-950/40 text-rose-400 border-rose-800/50',
    };
    return (
      <span
        className={`inline-flex items-center gap-1 font-mono font-medium rounded border ${sizeClasses} ${tierStyles[tier]} ${className}`}
      >
        <span className="w-1.5 h-1.5 rounded-full bg-current" />
        {tier}
      </span>
    );
  }

  const normalizedStatus = (status || 'UNKNOWN').toUpperCase();
  const statusStyles: Record<string, string> = {
    COMPLETED: 'bg-emerald-950/40 text-emerald-400 border-emerald-800/50',
    PROCESSING: 'bg-zinc-800 text-zinc-200 border-zinc-700',
    RUNNING: 'bg-zinc-800 text-zinc-200 border-zinc-700',
    QUEUED: 'bg-amber-950/40 text-amber-400 border-amber-800/50',
    PENDING: 'bg-zinc-900 text-zinc-400 border-zinc-800',
    FAILED: 'bg-rose-950/40 text-rose-400 border-rose-800/50',
    DLQ: 'bg-rose-950/60 text-rose-300 border-rose-800',
  };

  const style = statusStyles[normalizedStatus] || 'bg-zinc-900 text-zinc-400 border-zinc-800';

  return (
    <span
      className={`inline-flex items-center gap-1 font-mono uppercase tracking-wider rounded border ${sizeClasses} ${style} ${className}`}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-current" />
      {normalizedStatus}
    </span>
  );
};
