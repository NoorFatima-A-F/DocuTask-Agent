import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Layers, PlusCircle, Sparkles, Zap, } from 'lucide-react';
export const ArchitectureOptimizerView = () => {
    const optimizations = [
        {
            id: 'arch-opt-601',
            subsystem: 'EVENT_BUS_AND_DAG_SCHEDULER',
            type: 'COMMUNICATION_TOPOLOGY_FLATTENING',
            description: 'Replace serial point-to-point task routing with publish-subscribe multicast channels for validator strike teams.',
            latencySavingMs: 180.0,
            memoryDeltaMb: -24.0,
            confidence: 0.985,
            status: 'DEPLOYED',
        },
        {
            id: 'arch-opt-602',
            subsystem: 'DAG_EXECUTION_ENGINE',
            type: 'DAG_REDUNDANCY_REMOVAL',
            description: 'Eliminate redundant intermediate validation nodes when cryptographic SHA-256 parent hash matches trusted schema cache.',
            latencySavingMs: 95.0,
            memoryDeltaMb: -8.0,
            confidence: 0.992,
            status: 'APPROVED',
        },
        {
            id: 'arch-opt-603',
            subsystem: 'RUNTIME_MEMORY_LAYER',
            type: 'LOCK_FREE_RING_BUFFER',
            description: 'Transition hot telemetry fact emission from synchronized mutex to atomic lock-free circular ring buffer.',
            latencySavingMs: 45.0,
            memoryDeltaMb: +12.0,
            confidence: 0.978,
            status: 'PROPOSED',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Architecture Optimizer" }), _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: true, children: "STRUCTURAL REFACTORING ACTIVE" }), _jsx(Badge, { variant: "outline", size: "sm", children: "AMRS-RSIP Phase 13.9" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Continuous topological refactoring, DAG redundancy elimination, communication flattening, and memory concurrency optimization." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "intelligence", size: "sm", children: [_jsx(PlusCircle, { className: "w-3.5 h-3.5 mr-1.5" }), "Propose Optimization"] }) })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-3 gap-4", children: [_jsxs(Card, { className: "p-4 bg-purple-950/10 border-purple-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider", children: "Total Latency Saved" }), _jsx(Zap, { className: "w-4 h-4 text-purple-400" })] }), _jsx("div", { className: "text-2xl font-bold font-mono text-purple-400 mt-2", children: "320ms / Mission" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Sum of structural refactors" })] }), _jsxs(Card, { className: "p-4 bg-emerald-950/10 border-emerald-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider", children: "RAM Footprint Delta" }), _jsx(Layers, { className: "w-4 h-4 text-emerald-400" })] }), _jsx("div", { className: "text-2xl font-bold font-mono text-emerald-400 mt-2", children: "-20.0 MB" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Net memory reduction" })] }), _jsxs(Card, { className: "p-4 bg-blue-950/10 border-blue-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider", children: "Mean Confidence" }), _jsx(Sparkles, { className: "w-4 h-4 text-blue-400" })] }), _jsx("div", { className: "text-2xl font-bold font-mono text-blue-400 mt-2", children: "98.5%" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Mathematical verification score" })] })] }), _jsx("div", { className: "space-y-4", children: optimizations.map((opt) => (_jsxs(Card, { className: "p-5 border-border/40 space-y-3 hover:border-purple-500/30 transition-colors", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2", children: [_jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono font-bold text-foreground", children: opt.subsystem }), _jsx(Badge, { variant: opt.status === 'DEPLOYED'
                                                        ? 'success'
                                                        : opt.status === 'APPROVED'
                                                            ? 'info'
                                                            : 'default', size: "sm", children: opt.status })] }), _jsx("span", { className: "text-xs font-semibold text-purple-300", children: opt.type.replace(/_/g, ' ') })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Badge, { variant: "success", size: "sm", children: ["-", opt.latencySavingMs, "ms Latency"] }), _jsxs(Badge, { variant: "outline", size: "sm", children: [opt.memoryDeltaMb > 0 ? `+${opt.memoryDeltaMb}MB` : `${opt.memoryDeltaMb}MB`, " RAM"] })] })] }), _jsx("p", { className: "text-xs text-muted-foreground leading-relaxed", children: opt.description }), _jsxs("div", { className: "flex items-center justify-between text-xs pt-3 border-t border-border/30", children: [_jsxs("span", { className: "font-mono text-muted-foreground", children: ["Confidence: ", (opt.confidence * 100).toFixed(1), "%"] }), opt.status === 'PROPOSED' && (_jsx(Button, { variant: "outline", size: "sm", children: "Benchmark & Deploy" }))] })] }, opt.id))) })] }));
};
