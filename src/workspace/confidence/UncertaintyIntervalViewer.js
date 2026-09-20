import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { HelpCircle, Percent } from 'lucide-react';
const intervals = [
    {
        dimension: 'Overall Mission Confidence',
        mean: 98.42,
        ci95Low: 96.97,
        ci95High: 99.87,
        ci99Low: 96.25,
        ci99High: 99.98,
        aleatoric: 0.008,
        epistemic: 0.006,
    },
    {
        dimension: 'OCR Quality',
        mean: 99.20,
        ci95Low: 98.40,
        ci95High: 100.00,
        ci99Low: 97.90,
        ci99High: 100.00,
        aleatoric: 0.005,
        epistemic: 0.003,
    },
    {
        dimension: 'Schema Extraction',
        mean: 98.00,
        ci95Low: 96.80,
        ci95High: 99.20,
        ci99Low: 96.10,
        ci99High: 99.70,
        aleatoric: 0.009,
        epistemic: 0.004,
    },
    {
        dimension: 'Invariant Validation',
        mean: 99.90,
        ci95Low: 99.80,
        ci95High: 100.00,
        ci99Low: 99.70,
        ci99High: 100.00,
        aleatoric: 0.001,
        epistemic: 0.000,
    },
    {
        dimension: 'Planner Efficiency',
        mean: 95.00,
        ci95Low: 92.90,
        ci95High: 97.10,
        ci99Low: 91.80,
        ci99High: 98.20,
        aleatoric: 0.015,
        epistemic: 0.006,
    },
];
export const UncertaintyIntervalViewer = () => {
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsx("div", { className: "space-y-1", children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-violet-500/20 to-purple-500/20 border border-violet-500/30 rounded-xl text-violet-400", children: _jsx(Percent, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Uncertainty Intervals & Variance Decomposition", _jsx(Badge, { variant: "intelligence", size: "sm", children: "Aleatoric vs Epistemic" })] }), _jsx("p", { className: "text-xs text-slate-400", children: "Rigorous statistical confidence intervals (95% & 99%) and uncertainty variance decomposition." })] })] }) }), _jsx("div", { className: "flex items-center gap-3", children: _jsx(Badge, { variant: "success", size: "sm", children: "Bounds Narrow & Stable" }) })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: [_jsxs(Card, { className: "p-5 bg-[#0F172A] border-[#1E293B]", children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx("span", { className: "text-xs font-mono font-bold text-violet-400", children: "Aleatoric Uncertainty (Data / Noise)" }), _jsx(Badge, { variant: "outline", size: "sm", children: "0.008 Total" })] }), _jsx("p", { className: "text-xs text-slate-400", children: "Irreducible noise present in environment observations, tool responses, and document scans." })] }), _jsxs(Card, { className: "p-5 bg-[#0F172A] border-[#1E293B]", children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx("span", { className: "text-xs font-mono font-bold text-indigo-400", children: "Epistemic Uncertainty (Model / Knowledge)" }), _jsx(Badge, { variant: "success", size: "sm", children: "0.006 Total (Low)" })] }), _jsx("p", { className: "text-xs text-slate-400", children: "Reducible uncertainty due to lack of training/calibration data or missing runtime context." })] })] }), _jsxs(Card, { className: "p-5 bg-[#0F172A] border-[#1E293B]", children: [_jsxs("div", { className: "flex items-center justify-between mb-4", children: [_jsx("h2", { className: "text-sm font-bold font-mono text-slate-200", children: "Dimension Confidence Intervals" }), _jsxs("span", { className: "text-xs text-slate-500 font-mono flex items-center gap-1", children: [_jsx(HelpCircle, { className: "w-3.5 h-3.5" }), " Normal Gaussian Projection"] })] }), _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left text-xs font-mono", children: [_jsx("thead", { className: "bg-[#1E293B]/60 text-slate-400 border-b border-[#1E293B]", children: _jsxs("tr", { children: [_jsx("th", { className: "p-3", children: "Dimension" }), _jsx("th", { className: "p-3", children: "Mean (\u03BC)" }), _jsx("th", { className: "p-3", children: "95% CI Range" }), _jsx("th", { className: "p-3", children: "99% CI Range" }), _jsx("th", { className: "p-3", children: "Aleatoric" }), _jsx("th", { className: "p-3", children: "Epistemic" }), _jsx("th", { className: "p-3", children: "Total Width" })] }) }), _jsx("tbody", { className: "divide-y divide-[#1E293B]/40", children: intervals.map((item, idx) => (_jsxs("tr", { className: "hover:bg-slate-800/30 transition-colors", children: [_jsx("td", { className: "p-3 font-semibold text-slate-100", children: item.dimension }), _jsxs("td", { className: "p-3 text-cyan-400 font-bold", children: [item.mean.toFixed(2), "%"] }), _jsxs("td", { className: "p-3 text-emerald-400", children: ["[", item.ci95Low.toFixed(2), "%, ", item.ci95High.toFixed(2), "%]"] }), _jsxs("td", { className: "p-3 text-indigo-300", children: ["[", item.ci99Low.toFixed(2), "%, ", item.ci99High.toFixed(2), "%]"] }), _jsx("td", { className: "p-3 text-slate-400", children: item.aleatoric.toFixed(4) }), _jsx("td", { className: "p-3 text-slate-400", children: item.epistemic.toFixed(4) }), _jsxs("td", { className: "p-3 text-slate-200", children: ["\u00B1", ((item.ci95High - item.mean)).toFixed(2), "%"] })] }, idx))) })] }) })] })] }));
};
