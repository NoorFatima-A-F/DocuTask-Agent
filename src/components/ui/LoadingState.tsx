import React from 'react';
import { cn } from '../../utils/cn';

export interface LoadingStateProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'skeleton' | 'neural-pulse' | 'cognitive-deliberation';
  message?: string;
  submessage?: string;
  thinkingPhase?: string;
  rowsCount?: number;
}

export const LoadingState: React.FC<LoadingStateProps> = ({
  variant = 'neural-pulse',
  message = 'Agent is deliberating...',
  submessage,
  thinkingPhase,
  rowsCount = 3,
  className,
  ...props
}) => {
  if (variant === 'skeleton') {
    return (
      <div className={cn('space-y-3 w-full animate-pulse', className)} {...props}>
        <div className="h-4 bg-[#1E293B] rounded-md w-3/4" />
        {Array.from({ length: rowsCount }).map((_, i) => (
          <div
            key={i}
            className="h-3 bg-[#131D35] rounded-md"
            style={{ width: `${85 - i * 15}%` }}
          />
        ))}
      </div>
    );
  }

  if (variant === 'cognitive-deliberation') {
    return (
      <div
        className={cn(
          'flex flex-col items-center justify-center p-8 text-center rounded-xl bg-[#131D35]/50 border border-cyan-500/20 shadow-[0_0_30px_rgba(0,210,255,0.08)]',
          className
        )}
        {...props}
      >
        {/* Animated Neural Core */}
        <div className="relative flex items-center justify-center h-16 w-16 mb-4">
          <div className="absolute inset-0 rounded-full border border-cyan-400/40 animate-ping opacity-25" />
          <div className="absolute inset-2 rounded-full border-2 border-t-[#00D2FF] border-r-transparent border-b-[#0066FF] border-l-transparent animate-spin duration-700" />
          <div className="h-4 w-4 rounded-full bg-gradient-to-tr from-[#0066FF] to-[#00D2FF] shadow-[0_0_12px_rgba(0,210,255,0.8)]" />
        </div>

        {thinkingPhase && (
          <span className="text-[11px] font-mono uppercase tracking-widest text-[#00D2FF] bg-cyan-950/60 px-2.5 py-0.5 rounded border border-cyan-500/30 mb-2">
            Phase: {thinkingPhase}
          </span>
        )}

        <h4 className="text-sm font-semibold text-[#F8FAFC] tracking-tight">{message}</h4>

        {submessage && (
          <p className="mt-1 max-w-sm text-xs text-[#94A3B8] font-mono leading-relaxed">
            {submessage}
          </p>
        )}
      </div>
    );
  }

  // Default Neural Pulse Loader
  return (
    <div
      className={cn('flex items-center gap-3 p-4 rounded-lg bg-[#131D35] border border-[#1E293B]', className)}
      role="status"
      {...props}
    >
      <div className="relative flex items-center justify-center shrink-0 h-8 w-8">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-20" />
        <span className="relative inline-flex rounded-full h-3 w-3 bg-[#00D2FF] shadow-[0_0_10px_rgba(0,210,255,0.7)]" />
      </div>

      <div className="flex flex-col">
        <span className="text-xs font-medium text-[#F8FAFC]">{message}</span>
        {submessage && <span className="text-[11px] text-[#94A3B8]">{submessage}</span>}
      </div>
    </div>
  );
};
