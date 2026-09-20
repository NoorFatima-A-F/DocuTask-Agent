import { jsx as _jsx } from "react/jsx-runtime";
import React from 'react';
import { cn } from '../../utils/cn';
export const Card = React.forwardRef(({ className, variant = 'default', isClickable = false, isGlowing = false, children, ...props }, ref) => {
    const baseStyles = 'rounded-xl transition-all duration-200 text-[#F8FAFC] border';
    const variantStyles = {
        default: 'bg-[#131D35] border-[#1E293B]',
        elevated: 'bg-[#0F172A] border-[#334155] shadow-lg shadow-black/40',
        glassmorphic: 'bg-[#131D35]/80 backdrop-blur-md border-white/10 shadow-[inset_0_1px_0_0_rgba(255,255,255,0.08)]',
        intelligence: 'bg-[#131D35] border-cyan-500/30 shadow-[0_0_20px_rgba(0,210,255,0.15)]',
        subtle: 'bg-[#0A0F1D]/50 border-[#1E293B]/60',
    };
    return (_jsx("div", { ref: ref, className: cn(baseStyles, variantStyles[variant], isClickable &&
            'cursor-pointer hover:border-cyan-500/50 hover:shadow-[0_0_18px_rgba(0,102,255,0.25)] hover:scale-[1.005]', isGlowing && 'border-cyan-400 shadow-[0_0_25px_rgba(0,210,255,0.3)]', className), ...props, children: children }));
});
Card.displayName = 'Card';
export const CardHeader = React.forwardRef(({ className, ...props }, ref) => (_jsx("div", { ref: ref, className: cn('flex flex-col space-y-1.5 p-5 border-b border-[#1E293B]/60', className), ...props })));
CardHeader.displayName = 'CardHeader';
export const CardTitle = React.forwardRef(({ className, ...props }, ref) => (_jsx("h3", { ref: ref, className: cn('text-base font-semibold text-[#F8FAFC] tracking-tight leading-none', className), ...props })));
CardTitle.displayName = 'CardTitle';
export const CardDescription = React.forwardRef(({ className, ...props }, ref) => (_jsx("p", { ref: ref, className: cn('text-xs text-[#94A3B8] leading-relaxed', className), ...props })));
CardDescription.displayName = 'CardDescription';
export const CardContent = React.forwardRef(({ className, ...props }, ref) => (_jsx("div", { ref: ref, className: cn('p-5', className), ...props })));
CardContent.displayName = 'CardContent';
export const CardFooter = React.forwardRef(({ className, ...props }, ref) => (_jsx("div", { ref: ref, className: cn('flex items-center p-5 pt-0 border-t border-[#1E293B]/40 mt-4', className), ...props })));
CardFooter.displayName = 'CardFooter';
