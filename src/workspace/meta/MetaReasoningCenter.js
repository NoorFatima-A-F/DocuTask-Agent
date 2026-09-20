import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Brain, Sparkles, AlertTriangle, ArrowRight, RefreshCw, Zap, Target, Search, CheckCircle2, } from 'lucide-react';
export const MetaReasoningCenter = () => {
    const selectedGoal = 'Process 500 Enterprise Invoice Documents within $50 compute budget and 30s SLA';
    const [isSynthesizing, setIsSynthesizing] = useState(false);
    const [searchFilter, setSearchFilter] = useState('');
    const bottlenecks = [
        {
            id: 'btn-991',
            subsystem: 'OCR_EXTRACTION_PIPELINE',
            type: 'DEPENDENCY_SERIALIZATION',
            severity: 'HIGH',
            rootCause: 'Sequential page parsing in DAG without chunk partitioning',
            impactMs: 450,
            mitigation: 'Implement dynamic chunk fan-out across specialist swarm agents',
        },
        {
            id: 'btn-992',
            subsystem: 'CONSENSUS_QUORUM',
            type: 'GOVERNANCE_OVERHEAD',
            severity: 'MEDIUM',
            rootCause: 'Repeated cryptographic signature verification on static schemas',
            impactMs: 85,
            mitigation: 'Cache validated schema signatures in zero-trust memory layer',
        },
        {
            id: 'btn-993',
            subsystem: 'EVENT_BUS_ROUTER',
            type: 'RESOURCE_QUOTA',
            severity: 'LOW',
            rootCause: 'High burst event queuing during peak multi-page ingestion',
            impactMs: 35,
            mitigation: 'Dynamic memory buffer pool expansion up to 512MB',
        },
    ];
    const alternatives = [
        {
            id: 'alt-101',
            title: 'Dynamic DAG Chunk Fan-Out',
            description: 'Split multi-page documents into isolated sub-DAG tasks executed in parallel across available specialist agents.',
            latencyGainPct: 42.5,
            costReductionPct: 15.0,
            confidence: 0.982,
            tradeoffs: ['Requires 15% higher burst RAM allocation during peak load'],
        },
        {
            id: 'alt-102',
            title: 'Speculative Token Cache',
            description: 'Pre-compute and cache token embeddings for recurring corporate vendor invoice templates.',
            latencyGainPct: 28.0,
            costReductionPct: 22.0,
            confidence: 0.965,
            tradeoffs: ['Requires 150MB hot RAM cache reservation'],
        },
        {
            id: 'alt-103',
            title: 'Adaptive Specialist Auction Routing',
            description: 'Route complex balance sheet tables to high-reputation mathematical verification agents automatically.',
            latencyGainPct: 19.5,
            costReductionPct: 8.5,
            confidence: 0.991,
            tradeoffs: ['Slightly higher consensus voting latency (+15ms)'],
        },
    ];
    const handleSynthesize = () => {
        setIsSynthesizing(true);
        setTimeout(() => {
            setIsSynthesizing(false);
        }, 1200);
    };
    const filteredBottlenecks = bottlenecks.filter((b) => b.subsystem.toLowerCase().includes(searchFilter.toLowerCase()) ||
        b.rootCause.toLowerCase().includes(searchFilter.toLowerCase()));
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Meta-Reasoning Center" }), _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: true, children: "META-COGNITION ACTIVE" }), _jsx(Badge, { variant: "outline", size: "sm", children: "AMRS-RSIP Phase 13.9" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Autonomous goal abstraction, intent inference, systemic bottleneck detection, and counterfactual strategy formulation." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Button, { variant: "outline", size: "sm", onClick: handleSynthesize, disabled: isSynthesizing, children: [_jsx(RefreshCw, { className: `w-3.5 h-3.5 mr-1.5 ${isSynthesizing ? 'animate-spin' : ''}` }), isSynthesizing ? 'Synthesizing...' : 'Re-synthesize Graph'] }), _jsxs(Button, { variant: "intelligence", size: "sm", children: [_jsx(Sparkles, { className: "w-3.5 h-3.5 mr-1.5" }), "Trigger Deep Meta-Reasoning"] })] })] }), _jsx(Card, { className: "p-5 bg-gradient-to-r from-purple-950/30 via-indigo-950/20 to-background border-purple-500/30", children: _jsxs("div", { className: "flex items-start gap-4", children: [_jsx("div", { className: "p-3 bg-purple-500/10 rounded-xl border border-purple-500/20 text-purple-400", children: _jsx(Brain, { className: "w-6 h-6" }) }), _jsxs("div", { className: "space-y-1.5 flex-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-semibold text-purple-400 uppercase tracking-wider", children: "Active Goal Abstraction" }), _jsx(Badge, { variant: "success", size: "sm", children: "Confidence 98.4%" })] }), _jsx("p", { className: "text-sm font-medium text-foreground", children: selectedGoal }), _jsxs("div", { className: "flex flex-wrap items-center gap-4 text-xs text-muted-foreground pt-1", children: [_jsxs("span", { children: ["Abstracted Intent: ", _jsx("strong", { className: "text-foreground", children: "Maximize Multi-Document Throughput under Hard Budget Ceiling" })] }), _jsx("span", { children: "\u2022" }), _jsxs("span", { children: ["Decomposition Horizon: ", _jsx("strong", { className: "text-purple-400", children: "Multi-Stage Speculative DAG" })] })] })] })] }) }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 bg-purple-950/10 border-purple-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider", children: "Meta-Cognitive Depth" }), _jsx(Brain, { className: "w-4 h-4 text-purple-400" })] }), _jsx("div", { className: "text-2xl font-bold font-mono text-purple-400 mt-2", children: "7 Tiers" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Hierarchical recursive critique active" })] }), _jsxs(Card, { className: "p-4 bg-amber-950/10 border-amber-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider", children: "Active Bottlenecks" }), _jsx(AlertTriangle, { className: "w-4 h-4 text-amber-400" })] }), _jsxs("div", { className: "text-2xl font-bold font-mono text-amber-400 mt-2", children: [bottlenecks.length, " Detected"] }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "1 Critical serialization pattern" })] }), _jsxs(Card, { className: "p-4 bg-emerald-950/10 border-emerald-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider", children: "Predicted Throughput Gain" }), _jsx(Zap, { className: "w-4 h-4 text-emerald-400" })] }), _jsx("div", { className: "text-2xl font-bold font-mono text-emerald-400 mt-2", children: "+42.5%" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Validated via replay simulation" })] }), _jsxs(Card, { className: "p-4 bg-blue-950/10 border-blue-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider", children: "Pareto Optimization Score" }), _jsx(Target, { className: "w-4 h-4 text-blue-400" })] }), _jsx("div", { className: "text-2xl font-bold font-mono text-blue-400 mt-2", children: "0.985 / 1.0" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Optimal latency-cost frontier" })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-2 gap-6", children: [_jsxs(Card, { className: "p-5 border-border/40 space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(AlertTriangle, { className: "w-4 h-4 text-amber-400" }), _jsx("h2", { className: "text-base font-semibold", children: "Detected Systemic Bottlenecks" })] }), _jsxs("div", { className: "relative w-48", children: [_jsx(Search, { className: "w-3.5 h-3.5 absolute left-2.5 top-2.5 text-muted-foreground" }), _jsx("input", { type: "text", value: searchFilter, onChange: (e) => setSearchFilter(e.target.value), placeholder: "Filter bottlenecks...", className: "w-full bg-secondary/50 text-xs rounded-md pl-8 pr-2 py-1.5 border border-border/40 focus:outline-none focus:border-primary" })] })] }), _jsx("div", { className: "space-y-3", children: filteredBottlenecks.map((btn) => (_jsxs("div", { className: "p-3.5 rounded-lg border border-border/40 bg-secondary/20 hover:bg-secondary/40 transition-colors space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono font-bold text-foreground", children: btn.subsystem }), _jsx(Badge, { variant: btn.severity === 'CRITICAL'
                                                                ? 'error'
                                                                : btn.severity === 'HIGH'
                                                                    ? 'warning'
                                                                    : 'default', size: "sm", children: btn.severity })] }), _jsxs("span", { className: "text-xs font-mono text-amber-400", children: ["+", btn.impactMs, "ms impact"] })] }), _jsx("p", { className: "text-xs text-muted-foreground", children: btn.rootCause }), _jsxs("div", { className: "flex items-center gap-1.5 text-xs text-purple-400 bg-purple-500/10 p-2 rounded border border-purple-500/20", children: [_jsx(ArrowRight, { className: "w-3.5 h-3.5 flex-shrink-0" }), _jsxs("span", { children: ["Mitigation: ", btn.mitigation] })] })] }, btn.id))) })] }), _jsxs(Card, { className: "p-5 border-border/40 space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4 text-purple-400" }), _jsx("h2", { className: "text-base font-semibold", children: "Synthesized Strategic Alternatives" })] }), _jsx(Badge, { variant: "outline", size: "sm", children: "Pareto Evaluated" })] }), _jsx("div", { className: "space-y-3", children: alternatives.map((alt) => (_jsxs("div", { className: "p-3.5 rounded-lg border border-purple-500/20 bg-purple-950/10 hover:bg-purple-950/20 transition-colors space-y-2.5", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-purple-300", children: alt.title }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Badge, { variant: "success", size: "sm", children: ["+", alt.latencyGainPct, "% Speed"] }), _jsxs(Badge, { variant: "info", size: "sm", children: ["-", alt.costReductionPct, "% Cost"] })] })] }), _jsx("p", { className: "text-xs text-muted-foreground", children: alt.description }), _jsxs("div", { className: "flex items-center justify-between text-xs pt-1 border-t border-border/30", children: [_jsxs("div", { className: "flex items-center gap-1 text-muted-foreground", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5 text-emerald-400" }), _jsxs("span", { children: ["Confidence: ", (alt.confidence * 100).toFixed(1), "%"] })] }), _jsx(Button, { variant: "outline", size: "sm", children: "Formulate Plan" })] })] }, alt.id))) })] })] })] }));
};
