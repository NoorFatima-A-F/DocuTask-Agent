import React from 'react';
import { cn } from '../../utils/cn';
import { Badge } from './Badge';

export type ZeroFabricationSentinelState =
  | 'UNKNOWN'
  | 'NOT_AVAILABLE'
  | 'NOT_COLLECTED'
  | 'NOT_EXECUTED'
  | 'INSUFFICIENT_CONTEXT'
  | 'INSUFFICIENT_EVIDENCE'
  | 'CAPABILITY_UNAVAILABLE'
  | 'DATASET_UNAVAILABLE'
  | 'RESOURCE_UNAVAILABLE'
  | 'PENDING_DISCOVERY';

export interface ConfidenceIndicatorProps extends React.HTMLAttributes<HTMLDivElement> {
  score?: number; // 0.0 to 1.0
  sentinelState?: ZeroFabricationSentinelState;
  sampleSize?: number;
  marginOfError?: number; // e.g. 0.03 for +/- 3%
  metricLabel?: string;
  variant?: 'bar' | 'compact' | 'badge';
}

export const ConfidenceIndicator: React.FC<ConfidenceIndicatorProps> = ({
  score,
  sentinelState,
  sampleSize,
  marginOfError,
  metricLabel = 'Confidence',
  variant = 'bar',
  className,
  ...props
}) => {
  // If Sentinel state is active (Zero-Fabrication Mode)
  if (sentinelState || score === undefined) {
    const sentinel = sentinelState || 'UNKNOWN';
    return (
      <div className={cn('inline-flex flex-col gap-1', className)} {...props}>
        {metricLabel && (
          <span className="text-[11px] font-medium text-[#94A3B8]">{metricLabel}</span>
        )}
        <Badge variant="sentinel" size="sm">
          {sentinel}
        </Badge>
      </div>
    );
  }

  const percentage = Math.min(Math.max(score * 100, 0), 100);

  // Determine color tier
  const getTierColor = (val: number) => {
    if (val >= 95) return { bar: 'bg-[#10B981]', text: 'text-[#34D399]', label: 'Very High' };
    if (val >= 85) return { bar: 'bg-[#34D399]', text: 'text-[#34D399]', label: 'High' };
    if (val >= 70) return { bar: 'bg-[#FBBF24]', text: 'text-[#FBBF24]', label: 'Moderate' };
    if (val >= 50) return { bar: 'bg-[#FB923C]', text: 'text-[#FB923C]', label: 'Low' };
    return { bar: 'bg-[#F87171]', text: 'text-[#F87171]', label: 'Uncertain' };
  };

  const tier = getTierColor(percentage);

  if (variant === 'compact') {
    return (
      <div className={cn('inline-flex items-center gap-2 font-mono text-xs', className)} {...props}>
        <span className={cn('font-semibold', tier.text)}>{percentage.toFixed(1)}%</span>
        {marginOfError !== undefined && (
          <span className="text-[#64748B] text-[11px]">±{(marginOfError * 100).toFixed(1)}%</span>
        )}
        {sampleSize !== undefined && (
          <span className="text-[#94A3B8] text-[10px] bg-[#1E293B] px-1.5 py-0.5 rounded border border-[#334155]">
            n={sampleSize}
          </span>
        )}
      </div>
    );
  }

  return (
    <div className={cn('w-full flex flex-col gap-1.5', className)} {...props}>
      <div className="flex items-center justify-between text-xs">
        <span className="font-medium text-[#94A3B8]">{metricLabel}</span>
        <div className="flex items-center gap-1.5 font-mono">
          <span className={cn('font-semibold', tier.text)}>{percentage.toFixed(1)}%</span>
          {marginOfError !== undefined && (
            <span className="text-[#64748B] text-[11px]">±{(marginOfError * 100).toFixed(1)}%</span>
          )}
          {sampleSize !== undefined && (
            <span className="text-[#94A3B8] text-[10px] bg-[#1E293B] px-1 py-0.5 rounded border border-[#334155]">
              n={sampleSize}
            </span>
          )}
        </div>
      </div>

      {/* Progress Track */}
      <div className="h-1.5 w-full bg-[#1E293B] rounded-full overflow-hidden relative">
        <div
          className={cn('h-full rounded-full transition-all duration-500 ease-out', tier.bar)}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
