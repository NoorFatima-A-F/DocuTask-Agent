import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { EsmrReplayApiClient } from '../../services/esmrReplayApiClient';
export const PlannerEvolutionHistoryView = ({ missionId }) => {
    const [decisions, setDecisions] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        EsmrReplayApiClient.getDecisions(missionId)
            .then(setDecisions)
            .catch(console.error)
            .finally(() => setLoading(false));
    }, [missionId]);
    if (loading) {
        return (_jsx("div", { className: "p-6 bg-slate-900 border border-slate-800 rounded-xl text-slate-400 animate-pulse", children: "Loading Planner Generation History..." }));
    }
    return (_jsxs("div", { className: "bg-slate-950 border border-slate-800 rounded-xl p-6 shadow-2xl space-y-6 text-slate-100", children: [_jsx("div", { className: "flex items-center justify-between border-b border-slate-800 pb-4", children: _jsxs("div", { children: [_jsxs("h3", { className: "text-lg font-bold text-white flex items-center gap-2", children: [_jsx("span", { children: "\uD83E\uDDEC" }), " Autonomous Planner Evolution & Mutation History"] }), _jsx("p", { className: "text-xs text-slate-400 mt-1", children: "Tracking multi-generational evolutionary planner mutations and strategy syntheses across execution cycles." })] }) }), _jsx("div", { className: "space-y-4", children: decisions.map((d) => (_jsxs("div", { className: "bg-slate-900/80 border border-slate-800 p-5 rounded-xl space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsxs("span", { className: "px-2.5 py-1 text-xs font-mono font-bold bg-indigo-950 border border-indigo-500/40 text-indigo-300 rounded", children: ["Generation ", d.planner_generation] }), _jsx("span", { className: "text-sm font-bold text-white", children: d.selected_strategy })] }), _jsxs("span", { className: "text-xs font-mono text-emerald-400", children: ["Utility: ", d.utility_breakdown.total_utility.toFixed(4)] })] }), _jsx("p", { className: "text-xs text-slate-300", children: d.why }), d.alternatives_evaluated.length > 0 && (_jsxs("div", { className: "bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-2", children: [_jsxs("span", { className: "text-[11px] font-bold text-slate-400 uppercase font-mono", children: ["Candidate Strategies Competed in Generation ", d.planner_generation] }), _jsx("div", { className: "space-y-1.5 text-xs", children: d.alternatives_evaluated.map((alt) => (_jsxs("div", { className: "flex items-center justify-between text-slate-300 border-b border-slate-850 pb-1", children: [_jsx("span", { className: "font-semibold text-slate-200", children: alt.strategy_name }), _jsxs("span", { className: "font-mono text-slate-400", children: ["Score: ", alt.utility_score.toFixed(3)] }), _jsx("span", { className: "text-rose-400 text-[11px]", children: alt.rejection_reason })] }, alt.strategy_name))) })] }))] }, d.decision_id))) })] }));
};
