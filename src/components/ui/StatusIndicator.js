import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { cn } from '../../utils/cn';
export const StatusIndicator = ({ status, label, sublabel, size = 'md', showPulse = true, className, ...props }) => {
    const statusConfig = {
        idle: {
            color: 'bg-slate-500',
            ringColor: 'ring-slate-500/30',
            glowColor: 'shadow-none',
            defaultLabel: 'Idle / Standby',
        },
        thinking: {
            color: 'bg-cyan-400',
            ringColor: 'ring-cyan-400/50',
            glowColor: 'shadow-[0_0_12px_rgba(0,210,255,0.7)]',
            defaultLabel: 'Deliberating / Observing',
        },
        executing: {
            color: 'bg-[#0066FF]',
            ringColor: 'ring-blue-500/50',
            glowColor: 'shadow-[0_0_12px_rgba(0,102,255,0.7)]',
            defaultLabel: 'Autonomous Execution',
        },
        verifying: {
            color: 'bg-purple-500',
            ringColor: 'ring-purple-500/50',
            glowColor: 'shadow-[0_0_12px_rgba(168,85,247,0.7)]',
            defaultLabel: 'SLSA Cryptographic Verification',
        },
        learning: {
            color: 'bg-pink-500',
            ringColor: 'ring-pink-500/50',
            glowColor: 'shadow-[0_0_12px_rgba(236,72,153,0.7)]',
            defaultLabel: 'Consolidating Memory',
        },
        waiting: {
            color: 'bg-amber-400',
            ringColor: 'ring-amber-400/50',
            glowColor: 'shadow-[0_0_12px_rgba(245,158,11,0.7)]',
            defaultLabel: 'Awaiting Human-in-the-Loop Review',
        },
        completed: {
            color: 'bg-emerald-500',
            ringColor: 'ring-emerald-500/40',
            glowColor: 'shadow-[0_0_10px_rgba(16,185,129,0.5)]',
            defaultLabel: 'Mission Success',
        },
        failed: {
            color: 'bg-red-500',
            ringColor: 'ring-red-500/40',
            glowColor: 'shadow-[0_0_10px_rgba(239,68,68,0.5)]',
            defaultLabel: 'Execution Failure',
        },
        aborted: {
            color: 'bg-slate-400',
            ringColor: 'ring-slate-400/30',
            glowColor: 'shadow-none',
            defaultLabel: 'Aborted',
        },
        offline: {
            color: 'bg-slate-700',
            ringColor: 'ring-slate-700/20',
            glowColor: 'shadow-none',
            defaultLabel: 'Offline',
        },
    };
    const current = statusConfig[status];
    const isPulsing = showPulse && ['thinking', 'executing', 'verifying', 'learning', 'waiting'].includes(status);
    const dotSize = {
        sm: 'h-2 w-2',
        md: 'h-2.5 w-2.5',
        lg: 'h-3.5 w-3.5',
    };
    return (_jsxs("div", { className: cn('inline-flex items-center gap-2.5', className), role: "status", "aria-label": label || current.defaultLabel, ...props, children: [_jsxs("span", { className: "relative flex items-center justify-center shrink-0", children: [isPulsing && (_jsx("span", { className: cn('animate-ping absolute inline-flex h-full w-full rounded-full opacity-75', current.color) })), _jsx("span", { className: cn('relative inline-flex rounded-full ring-2 transition-all duration-300', dotSize[size], current.color, current.ringColor, current.glowColor) })] }), (label || current.defaultLabel || sublabel) && (_jsxs("div", { className: "flex flex-col text-left", children: [_jsx("span", { className: "text-xs font-medium text-[#F8FAFC] tracking-tight", children: label || current.defaultLabel }), sublabel && _jsx("span", { className: "text-[11px] text-[#94A3B8]", children: sublabel })] }))] }));
};
