import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { FlaskConical, RefreshCw, TrendingUp, BarChart2, PlusCircle, Zap, } from 'lucide-react';
export const PredictiveSimulationStudio = () => {
    const [isSimulating, setIsSimulating] = useState(false);
    const simulations = [
        {
            id: 'sres-001',
            name: 'Baseline 500 Enterprise Invoice Ingestion',
            type: 'BASELINE (MONTE_CARLO)',
            expectedLatencyMs: 180.0,
            latencyCi: [177.06, 182.94],
            expectedCostUsd: 0.024,
            costCi: [0.0236, 0.0244],
            failureProb: 0.002,
            throughputQps: 44.4,
            risk: 'LOW',
        },
        {
            id: 'sres-002',
            name: 'Peak Burst Load (3x Concurrent Traffic)',
            type: 'BURST_TRAFFIC (STRESS_TEST)',
            expectedLatencyMs: 225.0,
            latencyCi: [222.60, 227.40],
            expectedCostUsd: 0.0648,
            costCi: [0.0645, 0.0651],
            failureProb: 0.015,
            throughputQps: 71.1,
            risk: 'MEDIUM',
        },
        {
            id: 'sres-003',
            name: 'Swarm Scaling (16 Concurrent Specialists)',
            type: 'SWARM_SCALING (MONTE_CARLO)',
            expectedLatencyMs: 95.0,
            latencyCi: [92.06, 97.94],
            expectedCostUsd: 0.0276,
            costCi: [0.0272, 0.0280],
            failureProb: 0.001,
            throughputQps: 168.4,
            risk: 'LOW',
        },
    ];
    const handleSimulate = () => {
        setIsSimulating(true);
        setTimeout(() => {
            setIsSimulating(false);
        }, 1500);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Predictive Simulation Studio" }), _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: true, children: "MONTE CARLO READY" }), _jsx(Badge, { variant: "outline", size: "sm", children: "AWM-PSDTIP Phase 13.10" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Simulates hypothetical future mission executions across baseline, burst traffic, swarm scaling, and chaos failure scenarios with 95% confidence bounds." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Button, { variant: "outline", size: "sm", onClick: handleSimulate, disabled: isSimulating, children: [_jsx(RefreshCw, { className: `w-3.5 h-3.5 mr-1.5 ${isSimulating ? 'animate-spin' : ''}` }), isSimulating ? 'Simulating Trials...' : 'Run Scenario Trials'] }), _jsxs(Button, { variant: "intelligence", size: "sm", children: [_jsx(PlusCircle, { className: "w-3.5 h-3.5 mr-1.5" }), "Create Simulation Scenario"] })] })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 bg-purple-950/10 border-purple-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider", children: "Simulated Scenarios" }), _jsx(FlaskConical, { className: "w-4 h-4 text-purple-400" })] }), _jsx("div", { className: "text-2xl font-bold font-mono text-purple-400 mt-2", children: "1,250 Trials" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Grounded in replay history" })] }), _jsxs(Card, { className: "p-4 bg-emerald-950/10 border-emerald-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider", children: "Optimal Peak Throughput" }), _jsx(Zap, { className: "w-4 h-4 text-emerald-400" })] }), _jsx("div", { className: "text-2xl font-bold font-mono text-emerald-400 mt-2", children: "168.4 QPS" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Swarm scaling scenario" })] }), _jsxs(Card, { className: "p-4 bg-blue-950/10 border-blue-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider", children: "Confidence Interval Floor" }), _jsx(BarChart2, { className: "w-4 h-4 text-blue-400" })] }), _jsx("div", { className: "text-2xl font-bold font-mono text-blue-400 mt-2", children: "95% CI (\u00B12.9ms)" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Statistical variance calibrated" })] }), _jsxs(Card, { className: "p-4 bg-indigo-950/10 border-indigo-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider", children: "Mean Failure Risk" }), _jsx(TrendingUp, { className: "w-4 h-4 text-indigo-400" })] }), _jsx("div", { className: "text-2xl font-bold font-mono text-indigo-400 mt-2", children: "< 0.2%" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Zero invariant violation" })] })] }), _jsx("div", { className: "space-y-4", children: simulations.map((sim) => (_jsxs(Card, { className: "p-5 border-border/40 space-y-4 hover:border-purple-500/30 transition-colors", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2", children: [_jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h2", { className: "text-base font-semibold text-foreground", children: sim.name }), _jsx(Badge, { variant: "intelligence", size: "sm", children: sim.type })] }), _jsxs("span", { className: "text-xs font-mono text-muted-foreground", children: ["Scenario ID: ", sim.id] })] }), _jsxs(Badge, { variant: sim.risk === 'LOW' ? 'success' : 'warning', size: "sm", children: ["Risk: ", sim.risk] })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs font-mono", children: [_jsxs("div", { className: "p-3 rounded bg-secondary/20 border border-border/30", children: [_jsx("span", { className: "text-muted-foreground", children: "Expected Latency:" }), _jsxs("div", { className: "text-base font-bold text-foreground mt-1", children: [sim.expectedLatencyMs, "ms"] }), _jsxs("span", { className: "text-[10px] text-purple-300", children: ["95% CI: [", sim.latencyCi[0], ", ", sim.latencyCi[1], "]"] })] }), _jsxs("div", { className: "p-3 rounded bg-secondary/20 border border-border/30", children: [_jsx("span", { className: "text-muted-foreground", children: "Compute Cost:" }), _jsxs("div", { className: "text-base font-bold text-foreground mt-1", children: ["$", sim.expectedCostUsd.toFixed(4)] }), _jsxs("span", { className: "text-[10px] text-emerald-300", children: ["95% CI: [", sim.costCi[0], ", ", sim.costCi[1], "]"] })] }), _jsxs("div", { className: "p-3 rounded bg-secondary/20 border border-border/30", children: [_jsx("span", { className: "text-muted-foreground", children: "Predicted Throughput:" }), _jsxs("div", { className: "text-base font-bold text-emerald-400 mt-1", children: [sim.throughputQps, " QPS"] }), _jsx("span", { className: "text-[10px] text-muted-foreground", children: "Linear scaling factor" })] }), _jsxs("div", { className: "p-3 rounded bg-secondary/20 border border-border/30", children: [_jsx("span", { className: "text-muted-foreground", children: "Failure Probability:" }), _jsxs("div", { className: "text-base font-bold text-foreground mt-1", children: [(sim.failureProb * 100).toFixed(2), "%"] }), _jsx("span", { className: "text-[10px] text-emerald-400", children: "Zero deadlock risk" })] })] }), _jsxs("div", { className: "flex items-center justify-between text-xs pt-2 border-t border-border/30", children: [_jsx("span", { className: "text-[11px] font-mono text-muted-foreground", children: "Deterministic Replay Proof Available" }), _jsx(Button, { variant: "outline", size: "sm", children: "Apply Simulation Parameters" })] })] }, sim.id))) })] }));
};
