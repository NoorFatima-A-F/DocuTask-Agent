import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Sparkles, TrendingUp, CheckCircle2, RefreshCw, Trophy, } from 'lucide-react';
import { CognitiveEvolutionApiClient } from '../../services/cognitiveEvolutionApiClient';
export const PlannerEvolutionTimeline = () => {
    const [generations, setGenerations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [evolving, setEvolving] = useState(false);
    const [evolutionReport, setEvolutionReport] = useState(null);
    useEffect(() => {
        loadGenerations();
    }, []);
    const loadGenerations = async () => {
        setLoading(true);
        try {
            const data = await CognitiveEvolutionApiClient.listPlannerGenerations();
            setGenerations(data);
        }
        catch (e) {
            console.error('Failed to load planner generations:', e);
        }
        finally {
            setLoading(false);
        }
    };
    const handleTriggerEvolution = async () => {
        setEvolving(true);
        try {
            const report = await CognitiveEvolutionApiClient.evolvePlanner('Sub-optimal token allocation in high-noise scans');
            setEvolutionReport(report);
            await loadGenerations();
        }
        catch (e) {
            console.error('Planner self-evolution failed:', e);
        }
        finally {
            setEvolving(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-bold font-mono text-cyan-300 flex items-center gap-2", children: [_jsx(TrendingUp, { className: "w-4 h-4 text-cyan-400" }), "Planner Self-Evolution & Continuous Rewriting Engine"] }), _jsx("p", { className: "text-xs text-slate-400 mt-0.5", children: "Closed-loop evolutionary self-rewriting: Weakness Detection \u2192 Chromosome Mutation \u2192 1,000 Trial Digital Twin Simulation \u2192 Canary Promotion." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs("button", { onClick: handleTriggerEvolution, disabled: evolving, className: "flex items-center gap-2 px-3 py-1.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white rounded-lg text-xs font-mono font-bold shadow-lg shadow-purple-950/40 transition-all disabled:opacity-50", children: [_jsx(Sparkles, { className: `w-3.5 h-3.5 ${evolving ? 'animate-spin' : ''}` }), "Evolve Next Planner Generation"] }), _jsx("button", { onClick: loadGenerations, disabled: loading, className: "text-slate-400 hover:text-cyan-400 p-1.5 rounded", title: "Refresh generations", children: _jsx(RefreshCw, { className: `w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}` }) })] })] }), evolutionReport && (_jsxs("div", { className: "p-4 bg-purple-950/40 border border-purple-800/60 rounded-lg space-y-2 font-mono text-xs", children: [_jsxs("div", { className: "flex items-center justify-between text-purple-300 font-bold", children: [_jsxs("span", { className: "flex items-center gap-1.5", children: [_jsx(CheckCircle2, { className: "w-4 h-4 text-emerald-400" }), "Evolution Cycle Success: ", evolutionReport.previous_version, " \u2192 ", evolutionReport.candidate_version] }), _jsxs("span", { className: "text-emerald-400 font-bold", children: ["+", evolutionReport.utility_gain_pct, "% Pareto Gain"] })] }), _jsx("p", { className: "text-slate-300 text-[11px]", children: evolutionReport.rationale })] }))] }), _jsxs("div", { className: "space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("h4", { className: "text-xs font-mono uppercase tracking-wider text-slate-400", children: ["Immutable Planner Generation Genealogy (", generations.length, " Versions)"] }), _jsx("span", { className: "text-[10px] font-mono text-slate-500", children: "Cryptographically Sealed Merkle Lineage" })] }), _jsx("div", { className: "space-y-3", children: generations.map((gen, idx) => {
                            const isProduction = gen.is_promoted_production;
                            return (_jsxs("div", { className: `p-5 rounded-xl border font-mono transition-all ${isProduction
                                    ? 'bg-slate-900/90 border-cyan-500/60 shadow-lg shadow-cyan-950/20'
                                    : 'bg-slate-950/70 border-slate-800/80'}`, children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 text-cyan-300 flex items-center justify-center font-bold text-sm", children: gen.version_tag }), _jsxs("div", { children: [_jsxs("div", { className: "text-sm font-bold text-slate-100 flex items-center gap-2", children: [_jsxs("span", { children: ["Generation ", idx + 1] }), isProduction && (_jsxs("span", { className: "px-2 py-0.5 rounded text-[10px] bg-cyan-950 text-cyan-300 border border-cyan-800 flex items-center gap-1", children: [_jsx(Trophy, { className: "w-3 h-3 text-amber-400" }), "ACTIVE PRODUCTION"] }))] }), _jsxs("div", { className: "text-[10px] text-slate-500 mt-0.5", children: ["Parent: ", gen.parent_version || 'None (Genesis)', " \u2022 Sealed:", ' ', _jsxs("span", { className: "text-purple-400", children: [gen.cryptographic_seal_hash.slice(0, 16), "..."] })] })] })] }), _jsxs("div", { className: "flex items-center gap-4 text-right", children: [_jsxs("div", { children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "Benchmark Utility" }), _jsx("div", { className: "text-base font-bold text-emerald-400", children: gen.benchmark_utility.toFixed(4) })] }), _jsxs("div", { children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "Brier Error (\u2193)" }), _jsx("div", { className: "text-base font-bold text-purple-300", children: gen.brier_score.toFixed(3) })] })] })] }), _jsxs("div", { className: "grid grid-cols-2 sm:grid-cols-4 gap-2 pt-3 text-xs", children: [_jsxs("div", { className: "bg-slate-950/60 border border-slate-800/60 rounded p-2 text-center", children: [_jsx("span", { className: "text-[10px] text-slate-500 uppercase", children: "Weight Acc" }), _jsx("div", { className: "font-bold text-slate-200 mt-0.5", children: gen.parameters.weight_accuracy || 0.5 })] }), _jsxs("div", { className: "bg-slate-950/60 border border-slate-800/60 rounded p-2 text-center", children: [_jsx("span", { className: "text-[10px] text-slate-500 uppercase", children: "Weight Cost" }), _jsx("div", { className: "font-bold text-slate-200 mt-0.5", children: gen.parameters.weight_cost || 0.3 })] }), _jsxs("div", { className: "bg-slate-950/60 border border-slate-800/60 rounded p-2 text-center", children: [_jsx("span", { className: "text-[10px] text-slate-500 uppercase", children: "Beam Width" }), _jsx("div", { className: "font-bold text-cyan-300 mt-0.5", children: gen.parameters.beam_width || 8 })] }), _jsxs("div", { className: "bg-slate-950/60 border border-slate-800/60 rounded p-2 text-center", children: [_jsx("span", { className: "text-[10px] text-slate-500 uppercase", children: "Sim. Trials" }), _jsx("div", { className: "font-bold text-amber-300 mt-0.5", children: gen.simulated_trials_count })] })] })] }, gen.generation_id || idx));
                        }) })] })] }));
};
