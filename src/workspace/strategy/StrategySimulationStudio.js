import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { FlaskConical, CheckCircle2, RefreshCw, } from 'lucide-react';
export const StrategySimulationStudio = () => {
    const [simulations, setSimulations] = useState([
        {
            id: 'sim-surge-3x-opt',
            name: 'Q4 Year-End 300% Invoicing Peak Surge',
            horizon: 'DAYS_90',
            budgetDeltaUsd: 6000.0,
            workerDelta: 12,
            cacheHitPct: 88.0,
            trafficGrowthPct: 300.0,
            expectedRoi: 4.20,
            expectedP95Ms: 195.0,
            expectedThroughputQps: 3200.0,
            riskScore: 0.065,
            actions: [
                'Deploy +12 pre-warmed worker replicas across AWS us-east-1 and us-west-2.',
                'Activate aggressive 88% speculative tensor caching on corporate schemas.',
                'Enable triadic agent coalitions on balance sheet queue.',
            ],
        },
        {
            id: 'sim-budget-cut-opt',
            name: 'Operational Efficiency & -20% Cost Constraint',
            horizon: 'DAYS_180',
            budgetDeltaUsd: -4000.0,
            workerDelta: -2,
            cacheHitPct: 92.0,
            trafficGrowthPct: 50.0,
            expectedRoi: 3.10,
            expectedP95Ms: 260.0,
            expectedThroughputQps: 1800.0,
            riskScore: 0.120,
            actions: [
                'Maximize lock-free memory ring buffer cache utilization to 92%.',
                'Consolidate idle night-time worker nodes into spot instances.',
            ],
        },
    ]);
    const [isSimulating, setIsSimulating] = useState(false);
    const [notice, setNotice] = useState(null);
    const handleRunNewSim = () => {
        setIsSimulating(true);
        setTimeout(() => {
            const newSim = {
                id: `sim-new-${Date.now().toString().slice(-4)}`,
                name: 'Autonomous Multi-Datacenter Federation (Simulated)',
                horizon: 'DAYS_365',
                budgetDeltaUsd: 12000.0,
                workerDelta: 16,
                cacheHitPct: 94.0,
                trafficGrowthPct: 500.0,
                expectedRoi: 5.10,
                expectedP95Ms: 165.0,
                expectedThroughputQps: 4800.0,
                riskScore: 0.045,
                actions: [
                    'Federate EU and US GPU swarms with zero-lock synchronizer.',
                    'Pre-warm layout embeddings for all Fortune 500 vendor schemas.',
                ],
            };
            setSimulations((prev) => [newSim, ...prev]);
            setIsSimulating(false);
            setNotice('Strategic Scenario Simulation complete: High-confidence multi-datacenter projection added.');
            setTimeout(() => setNotice(null), 4000);
        }, 1200);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(FlaskConical, { className: "w-6 h-6 text-indigo-500" }), "Strategic Scenario Simulation Studio"] }), _jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: "Phase 13.11 \u2014 Multi-horizon strategic stress testing, macroeconomic cost modeling, and throughput projection simulations." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "intelligence", size: "sm", onClick: handleRunNewSim, disabled: isSimulating, children: [_jsx(RefreshCw, { className: `w-3.5 h-3.5 mr-1.5 ${isSimulating ? 'animate-spin' : ''}` }), isSimulating ? 'Simulating Scenario...' : 'Simulate New Scenario'] }) })] }), notice && (_jsxs("div", { className: "p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-lg text-sm text-emerald-800 dark:text-emerald-300 flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-5 h-5 flex-shrink-0" }), _jsx("span", { children: notice })] })), _jsxs("div", { className: "space-y-4", children: [_jsx("h3", { className: "text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider", children: "Simulated Strategic Scenarios" }), _jsx("div", { className: "grid grid-cols-1 gap-4", children: simulations.map((sim) => (_jsxs(Card, { className: "p-5 border-l-4 border-l-indigo-500 hover:shadow-md transition-shadow", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-xs text-indigo-600 dark:text-indigo-400 font-semibold", children: sim.id }), _jsx(Badge, { variant: "outline", size: "sm", children: sim.horizon })] }), _jsx("h4", { className: "font-semibold text-gray-900 dark:text-white text-base mt-1", children: sim.name })] }), _jsx("div", { className: "flex items-center gap-4", children: _jsxs("div", { className: "text-right", children: [_jsx("span", { className: "text-xs text-gray-400 block", children: "Expected ROI" }), _jsxs("span", { className: "text-lg font-bold text-emerald-600 dark:text-emerald-400 font-mono", children: [sim.expectedRoi, "x"] })] }) })] }), _jsxs("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-3 mt-4 text-xs", children: [_jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "text-gray-400 block mb-0.5", children: "Throughput Proj" }), _jsxs("span", { className: "font-semibold text-gray-900 dark:text-white font-mono", children: [sim.expectedThroughputQps.toLocaleString(), " QPS"] })] }), _jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "text-gray-400 block mb-0.5", children: "P95 Latency" }), _jsxs("span", { className: "font-semibold text-indigo-600 dark:text-indigo-400 font-mono", children: [sim.expectedP95Ms, " ms"] })] }), _jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "text-gray-400 block mb-0.5", children: "Traffic Growth" }), _jsxs("span", { className: "font-semibold text-purple-600 dark:text-purple-400 font-mono", children: ["+", sim.trafficGrowthPct, "%"] })] }), _jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "text-gray-400 block mb-0.5", children: "Risk Score" }), _jsx("span", { className: "font-semibold text-sky-600 dark:text-sky-400 font-mono", children: sim.riskScore.toFixed(3) })] })] }), _jsxs("div", { className: "mt-4 pt-3 border-t border-gray-100 dark:border-gray-800 text-xs", children: [_jsx("span", { className: "text-gray-400 block mb-1", children: "Recommended Strategic Directives:" }), _jsx("div", { className: "space-y-1", children: sim.actions.map((act, actIdx) => (_jsxs("div", { className: "flex items-center gap-1.5 text-gray-700 dark:text-gray-300", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5 text-emerald-500 flex-shrink-0" }), _jsx("span", { children: act })] }, actIdx))) })] })] }, sim.id))) })] })] }));
};
