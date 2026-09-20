import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Layers } from 'lucide-react';
export const StrategyComparisonStudio = () => {
    const [selectedObjective, setSelectedObjective] = useState('BALANCED_UTILITY');
    const strategies = [
        {
            id: 'strat-01',
            name: 'Budget Sequential Plan',
            model: 'gemini-1.5-flash',
            ocr: 'TESSERACT_FAST',
            concurrency: 1,
            costUsd: 0.0018,
            latencyMs: 4200,
            confidence: 0.960,
            utility: 0.88,
            isWinner: selectedObjective === 'MINIMIZE_COST',
        },
        {
            id: 'strat-02',
            name: 'High-Throughput Wavefront',
            model: 'gemini-1.5-flash',
            ocr: 'TESSERACT_FAST',
            concurrency: 6,
            costUsd: 0.0032,
            latencyMs: 1850,
            confidence: 0.965,
            utility: 0.945,
            isWinner: selectedObjective === 'BALANCED_UTILITY' || selectedObjective === 'MINIMIZE_LATENCY',
        },
        {
            id: 'strat-03',
            name: 'High-Reasoning Invariant Plan',
            model: 'gemini-1.5-pro',
            ocr: 'DOCUMENT_AI_ADVANCED',
            concurrency: 4,
            costUsd: 0.0120,
            latencyMs: 3100,
            confidence: 0.992,
            utility: 0.91,
            isWinner: selectedObjective === 'MAXIMIZE_CONFIDENCE',
        },
    ];
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-purple-500/20 to-indigo-500/20 border border-purple-500/30 rounded-xl text-purple-400", children: _jsx(Layers, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Strategy Comparison Studio", _jsx(Badge, { variant: "intelligence", size: "sm", children: "Phase 13.6 ARIA-EOP" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] font-mono", children: "Multi-dimensional Pareto frontier comparison across cost, latency, confidence, and resource footprint" })] })] }), _jsxs("select", { value: selectedObjective, onChange: (e) => setSelectedObjective(e.target.value), className: "bg-[#0F172A] border border-[#334155] rounded-lg px-3 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-purple-500", children: [_jsx("option", { value: "BALANCED_UTILITY", children: "Objective: Balanced Utility" }), _jsx("option", { value: "MINIMIZE_COST", children: "Objective: Minimize Cost" }), _jsx("option", { value: "MINIMIZE_LATENCY", children: "Objective: Minimize Latency" }), _jsx("option", { value: "MAXIMIZE_CONFIDENCE", children: "Objective: Maximize Confidence" })] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-6 font-mono", children: strategies.map((strat) => (_jsxs(Card, { className: `p-5 rounded-2xl border space-y-4 flex flex-col justify-between ${strat.isWinner
                        ? 'border-indigo-500/60 bg-gradient-to-br from-[#0F172A] to-[#151B38] shadow-[0_0_20px_rgba(99,102,241,0.2)]'
                        : 'border-[#1E293B] bg-[#0F172A]'}`, children: [_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between gap-2", children: [_jsx("span", { className: "text-xs text-[#64748B]", children: strat.id }), strat.isWinner ? (_jsx(Badge, { variant: "success", size: "sm", children: "WINNING STRATEGY" })) : (_jsx(Badge, { variant: "outline", size: "sm", children: "Candidate" }))] }), _jsxs("div", { children: [_jsx("h3", { className: "text-sm font-bold text-white", children: strat.name }), _jsxs("span", { className: "text-xs text-indigo-400 font-bold block mt-0.5", children: ["Utility: ", strat.utility] })] }), _jsxs("div", { className: "space-y-2 text-xs pt-2 border-t border-[#1E293B]", children: [_jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Model:" }), _jsx("span", { className: "text-white font-bold", children: strat.model })] }), _jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "OCR Engine:" }), _jsx("span", { className: "text-cyan-400 font-bold", children: strat.ocr })] }), _jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Estimated Cost:" }), _jsxs("span", { className: "text-emerald-400 font-bold", children: ["$", strat.costUsd.toFixed(4)] })] }), _jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Latency:" }), _jsxs("span", { className: "text-amber-400 font-bold", children: [strat.latencyMs, " ms"] })] }), _jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Confidence:" }), _jsxs("span", { className: "text-teal-400 font-bold", children: [(strat.confidence * 100).toFixed(1), "%"] })] })] })] }), _jsxs("div", { className: "pt-3 border-t border-[#1E293B] flex items-center justify-between text-xs text-[#64748B]", children: [_jsxs("span", { children: ["Workers: ", strat.concurrency] }), _jsx("span", { className: "text-indigo-400 font-bold", children: "Pareto Feasible" })] })] }, strat.id))) })] }));
};
