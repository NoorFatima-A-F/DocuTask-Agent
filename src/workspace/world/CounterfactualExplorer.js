import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { HelpCircle, TrendingDown, TrendingUp, Sparkles, Lock, Search, } from 'lucide-react';
export const CounterfactualExplorer = () => {
    const [customPremise, setCustomPremise] = useState('What if worker concurrency is scaled up to 32 and token caching is enabled?');
    const counterfactuals = [
        {
            id: 'cfo-101',
            premise: 'What if worker concurrency is scaled up to 16 and token caching is enabled?',
            latencyDeltaPct: -28.5,
            costDeltaPct: 12.0,
            riskShift: 'REDUCED',
            confidence: 0.985,
            tradeoffs: 'Provides 28.5% faster end-to-end mission delivery at the cost of 12% higher burst memory usage.',
            hash: '0x4a9b8c7d...221e',
        },
        {
            id: 'cfo-102',
            premise: 'What if token caching is disabled during high-density financial balance sheet parsing?',
            latencyDeltaPct: 35.0,
            costDeltaPct: 20.0,
            riskShift: 'ELEVATED',
            confidence: 0.990,
            tradeoffs: 'Disabling cache forces cold model inference on repetitive templates with higher latency.',
            hash: '0x1b2c3d4e...990f',
        },
        {
            id: 'cfo-103',
            premise: 'What if OCR extraction worker pool experiences a 50% node crash?',
            latencyDeltaPct: 45.0,
            costDeltaPct: 0.0,
            riskShift: 'ELEVATED',
            confidence: 0.978,
            tradeoffs: 'Fallback to secondary specialist agents preserves 100% zero-fabrication floor while latency increases by 45%.',
            hash: '0x7e8f9a0b...334a',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Counterfactual Reasoning Explorer" }), _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: true, children: "\"WHAT-IF\" REASONING ACTIVE" }), _jsx(Badge, { variant: "outline", size: "sm", children: "AWM-PSDTIP Phase 13.10" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Evaluate hypothetical interventions, alternative planner graphs, policy mutations, and recovery trajectories without live system disruption." })] }) }), _jsxs(Card, { className: "p-5 bg-gradient-to-r from-purple-950/30 via-indigo-950/20 to-background border-purple-500/30 space-y-3", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(HelpCircle, { className: "w-5 h-5 text-purple-400" }), _jsx("h2", { className: "text-sm font-bold text-foreground", children: "Hypothetical Intervention Query" })] }), _jsxs("div", { className: "flex flex-col sm:flex-row gap-3", children: [_jsxs("div", { className: "relative flex-1", children: [_jsx(Search, { className: "w-4 h-4 absolute left-3 top-3 text-muted-foreground" }), _jsx("input", { type: "text", value: customPremise, onChange: (e) => setCustomPremise(e.target.value), className: "w-full bg-secondary/50 text-xs rounded-lg pl-9 pr-3 py-2.5 border border-border/40 focus:outline-none focus:border-primary text-foreground", placeholder: "Enter hypothetical what-if scenario..." })] }), _jsxs(Button, { variant: "intelligence", size: "sm", children: [_jsx(Sparkles, { className: "w-3.5 h-3.5 mr-1.5" }), "Evaluate Counterfactual"] })] })] }), _jsx("div", { className: "space-y-4", children: counterfactuals.map((cf) => (_jsxs(Card, { className: "p-5 border-border/40 space-y-4 hover:border-purple-500/30 transition-colors", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2", children: [_jsxs("div", { className: "space-y-1", children: [_jsx("span", { className: "text-xs font-mono font-bold text-purple-400", children: cf.id }), _jsx("h3", { className: "text-sm font-semibold text-foreground", children: cf.premise })] }), _jsxs(Badge, { variant: cf.riskShift === 'REDUCED'
                                        ? 'success'
                                        : cf.riskShift === 'ELEVATED'
                                            ? 'warning'
                                            : 'default', size: "sm", children: ["Risk: ", cf.riskShift] })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-mono", children: [_jsxs("div", { className: "p-3 rounded bg-secondary/20 border border-border/30 flex items-center justify-between", children: [_jsx("span", { className: "text-muted-foreground", children: "Latency Delta:" }), _jsxs("span", { className: `font-bold flex items-center gap-1 ${cf.latencyDeltaPct < 0 ? 'text-emerald-400' : 'text-amber-400'}`, children: [cf.latencyDeltaPct < 0 ? _jsx(TrendingDown, { className: "w-3.5 h-3.5" }) : _jsx(TrendingUp, { className: "w-3.5 h-3.5" }), cf.latencyDeltaPct > 0 ? `+${cf.latencyDeltaPct}%` : `${cf.latencyDeltaPct}%`] })] }), _jsxs("div", { className: "p-3 rounded bg-secondary/20 border border-border/30 flex items-center justify-between", children: [_jsx("span", { className: "text-muted-foreground", children: "Compute Cost Delta:" }), _jsx("span", { className: "font-bold text-foreground", children: cf.costDeltaPct > 0 ? `+${cf.costDeltaPct}%` : `${cf.costDeltaPct}%` })] }), _jsxs("div", { className: "p-3 rounded bg-secondary/20 border border-border/30 flex items-center justify-between", children: [_jsx("span", { className: "text-muted-foreground", children: "Prediction Confidence:" }), _jsxs("span", { className: "font-bold text-purple-300", children: [(cf.confidence * 100).toFixed(1), "%"] })] })] }), _jsx("p", { className: "text-xs text-muted-foreground", children: cf.tradeoffs }), _jsxs("div", { className: "flex items-center justify-between text-[11px] text-muted-foreground pt-3 border-t border-border/30 font-mono", children: [_jsxs("div", { className: "flex items-center gap-1.5 truncate max-w-md", children: [_jsx(Lock, { className: "w-3.5 h-3.5 text-purple-400 flex-shrink-0" }), _jsxs("span", { children: ["Proof Hash: ", cf.hash] })] }), _jsx(Button, { variant: "outline", size: "sm", children: "Apply as Candidate Policy" })] })] }, cf.id))) })] }));
};
