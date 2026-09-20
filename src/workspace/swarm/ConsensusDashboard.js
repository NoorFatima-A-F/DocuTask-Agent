import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { ShieldCheck, Lock, } from 'lucide-react';
export const ConsensusDashboard = () => {
    const [sessions] = useState([
        {
            id: 'cns-001',
            topic: 'UPGRADE_EXTRACTION_MODEL_V2',
            mode: 'WEIGHTED_REPUTATION',
            winningOutcome: 'APPROVE',
            totalVotes: 3,
            quorumReached: true,
            consensusRatio: 1.0,
            signature: 'a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8',
            finalizedAt: '14:22:06.210',
            votes: [
                { agentId: 'agent-exec-01', choice: 'APPROVE', weight: 1.0, confidence: 0.99 },
                { agentId: 'agent-plan-01', choice: 'APPROVE', weight: 1.0, confidence: 0.98 },
                { agentId: 'agent-val-sec', choice: 'APPROVE', weight: 1.2, confidence: 0.99 },
            ],
        },
        {
            id: 'cns-002',
            topic: 'VERIFY_SCHEMA_INVARIANT_MISSION_9482',
            mode: 'CONFIDENCE_WEIGHTED',
            winningOutcome: 'APPROVED',
            totalVotes: 4,
            quorumReached: true,
            consensusRatio: 0.98,
            signature: 'f1e2d3c4b5a6f7e8d9c0b1a2f3e4d5c6b7a8f9e0d1c2b3a4f5e6d7c8b9a0f1e2',
            finalizedAt: '14:22:06.550',
            votes: [
                { agentId: 'agent-spec-ocr', choice: 'APPROVED', weight: 1.0, confidence: 0.985 },
                { agentId: 'agent-val-sec', choice: 'APPROVED', weight: 1.5, confidence: 0.995 },
                { agentId: 'agent-res-opt', choice: 'APPROVED', weight: 0.9, confidence: 0.960 },
                { agentId: 'agent-coord-01', choice: 'APPROVED', weight: 1.0, confidence: 0.970 },
            ],
        },
    ]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Consensus & Voting Engine" }), _jsx(Badge, { variant: "success", size: "sm", children: "100% Quorum Satisfied" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Decentralized multi-agent consensus with weighted reputation scoring, Byzantine fault tolerance, and cryptographic decision proofs." })] }) }), _jsx("div", { className: "space-y-4", children: sessions.map(s => (_jsxs(Card, { className: "p-5 border-border/60 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border/40 pb-3", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "outline", size: "sm", className: "font-mono", children: s.id }), _jsx("h3", { className: "font-bold text-sm", children: s.topic })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: s.mode }), _jsxs(Badge, { variant: "success", size: "sm", children: ["WINNER: ", s.winningOutcome] })] })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-3 gap-3", children: [_jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/30", children: [_jsx("span", { className: "text-[11px] text-muted-foreground block", children: "Consensus Ratio" }), _jsxs("span", { className: "text-xl font-bold font-mono text-emerald-400", children: [(s.consensusRatio * 100).toFixed(1), "% Affirmative"] })] }), _jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/30", children: [_jsx("span", { className: "text-[11px] text-muted-foreground block", children: "Quorum Status" }), _jsx("span", { className: "text-xl font-bold font-mono text-blue-400", children: s.quorumReached ? 'Quorum Met' : 'Quorum Pending' })] }), _jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/30", children: [_jsx("span", { className: "text-[11px] text-muted-foreground block", children: "Total Ballots Cast" }), _jsxs("span", { className: "text-xl font-bold font-mono text-purple-400", children: [s.totalVotes, " Verified Votes"] })] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground block mb-2", children: "Verified Agent Ballots" }), _jsx("div", { className: "grid grid-cols-1 sm:grid-cols-2 gap-2", children: s.votes.map(v => (_jsxs("div", { className: "flex items-center justify-between p-2.5 rounded bg-muted/10 border border-border/20 text-xs font-mono", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(ShieldCheck, { className: "w-3.5 h-3.5 text-emerald-400" }), _jsx("span", { className: "font-semibold", children: v.agentId })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsxs("span", { className: "text-muted-foreground", children: ["Weight: ", v.weight] }), _jsx("span", { className: "text-emerald-400 font-bold", children: v.choice })] })] }, v.agentId))) })] }), _jsxs("div", { className: "p-2 rounded bg-background/80 border border-border/30 text-[10px] font-mono text-muted-foreground flex items-center gap-2", children: [_jsx(Lock, { className: "w-3 h-3 text-primary shrink-0" }), _jsxs("span", { className: "truncate", children: ["Decision Merkle Signature: ", s.signature] })] })] }, s.id))) })] }));
};
