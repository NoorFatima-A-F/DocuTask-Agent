import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { RefreshCw, } from 'lucide-react';
export const StrategicKnowledgeGraph = () => {
    const [selectedNodeId, setSelectedNodeId] = useState('obs-node-1');
    const nodes = [
        {
            id: 'obs-node-1',
            type: 'SUBSYSTEM',
            label: 'APDLE Live DAG Scheduler',
            details: 'Current greedy critical-path heuristic scheduler operating at 180ms baseline.',
            connections: 3,
        },
        {
            id: 'obs-node-2',
            type: 'METRIC_ANOMALY',
            label: 'OCR Burst Serialization',
            details: 'Queue depth spiked to 14 tasks during 50-page PDF ingestion (+128% latency).',
            connections: 2,
        },
        {
            id: 'obs-node-3',
            type: 'SUBSYSTEM',
            label: 'Ed25519 Validator Strike Team',
            details: 'Triadic consensus verification engine with 100% mathematical zero-fabrication ratio.',
            connections: 2,
        },
        {
            id: 'obs-node-4',
            type: 'FAILURE_PATTERN',
            label: 'Repeated Cold Embedding Overhead',
            details: 'Redundant token embedding calls for recurrent corporate balance sheet templates.',
            connections: 1,
        },
    ];
    const edges = [
        { source: 'OCR Burst Serialization', target: 'APDLE Live DAG Scheduler', relationship: 'CONSTRAINED_BY', weight: 0.88 },
        { source: 'APDLE Live DAG Scheduler', target: 'Ed25519 Validator Strike Team', relationship: 'CORRELATES_WITH', weight: 0.96 },
        { source: 'Repeated Cold Embedding Overhead', target: 'APDLE Live DAG Scheduler', relationship: 'CAUSED_BY', weight: 0.74 },
    ];
    const selectedNode = nodes.find((n) => n.id === selectedNodeId) ?? nodes[0];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Strategic Knowledge Graph" }), _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: true, children: "CROSS-MISSION GRAPH ONLINE" }), _jsx(Badge, { variant: "outline", size: "sm", children: "AMRS-RSIP Phase 13.9" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Queryable Strategic Evidence Graph connecting operational incidents, bottlenecks, failure patterns, and verifiable causal links." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "outline", size: "sm", children: [_jsx(RefreshCw, { className: "w-3.5 h-3.5 mr-1.5" }), "Re-index Graph"] }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-12 gap-6", children: [_jsxs("div", { className: "lg:col-span-5 space-y-3", children: [_jsxs("h2", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider", children: ["Evidence Nodes (", nodes.length, ")"] }), nodes.map((n) => (_jsxs(Card, { onClick: () => setSelectedNodeId(n.id), className: `p-4 cursor-pointer transition-all border ${selectedNodeId === n.id
                                    ? 'border-purple-500/60 bg-purple-950/30 shadow-sm'
                                    : 'border-border/40 bg-secondary/10 hover:bg-secondary/20'}`, children: [_jsxs("div", { className: "flex items-start justify-between gap-2", children: [_jsxs("div", { className: "space-y-1", children: [_jsx(Badge, { variant: n.type === 'METRIC_ANOMALY'
                                                            ? 'warning'
                                                            : n.type === 'FAILURE_PATTERN'
                                                                ? 'error'
                                                                : 'intelligence', size: "sm", children: n.type.replace('_', ' ') }), _jsx("h3", { className: "text-sm font-semibold text-foreground", children: n.label })] }), _jsxs("span", { className: "text-xs font-mono text-muted-foreground", children: [n.connections, " Edges"] })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-2", children: n.details })] }, n.id)))] }), _jsx("div", { className: "lg:col-span-7 space-y-4", children: _jsxs(Card, { className: "p-5 border-border/40 space-y-4", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx("span", { className: "text-xs font-mono font-bold text-purple-400", children: "NODE INSPECTION" }), _jsx("h3", { className: "text-lg font-bold text-foreground mt-0.5", children: selectedNode.label })] }), _jsxs(Badge, { variant: "outline", size: "sm", children: ["Type: ", selectedNode.type] })] }), _jsx("p", { className: "text-xs text-muted-foreground leading-relaxed", children: selectedNode.details }), _jsxs("div", { className: "space-y-2 pt-2", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider", children: "Cryptographic Causal Edges" }), _jsx("div", { className: "space-y-2", children: edges.map((e, idx) => (_jsxs("div", { className: "flex items-center justify-between p-3 rounded-lg border border-purple-500/20 bg-purple-950/10 text-xs font-mono", children: [_jsxs("div", { className: "flex items-center gap-2 truncate max-w-sm", children: [_jsx("span", { className: "text-foreground", children: e.source }), _jsxs("span", { className: "text-purple-400 font-bold", children: ["-[ ", e.relationship, " ]->"] }), _jsx("span", { className: "text-foreground", children: e.target })] }), _jsxs(Badge, { variant: "success", size: "sm", children: ["Weight: ", e.weight] })] }, idx))) })] })] }) })] })] }));
};
