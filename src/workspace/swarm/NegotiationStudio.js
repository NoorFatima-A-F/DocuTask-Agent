import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Scale, Handshake, Lock, ArrowRightLeft, } from 'lucide-react';
export const NegotiationStudio = () => {
    const [agreements] = useState([
        {
            id: 'agr-001',
            topic: 'OCR_BURST_QUOTA_AND_SLA',
            initiator: 'agent-coord-01',
            receiver: 'agent-spec-ocr',
            costUsd: 0.032,
            latencyMs: 160.0,
            confidence: 0.985,
            rounds: 2,
            sha256Hash: '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
            signedAt: '14:22:04.110',
        },
        {
            id: 'agr-002',
            topic: 'SECURITY_AUDIT_THROUGHPUT',
            initiator: 'agent-plan-01',
            receiver: 'agent-val-sec',
            costUsd: 0.015,
            latencyMs: 90.0,
            confidence: 0.999,
            rounds: 1,
            sha256Hash: '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
            signedAt: '14:22:04.450',
        },
        {
            id: 'agr-003',
            topic: 'TOKEN_RATE_LIMIT_ARBITRATION',
            initiator: 'agent-res-opt',
            receiver: 'agent-coord-01',
            costUsd: 0.008,
            latencyMs: 50.0,
            confidence: 0.970,
            rounds: 3,
            sha256Hash: '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a',
            signedAt: '14:22:04.890',
        },
    ]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Autonomous Negotiation Studio" }), _jsxs(Badge, { variant: "success", size: "sm", children: [agreements.length, " Agreements Settled"] })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Multi-objective Pareto bargaining over compute cost, latency, and confidence with immutable SHA-256 agreement ledgers." })] }) }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-4", children: [_jsxs(Card, { className: "p-4 bg-purple-950/10 border-purple-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground", children: "Demands & Concessions" }), _jsx(Scale, { className: "w-4 h-4 text-purple-400" })] }), _jsx("div", { className: "text-xl font-bold font-mono text-purple-400 mt-2", children: "Pareto Optimal" }), _jsx("p", { className: "text-[11px] text-muted-foreground mt-1", children: "Bargaining engine computes 10% concession steps per round." })] }), _jsxs(Card, { className: "p-4 bg-emerald-950/10 border-emerald-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground", children: "Conflict Resolution" }), _jsx(Handshake, { className: "w-4 h-4 text-emerald-400" })] }), _jsx("div", { className: "text-xl font-bold font-mono text-emerald-400 mt-2", children: "Zero Deadlock" }), _jsx("p", { className: "text-[11px] text-muted-foreground mt-1", children: "Reputation-weighted arbitration resolves concurrent resource claims." })] }), _jsxs(Card, { className: "p-4 bg-blue-950/10 border-blue-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground", children: "Agreement Ledger" }), _jsx(Lock, { className: "w-4 h-4 text-blue-400" })] }), _jsx("div", { className: "text-xl font-bold font-mono text-blue-400 mt-2", children: "SHA-256 Chained" }), _jsx("p", { className: "text-[11px] text-muted-foreground mt-1", children: "Every agreed contract is cryptographically signed and hash-chained." })] })] }), _jsxs(Card, { className: "p-5 border-border/60", children: [_jsx("h3", { className: "font-semibold text-sm mb-4", children: "Settled Negotiation Agreements" }), _jsx("div", { className: "space-y-3", children: agreements.map(a => (_jsxs("div", { className: "p-4 rounded-lg bg-muted/20 border border-border/40 space-y-3", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "outline", size: "sm", className: "font-mono", children: a.id }), _jsx("span", { className: "font-bold text-xs", children: a.topic })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Badge, { variant: "success", size: "sm", children: ["SETTLED IN ", a.rounds, " ROUNDS"] }), _jsx("span", { className: "text-[11px] font-mono text-muted-foreground", children: a.signedAt })] })] }), _jsxs("div", { className: "flex items-center gap-2 text-xs font-mono text-muted-foreground", children: [_jsx("span", { className: "font-semibold text-foreground", children: a.initiator }), _jsx(ArrowRightLeft, { className: "w-3.5 h-3.5 text-primary" }), _jsx("span", { className: "font-semibold text-foreground", children: a.receiver })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-mono", children: [_jsxs("div", { className: "p-2 rounded bg-background/50 border border-border/30", children: [_jsx("span", { className: "text-[10px] text-muted-foreground block", children: "Agreed Compute Cost" }), _jsxs("span", { className: "font-bold text-emerald-400", children: ["$", a.costUsd, " USD"] })] }), _jsxs("div", { className: "p-2 rounded bg-background/50 border border-border/30", children: [_jsx("span", { className: "text-[10px] text-muted-foreground block", children: "Agreed Max Latency" }), _jsxs("span", { className: "font-bold text-blue-400", children: [a.latencyMs, " ms"] })] }), _jsxs("div", { className: "p-2 rounded bg-background/50 border border-border/30", children: [_jsx("span", { className: "text-[10px] text-muted-foreground block", children: "Confidence Floor" }), _jsxs("span", { className: "font-bold text-purple-400", children: [(a.confidence * 100).toFixed(1), "%"] })] })] }), _jsxs("div", { className: "p-2 rounded bg-background/70 border border-border/30 text-[10px] font-mono text-muted-foreground flex items-center gap-2", children: [_jsx(Lock, { className: "w-3 h-3 text-primary shrink-0" }), _jsxs("span", { className: "truncate", children: ["SHA-256 Ledger Hash: ", a.sha256Hash] })] })] }, a.id))) })] })] }));
};
