import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Key, Lock, ArrowRight, } from 'lucide-react';
export const SwarmGovernanceCenter = () => {
    const [grants] = useState([
        {
            id: 'grant_001',
            delegator: 'agent-exec-01',
            delegatorRole: 'EXECUTIVE (Tier 1)',
            delegatee: 'agent-plan-01',
            delegateeRole: 'PLANNER (Tier 2)',
            scope: 'MISSION_DECOMPOSITION',
            depth: 1,
            signature: 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2',
            grantedAt: '14:22:00.050',
        },
        {
            id: 'grant_002',
            delegator: 'agent-plan-01',
            delegatorRole: 'PLANNER (Tier 2)',
            delegatee: 'agent-coord-01',
            delegateeRole: 'COORDINATOR (Tier 2)',
            scope: 'DAG_TASK_DISPATCH',
            depth: 2,
            signature: 'c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4',
            grantedAt: '14:22:00.080',
        },
        {
            id: 'grant_003',
            delegator: 'agent-coord-01',
            delegatorRole: 'COORDINATOR (Tier 2)',
            delegatee: 'agent-spec-ocr',
            delegateeRole: 'SPECIALIST (Tier 4)',
            scope: 'IMAGE_PARSE_EXECUTE',
            depth: 3,
            signature: 'e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6',
            grantedAt: '14:22:00.120',
        },
    ]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Swarm Governance Center" }), _jsx(Badge, { variant: "success", size: "sm", children: "ANTI-USURPATION ENFORCED" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Tiered authority hierarchy (Tiers 1-5), cryptographic delegation contracts, and invariant audit logs." })] }) }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-5 gap-3", children: [_jsxs(Card, { className: "p-3 bg-purple-950/20 border-purple-500/30", children: [_jsx("span", { className: "text-[10px] font-bold text-purple-400 uppercase tracking-wider block", children: "Tier 1 Executive" }), _jsx("span", { className: "text-xs font-semibold mt-1 block", children: "Executive Director" }), _jsx("span", { className: "text-[10px] text-muted-foreground mt-0.5 block", children: "Mission Authority" })] }), _jsxs(Card, { className: "p-3 bg-indigo-950/20 border-indigo-500/30", children: [_jsx("span", { className: "text-[10px] font-bold text-indigo-400 uppercase tracking-wider block", children: "Tier 2 Orchestrator" }), _jsx("span", { className: "text-xs font-semibold mt-1 block", children: "Planner & Coord" }), _jsx("span", { className: "text-[10px] text-muted-foreground mt-0.5 block", children: "DAG Dispatch" })] }), _jsxs(Card, { className: "p-3 bg-blue-950/20 border-blue-500/30", children: [_jsx("span", { className: "text-[10px] font-bold text-blue-400 uppercase tracking-wider block", children: "Tier 3 Governor" }), _jsx("span", { className: "text-xs font-semibold mt-1 block", children: "Resource & Security" }), _jsx("span", { className: "text-[10px] text-muted-foreground mt-0.5 block", children: "Policy Control" })] }), _jsxs(Card, { className: "p-3 bg-emerald-950/20 border-emerald-500/30", children: [_jsx("span", { className: "text-[10px] font-bold text-emerald-400 uppercase tracking-wider block", children: "Tier 4 Operator" }), _jsx("span", { className: "text-xs font-semibold mt-1 block", children: "Specialists" }), _jsx("span", { className: "text-[10px] text-muted-foreground mt-0.5 block", children: "Task Execution" })] }), _jsxs(Card, { className: "p-3 bg-teal-950/20 border-teal-500/30", children: [_jsx("span", { className: "text-[10px] font-bold text-teal-400 uppercase tracking-wider block", children: "Tier 5 Auditor" }), _jsx("span", { className: "text-xs font-semibold mt-1 block", children: "Observers" }), _jsx("span", { className: "text-[10px] text-muted-foreground mt-0.5 block", children: "Zero Authority / Audit" })] })] }), _jsxs(Card, { className: "p-5 border-border/60", children: [_jsxs("div", { className: "flex items-center justify-between mb-4", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Key, { className: "w-4 h-4 text-primary" }), _jsx("h3", { className: "font-semibold text-sm", children: "Active Delegation Grants" })] }), _jsx("span", { className: "text-xs text-muted-foreground", children: "Max Depth: 3 Enforced" })] }), _jsx("div", { className: "space-y-3", children: grants.map(g => (_jsxs("div", { className: "p-4 rounded-lg bg-muted/20 border border-border/40 space-y-2", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "outline", size: "sm", className: "font-mono", children: g.id }), _jsxs("span", { className: "font-bold text-xs", children: ["Scope: ", g.scope] })] }), _jsxs(Badge, { variant: "success", size: "sm", children: ["DEPTH ", g.depth, " / 3"] })] }), _jsxs("div", { className: "flex items-center gap-2 text-xs font-mono", children: [_jsxs("div", { children: [_jsx("span", { className: "font-bold text-foreground", children: g.delegator }), _jsx("span", { className: "text-[10px] text-muted-foreground block", children: g.delegatorRole })] }), _jsx(ArrowRight, { className: "w-3.5 h-3.5 text-primary shrink-0" }), _jsxs("div", { children: [_jsx("span", { className: "font-bold text-foreground", children: g.delegatee }), _jsx("span", { className: "text-[10px] text-muted-foreground block", children: g.delegateeRole })] })] }), _jsxs("div", { className: "p-2 rounded bg-background/60 border border-border/30 text-[10px] font-mono text-muted-foreground flex items-center gap-2", children: [_jsx(Lock, { className: "w-3 h-3 text-primary shrink-0" }), _jsxs("span", { className: "truncate", children: ["Delegation Grant Signature: ", g.signature] })] })] }, g.id))) })] })] }));
};
