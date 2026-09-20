import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { cn } from '../../utils/cn';
export const ProgressRing = ({ value = 0, size = 48, strokeWidth = 4, isIndeterminate = false, variant = 'intelligence', showLabel = false, children, className, ...props }) => {
    const radius = (size - strokeWidth) / 2;
    const circumference = 2 * Math.PI * radius;
    const clampedValue = Math.min(Math.max(value, 0), 100);
    const strokeDashoffset = circumference - (clampedValue / 100) * circumference;
    const colorMap = {
        primary: '#0066FF',
        intelligence: '#00D2FF',
        success: '#10B981',
        warning: '#F59E0B',
        danger: '#EF4444',
    };
    const strokeColor = colorMap[variant];
    return (_jsxs("div", { className: cn('relative inline-flex items-center justify-center', className), style: { width: size, height: size }, children: [_jsxs("svg", { width: size, height: size, viewBox: `0 0 ${size} ${size}`, className: cn('transform -rotate-90 origin-center', isIndeterminate && 'animate-spin duration-1000'), ...props, children: [_jsx("circle", { cx: size / 2, cy: size / 2, r: radius, stroke: "#1E293B", strokeWidth: strokeWidth, fill: "none" }), _jsx("circle", { cx: size / 2, cy: size / 2, r: radius, stroke: strokeColor, strokeWidth: strokeWidth, strokeDasharray: circumference, strokeDashoffset: isIndeterminate ? circumference * 0.75 : strokeDashoffset, strokeLinecap: "round", fill: "none", className: "transition-all duration-500 ease-out", style: {
                            filter: `drop-shadow(0 0 4px ${strokeColor})`,
                        } })] }), _jsx("div", { className: "absolute inset-0 flex items-center justify-center text-center", children: children ? (children) : showLabel ? (_jsxs("span", { className: "text-xs font-semibold text-[#F8FAFC] font-mono", children: [Math.round(clampedValue), "%"] })) : null })] }));
};
