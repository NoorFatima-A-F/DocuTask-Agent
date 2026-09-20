import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Sparkles, GitBranch, RefreshCw, Plus, Minus, } from 'lucide-react';
import { ApdlePlannerApiClient } from '../../services/apdlePlannerApiClient';
export const GraphMutationTimeline = () => {
    const [mutations, setMutations] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        loadMutations();
    }, []);
    const loadMutations = async () => {
        setLoading(true);
        try {
            const data = await ApdlePlannerApiClient.getMutations('default_mission');
            setMutations(data);
        }
        catch (e) {
            console.error('Failed to load mutations:', e);
        }
        finally {
            setLoading(false);
        }
    };
    return (_jsx("div", { className: "space-y-6 font-mono", children: _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-bold text-cyan-300 flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4 text-purple-400" }), "Runtime Graph Mutation & Replanning History"] }), _jsx("p", { className: "text-xs text-slate-400 mt-0.5", children: "Audit log of in-flight structural DAG alterations. Inspects injected recovery pipelines and topology diffs." })] }), _jsx("button", { onClick: loadMutations, disabled: loading, className: "text-slate-400 hover:text-cyan-400 p-1.5 rounded", title: "Refresh", children: _jsx(RefreshCw, { className: `w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}` }) })] }), mutations.length === 0 ? (_jsx("div", { className: "p-8 text-center text-slate-500 text-xs bg-slate-950/60 rounded-lg", children: "No runtime mutations applied yet. The DAG is currently executing on its nominal synthesis plan." })) : (_jsx("div", { className: "space-y-3", children: mutations.map((m, idx) => (_jsxs("div", { className: "p-4 bg-slate-950/80 border border-purple-800/60 rounded-xl space-y-2 text-xs", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("span", { className: "font-bold text-purple-300 flex items-center gap-2", children: [_jsx(GitBranch, { className: "w-3.5 h-3.5" }), "Mutation ", m.mutation_type] }), _jsx("span", { className: "text-[10px] text-slate-500", children: m.mutation_id })] }), _jsx("div", { className: "text-slate-300 text-[11px]", children: m.trigger_reason }), _jsxs("div", { className: "grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 border-t border-slate-800/80 text-[10px]", children: [_jsxs("div", { className: "flex items-center gap-1 text-emerald-400", children: [_jsx(Plus, { className: "w-3 h-3" }), " ", m.nodes_added_count, " Nodes Added"] }), _jsxs("div", { className: "flex items-center gap-1 text-slate-400", children: [_jsx(Minus, { className: "w-3 h-3" }), " ", m.nodes_removed_count, " Nodes Removed"] }), _jsxs("div", { className: "flex items-center gap-1 text-cyan-300", children: ["+", m.edges_added_count, " Edges Rewired"] }), _jsx("div", { className: "text-right text-slate-500", children: new Date(m.timestamp * 1000).toLocaleTimeString() })] })] }, m.mutation_id || idx))) }))] }) }));
};
