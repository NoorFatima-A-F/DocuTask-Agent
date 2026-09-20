import React from 'react';
import { cn } from '../../utils/cn';

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?:
    | 'default'
    | 'success'
    | 'warning'
    | 'error'
    | 'info'
    | 'intelligence'
    | 'sentinel'
    | 'outline';
  size?: 'sm' | 'md';
  hasDot?: boolean;
  isPulsing?: boolean;
}

export const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  (
    {
      className,
      variant = 'default',
      size = 'md',
      hasDot = false,
      isPulsing = false,
      children,
      ...props
    },
    ref
  ) => {
    const baseStyles =
      'inline-flex items-center font-medium rounded-full select-none transition-colors';

    const sizeStyles = {
      sm: 'px-2 py-0.5 text-[11px] gap-1.5',
      md: 'px-2.5 py-1 text-xs gap-1.5',
    };

    const variantStyles = {
      default: 'bg-[#1E293B] text-[#94A3B8] border border-[#334155]',
      success: 'bg-[#10B981]/15 text-[#34D399] border border-[#10B981]/30',
      warning: 'bg-[#F59E0B]/15 text-[#FBBF24] border border-[#F59E0B]/30',
      error: 'bg-[#EF4444]/15 text-[#F87171] border border-[#EF4444]/30',
      info: 'bg-[#0066FF]/15 text-[#38BDF8] border border-[#0066FF]/30',
      intelligence:
        'bg-cyan-950/50 text-[#00D2FF] border border-cyan-400/40 shadow-[0_0_10px_rgba(0,210,255,0.2)]',
      sentinel:
        'bg-purple-950/40 text-purple-300 border border-purple-500/30 font-mono',
      outline: 'bg-transparent text-[#F8FAFC] border border-[#334155]',
    };

    const dotColorMap = {
      default: 'bg-[#94A3B8]',
      success: 'bg-[#10B981]',
      warning: 'bg-[#F59E0B]',
      error: 'bg-[#EF4444]',
      info: 'bg-[#0066FF]',
      intelligence: 'bg-[#00D2FF]',
      sentinel: 'bg-purple-400',
      outline: 'bg-[#F8FAFC]',
    };

    return (
      <span
        ref={ref}
        className={cn(baseStyles, sizeStyles[size], variantStyles[variant], className)}
        {...props}
      >
        {hasDot && (
          <span className="relative flex h-1.5 w-1.5">
            {isPulsing && (
              <span
                className={cn(
                  'animate-ping absolute inline-flex h-full w-full rounded-full opacity-75',
                  dotColorMap[variant]
                )}
              />
            )}
            <span
              className={cn('relative inline-flex rounded-full h-1.5 w-1.5', dotColorMap[variant])}
            />
          </span>
        )}
        {children}
      </span>
    );
  }
);

Badge.displayName = 'Badge';
