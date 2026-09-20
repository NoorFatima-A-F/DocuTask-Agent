import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const RiskExplorerView = () => {
    const failureProbabilities = [
        { name: 'P(timeout)', value: 0.018, threshold: 0.05, status: 'LOW' },
        { name: 'P(validation failure)', value: 0.012, threshold: 0.04, status: 'LOW' },
        { name: 'P(OCR degradation)', value: 0.035, threshold: 0.10, status: 'LOW' },
        { name: 'P(retry requirement)', value: 0.024, threshold: 0.08, status: 'LOW' },
        { name: 'P(memory mismatch)', value: 0.015, threshold: 0.05, status: 'LOW' },
        { name: 'P(worker failure)', value: 0.008, threshold: 0.03, status: 'MINIMAL' },
    ];
    const mitigations = [
        {
            id: 'MIT-01',
            target: 'P(OCR degradation)',
            action: 'Auto-enable dual-engine ensemble (PyTesseract + Vision Transformer)',
            reduction: '-65% Risk',
            cost: '+$0.005',
        },
        {
            id: 'MIT-02',
            target: 'P(timeout)',
            action: 'Speculative sub-task branch parallelization with fast Flash fallback',
            reduction: '-70% Risk',
            cost: '-$0.002',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\u26A0\uFE0F" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Scientific Risk Engine & Hazard Modeler" }), _jsx(Badge, { variant: "success", size: "sm", children: "JOINT HAZARD: 2.0%" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] mt-1", children: "Replaces qualitative labels with explicit marginal failure probabilities: $P(timeout)$, $P(validation)$, $P(retry)$." })] }), _jsxs("div", { className: "text-right", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Overall Failure Probability" }), _jsx("div", { className: "text-2xl font-mono font-extrabold text-emerald-400", children: "1.98%" })] })] }) }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: failureProbabilities.map((p) => (_jsxs(Card, { className: "p-4 bg-[#0F172A] border border-[#1E293B] space-y-2", children: [_jsxs("div", { className: "flex justify-between items-center text-xs font-mono", children: [_jsx("span", { className: "text-cyan-400 font-bold", children: p.name }), _jsx(Badge, { variant: "outline", size: "sm", children: p.status })] }), _jsxs("div", { className: "flex justify-between items-baseline pt-1", children: [_jsxs("span", { className: "text-xl font-mono font-bold text-[#F8FAFC]", children: [(p.value * 100).toFixed(2), "%"] }), _jsxs("span", { className: "text-[11px] font-mono text-[#64748B]", children: ["Cap: ", (p.threshold * 100).toFixed(1), "%"] })] }), _jsx("div", { className: "w-full bg-[#131D35] h-1.5 rounded-full overflow-hidden", children: _jsx("div", { className: "bg-emerald-400 h-1.5 rounded-full", style: { width: `${(p.value / p.threshold) * 100}%` } }) })] }, p.name))) }), _jsxs(Card, { className: "p-5 bg-[#0F172A] border border-[#1E293B] space-y-3", children: [_jsxs("h3", { className: "text-sm font-bold font-mono text-[#F8FAFC] flex items-center gap-2", children: [_jsx("span", { children: "\uD83E\uDE79" }), " Prescriptive Dynamic Risk Mitigations"] }), _jsx("div", { className: "space-y-2", children: mitigations.map((m) => (_jsxs("div", { className: "p-3 rounded-xl bg-[#131D35]/50 border border-[#1E293B] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs font-mono", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: "outline", size: "sm", children: m.id }), _jsxs("div", { children: [_jsx("div", { className: "text-cyan-400 font-bold", children: m.target }), _jsx("div", { className: "text-[#94A3B8] font-sans text-[11px]", children: m.action })] })] }), _jsxs("div", { className: "flex items-center gap-3 text-right shrink-0", children: [_jsx("span", { className: "text-emerald-400 font-bold", children: m.reduction }), _jsx("span", { className: "text-[#64748B]", children: m.cost })] })] }, m.id))) })] })] }));
};
