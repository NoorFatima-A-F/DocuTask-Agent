import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Network, Info } from 'lucide-react';
export const KnowledgeGraphExplorer = () => {
    const [selectedNode, setSelectedNode] = useState('node-ocr-shard');
    const nodes = [
        {
            id: 'node-ocr-shard',
            label: 'Parallel OCR Sharding',
            type: 'EXECUTION_RULE',
            confidence: 0.965,
            version: '1.2.0',
            description: 'Partitions large PDF batches across 4 worker threads with jitter retry.',
            x: 180,
            y: 120,
            color: '#6366F1',
        },
        {
            id: 'node-smt-verify',
            label: 'Dynamic SMT Verification',
            type: 'VALIDATION_STRATEGY',
            confidence: 0.991,
            version: '1.0.0',
            description: 'Z3 SMT solver proving semantic schema constraints.',
            x: 460,
            y: 100,
            color: '#06B6D4',
        },
        {
            id: 'node-retry-backoff',
            label: 'Exponential Jitter Backoff',
            type: 'RESILIENCE_STRATEGY',
            confidence: 0.978,
            version: '1.1.0',
            description: 'Mitigates transient 429 throttling on worker API endpoints.',
            x: 180,
            y: 280,
            color: '#10B981',
        },
        {
            id: 'node-dag-opt',
            label: 'DAG Topology Optimizer',
            type: 'PLANNER_POLICY',
            confidence: 0.955,
            version: '2.0.0',
            description: 'Autonomous planner dynamic replanning and mutation heuristics.',
            x: 460,
            y: 280,
            color: '#A855F7',
        },
    ];
    const edges = [
        { source: 'node-ocr-shard', target: 'node-smt-verify', label: 'PRODUCES_EVIDENCE', weight: 0.95 },
        { source: 'node-ocr-shard', target: 'node-retry-backoff', label: 'FALLS_BACK_TO', weight: 0.88 },
        { source: 'node-dag-opt', target: 'node-ocr-shard', label: 'GOVERNS_EXECUTION', weight: 0.98 },
        { source: 'node-dag-opt', target: 'node-smt-verify', label: 'ENFORCES_INVARIANT', weight: 0.96 },
    ];
    const activeNodeData = nodes.find((n) => n.id === selectedNode);
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-indigo-500/20 to-cyan-500/20 border border-indigo-500/30 rounded-xl text-indigo-400", children: _jsx(Network, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Institutional Knowledge Graph", _jsx(Badge, { variant: "intelligence", size: "sm", children: "Phase 13.5" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] font-mono", children: "Semantic topology mapping relationships between execution rules, validation strategies, and planner heuristics" })] })] }), _jsxs("div", { className: "flex items-center gap-3 font-mono text-xs", children: [_jsx("span", { className: "text-[#94A3B8]", children: "Graph Density:" }), _jsx(Badge, { variant: "outline", size: "sm", children: "0.667 (Connected)" })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsx(Card, { className: "p-4 lg:col-span-2 rounded-2xl border border-[#1E293B] bg-[#0F172A] font-mono relative overflow-hidden h-[420px] flex items-center justify-center", children: _jsxs("svg", { className: "w-full h-full", viewBox: "0 0 640 400", children: [edges.map((edge, idx) => {
                                    const srcNode = nodes.find((n) => n.id === edge.source);
                                    const tgtNode = nodes.find((n) => n.id === edge.target);
                                    if (!srcNode || !tgtNode)
                                        return null;
                                    return (_jsxs("g", { children: [_jsx("line", { x1: srcNode.x, y1: srcNode.y, x2: tgtNode.x, y2: tgtNode.y, stroke: "#334155", strokeWidth: 2, strokeDasharray: "4 4" }), _jsx("text", { x: (srcNode.x + tgtNode.x) / 2, y: (srcNode.y + tgtNode.y) / 2 - 8, fill: "#64748B", fontSize: 9, textAnchor: "middle", fontFamily: "monospace", children: edge.label })] }, idx));
                                }), nodes.map((node) => {
                                    const isSelected = selectedNode === node.id;
                                    return (_jsxs("g", { onClick: () => setSelectedNode(node.id), className: "cursor-pointer transition-transform hover:scale-105", children: [_jsx("circle", { cx: node.x, cy: node.y, r: isSelected ? 32 : 26, fill: "#0F172A", stroke: node.color, strokeWidth: isSelected ? 3 : 2, filter: isSelected ? 'drop-shadow(0 0 8px rgba(99,102,241,0.5))' : undefined }), _jsx("text", { x: node.x, y: node.y + 4, fill: "#FFFFFF", fontSize: 10, fontWeight: "bold", textAnchor: "middle", fontFamily: "monospace", children: node.type.slice(0, 4) }), _jsx("text", { x: node.x, y: node.y + 44, fill: "#94A3B8", fontSize: 10, textAnchor: "middle", fontFamily: "monospace", children: node.label })] }, node.id));
                                })] }) }), _jsxs(Card, { className: "p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] font-mono space-y-4 flex flex-col justify-between", children: [_jsxs("div", { className: "space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-[#1E293B] pb-3", children: [_jsxs("span", { className: "text-xs font-bold text-white flex items-center gap-1.5", children: [_jsx(Info, { className: "w-4 h-4 text-indigo-400" }), "Node Inspector"] }), activeNodeData && (_jsxs(Badge, { variant: "outline", size: "sm", children: ["v", activeNodeData.version] }))] }), activeNodeData ? (_jsxs("div", { className: "space-y-3 text-xs", children: [_jsxs("div", { children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "NODE LABEL" }), _jsx("span", { className: "text-sm font-bold text-white", children: activeNodeData.label })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "CATEGORY TYPE" }), _jsx(Badge, { variant: "intelligence", size: "sm", className: "mt-1", children: activeNodeData.type })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "CONFIDENCE POSTERIOR" }), _jsxs("span", { className: "text-emerald-400 font-bold", children: [(activeNodeData.confidence * 100).toFixed(1), "% Verified"] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "ACTIONABLE DESCRIPTION" }), _jsx("p", { className: "text-[#94A3B8] mt-1 leading-relaxed", children: activeNodeData.description })] })] })) : (_jsx("div", { className: "text-xs text-[#64748B] text-center py-8", children: "Click any node in the topology canvas to inspect semantic properties." }))] }), _jsxs("div", { className: "pt-3 border-t border-[#1E293B] text-[11px] text-[#64748B] flex items-center justify-between", children: [_jsxs("span", { children: ["Graph Nodes: ", nodes.length] }), _jsxs("span", { children: ["Graph Edges: ", edges.length] })] })] })] })] }));
};
