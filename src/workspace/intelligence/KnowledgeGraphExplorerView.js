import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const KnowledgeGraphExplorerView = () => {
    const nodes = [
        { id: 'msn_1001', type: 'MISSION', label: 'Invoice Mission #1001' },
        { id: 'ent_invoice', type: 'ENTITY', label: 'Invoice Schema v2' },
        { id: 'strat_fast', type: 'STRATEGY', label: 'Fast-Track Fan-Out Strategy' },
        { id: 'pol_gdpr', type: 'POLICY', label: 'EU Data Boundary Policy' },
        { id: 'ev_001', type: 'EVIDENCE', label: 'Merkle Root 0x8f2a...c31b' },
        { id: 'out_json', type: 'OUTCOME', label: 'Verified Document JSON' },
    ];
    const edges = [
        { from: 'msn_1001', to: 'ent_invoice', rel: 'PROCESSES_SCHEMA', evidence: '0x8f2a...c31b' },
        { from: 'msn_1001', to: 'strat_fast', rel: 'APPLIES_STRATEGY', evidence: '0x8f2a...c31b' },
        { from: 'strat_fast', to: 'pol_gdpr', rel: 'GOVERNED_BY', evidence: '0x8f2a...c31b' },
        { from: 'msn_1001', to: 'ev_001', rel: 'SUPPORTED_BY_EVIDENCE', evidence: '0x8f2a...c31b' },
        { from: 'ev_001', to: 'out_json', rel: 'PRODUCED_OUTCOME', evidence: '0x8f2a...c31b' },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Adaptive Knowledge Graph" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Pillar 6" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Evidence-linked knowledge graph connecting Missions \u2192 Entities \u2192 Strategies \u2192 Policies \u2192 Evidence \u2192 Outcomes." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Badge, { variant: "success", size: "md", children: ["Nodes: ", nodes.length, " | Edges: ", edges.length] }) })] }), _jsxs(Card, { className: "p-5 border-border/60", children: [_jsx("h3", { className: "text-sm font-semibold text-foreground mb-3", children: "Knowledge Graph Active Topology" }), _jsx("div", { className: "grid grid-cols-1 sm:grid-cols-3 gap-3 mb-6", children: nodes.map((n) => (_jsxs("div", { className: "p-3 rounded-lg border border-border/40 bg-muted/10", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-mono text-xs text-primary font-semibold", children: n.id }), _jsx(Badge, { variant: n.type === 'EVIDENCE' ? 'success' : n.type === 'STRATEGY' ? 'intelligence' : 'outline', size: "sm", children: n.type })] }), _jsx("div", { className: "text-xs font-medium text-foreground mt-1", children: n.label })] }, n.id))) }), _jsx("h3", { className: "text-sm font-semibold text-foreground mb-3", children: "Cryptographically Linked Graph Relationships" }), _jsx("div", { className: "space-y-2", children: edges.map((e, idx) => (_jsxs("div", { className: "p-2.5 rounded border border-border/40 bg-muted/5 flex items-center justify-between text-xs", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono font-semibold text-foreground", children: e.from }), _jsxs("span", { className: "text-primary font-mono", children: ["\u2192 [", e.rel, "] \u2192"] }), _jsx("span", { className: "font-mono font-semibold text-foreground", children: e.to })] }), _jsxs("div", { className: "text-[11px] font-mono text-muted-foreground", children: ["Proof Hash: ", _jsx("span", { className: "text-emerald-400", children: e.evidence })] })] }, idx))) })] })] }));
};
