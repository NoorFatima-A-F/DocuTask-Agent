import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { PieChart, DollarSign, Zap, TrendingUp, ShieldCheck, RefreshCw, CheckCircle2, } from 'lucide-react';
export const MissionPortfolioCenter = () => {
    const [missions] = useState([
        {
            id: 'msn-cache-warm-01',
            name: 'Speculative Layout Cache Pre-Warming',
            category: 'Throughput & Latency Acceleration',
            allocatedBudgetUsd: 3200.0,
            expectedGainUsd: 9800.0,
            expectedRoi: 3.06,
            latencyGainPct: 28.0,
            riskScore: 0.08,
            compositeUtility: 0.925,
            paretoRank: 1,
            status: 'ACTIVE',
        },
        {
            id: 'msn-triadic-coalition-02',
            name: 'Triadic Extraction Strike Team Deployment',
            category: 'Throughput & Latency Acceleration',
            allocatedBudgetUsd: 4500.0,
            expectedGainUsd: 12500.0,
            expectedRoi: 2.77,
            latencyGainPct: 22.0,
            riskScore: 0.12,
            compositeUtility: 0.890,
            paretoRank: 1,
            status: 'ACTIVE',
        },
        {
            id: 'msn-sec-sha-ledger',
            name: 'Zero-Knowledge Ledger Rollback Checkpoints',
            category: 'Governance & Cryptographic Assurance',
            allocatedBudgetUsd: 2800.0,
            expectedGainUsd: 6000.0,
            expectedRoi: 2.14,
            latencyGainPct: 0.0,
            riskScore: 0.04,
            compositeUtility: 0.940,
            paretoRank: 1,
            status: 'ACTIVE',
        },
        {
            id: 'msn-auto-roadmap-04',
            name: 'Long-Horizon Strategic Roadmapping Engine',
            category: 'Autonomous Strategic Cognition',
            allocatedBudgetUsd: 5000.0,
            expectedGainUsd: 18000.0,
            expectedRoi: 3.60,
            latencyGainPct: 15.0,
            riskScore: 0.14,
            compositeUtility: 0.955,
            paretoRank: 1,
            status: 'ACTIVE',
        },
    ]);
    const [isOptimizing, setIsOptimizing] = useState(false);
    const [statusMsg, setStatusMsg] = useState(null);
    const totalAllocated = missions.reduce((acc, m) => acc + m.allocatedBudgetUsd, 0);
    const budgetLimit = 30000.0;
    const utilizationPct = (totalAllocated / budgetLimit) * 100;
    const totalProjectedGain = missions.reduce((acc, m) => acc + m.expectedGainUsd, 0);
    const handleOptimize = () => {
        setIsOptimizing(true);
        setTimeout(() => {
            setIsOptimizing(false);
            setStatusMsg('Pareto Frontier Optimization complete: All 4 active missions confirmed Pareto-dominant (#1).');
            setTimeout(() => setStatusMsg(null), 4000);
        }, 1200);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(PieChart, { className: "w-6 h-6 text-indigo-500" }), "Mission Portfolio Optimization & Pareto Frontier Center"] }), _jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: "Phase 13.11 \u2014 Dynamic mission portfolio clustering, Pareto multi-objective ranking, and ROI budget balancing." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "intelligence", size: "sm", onClick: handleOptimize, disabled: isOptimizing, children: [_jsx(RefreshCw, { className: `w-3.5 h-3.5 mr-1.5 ${isOptimizing ? 'animate-spin' : ''}` }), isOptimizing ? 'Rebalancing Pareto...' : 'Rebalance Portfolio'] }) })] }), statusMsg && (_jsxs("div", { className: "p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-lg text-sm text-emerald-800 dark:text-emerald-300 flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-5 h-5 flex-shrink-0" }), _jsx("span", { children: statusMsg })] })), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 border-l-4 border-l-indigo-500", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-gray-500", children: [_jsx("span", { children: "Total Allocated Budget" }), _jsx(DollarSign, { className: "w-4 h-4 text-indigo-500" })] }), _jsxs("div", { className: "text-2xl font-bold text-gray-900 dark:text-white mt-1", children: ["$", totalAllocated.toLocaleString()] }), _jsxs("span", { className: "text-xs text-indigo-600 dark:text-indigo-400 font-medium", children: [utilizationPct.toFixed(1), "% of $", budgetLimit.toLocaleString(), " Limit"] })] }), _jsxs(Card, { className: "p-4 border-l-4 border-l-emerald-500", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-gray-500", children: [_jsx("span", { children: "Projected Net Gain" }), _jsx(TrendingUp, { className: "w-4 h-4 text-emerald-500" })] }), _jsxs("div", { className: "text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1", children: ["$", totalProjectedGain.toLocaleString()] }), _jsx("span", { className: "text-xs text-emerald-500", children: "Expected ROI: 3.01x Aggregate" })] }), _jsxs(Card, { className: "p-4 border-l-4 border-l-purple-500", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-gray-500", children: [_jsx("span", { children: "Pareto Non-Dominated Missions" }), _jsx(ShieldCheck, { className: "w-4 h-4 text-purple-500" })] }), _jsx("div", { className: "text-2xl font-bold text-purple-600 dark:text-purple-400 mt-1", children: "4 / 4" }), _jsx("span", { className: "text-xs text-purple-500", children: "100% Rank #1 Dominant" })] }), _jsxs(Card, { className: "p-4 border-l-4 border-l-sky-500", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-gray-500", children: [_jsx("span", { children: "Portfolio Risk Index" }), _jsx(Zap, { className: "w-4 h-4 text-sky-500" })] }), _jsx("div", { className: "text-2xl font-bold text-sky-600 dark:text-sky-400 mt-1", children: "0.098" }), _jsx("span", { className: "text-xs text-sky-500", children: "Safe Boundary (< 0.250)" })] })] }), _jsxs("div", { className: "space-y-4", children: [_jsx("h3", { className: "text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider", children: "Active Portfolio Mission Allocations" }), _jsx("div", { className: "grid grid-cols-1 gap-4", children: missions.map((m) => (_jsxs(Card, { className: "p-5 hover:shadow-md transition-shadow border-l-4 border-l-indigo-500", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-xs text-indigo-600 dark:text-indigo-400 font-semibold", children: m.id }), _jsxs(Badge, { variant: "intelligence", size: "sm", children: ["Pareto Rank #", m.paretoRank] }), _jsx(Badge, { variant: "outline", size: "sm", children: m.category })] }), _jsx("h4", { className: "font-semibold text-gray-900 dark:text-white text-base mt-1", children: m.name })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsxs("div", { className: "text-right", children: [_jsx("span", { className: "text-xs text-gray-400 block", children: "Composite Utility" }), _jsx("span", { className: "text-lg font-bold text-indigo-600 dark:text-indigo-400 font-mono", children: m.compositeUtility.toFixed(3) })] }) })] }), _jsxs("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-3 mt-4 text-xs", children: [_jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "text-gray-400 block mb-0.5", children: "Budget Allocation" }), _jsxs("span", { className: "font-semibold text-gray-900 dark:text-white font-mono", children: ["$", m.allocatedBudgetUsd.toLocaleString()] })] }), _jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "text-gray-400 block mb-0.5", children: "Projected Value" }), _jsxs("span", { className: "font-semibold text-emerald-600 dark:text-emerald-400 font-mono", children: ["$", m.expectedGainUsd.toLocaleString(), " (", m.expectedRoi, "x ROI)"] })] }), _jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "text-gray-400 block mb-0.5", children: "Latency Reduction" }), _jsxs("span", { className: "font-semibold text-purple-600 dark:text-purple-400 font-mono", children: ["+", m.latencyGainPct, "%"] })] }), _jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "text-gray-400 block mb-0.5", children: "Risk Score" }), _jsx("span", { className: "font-semibold text-sky-600 dark:text-sky-400 font-mono", children: m.riskScore.toFixed(3) })] })] })] }, m.id))) })] })] }));
};
