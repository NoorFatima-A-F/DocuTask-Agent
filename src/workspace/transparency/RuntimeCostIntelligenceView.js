import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const RuntimeCostIntelligenceView = () => {
    const modelBreakdowns = [
        {
            model: 'Gemini 2.5 Flash',
            role: 'High-Throughput Structured Extraction',
            inputTokens: '2,200',
            outputTokens: '650',
            cachedTokens: '1,000 (45%)',
            cost: '$0.00185',
            cacheSavings: '$0.00006',
            energyKwh: '0.00085 kWh',
            co2Grams: '0.32 g',
            pctTotal: '77.0%',
        },
        {
            model: 'Gemini Flash-Lite',
            role: 'Cross-Validation & Invariant Checking',
            inputTokens: '600',
            outputTokens: '150',
            cachedTokens: '400 (66%)',
            cost: '$0.00035',
            cacheSavings: '$0.00002',
            energyKwh: '0.00022 kWh',
            co2Grams: '0.08 g',
            pctTotal: '14.5%',
        },
        {
            model: 'Local LayoutLM / Tesseract',
            role: 'Zero API Token OCR Preprocessing',
            inputTokens: '800',
            outputTokens: '300',
            cachedTokens: '0 (0%)',
            cost: '$0.00020 (Compute)',
            cacheSavings: '$0.00000',
            energyKwh: '0.00033 kWh',
            co2Grams: '0.12 g',
            pctTotal: '8.5%',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsx("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\uD83D\uDCB0" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Runtime Cost & Carbon Energy Intelligence" }), _jsx(Badge, { variant: "success", size: "sm", children: "DYNAMIC PARETO GOVERNED" })] }), _jsx("p", { className: "text-sm font-mono text-[#94A3B8] mt-1", children: "Multi-dimensional cost accounting per tool, model, prompt cache hits, and datacenter energy footprints." })] }) }) }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Total Net Mission Cost" }), _jsx("div", { className: "text-2xl font-bold font-mono text-emerald-400 mt-1", children: "$0.00240" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "Budget Ceiling: $0.01000 (24% utilized)" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Prompt Cache Savings" }), _jsx("div", { className: "text-2xl font-bold font-mono text-cyan-400 mt-1", children: "+$0.00008" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "3.2% net discount from prefix cache" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Total Tokens Consumed" }), _jsx("div", { className: "text-2xl font-bold font-mono text-indigo-400 mt-1", children: "4,700 tokens" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "Input: 3,600 \u2022 Output: 1,100" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Estimated Compute Carbon" }), _jsx("div", { className: "text-2xl font-bold font-mono text-emerald-400 mt-1", children: "0.52 g CO\u2082" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "0.0014 kWh cluster energy" })] })] }), _jsxs(Card, { className: "p-6 bg-[#0F172A] border-[#1E293B]", children: [_jsx("h3", { className: "text-sm font-bold font-mono text-[#F8FAFC] mb-4", children: "Subsystem Token, Financial & Environmental Matrix" }), _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left font-mono text-xs", children: [_jsx("thead", { children: _jsxs("tr", { className: "border-b border-[#1E293B] text-[#94A3B8]", children: [_jsx("th", { className: "pb-3", children: "Model & Role" }), _jsx("th", { className: "pb-3", children: "Input / Output Tokens" }), _jsx("th", { className: "pb-3", children: "Cached Tokens" }), _jsx("th", { className: "pb-3", children: "Net Cost" }), _jsx("th", { className: "pb-3", children: "Cache Savings" }), _jsx("th", { className: "pb-3", children: "Carbon (CO\u2082)" }), _jsx("th", { className: "pb-3", children: "Share" })] }) }), _jsx("tbody", { className: "divide-y divide-[#1E293B]", children: modelBreakdowns.map((m, idx) => (_jsxs("tr", { className: "hover:bg-[#1E293B]/40 transition-colors", children: [_jsxs("td", { className: "py-3", children: [_jsx("div", { className: "font-bold text-[#F8FAFC]", children: m.model }), _jsx("div", { className: "text-[#64748B] text-[11px]", children: m.role })] }), _jsxs("td", { className: "py-3 text-[#E2E8F0]", children: [m.inputTokens, " in / ", m.outputTokens, " out"] }), _jsx("td", { className: "py-3 text-cyan-400", children: m.cachedTokens }), _jsx("td", { className: "py-3 text-emerald-400 font-bold", children: m.cost }), _jsx("td", { className: "py-3 text-cyan-400", children: m.cacheSavings }), _jsx("td", { className: "py-3 text-[#94A3B8]", children: m.co2Grams }), _jsx("td", { className: "py-3 text-indigo-400 font-bold", children: m.pctTotal })] }, idx))) })] }) })] })] }));
};
