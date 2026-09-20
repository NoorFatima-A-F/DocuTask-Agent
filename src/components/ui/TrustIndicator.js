import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { polishTokens } from '../../design-system/tokens/polish';
export const TrustIndicator = ({ state, customLabel, showIcon = true, className = '', ...props }) => {
    const config = polishTokens.trustStates[state] || polishTokens.trustStates.UNKNOWN;
    return (_jsxs("span", { className: `inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-mono font-medium border transition-all ${className}`, style: {
            backgroundColor: config.bg,
            borderColor: config.border,
            color: config.color,
        }, title: `Trust Class: ${config.label}`, ...props, children: [showIcon && _jsx("span", { className: "text-[11px]", children: config.icon }), _jsx("span", { children: customLabel || config.label })] }));
};
