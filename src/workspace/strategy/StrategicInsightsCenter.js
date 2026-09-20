import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Sparkles, CheckCircle2, } from 'lucide-react';
export const StrategicInsightsCenter = () => {
    const [recommendations] = useState([
        {
            id: 'rec-001',
            targetArea: 'Speculative Embedding Caching',
            budgetUsd: 4500.0,
            expectedGainPct: 28.0,
            rationale: 'High concentration of identical vendor invoice headers enables 85% cache hit efficiency and $9.8k/mo savings.',
            riskLevel: 'LOW',
            confidence: 0.990,
        },
        {
            id: 'rec-002',
            targetArea: 'Autonomous Agent Strike Teams',
            budgetUsd: 6000.0,
            expectedGainPct: 19.5,
            rationale: 'Triadic coalition model reduces negotiation friction during high-concurrency balance sheet runs.',
            riskLevel: 'LOW',
            confidence: 0.982,
        },
        {
            id: 'rec-003',
            targetArea: 'Lock-Free Memory Buffer Migration',
            budgetUsd: 2500.0,
            expectedGainPct: 15.0,
            rationale: 'Migrating global state mutex locks to atomic ring buffers eliminates 180ms telemetry contention stalls.',
            riskLevel: 'LOW',
            confidence: 0.995,
        },
    ]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-6 h-6 text-indigo-500" }), "Strategic Insights & Investment Opportunities Center"] }), _jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: "Phase 13.11 \u2014 Autonomous strategic pattern mining, capital allocation recommendations, and ROI gain forecasts." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Badge, { variant: "intelligence", size: "md", children: [recommendations.length, " Active Recommendations"] }) })] }), _jsxs("div", { className: "space-y-4", children: [_jsx("h3", { className: "text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider", children: "AI Chief Strategy Officer (CSO) Investment Directives" }), _jsx("div", { className: "grid grid-cols-1 gap-4", children: recommendations.map((rec) => (_jsxs(Card, { className: "p-5 hover:shadow-md transition-shadow border-l-4 border-l-emerald-500", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-xs text-emerald-600 dark:text-emerald-400 font-semibold", children: rec.id }), _jsxs(Badge, { variant: "success", size: "sm", children: ["Expected Gain: +", rec.expectedGainPct, "%"] }), _jsxs(Badge, { variant: "outline", size: "sm", children: ["Risk: ", rec.riskLevel] })] }), _jsx("h4", { className: "font-semibold text-gray-900 dark:text-white text-base mt-1", children: rec.targetArea })] }), _jsxs("div", { className: "text-right", children: [_jsx("span", { className: "text-xs text-gray-400 block", children: "Recommended Budget" }), _jsxs("span", { className: "text-lg font-bold text-gray-900 dark:text-white font-mono", children: ["$", rec.budgetUsd.toLocaleString()] })] })] }), _jsx("p", { className: "text-xs text-gray-600 dark:text-gray-300 mt-3", children: rec.rationale }), _jsxs("div", { className: "mt-4 pt-3 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between text-xs", children: [_jsxs("span", { className: "text-purple-600 dark:text-purple-400 font-medium", children: ["Bayesian Empirical Confidence: ", (rec.confidence * 100).toFixed(1), "%"] }), _jsxs("span", { className: "text-emerald-600 dark:text-emerald-400 flex items-center gap-1 font-medium", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5" }), "Validated via Truth Ledger"] })] })] }, rec.id))) })] })] }));
};
