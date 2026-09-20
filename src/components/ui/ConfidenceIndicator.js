import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { cn } from '../../utils/cn';
import { Badge } from './Badge';
export const ConfidenceIndicator = ({ score, sentinelState, sampleSize, marginOfError, metricLabel = 'Confidence', variant = 'bar', className, ...props }) => {
    // If Sentinel state is active (Zero-Fabrication Mode)
    if (sentinelState || score === undefined) {
        const sentinel = sentinelState || 'UNKNOWN';
        return (_jsxs("div", { className: cn('inline-flex flex-col gap-1', className), ...props, children: [metricLabel && (_jsx("span", { className: "text-[11px] font-medium text-[#94A3B8]", children: metricLabel })), _jsx(Badge, { variant: "sentinel", size: "sm", children: sentinel })] }));
    }
    const percentage = Math.min(Math.max(score * 100, 0), 100);
    // Determine color tier
    const getTierColor = (val) => {
        if (val >= 95)
            return { bar: 'bg-[#10B981]', text: 'text-[#34D399]', label: 'Very High' };
        if (val >= 85)
            return { bar: 'bg-[#34D399]', text: 'text-[#34D399]', label: 'High' };
        if (val >= 70)
            return { bar: 'bg-[#FBBF24]', text: 'text-[#FBBF24]', label: 'Moderate' };
        if (val >= 50)
            return { bar: 'bg-[#FB923C]', text: 'text-[#FB923C]', label: 'Low' };
        return { bar: 'bg-[#F87171]', text: 'text-[#F87171]', label: 'Uncertain' };
    };
    const tier = getTierColor(percentage);
    if (variant === 'compact') {
        return (_jsxs("div", { className: cn('inline-flex items-center gap-2 font-mono text-xs', className), ...props, children: [_jsxs("span", { className: cn('font-semibold', tier.text), children: [percentage.toFixed(1), "%"] }), marginOfError !== undefined && (_jsxs("span", { className: "text-[#64748B] text-[11px]", children: ["\u00B1", (marginOfError * 100).toFixed(1), "%"] })), sampleSize !== undefined && (_jsxs("span", { className: "text-[#94A3B8] text-[10px] bg-[#1E293B] px-1.5 py-0.5 rounded border border-[#334155]", children: ["n=", sampleSize] }))] }));
    }
    return (_jsxs("div", { className: cn('w-full flex flex-col gap-1.5', className), ...props, children: [_jsxs("div", { className: "flex items-center justify-between text-xs", children: [_jsx("span", { className: "font-medium text-[#94A3B8]", children: metricLabel }), _jsxs("div", { className: "flex items-center gap-1.5 font-mono", children: [_jsxs("span", { className: cn('font-semibold', tier.text), children: [percentage.toFixed(1), "%"] }), marginOfError !== undefined && (_jsxs("span", { className: "text-[#64748B] text-[11px]", children: ["\u00B1", (marginOfError * 100).toFixed(1), "%"] })), sampleSize !== undefined && (_jsxs("span", { className: "text-[#94A3B8] text-[10px] bg-[#1E293B] px-1 py-0.5 rounded border border-[#334155]", children: ["n=", sampleSize] }))] })] }), _jsx("div", { className: "h-1.5 w-full bg-[#1E293B] rounded-full overflow-hidden relative", children: _jsx("div", { className: cn('h-full rounded-full transition-all duration-500 ease-out', tier.bar), style: { width: `${percentage}%` } }) })] }));
};
