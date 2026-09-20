import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Sparkles, } from 'lucide-react';
export const SwarmLearningDashboard = () => {
    const [patterns] = useState([
        {
            id: 'pat-001',
            name: 'Triadic Verification Pipeline',
            type: 'CROSS_VALIDATION_TRIAD',
            roles: ['SPECIALIST', 'VALIDATOR', 'REVIEWER'],
            successRate: 0.998,
            latencyMs: 310.0,
            description: 'Specialist extracts metadata, validator checks cryptographic checksums, reviewer verifies business invariants.',
        },
        {
            id: 'pat-002',
            name: 'Hierarchical Delegation Matrix',
            type: 'HIERARCHICAL_DELEGATION',
            roles: ['EXECUTIVE', 'PLANNER', 'COORDINATOR', 'RESOURCE'],
            successRate: 0.985,
            latencyMs: 450.0,
            description: 'Executive partitions high-level mission into parallel sub-graphs governed by Coordinator under Resource budget constraints.',
        },
        {
            id: 'pat-003',
            name: 'Bargaining-Based Task Allocation',
            type: 'DECOMPOSITION_PIPELINE',
            roles: ['NEGOTIATOR', 'COORDINATOR', 'SPECIALIST'],
            successRate: 0.992,
            latencyMs: 220.0,
            description: 'Auctions high-priority extraction batches to available specialists using SLA & compute cost bargaining.',
        },
    ]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Swarm Collective Learning Dashboard" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "3 STRATEGIES MINED" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Mined collaboration patterns, semantic swarm knowledge graph, emergent multi-agent coordination strategies, and efficiency benchmarks." })] }) }), _jsx("div", { className: "space-y-4", children: patterns.map(p => (_jsxs(Card, { className: "p-5 border-border/60 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border/40 pb-3", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4 text-cyan-400" }), _jsx("h3", { className: "font-bold text-sm", children: p.name }), _jsx(Badge, { variant: "outline", size: "sm", className: "font-mono", children: p.type })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Badge, { variant: "success", size: "sm", children: [(p.successRate * 100).toFixed(1), "% Success Rate"] }), _jsxs("span", { className: "text-xs font-mono text-muted-foreground", children: [p.latencyMs, " ms Avg"] })] })] }), _jsx("p", { className: "text-xs text-muted-foreground leading-relaxed", children: p.description }), _jsxs("div", { children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground block mb-2", children: "Required Agent Roles in Triad" }), _jsx("div", { className: "flex flex-wrap gap-2", children: p.roles.map(r => (_jsx(Badge, { variant: "outline", size: "md", className: "font-mono", children: r }, r))) })] })] }, p.id))) })] }));
};
