import React from 'react';
import { CheckCircle2, AlertTriangle, ShieldAlert, Clock, AlertCircle } from 'lucide-react';

interface StatusBadgeProps {
  status?: string;
  reason?: string;
  delta?: string;
  confidence?: number;
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status = 'COMPLETED',
  reason,
  className = '',
}) => {
  const normalized = status.toUpperCase();

  if (normalized === 'COMPLETED') {
    return (
      <span className={`inline-flex items-center gap-1.5 rounded-md bg-emerald-500/10 px-2 py-1 text-xs font-medium text-emerald-400 border border-emerald-500/20 ${className}`}>
        <CheckCircle2 className="h-3.5 w-3.5" />
        <span>Completed</span>
      </span>
    );
  }

  if (normalized === 'TAX_ANOMALY' || (reason && reason.toLowerCase().includes('tax'))) {
    return (
      <div className={`flex flex-col ${className}`}>
        <span className="inline-flex items-center gap-1 rounded-md bg-amber-500/10 px-2 py-0.5 text-xs font-medium text-amber-400 border border-amber-500/20 w-fit">
          <AlertTriangle className="h-3.5 w-3.5" />
          <span>Tax Discrepancy</span>
        </span>
        <span className="mt-0.5 text-[11px] text-zinc-400 font-sans">
          {reason || 'Calculated tax variance (68% vs 85% expected)'}
        </span>
      </div>
    );
  }

  if (normalized === 'LOW_CONFIDENCE' || normalized === 'REVIEW_REQ' || (reason && reason.toLowerCase().includes('confidence'))) {
    return (
      <div className={`flex flex-col ${className}`}>
        <span className="inline-flex items-center gap-1 rounded-md bg-amber-500/10 px-2 py-0.5 text-xs font-medium text-amber-400 border border-amber-500/20 w-fit">
          <ShieldAlert className="h-3.5 w-3.5" />
          <span>Needs Review</span>
        </span>
        <span className="mt-0.5 text-[11px] text-zinc-400 font-sans">
          {reason || 'Model confidence (72.4%) below 75% threshold'}
        </span>
      </div>
    );
  }

  if (normalized === 'PROCESSING' || normalized === 'RUNNING') {
    return (
      <span className={`inline-flex items-center gap-1.5 rounded-md bg-indigo-500/10 px-2 py-1 text-xs font-medium text-indigo-400 border border-indigo-500/20 ${className}`}>
        <Clock className="h-3.5 w-3.5 animate-spin" />
        <span>Processing</span>
      </span>
    );
  }

  if (normalized === 'FAILED' || normalized === 'DLQ') {
    return (
      <span className={`inline-flex items-center gap-1.5 rounded-md bg-rose-500/10 px-2 py-1 text-xs font-medium text-rose-400 border border-rose-500/20 ${className}`}>
        <AlertCircle className="h-3.5 w-3.5" />
        <span>Quarantined</span>
      </span>
    );
  }

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-md bg-zinc-800 px-2 py-1 text-xs font-medium text-zinc-300 border border-zinc-700 ${className}`}>
      <span>{status}</span>
    </span>
  );
};
