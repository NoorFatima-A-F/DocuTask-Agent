import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Mutable Execution DAG Visualizer & Interactive Mutation Console.
 * Visualizes dynamic execution topology, node states, and supports runtime DAG splitting, replacement, and cloning.
 */
import React, { useState, useEffect } from 'react';
import { PlanningApiClient } from '../../services/planningApiClient';
export const MutableDAGViewerView = ({ missionId = 'mission_active_001', }) => {
    const [dag, setDag] = useState(null);
    const [loading, setLoading] = useState(true);
    const [selectedNodeId, setSelectedNodeId] = useState(null);
    const [mutationActionLoading, setMutationActionLoading] = useState(false);
    useEffect(() => {
        loadDAG();
    }, [missionId]);
    const loadDAG = async () => {
        setLoading(true);
        try {
            const activeDag = await PlanningApiClient.getDAG(missionId);
            setDag(activeDag);
            const nodeKeys = Object.keys(activeDag.nodes);
            const firstKey = nodeKeys[0];
            if (firstKey) {
                setSelectedNodeId(firstKey);
            }
        }
        catch (err) {
            console.error('Failed to load DAG', err);
        }
        finally {
            setLoading(false);
        }
    };
    const handleSplitNode = async (nodeId) => {
        setMutationActionLoading(true);
        try {
            const updatedDag = await PlanningApiClient.mutateDAG(missionId, 'NODE_SPLIT', nodeId, 2);
            setDag(updatedDag);
        }
        catch (err) {
            console.error('Split failed', err);
        }
        finally {
            setMutationActionLoading(false);
        }
    };
    const handleReplaceNode = async (nodeId) => {
        setMutationActionLoading(true);
        try {
            const updatedDag = await PlanningApiClient.mutateDAG(missionId, 'NODE_REPLACE', nodeId, 2);
            setDag(updatedDag);
        }
        catch (err) {
            console.error('Replace failed', err);
        }
        finally {
            setMutationActionLoading(false);
        }
    };
    if (loading || !dag) {
        return (_jsxs("div", { className: "flex items-center justify-center p-12 text-slate-400", children: [_jsx("div", { className: "animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500 mr-3" }), _jsx("span", { children: "Constructing Mutable Execution Topology..." })] }));
    }
    const nodesList = Object.values(dag.nodes);
    const selectedNode = selectedNodeId ? dag.nodes[selectedNodeId] : null;
    return (_jsxs("div", { className: "bg-slate-900 border border-slate-800 rounded-xl p-6 text-slate-100 shadow-2xl space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between border-b border-slate-800 pb-4 gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center space-x-3", children: [_jsx("span", { className: "px-2.5 py-1 text-xs font-bold uppercase tracking-wider bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 rounded-md", children: "Dynamic Execution Topology" }), _jsxs("span", { className: "text-xs text-slate-400 font-mono", children: ["DAG: ", dag.dag_id, " (v", dag.version, ")"] })] }), _jsx("h2", { className: "text-xl font-bold text-white mt-1", children: "Mutable Execution DAG & Live Mutations" }), _jsx("p", { className: "text-sm text-slate-400", children: "Runtime-adaptable graph supporting live shard splitting, capability hot-swapping, and branch rewiring." })] }), _jsx("div", { className: "flex items-center space-x-2", children: _jsx("button", { onClick: loadDAG, className: "px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold border border-slate-700 transition", children: "Refresh DAG" }) })] }), _jsx("div", { className: "bg-slate-950/70 border border-slate-800 rounded-lg p-5 overflow-x-auto", children: _jsx("div", { className: "flex items-center space-x-4 min-w-[700px]", children: nodesList.map((node, index) => {
                        const isSelected = node.node_id === selectedNodeId;
                        const isCompleted = node.status === 'COMPLETED';
                        const isRunning = node.status === 'RUNNING';
                        const isMutated = node.status === 'MUTATED';
                        return (_jsxs(React.Fragment, { children: [index > 0 && (_jsx("div", { className: "flex items-center text-slate-600 font-mono text-lg select-none", children: "\u2192" })), _jsxs("div", { onClick: () => setSelectedNodeId(node.node_id), className: `flex-1 min-w-[180px] p-3.5 rounded-lg border cursor-pointer transition-all duration-200 ${isSelected
                                        ? 'border-indigo-500 bg-indigo-950/40 shadow-lg shadow-indigo-500/10'
                                        : isCompleted
                                            ? 'border-emerald-700/60 bg-emerald-950/20 hover:border-emerald-600'
                                            : isRunning
                                                ? 'border-cyan-500/60 bg-cyan-950/30 animate-pulse'
                                                : isMutated
                                                    ? 'border-slate-800 bg-slate-900/40 opacity-50'
                                                    : 'border-slate-800 bg-slate-900/80 hover:border-slate-700'}`, children: [_jsxs("div", { className: "flex items-center justify-between mb-1.5", children: [_jsx("span", { className: "text-[10px] font-mono text-slate-400 truncate", children: node.node_id }), _jsx("span", { className: `text-[9px] font-bold uppercase px-1.5 py-0.5 rounded ${isCompleted
                                                        ? 'bg-emerald-500/20 text-emerald-400'
                                                        : isRunning
                                                            ? 'bg-cyan-500/20 text-cyan-300'
                                                            : isMutated
                                                                ? 'bg-slate-800 text-slate-500'
                                                                : 'bg-slate-800 text-slate-400'}`, children: node.status })] }), _jsx("div", { className: "font-semibold text-xs text-white truncate", children: node.name }), _jsx("div", { className: "text-[11px] font-mono text-indigo-300 mt-1 truncate", children: node.provider })] })] }, node.node_id));
                    }) }) }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: [selectedNode ? (_jsxs("div", { className: "bg-slate-950/60 border border-slate-800 rounded-lg p-4 space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-slate-800/80 pb-2", children: [_jsxs("h4", { className: "text-xs font-bold uppercase tracking-wider text-slate-300", children: ["Node Inspector: ", _jsx("span", { className: "text-indigo-400 font-mono", children: selectedNode.node_id })] }), _jsx("span", { className: "text-xs font-mono text-emerald-400", children: selectedNode.status })] }), _jsxs("div", { className: "grid grid-cols-2 gap-2 text-xs font-mono", children: [_jsxs("div", { children: [_jsx("span", { className: "text-slate-500 block text-[10px]", children: "CAPABILITY" }), _jsx("span", { className: "text-slate-300", children: selectedNode.capability_id })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500 block text-[10px]", children: "PROVIDER" }), _jsx("span", { className: "text-slate-300", children: selectedNode.provider })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500 block text-[10px]", children: "RETRIES" }), _jsxs("span", { className: "text-slate-300", children: [selectedNode.retry_count, " / ", selectedNode.max_retries] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500 block text-[10px]", children: "TIMEOUT" }), _jsxs("span", { className: "text-slate-300", children: [selectedNode.timeout_ms, " ms"] })] })] }), _jsxs("div", { className: "pt-2 border-t border-slate-800 flex flex-wrap gap-2", children: [_jsx("button", { onClick: () => handleSplitNode(selectedNode.node_id), disabled: mutationActionLoading || selectedNode.status === 'COMPLETED', className: "px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white rounded text-xs font-semibold transition", children: "Split into 2 Shards" }), _jsx("button", { onClick: () => handleReplaceNode(selectedNode.node_id), disabled: mutationActionLoading || selectedNode.status === 'COMPLETED', className: "px-3 py-1.5 bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-slate-200 border border-slate-700 rounded text-xs font-semibold transition", children: "Hot-Swap Capability" })] })] })) : (_jsx("div", { className: "bg-slate-950/60 border border-slate-800 rounded-lg p-4 text-xs text-slate-500 flex items-center justify-center", children: "Select a DAG node to inspect properties and trigger mutations." })), _jsxs("div", { className: "bg-slate-950/60 border border-slate-800 rounded-lg p-4 space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-slate-800/80 pb-2", children: [_jsx("h4", { className: "text-xs font-bold uppercase tracking-wider text-slate-300", children: "DAG Mutation Audit Trail" }), _jsxs("span", { className: "text-[10px] font-mono text-slate-500", children: [dag.mutation_history.length, " events"] })] }), _jsx("div", { className: "space-y-2 max-h-48 overflow-y-auto pr-1", children: dag.mutation_history.length === 0 ? (_jsx("p", { className: "text-xs text-slate-500 font-mono", children: "No mutations applied to current topology." })) : (dag.mutation_history.map((m) => (_jsxs("div", { className: "p-2 bg-slate-900/90 rounded border border-slate-800 text-xs font-mono", children: [_jsxs("div", { className: "flex items-center justify-between text-[10px]", children: [_jsx("span", { className: "font-bold text-cyan-400", children: m.mutation_type }), _jsx("span", { className: "text-slate-500", children: new Date(m.timestamp).toLocaleTimeString() })] }), _jsx("div", { className: "text-slate-300 mt-1 font-sans", children: m.diff_summary }), _jsx("div", { className: "text-[10px] text-slate-500 mt-0.5", children: m.rationale })] }, m.mutation_id)))) })] })] })] }));
};
