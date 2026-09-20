import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Network, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { cognitiveApiClient } from '../../services/cognitiveApiClient';
export const EnterpriseCognitiveGraph = () => {
    const [graph, setGraph] = useState(null);
    const loadData = async () => {
        const data = await cognitiveApiClient.getCognitiveGraph();
        setGraph(data);
    };
    useEffect(() => {
        loadData();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Network, { className: "w-7 h-7 text-cyan-400" }), "Enterprise Cognitive Reasoning Graph"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Visual multi-hop causal reasoning connecting KPIs, Business Goals, Agents, Risks, and Hypotheses." })] }), _jsx(Button, { variant: "outline", onClick: loadData, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: "w-4 h-4" }), "Refresh Graph"] }) })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6", children: [_jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 space-y-3", children: [_jsxs("h2", { className: "text-base font-semibold text-slate-200", children: ["Cognitive Reasoning Nodes (", graph?.nodes.length || 0, ")"] }), _jsx("div", { className: "space-y-2 max-h-[460px] overflow-y-auto", children: graph?.nodes.map((n) => (_jsxs("div", { className: "p-3 rounded-lg bg-slate-800/40 border border-slate-700/60 space-y-1", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsx(Badge, { variant: "outline", className: "text-cyan-400 border-cyan-500/30 text-[10px]", children: n.node_type }), _jsx("span", { className: "text-[10px] text-slate-500 font-mono", children: n.id })] }), _jsx("p", { className: "text-sm font-medium text-slate-200", children: n.name })] }, n.id))) })] }), _jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 space-y-3", children: [_jsxs("h2", { className: "text-base font-semibold text-slate-200", children: ["Causal Relational Edges (", graph?.edges.length || 0, ")"] }), _jsx("div", { className: "space-y-2 max-h-[460px] overflow-y-auto", children: graph?.edges.map((e) => {
                                    const src = graph.nodes.find(n => n.id === e.source_node_id);
                                    const tgt = graph.nodes.find(n => n.id === e.target_node_id);
                                    return (_jsxs("div", { className: "p-3 rounded-lg bg-slate-800/40 border border-slate-700/60 text-xs flex items-center justify-between", children: [_jsx("span", { className: "font-medium text-slate-200", children: src?.name || e.source_node_id }), _jsxs("span", { className: "px-2 py-1 bg-indigo-950/60 text-indigo-300 rounded font-mono", children: ["--(", e.relation, ")-->"] }), _jsx("span", { className: "font-medium text-slate-200", children: tgt?.name || e.target_node_id })] }, e.id));
                                }) })] })] })] }));
};
