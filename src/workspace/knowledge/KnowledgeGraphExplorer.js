import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Layers, Network, Cpu, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { knowledgeApiClient } from '../../services/knowledgeApiClient';
export const KnowledgeGraphExplorer = () => {
    const [graphData, setGraphData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [selectedNode, setSelectedNode] = useState(null);
    const loadGraph = async () => {
        setLoading(true);
        try {
            const data = await knowledgeApiClient.getGraphOverview();
            setGraphData(data);
            if (data.nodes.length > 0 && !selectedNode) {
                setSelectedNode(data.nodes[0] || null);
            }
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadGraph();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Network, { className: "w-7 h-7 text-cyan-400" }), "Enterprise Knowledge Graph & Ontology"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Visual organizational ontology connecting employees, departments, AI agents, systems, and policies." })] }), _jsx(Button, { variant: "outline", onClick: loadGraph, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh Graph"] }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 space-y-4", children: [_jsxs("h2", { className: "text-base font-semibold text-slate-200 flex items-center gap-2", children: [_jsx(Layers, { className: "w-4 h-4 text-cyan-400" }), "Ontology Nodes (", graphData?.total_nodes || 0, ")"] }), _jsx("div", { className: "space-y-2 max-h-[460px] overflow-y-auto", children: graphData?.nodes.map((node) => (_jsxs("div", { onClick: () => setSelectedNode(node), className: `p-3 rounded-lg border cursor-pointer transition-colors ${selectedNode?.id === node.id
                                        ? 'bg-cyan-950/40 border-cyan-500/50'
                                        : 'bg-slate-800/40 border-slate-700/50 hover:border-slate-600'}`, children: [_jsxs("div", { className: "flex justify-between items-center mb-1", children: [_jsx(Badge, { variant: "outline", className: "text-cyan-400 border-cyan-500/30 text-[10px]", children: node.entity_type }), _jsx("span", { className: "text-[10px] text-slate-500", children: "Confidence: 100%" })] }), _jsx("p", { className: "text-sm font-medium text-slate-200", children: node.name })] }, node.id))) })] }), _jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 lg:col-span-2 space-y-5", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-lg font-semibold text-slate-100 flex items-center gap-2 mb-1", children: [_jsx(Cpu, { className: "w-5 h-5 text-indigo-400" }), "Entity Traversal & Impact Analysis"] }), _jsxs("p", { className: "text-xs text-slate-400", children: ["Selected node: ", _jsx("span", { className: "text-cyan-400 font-semibold", children: selectedNode?.name || 'None' })] })] }), selectedNode && (_jsxs("div", { className: "p-4 rounded-lg bg-slate-800/60 border border-slate-700 space-y-3", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsx("span", { className: "text-xs text-slate-400 uppercase font-semibold", children: "Node ID" }), _jsx("span", { className: "font-mono text-xs text-slate-300", children: selectedNode.id })] }), _jsxs("div", { className: "flex justify-between items-center", children: [_jsx("span", { className: "text-xs text-slate-400 uppercase font-semibold", children: "Entity Type" }), _jsx(Badge, { variant: "info", children: selectedNode.entity_type })] })] })), _jsxs("div", { children: [_jsx("h3", { className: "text-sm font-semibold text-slate-200 mb-3", children: "Relational Graph Connections" }), _jsx("div", { className: "space-y-2", children: graphData?.edges.map((edge) => {
                                            const src = graphData.nodes.find(n => n.id === edge.source_node_id);
                                            const tgt = graphData.nodes.find(n => n.id === edge.target_node_id);
                                            return (_jsxs("div", { className: "p-3 bg-slate-800/40 rounded border border-slate-700/60 flex items-center justify-between text-xs", children: [_jsx("span", { className: "font-medium text-slate-200", children: src?.name || edge.source_node_id }), _jsxs("span", { className: "px-2 py-1 bg-cyan-950/60 text-cyan-300 rounded font-mono", children: ["--(", edge.relation_type, ")-->"] }), _jsx("span", { className: "font-medium text-slate-200", children: tgt?.name || edge.target_node_id })] }, edge.id));
                                        }) })] })] })] })] }));
};
