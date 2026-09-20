import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { cn } from '../../utils/cn';
export const Timeline = ({ items, orientation = 'vertical', onItemClick, className, ...props }) => {
    const getStatusColor = (status) => {
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
        return (_jsx("div", { className: cn('flex items-center w-full overflow-x-auto py-4', className), ...props, children: items.map((item, index) => {
                const statusStyle = getStatusColor(item.status);
                const isLast = index === items.length - 1;
                return (_jsxs("div", { onClick: () => onItemClick?.(item), className: cn('flex items-center flex-1 min-w-[140px]', onItemClick && 'cursor-pointer group'), children: [_jsxs("div", { className: "flex flex-col items-center", children: [_jsx("div", { className: cn('h-3.5 w-3.5 rounded-full ring-4 transition-all duration-200', statusStyle.dot) }), _jsx("span", { className: "mt-2 text-xs font-medium text-[#F8FAFC] text-center line-clamp-1", children: item.title }), item.timestamp && (_jsx("span", { className: "text-[10px] text-[#64748B] font-mono", children: item.timestamp }))] }), !isLast && _jsx("div", { className: cn('h-0.5 flex-1 mx-2 transition-colors', statusStyle.line) })] }, item.id));
            }) }));
    }
    return (_jsx("div", { className: cn('relative flex flex-col space-y-6', className), ...props, children: items.map((item, index) => {
            const statusStyle = getStatusColor(item.status);
            const isLast = index === items.length - 1;
            return (_jsxs("div", { onClick: () => onItemClick?.(item), className: cn('relative flex items-start gap-3.5 group', onItemClick && 'cursor-pointer'), children: [!isLast && (_jsx("div", { className: cn('absolute top-4 left-[7px] w-0.5 h-[calc(100%+16px)] transition-colors', statusStyle.line) })), _jsx("div", { className: "relative z-10 flex items-center justify-center shrink-0 mt-1", children: item.icon ? (_jsx("div", { className: "h-6 w-6 rounded-full bg-[#131D35] border border-[#334155] flex items-center justify-center text-xs", children: item.icon })) : (_jsx("div", { className: cn('h-3.5 w-3.5 rounded-full ring-4 transition-all duration-200', statusStyle.dot) })) }), _jsxs("div", { className: "flex-1 flex flex-col", children: [_jsxs("div", { className: "flex items-baseline justify-between gap-2", children: [_jsx("span", { className: "text-sm font-medium text-[#F8FAFC] group-hover:text-[#00D2FF] transition-colors", children: item.title }), item.timestamp && (_jsx("span", { className: "text-[11px] text-[#64748B] font-mono shrink-0", children: item.timestamp }))] }), item.description && (_jsx("p", { className: "mt-0.5 text-xs text-[#94A3B8] leading-relaxed", children: item.description })), item.tags && item.tags.length > 0 && (_jsx("div", { className: "flex flex-wrap gap-1 mt-2", children: item.tags.map((tag) => (_jsx("span", { className: "text-[10px] bg-[#1E293B] text-[#94A3B8] px-1.5 py-0.5 rounded border border-[#334155]/60 font-mono", children: tag }, tag))) }))] })] }, item.id));
        }) }));
};
