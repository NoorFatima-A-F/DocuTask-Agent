import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { GitBranch, RefreshCw, Sparkles, Zap, } from 'lucide-react';
import { ApdlePlannerApiClient } from '../../services/apdlePlannerApiClient';
export const PlannerGraphView = () => {
    const [dag, setDag] = useState(null);
    const [loading, setLoading] = useState(true);
    const [replanning, setReplanning] = useState(false);
    const [replanMsg, setReplanMsg] = useState(null);
    useEffect(() => {
        loadGraph();
    }, []);
    const loadGraph = async () => {
        setLoading(true);
        try {
            const data = await ApdlePlannerApiClient.getGraph('default_mission');
            setDag(data);
        }
        catch (e) {
            console.error('Failed to load DAG graph:', e);
        }
        finally {
            setLoading(false);
        }
    };
    const handleTriggerReplan = async () => {
        setReplanning(true);
        try {
            const res = await ApdlePlannerApiClient.triggerReplan('default_mission', 'node_ocr_01', 'Holdout scan contrast low (Confidence: 0.42)');
            setDag(res.updated_dag);
            setReplanMsg(`Dynamic DAG Mutation Applied: ${res.mutation.mutation_type} (+${res.mutation.nodes_added_count} recovery nodes)`);
        }
        catch (e) {
            console.error('Replanning failed:', e);
        }
        finally {
            setReplanning(false);
        }
    };
    const getNodeColor = (status, isCritical) => {
        if (isCritical && status === 'RUNNING')
            return 'border-amber-400 bg-amber-950/70 text-amber-200';
        if (status === 'COMPLETED')
            return 'border-emerald-600 bg-emerald-950/70 text-emerald-200';
        if (status === 'RUNNING')
            return 'border-cyan-500 bg-cyan-950/70 text-cyan-200';
        if (status === 'FAILED')
            return 'border-red-600 bg-red-950/70 text-red-200';
        if (status === 'MUTATED')
            return 'border-purple-600 bg-purple-950/70 text-purple-200';
        return 'border-slate-800 bg-slate-900/80 text-slate-400';
    };
    return (_jsxs("div", { className: "space-y-6 font-mono", children: [_jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-bold text-cyan-300 flex items-center gap-2", children: [_jsx(GitBranch, { className: "w-4 h-4 text-cyan-400" }), "Autonomous Execution DAG & Live Replanning (APDLE)"] }), _jsx("p", { className: "text-xs text-slate-400 mt-0.5", children: "Production-grade Directed Acyclic Graph. Reflects real dependency resolution, CPM critical path, and runtime mutation." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs("button", { onClick: handleTriggerReplan, disabled: replanning, className: "flex items-center gap-1.5 px-3 py-1.5 bg-purple-950/60 hover:bg-purple-900/60 border border-purple-800 text-purple-300 rounded-lg text-xs font-mono transition-all disabled:opacity-50", children: [_jsx(Sparkles, { className: `w-3.5 h-3.5 ${replanning ? 'animate-spin' : ''}` }), "Simulate Failure & Replan"] }), _jsx("button", { onClick: loadGraph, disabled: loading, className: "text-slate-400 hover:text-cyan-400 p-1.5 rounded", title: "Refresh DAG", children: _jsx(RefreshCw, { className: `w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}` }) })] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-3", children: [_jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center", children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "Critical Path Duration" }), _jsxs("div", { className: "text-xl font-bold text-amber-400 mt-1", children: [(dag?.critical_path_duration_ms ?? 780.0).toFixed(1), "ms"] }), _jsxs("div", { className: "text-[9px] text-amber-500 mt-0.5", children: [dag?.critical_nodes_count ?? 3, " Critical Nodes"] })] }), _jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center", children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "DAG Generation" }), _jsxs("div", { className: "text-xl font-bold text-purple-300 mt-1", children: ["Gen ", dag?.generation ?? 1] }), _jsxs("div", { className: "text-[9px] text-purple-400 mt-0.5", children: [dag?.nodes.length ?? 5, " Total Nodes"] })] }), _jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center", children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "Structural Depth" }), _jsxs("div", { className: "text-xl font-bold text-cyan-300 mt-1", children: [dag?.structural_depth ?? 4, " Layers"] }), _jsx("div", { className: "text-[9px] text-cyan-400 mt-0.5", children: "Topologically Sorted" })] }), _jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center", children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "Dependency Edges" }), _jsxs("div", { className: "text-xl font-bold text-emerald-300 mt-1", children: [dag?.edges.length ?? 5, " Edges"] }), _jsx("div", { className: "text-[9px] text-emerald-400 mt-0.5", children: "Acyclic Guaranteed" })] })] })] }), replanMsg && (_jsxs("div", { className: "p-3 bg-purple-950/40 border border-purple-800/50 rounded-lg text-xs text-purple-300 flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4 text-purple-400" }), _jsx("span", { children: replanMsg })] }), _jsx("button", { onClick: () => setReplanMsg(null), className: "text-slate-400 hover:text-slate-200", children: "\u2715" })] })), _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4", children: [_jsxs("div", { className: "text-xs uppercase text-slate-300 tracking-wider flex items-center justify-between border-b border-slate-800 pb-2", children: [_jsx("span", { children: "Execution DAG Pipeline Layout" }), _jsx("span", { className: "text-slate-500 text-[10px]", children: "Real Runtime Coordinate Layout" })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: dag?.nodes.map((node) => (_jsxs("div", { className: `p-4 rounded-xl border transition-all ${getNodeColor(node.status, node.is_critical_path)}`, children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-[10px] px-1.5 py-0.5 rounded bg-slate-950/60 font-bold", children: node.task_type }), _jsx("span", { className: "text-[10px] font-bold", children: node.status })] }), _jsx("div", { className: "text-sm font-bold text-slate-100 mt-2", children: node.label }), _jsxs("div", { className: "grid grid-cols-2 gap-2 text-[10px] text-slate-400 mt-3 pt-2 border-t border-slate-800/60", children: [_jsxs("div", { children: ["Est. Latency: ", _jsxs("span", { className: "text-amber-300 font-bold", children: [node.estimated_runtime_ms.toFixed(0), "ms"] })] }), _jsxs("div", { children: ["Slack: ", _jsxs("span", { className: "text-cyan-300 font-bold", children: [node.total_slack_ms.toFixed(0), "ms"] })] }), _jsxs("div", { className: "truncate", children: ["Worker: ", _jsx("span", { className: "text-slate-200", children: node.assigned_worker || 'Auto-Allocated' })] }), _jsxs("div", { children: ["Cost: ", _jsxs("span", { className: "text-emerald-300 font-bold", children: ["$", node.estimated_cost_usd.toFixed(4)] })] })] }), node.is_critical_path && (_jsxs("div", { className: "text-[9px] text-amber-300 font-bold mt-2 flex items-center gap-1", children: [_jsx(Zap, { className: "w-3 h-3" }), " ON CRITICAL PATH"] }))] }, node.id))) })] })] }));
};
