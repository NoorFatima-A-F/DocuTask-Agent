import React from 'react';
import { cn } from '../../utils/cn';

export interface TimelineItem {
  id: string;
  title: string;
  description?: string;
  timestamp?: string;
  status?: 'completed' | 'in-progress' | 'failed' | 'pending';
  icon?: React.ReactNode;
  tags?: string[];
  metadata?: Record<string, unknown>;
}

export interface TimelineProps extends React.HTMLAttributes<HTMLDivElement> {
  items: TimelineItem[];
  orientation?: 'vertical' | 'horizontal';
  onItemClick?: (item: TimelineItem) => void;
}

export const Timeline: React.FC<TimelineProps> = ({
  items,
  orientation = 'vertical',
  onItemClick,
  className,
  ...props
}) => {
  const getStatusColor = (status?: TimelineItem['status']) => {
    switch (status) {
      case 'completed':
        return {
          dot: 'bg-emerald-500 ring-emerald-500/30',
          line: 'bg-emerald-500/50',
        };
      case 'in-progress':
        return {
          dot: 'bg-[#00D2FF] ring-cyan-400/50 animate-pulse shadow-[0_0_10px_rgba(0,210,255,0.6)]',
          line: 'bg-cyan-500/40',
        };
      case 'failed':
        return {
          dot: 'bg-red-500 ring-red-500/30',
          line: 'bg-red-500/40',
        };
      case 'pending':
      default:
        return {
          dot: 'bg-slate-600 ring-slate-600/30',
          line: 'bg-[#1E293B]',
        };
    }
  };

  if (orientation === 'horizontal') {
    return (
      <div className={cn('flex items-center w-full overflow-x-auto py-4', className)} {...props}>
        {items.map((item, index) => {
          const statusStyle = getStatusColor(item.status);
          const isLast = index === items.length - 1;
          return (
            <div
              key={item.id}
              onClick={() => onItemClick?.(item)}
              className={cn(
                'flex items-center flex-1 min-w-[140px]',
                onItemClick && 'cursor-pointer group'
              )}
            >
              <div className="flex flex-col items-center">
                <div
                  className={cn(
                    'h-3.5 w-3.5 rounded-full ring-4 transition-all duration-200',
                    statusStyle.dot
                  )}
                />
                <span className="mt-2 text-xs font-medium text-[#F8FAFC] text-center line-clamp-1">
                  {item.title}
                </span>
                {item.timestamp && (
                  <span className="text-[10px] text-[#64748B] font-mono">{item.timestamp}</span>
                )}
              </div>
              {!isLast && <div className={cn('h-0.5 flex-1 mx-2 transition-colors', statusStyle.line)} />}
            </div>
          );
        })}
      </div>
    );
  }

  return (
    <div className={cn('relative flex flex-col space-y-6', className)} {...props}>
      {items.map((item, index) => {
        const statusStyle = getStatusColor(item.status);
        const isLast = index === items.length - 1;

        return (
          <div
            key={item.id}
            onClick={() => onItemClick?.(item)}
            className={cn('relative flex items-start gap-3.5 group', onItemClick && 'cursor-pointer')}
          >
            {/* Connecting line */}
            {!isLast && (
              <div
                className={cn(
                  'absolute top-4 left-[7px] w-0.5 h-[calc(100%+16px)] transition-colors',
                  statusStyle.line
                )}
              />
            )}

            {/* Node Dot / Custom Icon */}
            <div className="relative z-10 flex items-center justify-center shrink-0 mt-1">
              {item.icon ? (
                <div className="h-6 w-6 rounded-full bg-[#131D35] border border-[#334155] flex items-center justify-center text-xs">
                  {item.icon}
                </div>
              ) : (
                <div
                  className={cn(
                    'h-3.5 w-3.5 rounded-full ring-4 transition-all duration-200',
                    statusStyle.dot
                  )}
                />
              )}
            </div>

            {/* Content Card */}
            <div className="flex-1 flex flex-col">
              <div className="flex items-baseline justify-between gap-2">
                <span className="text-sm font-medium text-[#F8FAFC] group-hover:text-[#00D2FF] transition-colors">
                  {item.title}
                </span>
                {item.timestamp && (
                  <span className="text-[11px] text-[#64748B] font-mono shrink-0">
                    {item.timestamp}
                  </span>
                )}
              </div>
              {item.description && (
                <p className="mt-0.5 text-xs text-[#94A3B8] leading-relaxed">
                  {item.description}
                </p>
              )}
              {item.tags && item.tags.length > 0 && (
                <div className="flex flex-wrap gap-1 mt-2">
                  {item.tags.map((tag) => (
                    <span
                      key={tag}
                      className="text-[10px] bg-[#1E293B] text-[#94A3B8] px-1.5 py-0.5 rounded border border-[#334155]/60 font-mono"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
