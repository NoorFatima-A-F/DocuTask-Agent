import React from 'react';
import { cn } from '../../utils/cn';
import { Button, type ButtonProps } from './Button';

export interface EmptyStateProps extends React.HTMLAttributes<HTMLDivElement> {
  icon?: React.ReactNode;
  title: string;
  description: string;
  primaryAction?: {
    label: string;
    onClick: () => void;
    icon?: React.ReactNode;
    variant?: ButtonProps['variant'];
  };
  secondaryAction?: {
    label: string;
    onClick: () => void;
  };
  reasonExplanation?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon,
  title,
  description,
  primaryAction,
  secondaryAction,
  reasonExplanation,
  className,
  ...props
}) => {
  return (
    <div
      className={cn(
        'flex flex-col items-center justify-center p-8 text-center rounded-xl border border-dashed border-[#334155] bg-[#131D35]/30',
        className
      )}
      {...props}
    >
      {icon ? (
        <div className="mb-4 flex items-center justify-center h-12 w-12 rounded-xl bg-[#1E293B] border border-[#334155] text-cyan-400 shadow-[0_0_15px_rgba(0,210,255,0.15)]">
          {icon}
        </div>
      ) : (
        <div className="mb-4 flex items-center justify-center h-12 w-12 rounded-xl bg-[#1E293B] border border-[#334155] text-[#94A3B8]">
          <svg
            className="w-6 h-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
        </div>
      )}

      <h3 className="text-base font-semibold text-[#F8FAFC] tracking-tight">{title}</h3>
      <p className="mt-1.5 max-w-sm text-xs text-[#94A3B8] leading-relaxed">
        {description}
      </p>

      {reasonExplanation && (
        <div className="mt-3 px-3 py-1.5 rounded bg-[#0A0F1D] border border-[#1E293B] text-[11px] text-[#64748B] font-mono">
          {reasonExplanation}
        </div>
      )}

      {(primaryAction || secondaryAction) && (
        <div className="mt-6 flex items-center gap-3">
          {secondaryAction && (
            <Button variant="ghost" size="sm" onClick={secondaryAction.onClick}>
              {secondaryAction.label}
            </Button>
          )}
          {primaryAction && (
            <Button
              variant={primaryAction.variant || 'intelligence'}
              size="sm"
              leftIcon={primaryAction.icon}
              onClick={primaryAction.onClick}
            >
              {primaryAction.label}
            </Button>
          )}
        </div>
      )}
    </div>
  );
};
