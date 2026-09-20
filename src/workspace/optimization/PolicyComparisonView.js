import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const PolicyComparisonView = () => {
    const comparisonStats = {
        activePolicy: 'Multi-Objective QDIOP v1.4 (Augmented Chebyshev)',
        baselinePolicy: 'Greedy First-Fit Heuristic',
        sampleSize: 100,
        winRate: 94.0,
        meanUtilityGain: '+22.4%',
        latencyReductionMs: '-420.0ms',
        costSavingsUsd: '+$0.014 / doc',
        regretReduction: '-88.5%',
    };
    const regretPoints = [
        { step: 'M1', instantRegret: 0.042, cumRegret: 0.042 },
        { step: 'M2', instantRegret: 0.018, cumRegret: 0.060 },
        { step: 'M3', instantRegret: 0.012, cumRegret: 0.072 },
        { step: 'M4', instantRegret: 0.008, cumRegret: 0.080 },
        { step: 'M5', instantRegret: 0.005, cumRegret: 0.085 },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\u2696\uFE0F" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Planner Policy Evaluation & Regret Analysis" }), _jsx(Badge, { variant: "success", size: "sm", children: "SUBLINEAR REGRET (O(log T))" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] mt-1", children: "Evaluating active planner version against ex-post oracle decisions and legacy baseline planners." })] }), _jsxs("div", { className: "text-right", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Head-to-Head Win Rate" }), _jsxs("div", { className: "text-2xl font-mono font-extrabold text-emerald-400", children: [comparisonStats.winRate, "%"] })] })] }) }), _jsxs("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-4 text-center font-mono", children: [_jsxs(Card, { className: "p-4 bg-[#0F172A] border border-[#1E293B]", children: [_jsx("div", { className: "text-xs text-[#94A3B8]", children: "Mean Utility Gain" }), _jsx("div", { className: "text-lg font-bold text-emerald-400 mt-1", children: comparisonStats.meanUtilityGain })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border border-[#1E293B]", children: [_jsx("div", { className: "text-xs text-[#94A3B8]", children: "Latency Reduction" }), _jsx("div", { className: "text-lg font-bold text-cyan-400 mt-1", children: comparisonStats.latencyReductionMs })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border border-[#1E293B]", children: [_jsx("div", { className: "text-xs text-[#94A3B8]", children: "Cost Efficiency" }), _jsx("div", { className: "text-lg font-bold text-[#F8FAFC] mt-1", children: comparisonStats.costSavingsUsd })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border border-[#1E293B]", children: [_jsx("div", { className: "text-xs text-[#94A3B8]", children: "Planner Regret Drop" }), _jsx("div", { className: "text-lg font-bold text-emerald-400 mt-1", children: comparisonStats.regretReduction })] })] }), _jsxs(Card, { className: "p-5 bg-[#0F172A] border border-[#1E293B] space-y-3", children: [_jsx("h3", { className: "text-sm font-bold font-mono text-[#F8FAFC]", children: "Instantaneous & Cumulative Regret Trajectory ($R_t = U(\\pi^*) - U(\\pi_t)$)" }), _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left text-xs font-mono", children: [_jsx("thead", { children: _jsxs("tr", { className: "border-b border-[#1E293B] text-[#64748B]", children: [_jsx("th", { className: "pb-2", children: "Mission Horizon" }), _jsx("th", { className: "pb-2", children: "Instantaneous Regret ($r_t$)" }), _jsx("th", { className: "pb-2", children: "Cumulative Regret ($R_T$)" }), _jsx("th", { className: "pb-2", children: "Sublinear Decay Rate" })] }) }), _jsx("tbody", { className: "divide-y divide-[#1E293B]/60", children: regretPoints.map((r) => (_jsxs("tr", { children: [_jsx("td", { className: "py-2.5 text-[#F8FAFC]", children: r.step }), _jsx("td", { className: "py-2.5 text-cyan-400", children: r.instantRegret.toFixed(4) }), _jsx("td", { className: "py-2.5 text-amber-400", children: r.cumRegret.toFixed(4) }), _jsx("td", { className: "py-2.5 text-emerald-400", children: "Converging to 0" })] }, r.step))) })] }) })] })] }));
};
