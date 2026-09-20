import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Sparkles, } from 'lucide-react';
export const ScenarioComparisonWorkbench = () => {
    const scenarios = [
        {
            id: 'scen-opt-01',
            name: 'Dynamic Fan-Out + Speculative Caching',
            mode: 'AUTONOMOUS_OPTIMAL',
            latencyMs: 95.0,
            costUsd: 0.0276,
            riskScore: 0.05,
            throughputQps: 168.4,
            paretoOptimality: 0.985,
            isOptimal: true,
        },
        {
            id: 'scen-opt-02',
            name: 'Dynamic Fan-Out (No Cache)',
            mode: 'PARTIAL_CONCURRENCY',
            latencyMs: 145.0,
            costUsd: 0.0380,
            riskScore: 0.12,
            throughputQps: 110.3,
            paretoOptimality: 0.912,
            isOptimal: false,
        },
        {
            id: 'scen-opt-03',
            name: 'Sequential Greedy Execution Baseline',
            mode: 'LEGACY_BASELINE',
            latencyMs: 380.0,
            costUsd: 0.0480,
            riskScore: 0.28,
            throughputQps: 42.1,
            paretoOptimality: 0.740,
            isOptimal: false,
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Scenario Comparison Workbench" }), _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: true, children: "PARETO EVALUATION" }), _jsx(Badge, { variant: "outline", size: "sm", children: "AWM-PSDTIP Phase 13.10" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Side-by-side Pareto scenario comparison across predicted latency, monetary compute cost, risk index, and throughput capacity." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "intelligence", size: "sm", children: [_jsx(Sparkles, { className: "w-3.5 h-3.5 mr-1.5" }), "Synthesize New Scenario"] }) })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: scenarios.map((scen) => (_jsxs(Card, { className: `p-5 border space-y-4 transition-all flex flex-col justify-between ${scen.isOptimal
                        ? 'border-purple-500/50 bg-purple-950/20 shadow-md'
                        : 'border-border/40 bg-secondary/10'}`, children: [_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between gap-2", children: [_jsx(Badge, { variant: scen.isOptimal ? 'intelligence' : 'outline', size: "sm", children: scen.isOptimal ? '★ Pareto Optimal' : scen.mode }), _jsxs("span", { className: "text-xs font-mono text-purple-400 font-bold", children: ["Score: ", (scen.paretoOptimality * 100).toFixed(1)] })] }), _jsx("h2", { className: "text-sm font-bold text-foreground", children: scen.name }), _jsxs("div", { className: "space-y-2 pt-2 text-xs border-t border-border/30", children: [_jsxs("div", { className: "flex justify-between", children: [_jsx("span", { className: "text-muted-foreground", children: "Predicted Latency:" }), _jsxs("span", { className: "font-mono font-bold text-foreground", children: [scen.latencyMs, "ms"] })] }), _jsxs("div", { className: "flex justify-between", children: [_jsx("span", { className: "text-muted-foreground", children: "Compute Cost:" }), _jsxs("span", { className: "font-mono font-bold text-foreground", children: ["$", scen.costUsd.toFixed(4), "/doc"] })] }), _jsxs("div", { className: "flex justify-between", children: [_jsx("span", { className: "text-muted-foreground", children: "Throughput:" }), _jsxs("span", { className: "font-mono font-bold text-emerald-400", children: [scen.throughputQps, " QPS"] })] }), _jsxs("div", { className: "flex justify-between", children: [_jsx("span", { className: "text-muted-foreground", children: "Risk Exposure:" }), _jsxs("span", { className: "font-mono font-bold text-muted-foreground", children: [(scen.riskScore * 100).toFixed(1), "%"] })] })] })] }), _jsx("div", { className: "pt-3 border-t border-border/30", children: _jsx(Button, { variant: scen.isOptimal ? 'primary' : 'outline', size: "sm", className: "w-full", children: scen.isOptimal ? 'Authorize For Production' : 'Simulate Monte Carlo' }) })] }, scen.id))) })] }));
};
