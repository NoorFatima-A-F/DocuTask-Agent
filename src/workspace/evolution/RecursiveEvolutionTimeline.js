import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { GitCommit, Clock, RefreshCw, ArrowRight, } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
export const RecursiveEvolutionTimeline = () => {
    const [cycles, setCycles] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        loadTimeline();
    }, []);
    const loadTimeline = async () => {
        setLoading(true);
        try {
            const data = await EvolutionPlatformApiClient.listCycleHistory();
            setCycles(data);
        }
        catch (err) {
            console.error('Failed to load cycle history:', err);
        }
        finally {
            setLoading(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-indigo-500/10 border border-indigo-500/20 rounded-xl", children: _jsx(GitCommit, { className: "w-6 h-6 text-indigo-400" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-xl font-bold text-slate-100", children: "Recursive Evolution Timeline & Genealogy" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Immutable Lineage" })] }), _jsx("p", { className: "text-sm text-slate-400 mt-0.5", children: "Chronological log of closed-loop self-evolution cycles, empirical fitness gains, and promoted architecture generations." })] })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsx(Button, { variant: "outline", onClick: loadTimeline, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }) })] }), _jsx("div", { className: "relative border-l-2 border-indigo-500/30 ml-4 pl-6 space-y-8 py-2", children: cycles.map((c) => (_jsxs("div", { className: "relative group", children: [_jsx("div", { className: "absolute -left-[31px] top-1.5 w-4 h-4 rounded-full bg-slate-950 border-2 border-indigo-500 group-hover:bg-indigo-500 transition-colors" }), _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3 hover:border-slate-700 transition-all", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-2", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("span", { className: "font-mono text-sm font-bold text-indigo-400", children: c.cycle_id }), _jsxs("span", { className: "text-sm font-semibold text-slate-200", children: ["Target: ", c.target_subsystem] }), _jsx(Badge, { variant: c.deployment_state === 'PROMOTED' ? 'success' : 'outline', size: "sm", children: c.stage })] }), _jsxs("div", { className: "flex items-center gap-2 text-xs font-mono text-slate-400", children: [_jsx(Clock, { className: "w-3.5 h-3.5" }), _jsx("span", { children: new Date(c.completed_at).toLocaleString() })] })] }), _jsxs("div", { className: "p-3 bg-slate-950/80 border border-slate-800 rounded-lg flex flex-wrap items-center gap-2 text-xs font-mono text-slate-400", children: [_jsx("span", { className: "text-slate-300 font-semibold", children: "Profile" }), _jsx(ArrowRight, { className: "w-3.5 h-3.5 text-slate-600" }), _jsxs("span", { className: "text-slate-300 font-semibold", children: [c.diagnosis_count, " Diagnoses"] }), _jsx(ArrowRight, { className: "w-3.5 h-3.5 text-slate-600" }), _jsxs("span", { className: "text-slate-300 font-semibold", children: [c.capability_gaps_found, " Gaps"] }), _jsx(ArrowRight, { className: "w-3.5 h-3.5 text-slate-600" }), _jsxs("span", { className: "text-amber-400 font-semibold", children: ["Pareto (", c.candidate_id, ")"] }), _jsx(ArrowRight, { className: "w-3.5 h-3.5 text-slate-600" }), _jsxs("span", { className: "text-purple-400 font-semibold", children: ["Mutation (", c.mutation_id, ")"] }), _jsx(ArrowRight, { className: "w-3.5 h-3.5 text-slate-600" }), _jsx("span", { className: "text-cyan-400 font-semibold", children: "Shadow Replay" }), _jsx(ArrowRight, { className: "w-3.5 h-3.5 text-slate-600" }), _jsxs("span", { className: "text-emerald-400 font-semibold", children: ["Gain +", c.benchmark_improvement_pct, "%"] })] }), _jsxs("div", { className: "flex items-center justify-between text-xs font-mono pt-1", children: [_jsxs("div", { className: "text-slate-400", children: ["Health Delta: ", _jsxs("span", { className: "text-slate-300", children: [(c.health_score_before * 100).toFixed(1), "%"] }), " \u2192 ", _jsxs("span", { className: "text-emerald-400 font-bold", children: [(c.health_score_after * 100).toFixed(1), "%"] })] }), _jsxs("div", { className: "text-slate-400", children: ["Governance: ", _jsx("span", { className: "text-emerald-400 font-semibold", children: c.governance_approved ? 'APPROVED' : 'PENDING' })] })] })] })] }, c.cycle_id))) })] }));
};
