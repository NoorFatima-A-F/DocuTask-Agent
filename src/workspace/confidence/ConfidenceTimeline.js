import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Clock, TrendingUp, ArrowRight, ShieldCheck, CheckCircle2 } from 'lucide-react';
const timelineData = [
    {
        step: 1,
        time: '22:45:00',
        label: 'Prior Initialization',
        dimension: 'All Dimensions',
        scoreBefore: 50.0,
        scoreAfter: 85.0,
        delta: 35.0,
        triggerEvent: 'dag.init',
        confidenceInterval: '[80.0%, 90.0%]',
    },
    {
        step: 2,
        time: '22:45:08',
        label: 'OCR Parsing Complete',
        dimension: 'OCR Quality',
        scoreBefore: 85.0,
        scoreAfter: 94.2,
        delta: 9.2,
        triggerEvent: 'ocr.completed',
        confidenceInterval: '[92.5%, 95.9%]',
    },
    {
        step: 3,
        time: '22:45:15',
        label: 'Schema Validation Succeeded',
        dimension: 'Schema Extraction',
        scoreBefore: 94.2,
        scoreAfter: 97.5,
        delta: 3.3,
        triggerEvent: 'schema.validated',
        confidenceInterval: '[96.2%, 98.8%]',
    },
    {
        step: 4,
        time: '22:45:21',
        label: 'Invariant Verification Passed',
        dimension: 'Invariant Validation',
        scoreBefore: 97.5,
        scoreAfter: 98.42,
        delta: 0.92,
        triggerEvent: 'ledger.invariants.ok',
        confidenceInterval: '[97.8%, 99.0%]',
    },
];
export const ConfidenceTimeline = () => {
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsx("div", { className: "space-y-1", children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 rounded-xl text-indigo-400", children: _jsx(Clock, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Confidence Progression Timeline", _jsx(Badge, { variant: "intelligence", size: "sm", children: "Bayesian Update Flow" })] }), _jsx("p", { className: "text-xs text-slate-400", children: "Step-by-step evidence accumulation and posterior confidence calculation over execution lifecycle." })] })] }) }), _jsx("div", { className: "flex items-center gap-3", children: _jsx(Badge, { variant: "success", size: "sm", children: "Converged: 98.42%" }) })] }), _jsx("div", { className: "space-y-4", children: timelineData.map((ev, idx) => (_jsx(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B] hover:border-indigo-500/40 transition-all", children: _jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4", children: [_jsxs("div", { className: "flex items-center gap-4", children: [_jsxs("div", { className: "flex flex-col items-center justify-center w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 font-mono font-bold text-sm", children: ["#", ev.step] }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-semibold text-slate-100 text-sm", children: ev.label }), _jsx(Badge, { variant: "outline", size: "sm", children: ev.dimension }), _jsxs("span", { className: "text-xs text-slate-500 font-mono", children: ["@", ev.time] })] }), _jsxs("div", { className: "text-xs text-slate-400 font-mono mt-1 flex items-center gap-2", children: [_jsxs("span", { children: ["Trigger: ", _jsx("span", { className: "text-indigo-300", children: ev.triggerEvent })] }), _jsx("span", { children: "\u2022" }), _jsxs("span", { children: ["95% CI: ", _jsx("span", { className: "text-slate-300", children: ev.confidenceInterval })] })] })] })] }), _jsxs("div", { className: "flex items-center gap-6", children: [_jsxs("div", { className: "text-right font-mono", children: [_jsxs("div", { className: "text-xs text-slate-400 flex items-center gap-1.5 justify-end", children: [_jsxs("span", { children: [ev.scoreBefore.toFixed(1), "%"] }), _jsx(ArrowRight, { className: "w-3 h-3 text-slate-500" }), _jsxs("span", { className: "text-indigo-400 font-bold text-sm", children: [ev.scoreAfter.toFixed(2), "%"] })] }), _jsxs("div", { className: "text-[11px] text-emerald-400 font-semibold flex items-center gap-1 justify-end mt-0.5", children: [_jsx(TrendingUp, { className: "w-3 h-3" }), "+", ev.delta.toFixed(2), "%"] })] }), idx === timelineData.length - 1 ? (_jsxs(Badge, { variant: "success", size: "sm", className: "flex items-center gap-1", children: [_jsx(ShieldCheck, { className: "w-3 h-3" }), "Final"] })) : (_jsxs(Badge, { variant: "info", size: "sm", className: "flex items-center gap-1", children: [_jsx(CheckCircle2, { className: "w-3 h-3" }), "Passed"] }))] })] }) }, ev.step))) })] }));
};
