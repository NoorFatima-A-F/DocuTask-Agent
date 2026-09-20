import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const OptimizerExplorerView = () => {
    const [weights, setWeights] = useState({
        accuracy: 0.35,
        latency: 0.20,
        cost: 0.15,
        safety: 0.15,
        reliability: 0.15,
    });
    const candidatePlans = [
        {
            id: 'plan_opt_1',
            name: 'Dynamic Speculative Wavefront',
            accuracy: 0.985,
            latencyMs: 650,
            costUsd: 0.012,
            risk: 0.02,
            chebyshevUtility: 0.942,
            weightedUtility: 0.958,
            isPareto: true,
            status: 'SELECTED_OPTIMAL',
        },
        {
            id: 'plan_opt_2',
            name: 'Max-Accuracy Gemini Pro Serial',
            accuracy: 0.995,
            latencyMs: 2400,
            costUsd: 0.045,
            risk: 0.01,
            chebyshevUtility: 0.812,
            weightedUtility: 0.865,
            isPareto: true,
            status: 'PARETO_FRONTIER',
        },
        {
            id: 'plan_opt_3',
            name: 'Low-Cost Flash-Lite Batch',
            accuracy: 0.912,
            latencyMs: 320,
            costUsd: 0.002,
            risk: 0.08,
            chebyshevUtility: 0.835,
            weightedUtility: 0.884,
            isPareto: true,
            status: 'PARETO_FRONTIER',
        },
        {
            id: 'plan_opt_4',
            name: 'Heuristic Greedy Baseline',
            accuracy: 0.935,
            latencyMs: 1450,
            costUsd: 0.028,
            risk: 0.06,
            chebyshevUtility: 0.724,
            weightedUtility: 0.762,
            isPareto: false,
            status: 'DOMINATED',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\u26A1" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Multi-Objective Optimizer & Plan Selector" }), _jsx(Badge, { variant: "success", size: "sm", children: "AUGMENTED CHEBYSHEV" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] mt-1", children: "Deterministic scalarization solving $argmax\\ U(plan)$ subject to budget, latency, and compliance bounds." })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsx(Badge, { variant: "intelligence", size: "sm", children: "Deterministic Seed Verified" }) })] }), _jsx("div", { className: "mt-6 pt-4 border-t border-[#1E293B] grid grid-cols-2 md:grid-cols-5 gap-4", children: Object.entries(weights).map(([key, val]) => (_jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex justify-between text-[11px] font-mono", children: [_jsx("span", { className: "capitalize text-[#94A3B8]", children: key }), _jsxs("span", { className: "text-cyan-400 font-bold", children: [(val * 100).toFixed(0), "%"] })] }), _jsx("input", { type: "range", min: "0.05", max: "0.80", step: "0.05", value: val, onChange: (e) => setWeights({ ...weights, [key]: parseFloat(e.target.value) }), className: "w-full accent-cyan-400 h-1 bg-[#131D35] rounded-lg appearance-none cursor-pointer" })] }, key))) })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: candidatePlans.map((plan) => (_jsxs(Card, { className: `p-5 bg-[#0F172A] border transition-all ${plan.status === 'SELECTED_OPTIMAL'
                        ? 'border-emerald-500/70 shadow-[0_0_20px_rgba(16,185,129,0.15)] ring-1 ring-emerald-500/50'
                        : plan.isPareto
                            ? 'border-cyan-500/40'
                            : 'border-[#1E293B] opacity-70'}`, children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono font-bold text-[#F8FAFC]", children: plan.name }), plan.status === 'SELECTED_OPTIMAL' && (_jsx(Badge, { variant: "success", size: "sm", children: "OPTIMAL WINNER" })), plan.status === 'PARETO_FRONTIER' && (_jsx(Badge, { variant: "outline", size: "sm", children: "PARETO OPTIMAL" })), plan.status === 'DOMINATED' && (_jsx(Badge, { variant: "warning", size: "sm", children: "DOMINATED PLAN" }))] }), _jsxs("div", { className: "text-[11px] font-mono text-[#64748B] mt-0.5", children: ["ID: ", plan.id] })] }), _jsxs("div", { className: "text-right", children: [_jsx("div", { className: "text-[10px] text-[#94A3B8]", children: "Scalar Utility" }), _jsx("div", { className: "text-base font-mono font-extrabold text-cyan-400", children: plan.weightedUtility.toFixed(3) })] })] }), _jsxs("div", { className: "grid grid-cols-4 gap-2 mt-4 pt-3 border-t border-[#1E293B] text-center text-xs font-mono", children: [_jsxs("div", { className: "bg-[#131D35]/50 p-2 rounded-lg", children: [_jsx("div", { className: "text-[10px] text-[#64748B]", children: "Accuracy" }), _jsxs("div", { className: "font-bold text-emerald-400", children: [(plan.accuracy * 100).toFixed(1), "%"] })] }), _jsxs("div", { className: "bg-[#131D35]/50 p-2 rounded-lg", children: [_jsx("div", { className: "text-[10px] text-[#64748B]", children: "Latency" }), _jsxs("div", { className: "font-bold text-cyan-400", children: [plan.latencyMs, "ms"] })] }), _jsxs("div", { className: "bg-[#131D35]/50 p-2 rounded-lg", children: [_jsx("div", { className: "text-[10px] text-[#64748B]", children: "Cost" }), _jsxs("div", { className: "font-bold text-[#F8FAFC]", children: ["$", plan.costUsd.toFixed(3)] })] }), _jsxs("div", { className: "bg-[#131D35]/50 p-2 rounded-lg", children: [_jsx("div", { className: "text-[10px] text-[#64748B]", children: "Risk P(Fail)" }), _jsxs("div", { className: "font-bold text-amber-400", children: [(plan.risk * 100).toFixed(1), "%"] })] })] })] }, plan.id))) })] }));
};
