import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { GitCommit, ArrowRight, RefreshCw, } from 'lucide-react';
import { ApdlePlannerApiClient } from '../../services/apdlePlannerApiClient';
export const DependencyExplorer = () => {
    const [dag, setDag] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        loadDag();
    }, []);
    const loadDag = async () => {
        setLoading(true);
        try {
            const data = await ApdlePlannerApiClient.getGraph('default_mission');
            setDag(data);
        }
        catch (e) {
            console.error('Failed to load dependencies:', e);
        }
        finally {
            setLoading(false);
        }
    };
    return (_jsx("div", { className: "space-y-6 font-mono", children: _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-bold text-cyan-300 flex items-center gap-2", children: [_jsx(GitCommit, { className: "w-4 h-4 text-purple-400" }), "Dynamic Dependency Resolution Explorer"] }), _jsx("p", { className: "text-xs text-slate-400 mt-0.5", children: "Inspects typed dependency edges (Hard, Soft, Optional, Conditional) and runtime satisfaction states." })] }), _jsx("button", { onClick: loadDag, disabled: loading, className: "text-slate-400 hover:text-cyan-400 p-1.5 rounded", title: "Refresh", children: _jsx(RefreshCw, { className: `w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}` }) })] }), _jsx("div", { className: "space-y-3", children: dag?.edges.map((edge) => {
                        const sourceNode = dag.nodes.find((n) => n.id === edge.source);
                        const targetNode = dag.nodes.find((n) => n.id === edge.target);
                        return (_jsxs("div", { className: "p-3 bg-slate-950/80 border border-slate-800 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("span", { className: "font-bold text-slate-200", children: sourceNode?.label || edge.source }), _jsx(ArrowRight, { className: "w-4 h-4 text-slate-500 shrink-0" }), _jsx("span", { className: "font-bold text-slate-200", children: targetNode?.label || edge.target })] }), _jsxs("div", { className: "flex items-center gap-2 shrink-0", children: [_jsx("span", { className: "px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-300 border border-slate-700", children: edge.edge_type }), edge.is_critical_path && (_jsx("span", { className: "px-2 py-0.5 rounded text-[10px] bg-amber-950 text-amber-300 border border-amber-800 font-bold", children: "CRITICAL EDGE" }))] })] }, edge.id));
                    }) })] }) }));
};
