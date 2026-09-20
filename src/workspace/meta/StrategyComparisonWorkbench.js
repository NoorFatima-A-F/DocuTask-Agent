import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Sparkles, } from 'lucide-react';
export const StrategyComparisonWorkbench = () => {
    const strategies = [
        {
            id: 'strat-01',
            name: 'Dynamic Chunk Fan-Out + Schema Caching',
            type: 'AUTONOMOUS_SYNTHESIS',
            latencyMs: 165,
            costPerDocUsd: 0.024,
            accuracyFloorPct: 99.8,
            memoryOverheadMb: 150,
            paretoScore: 0.985,
            isRecommended: true,
        },
        {
            id: 'strat-02',
            name: 'Dynamic Fan-Out Only (No Cache)',
            type: 'PARTIAL_OPTIMIZATION',
            latencyMs: 210,
            costPerDocUsd: 0.034,
            accuracyFloorPct: 99.6,
            memoryOverheadMb: 64,
            paretoScore: 0.912,
            isRecommended: false,
        },
        {
            id: 'strat-03',
            name: 'Greedy Sequential Critical-Path Baseline',
            type: 'LEGACY_BASELINE',
            latencyMs: 380,
            costPerDocUsd: 0.048,
            accuracyFloorPct: 99.2,
            memoryOverheadMb: 32,
            paretoScore: 0.760,
            isRecommended: false,
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Strategy Comparison Workbench" }), _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: true, children: "PARETO EVALUATION" }), _jsx(Badge, { variant: "outline", size: "sm", children: "AMRS-RSIP Phase 13.9" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Side-by-side Pareto comparison of autonomous strategies against legacy baselines across latency, monetary cost, accuracy floor, and memory footprints." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "intelligence", size: "sm", children: [_jsx(Sparkles, { className: "w-3.5 h-3.5 mr-1.5" }), "Synthesize New Candidate"] }) })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: strategies.map((st) => (_jsxs(Card, { className: `p-5 border space-y-4 transition-all flex flex-col justify-between ${st.isRecommended
                        ? 'border-purple-500/50 bg-purple-950/20 shadow-md'
                        : 'border-border/40 bg-secondary/10'}`, children: [_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between gap-2", children: [_jsx(Badge, { variant: st.isRecommended ? 'intelligence' : 'outline', size: "sm", children: st.isRecommended ? '★ Recommended Strategy' : st.type }), _jsxs("span", { className: "text-xs font-mono text-purple-400 font-bold", children: ["Score: ", (st.paretoScore * 100).toFixed(1)] })] }), _jsx("h2", { className: "text-sm font-bold text-foreground", children: st.name }), _jsxs("div", { className: "space-y-2 pt-2 text-xs border-t border-border/30", children: [_jsxs("div", { className: "flex justify-between", children: [_jsx("span", { className: "text-muted-foreground", children: "Mean Latency:" }), _jsxs("span", { className: "font-mono font-bold text-foreground", children: [st.latencyMs, "ms"] })] }), _jsxs("div", { className: "flex justify-between", children: [_jsx("span", { className: "text-muted-foreground", children: "Compute Cost:" }), _jsxs("span", { className: "font-mono font-bold text-foreground", children: ["$", st.costPerDocUsd.toFixed(3), "/doc"] })] }), _jsxs("div", { className: "flex justify-between", children: [_jsx("span", { className: "text-muted-foreground", children: "Accuracy Guarantee:" }), _jsxs("span", { className: "font-mono font-bold text-emerald-400", children: [st.accuracyFloorPct, "%"] })] }), _jsxs("div", { className: "flex justify-between", children: [_jsx("span", { className: "text-muted-foreground", children: "RAM Overhead:" }), _jsxs("span", { className: "font-mono font-bold text-muted-foreground", children: [st.memoryOverheadMb, " MB"] })] })] })] }), _jsx("div", { className: "pt-3 border-t border-border/30", children: _jsx(Button, { variant: st.isRecommended ? 'primary' : 'outline', size: "sm", className: "w-full", children: st.isRecommended ? 'Deploy Active Policy' : 'Simulate Replay' }) })] }, st.id))) })] }));
};
