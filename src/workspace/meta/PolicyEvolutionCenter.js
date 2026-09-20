import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { PlusCircle, Lock, } from 'lucide-react';
export const PolicyEvolutionCenter = () => {
    const [activeTab, setActiveTab] = useState('ALL');
    const proposals = [
        {
            id: 'pol-prop-701',
            policyName: 'Dynamic Worker Concurrency Quota',
            category: 'PLANNER_CONCURRENCY',
            currentRule: 'Limit worker pool max concurrency to 4 simultaneous tasks per DAG.',
            proposedRule: 'Dynamically scale worker pool concurrency up to 12 tasks when host memory utilization is < 60%.',
            rationale: 'Batch invoice extraction DAGs queue unnecessarily under low system memory load.',
            evidence: ['obs-latency-spike-ocr', 'exp-dynamic-fanout'],
            latencyGainPct: 44.0,
            status: 'APPROVED',
            sha256Hash: '4a9c8b7e6f5d4c3b2a1e0f9d8c7b6a5e4d3c2b1a0f9e8d7c6b5a4f3e2d1c0b9a',
        },
        {
            id: 'pol-prop-702',
            policyName: 'SLA Budget Ceiling Dynamic Scaling',
            category: 'RESOURCE_ALLOCATION',
            currentRule: 'Hard cap token budget at $0.05 per document across all tiers.',
            proposedRule: 'Dynamically allow budget scale up to $0.065 for verified high-complexity multi-page legal contracts.',
            rationale: 'Prevents false fallback degradation on highly complex documents without violating organization budget SLA.',
            evidence: ['obs-complex-legal-99', 'exp-triadic-consensus'],
            latencyGainPct: 18.5,
            status: 'CANARY',
            sha256Hash: '7b8a9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b',
        },
        {
            id: 'pol-prop-703',
            policyName: 'Zero-Knowledge Cryptographic Schema Caching',
            category: 'SECURITY_QUORUM',
            currentRule: 'Verify full Ed25519 signature chain on every intermediate sub-task state.',
            proposedRule: 'Cache cryptographic verification proofs for static document schemas within 5-minute zero-trust TTL.',
            rationale: 'Reduces repeated SHA-256 verification overhead by 85ms on bulk recurring invoices.',
            evidence: ['obs-zk-cache-proof', 'rrt-reflection-t5'],
            latencyGainPct: 22.0,
            status: 'PENDING_APPROVAL',
            sha256Hash: '1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d',
        },
    ];
    const filteredProposals = proposals.filter((p) => {
        if (activeTab === 'PENDING')
            return p.status === 'PENDING_APPROVAL';
        if (activeTab === 'ACTIVE')
            return p.status === 'ACTIVE' || p.status === 'APPROVED';
        return true;
    });
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Policy Evolution Center" }), _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: true, children: "GOVERNANCE ENFORCED" }), _jsx(Badge, { variant: "outline", size: "sm", children: "AMRS-RSIP Phase 13.9" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Empirical runtime policy evolution, canary testing, SHA-256 cryptographic verification, and dual-signature approval workflows." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "intelligence", size: "sm", children: [_jsx(PlusCircle, { className: "w-3.5 h-3.5 mr-1.5" }), "Propose Policy Evolution"] }) })] }), _jsx("div", { className: "flex items-center gap-2 border-b border-border/40 pb-2", children: ['ALL', 'PENDING', 'ACTIVE'].map((tab) => (_jsx(Button, { variant: activeTab === tab ? 'primary' : 'ghost', size: "sm", onClick: () => setActiveTab(tab), children: tab }, tab))) }), _jsx("div", { className: "space-y-4", children: filteredProposals.map((prop) => (_jsxs(Card, { className: "p-5 border-border/40 space-y-4 hover:border-purple-500/30 transition-colors", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2", children: [_jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h2", { className: "text-base font-semibold text-foreground", children: prop.policyName }), _jsx(Badge, { variant: prop.status === 'APPROVED' || prop.status === 'ACTIVE'
                                                        ? 'success'
                                                        : prop.status === 'CANARY'
                                                            ? 'warning'
                                                            : 'default', size: "sm", children: prop.status })] }), _jsxs("span", { className: "text-xs font-mono text-muted-foreground", children: ["Category: ", prop.category] })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Badge, { variant: "success", size: "sm", children: ["+", prop.latencyGainPct, "% Efficiency"] }) })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: [_jsxs("div", { className: "p-3.5 rounded-lg border border-border/40 bg-secondary/20 space-y-1.5", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground", children: "Current Operating Rule" }), _jsx("p", { className: "text-xs font-mono text-foreground", children: prop.currentRule })] }), _jsxs("div", { className: "p-3.5 rounded-lg border border-purple-500/30 bg-purple-950/10 space-y-1.5", children: [_jsx("span", { className: "text-xs font-semibold text-purple-400", children: "Proposed Evolutionary Rule" }), _jsx("p", { className: "text-xs font-mono text-purple-200", children: prop.proposedRule })] })] }), _jsxs("div", { className: "text-xs text-muted-foreground space-y-1", children: [_jsxs("div", { children: [_jsx("strong", { className: "text-foreground", children: "Empirical Rationale:" }), " ", prop.rationale] }), _jsxs("div", { className: "flex items-center gap-2 pt-1 font-mono text-[11px]", children: [_jsx("span", { children: "Evidence Backing:" }), prop.evidence.map((ev, idx) => (_jsx("span", { className: "px-1.5 py-0.5 rounded bg-secondary/50 text-foreground", children: ev }, idx)))] })] }), _jsxs("div", { className: "flex items-center justify-between text-[11px] text-muted-foreground pt-3 border-t border-border/30 font-mono", children: [_jsxs("div", { className: "flex items-center gap-1.5 truncate max-w-md", children: [_jsx(Lock, { className: "w-3.5 h-3.5 text-purple-400 flex-shrink-0" }), _jsxs("span", { className: "truncate", children: ["SHA-256 Hash: ", prop.sha256Hash] })] }), prop.status === 'PENDING_APPROVAL' && (_jsx(Button, { variant: "primary", size: "sm", children: "Cast Governance Vote" }))] })] }, prop.id))) })] }));
};
