import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import React from 'react';
import { cn } from '../../utils/cn';
export const Button = React.forwardRef(({ className, variant = 'primary', size = 'md', isLoading = false, loadingText, leftIcon, rightIcon, isAutonomousAction = false, disabled, children, ...props }, ref) => {
    const baseStyles = 'inline-flex items-center justify-center font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-[#0A0F1D] disabled:opacity-50 disabled:cursor-not-allowed select-none rounded-lg';
    const sizeStyles = {
        sm: 'px-3 py-1.5 text-xs gap-1.5',
        md: 'px-4 py-2 text-sm gap-2',
        lg: 'px-5 py-2.5 text-base gap-2.5',
    };
    const variantStyles = {
        primary: 'bg-[#0066FF] text-white hover:bg-[#0052CC] focus:ring-[#0066FF] shadow-sm hover:shadow-[0_0_15px_rgba(0,102,255,0.4)]',
        secondary: 'bg-[#1E293B] text-[#F8FAFC] hover:bg-[#334155] border border-[#334155] focus:ring-[#64748B]',
        intelligence: 'bg-gradient-to-r from-[#0066FF] to-[#00D2FF] text-white hover:opacity-95 shadow-[0_0_20px_rgba(0,210,255,0.35)] focus:ring-[#00D2FF] border border-cyan-400/30',
        ghost: 'bg-transparent text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-[#1E293B]/50 focus:ring-[#64748B]',
        outline: 'bg-transparent text-[#F8FAFC] border border-[#334155] hover:bg-[#1E293B] hover:border-[#64748B] focus:ring-[#0066FF]',
        danger: 'bg-[#EF4444] text-white hover:bg-[#DC2626] focus:ring-[#EF4444] shadow-sm hover:shadow-[0_0_15px_rgba(239,68,68,0.4)]',
    };
    return (_jsx("button", { ref: ref, disabled: disabled || isLoading, className: cn(baseStyles, sizeStyles[size], variantStyles[variant], isAutonomousAction && 'border-dashed border-cyan-400/60 ring-1 ring-cyan-500/30', className), ...props, children: isLoading ? (_jsxs(_Fragment, { children: [_jsxs("svg", { className: "animate-spin -ml-1 mr-2 h-4 w-4 text-current", xmlns: "http://www.w3.org/2000/svg", fill: "none", viewBox: "0 0 24 24", "aria-hidden": "true", children: [_jsx("circle", { className: "opacity-25", cx: "12", cy: "12", r: "10", stroke: "currentColor", strokeWidth: "4" }), _jsx("path", { className: "opacity-75", fill: "currentColor", d: "M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" })] }), loadingText || children] })) : (_jsxs(_Fragment, { children: [leftIcon && _jsx("span", { className: "shrink-0", children: leftIcon }), _jsx("span", { children: children }), rightIcon && _jsx("span", { className: "shrink-0", children: rightIcon })] })) }));
});
Button.displayName = 'Button';
