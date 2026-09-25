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
    sm: 'text-xs px-2 py-0.5',
    md: 'text-xs px-2.5 py-1',
    lg: 'text-sm px-3 py-1.5',
  }[size];

  if (confidence !== undefined) {
    const pct = (confidence * 100).toFixed(1);
    let colorClass = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
    if (confidence < 0.70) {
      colorClass = 'bg-rose-500/10 text-rose-400 border-rose-500/30';
    } else if (confidence < 0.90) {
      colorClass = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
    }

    return (
      <span
        className={`inline-flex items-center gap-1.5 font-mono font-medium rounded-md border ${sizeClasses} ${colorClass} ${className}`}
      >
        <span className="w-1.5 h-1.5 rounded-full bg-current" />
        {pct}% Conf
      </span>
    );
  }

  if (tier) {
    const tierStyles: Record<ConfidenceTier, string> = {
      HIGH: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
      MEDIUM: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
      LOW: 'bg-rose-500/10 text-rose-400 border-rose-500/30',
    };
    return (
      <span
        className={`inline-flex items-center gap-1.5 font-mono font-medium rounded-md border ${sizeClasses} ${tierStyles[tier]} ${className}`}
      >
        <span className="w-1.5 h-1.5 rounded-full bg-current" />
        {tier}
      </span>
    );
  }

  const normalizedStatus = (status || 'UNKNOWN').toUpperCase();
  const statusStyles: Record<string, string> = {
    COMPLETED: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    PROCESSING: 'bg-blue-500/10 text-blue-400 border-blue-500/30 animate-pulse',
    RUNNING: 'bg-blue-500/10 text-blue-400 border-blue-500/30 animate-pulse',
    QUEUED: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
    PENDING: 'bg-slate-500/10 text-slate-400 border-slate-500/30',
    FAILED: 'bg-rose-500/10 text-rose-400 border-rose-500/30',
    DLQ: 'bg-rose-900/30 text-rose-300 border-rose-700/50',
  };

  const style = statusStyles[normalizedStatus] || 'bg-slate-800 text-slate-400 border-slate-700';

  return (
    <span
      className={`inline-flex items-center gap-1.5 font-mono uppercase tracking-wider rounded-md border ${sizeClasses} ${style} ${className}`}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-current" />
      {normalizedStatus}
    </span>
  );
};
