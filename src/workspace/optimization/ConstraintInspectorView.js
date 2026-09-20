import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const ConstraintInspectorView = () => {
    const constraints = [
        {
            id: 'c_budget',
            name: 'Max Cloud Execution Budget',
            type: 'HARD',
            expression: 'cost_usd <= $0.030',
            limit: '$0.030',
            actual: '$0.012',
            slack: '+$0.018',
            status: 'SATISFIED',
            isBinding: false,
        },
        {
            id: 'c_latency',
            name: 'End-to-End SLA Deadline',
            type: 'HARD',
            expression: 'latency_ms <= 1200ms',
            limit: '1200.0ms',
            actual: '650.0ms',
            slack: '+550.0ms',
            status: 'SATISFIED',
            isBinding: false,
        },
        {
            id: 'c_accuracy',
            name: 'Minimum Verifiable Accuracy',
            type: 'HARD',
            expression: 'accuracy >= 95.0%',
            limit: '95.0%',
            actual: '98.5%',
            slack: '+3.5%',
            status: 'SATISFIED',
            isBinding: true,
        },
        {
            id: 'c_privacy',
            name: 'Zero PII Exfiltration Tier',
            type: 'HARD',
            expression: 'pii_leakage == 0',
            limit: '0 leaks',
            actual: '0 leaks',
            slack: 'Exact',
            status: 'SATISFIED',
            isBinding: true,
        },
        {
            id: 'c_risk',
            name: 'Max Allowable Failure Hazard',
            type: 'SOFT',
            expression: 'overall_risk <= 0.050',
            limit: '0.050',
            actual: '0.020',
            slack: '+0.030',
            status: 'SATISFIED',
            isBinding: false,
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\uD83D\uDEE1\uFE0F" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Deterministic Constraint Solver & Feasibility Space" }), _jsx(Badge, { variant: "success", size: "sm", children: "100% FEASIBLE" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] mt-1", children: "Planners cannot violate hard mathematical or business boundaries. Validating slack variables, shadow prices, and binding constraints." })] }), _jsxs("div", { className: "text-right", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Active Hard Constraints" }), _jsx("div", { className: "text-lg font-mono font-bold text-emerald-400", children: "4 Enforced / 0 Violations" })] })] }) }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: constraints.map((c) => (_jsxs(Card, { className: "p-5 bg-[#0F172A] border border-[#1E293B] space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-bold font-mono text-[#F8FAFC]", children: c.name }), _jsx(Badge, { variant: c.type === 'HARD' ? 'intelligence' : 'outline', size: "sm", children: c.type })] }), _jsx("div", { className: "p-2.5 rounded-lg bg-[#131D35]/60 border border-[#1E293B] font-mono text-xs text-cyan-400", children: c.expression }), _jsxs("div", { className: "grid grid-cols-2 gap-2 text-xs font-mono pt-2", children: [_jsxs("div", { children: [_jsx("span", { className: "text-[#64748B] block text-[10px]", children: "Actual Value" }), _jsx("span", { className: "font-bold text-[#F8FAFC]", children: c.actual })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[#64748B] block text-[10px]", children: "Slack Variable" }), _jsx("span", { className: "font-bold text-emerald-400", children: c.slack })] })] }), _jsxs("div", { className: "flex items-center justify-between pt-2 border-t border-[#1E293B] text-[11px] font-mono", children: [_jsxs("span", { className: "text-emerald-400 flex items-center gap-1", children: [_jsx("span", { className: "h-2 w-2 rounded-full bg-emerald-400" }), " ", c.status] }), c.isBinding && (_jsx("span", { className: "text-amber-400 text-[10px] font-bold", children: "BINDING BOUNDARY" }))] })] }, c.id))) })] }));
};
