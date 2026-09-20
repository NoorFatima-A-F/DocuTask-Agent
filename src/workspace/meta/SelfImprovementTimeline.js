import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { PlusCircle, RotateCcw, CheckCircle2, } from 'lucide-react';
export const SelfImprovementTimeline = () => {
    const cycles = [
        {
            id: 'sic-501',
            targetArea: 'OCR_DAG_PARALLELIZATION',
            hypothesis: 'Parallel chunk fan-out in DAG execution reduces multi-page invoice extraction latency by >= 35%.',
            gainPct: 42.5,
            status: 'DEPLOYED',
            merkleRoot: '7e8f9a0b1c2d3e4f...990a',
            initiatedAt: '2026-09-12 08:30:00 UTC',
            completedAt: '2026-09-12 08:32:15 UTC',
        },
        {
            id: 'sic-502',
            targetArea: 'EMBEDDING_SCHEMA_CACHE',
            hypothesis: 'In-memory zero-copy cache for recurrent invoice templates reduces token compute by >= 20%.',
            gainPct: 22.0,
            status: 'GOVERNANCE_PENDING',
            merkleRoot: '3c4d5e6f7a8b9c0d...112b',
            initiatedAt: '2026-09-12 09:15:00 UTC',
        },
        {
            id: 'sic-503',
            targetArea: 'LOCK_FREE_TELEMETRY_STREAM',
            hypothesis: 'Atomic lock-free ring buffer prevents EventBus queue stalls during high-burst ingestion.',
            gainPct: 15.8,
            status: 'IN_EXPERIMENT',
            merkleRoot: 'a0b1c2d3e4f5a6b7...448c',
            initiatedAt: '2026-09-12 09:40:00 UTC',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Self-Improvement Timeline" }), _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: true, children: "CLOSED-LOOP ACTIVE" }), _jsx(Badge, { variant: "outline", size: "sm", children: "AMRS-RSIP Phase 13.9" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Chronological audit of recursive self-improvement cycles across observation, reflection, reasoning, experimentation, governance, and deployment." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "intelligence", size: "sm", children: [_jsx(PlusCircle, { className: "w-3.5 h-3.5 mr-1.5" }), "Initiate Self-Improvement Cycle"] }) })] }), _jsx("div", { className: "space-y-4", children: cycles.map((cycle) => (_jsxs(Card, { className: "p-5 border-border/40 space-y-3 hover:border-purple-500/30 transition-colors", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2", children: [_jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono font-bold text-foreground", children: cycle.targetArea }), _jsx(Badge, { variant: cycle.status === 'DEPLOYED'
                                                        ? 'success'
                                                        : cycle.status === 'GOVERNANCE_PENDING'
                                                            ? 'warning'
                                                            : 'default', size: "sm", children: cycle.status })] }), _jsx("div", { className: "text-xs font-medium text-foreground", children: cycle.hypothesis })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Badge, { variant: "success", size: "sm", children: ["+", cycle.gainPct, "% Measured Gain"] }) })] }), _jsxs("div", { className: "flex flex-wrap items-center justify-between text-xs pt-3 border-t border-border/30 text-muted-foreground font-mono", children: [_jsxs("div", { className: "flex items-center gap-4", children: [_jsxs("span", { children: ["Merkle Checkpoint: ", cycle.merkleRoot] }), _jsxs("span", { children: ["Initiated: ", cycle.initiatedAt] })] }), _jsxs("div", { className: "flex items-center gap-2 mt-2 sm:mt-0", children: [cycle.status === 'DEPLOYED' && (_jsxs(Button, { variant: "outline", size: "sm", children: [_jsx(RotateCcw, { className: "w-3.5 h-3.5 mr-1 text-amber-400" }), "Rollback Checkpoint"] })), cycle.status === 'GOVERNANCE_PENDING' && (_jsxs(Button, { variant: "primary", size: "sm", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5 mr-1" }), "Review & Sign"] }))] })] })] }, cycle.id))) })] }));
};
