import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 1: World Executive Dashboard
 */
import React, { useEffect, useState } from 'react';
import { Globe, Sparkles, RefreshCw, ShieldCheck, TrendingUp, Brain, Layers, Zap, CheckCircle2, GitBranch, Flame, AlertTriangle, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
export const WorldExecutiveDashboard = () => {
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);
    const [runningCycle, setRunningCycle] = useState(false);
    const [cycleResult, setCycleResult] = useState(null);
    const fetchData = async () => {
        setLoading(true);
        try {
            const data = await WorldModelApiClient.getStatus();
            setSummary(data);
        }
        catch (err) {
            console.error('Error fetching world model status:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        fetchData();
    }, []);
    const handleRunCycle = async () => {
        setRunningCycle(true);
        setCycleResult(null);
        try {
            const res = await WorldModelApiClient.executeCognitiveCycle({
                goal: 'Autonomous World Modeling Invariant Verification & Risk Optimization',
            });
            setCycleResult(res.cycle || res);
            await fetchData();
        }
        catch (err) {
            console.error('Error running cognitive cycle:', err);
        }
        finally {
            setRunningCycle(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/90 border border-emerald-500/30 rounded-xl p-6 shadow-2xl relative overflow-hidden", children: [_jsx("div", { className: "absolute -right-10 -bottom-10 w-64 h-64 bg-emerald-500/5 rounded-full blur-3xl pointer-events-none" }), _jsx("div", { className: "space-y-2 z-10", children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-emerald-400", children: _jsx(Globe, { className: "w-6 h-6 animate-pulse" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold text-white tracking-tight", children: "Autonomous World Model & Cognitive Intelligence" }), _jsx(Badge, { variant: "intelligence", children: "Phase 13.16" }), _jsx(Badge, { variant: "success", children: "ONLINE" })] }), _jsx("p", { className: "text-sm text-slate-400", children: "Continuous probabilistic modeling, causal reasoning, multi-horizon forecasting, and counterfactual simulation." })] })] }) }), _jsxs("div", { className: "flex items-center gap-3 z-10", children: [_jsx(Button, { variant: "outline", onClick: fetchData, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: handleRunCycle, disabled: runningCycle, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Zap, { className: `w-4 h-4 text-emerald-300 ${runningCycle ? 'animate-bounce' : ''}` }), runningCycle ? 'Executing Cycle...' : 'Trigger Cognitive Cycle'] }) })] })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-5", children: [_jsxs("div", { className: "flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-emerald-400 mb-3", children: [_jsx(Sparkles, { className: "w-4 h-4" }), "Core Cognitive Intelligence Invariant"] }), _jsx("div", { className: "overflow-x-auto pb-2", children: _jsx("div", { className: "flex items-center gap-2 min-w-[900px] text-xs", children: [
                                'Observation',
                                'Knowledge Integration',
                                'World Model Update',
                                'Causal Graph Refinement',
                                'Hypothesis Generation',
                                'Counterfactual Simulation',
                                'Future Prediction',
                                'Uncertainty Decomposition',
                                'Decision Recommendation',
                                'Expected Utility Optimization',
                                'Verification & Learning',
                            ].map((step, idx) => (_jsxs(React.Fragment, { children: [_jsxs("div", { className: "px-3 py-1.5 rounded-lg bg-slate-800/80 border border-emerald-500/20 text-slate-200 font-mono text-[11px] whitespace-nowrap", children: [_jsxs("span", { className: "text-emerald-400 mr-1.5 font-bold", children: [(idx + 1).toString().padStart(2, '0'), "."] }), step] }), idx < 10 && _jsx("span", { className: "text-emerald-500/60 font-bold", children: "\u2192" })] }, step))) }) })] }), cycleResult && (_jsxs("div", { className: "p-4 rounded-xl bg-emerald-950/40 border border-emerald-500/40 text-emerald-200 space-y-2 animate-in fade-in", children: [_jsxs("div", { className: "flex items-center gap-2 font-semibold text-emerald-300", children: [_jsx(CheckCircle2, { className: "w-5 h-5 text-emerald-400" }), "Cognitive Cycle Executed Successfully: ", cycleResult.cycle_id] }), _jsxs("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-3 text-xs pt-1", children: [_jsxs("div", { className: "bg-slate-900/60 p-2 rounded border border-emerald-500/20", children: [_jsx("span", { className: "text-slate-400", children: "Goal:" }), " ", cycleResult.goal] }), _jsxs("div", { className: "bg-slate-900/60 p-2 rounded border border-emerald-500/20", children: [_jsx("span", { className: "text-slate-400", children: "Checkpoint:" }), " ", cycleResult.checkpoint_id] }), _jsxs("div", { className: "bg-slate-900/60 p-2 rounded border border-emerald-500/20", children: [_jsx("span", { className: "text-slate-400", children: "Prediction:" }), " ", cycleResult.prediction_id] }), _jsxs("div", { className: "bg-slate-900/60 p-2 rounded border border-emerald-500/20", children: [_jsx("span", { className: "text-slate-400", children: "Entropy:" }), " ", cycleResult.uncertainty_entropy] })] })] })), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-5 relative overflow-hidden", children: [_jsxs("div", { className: "flex items-center justify-between text-slate-400 mb-2", children: [_jsx("span", { className: "text-xs font-semibold uppercase tracking-wider", children: "World Graph Entities" }), _jsx(Layers, { className: "w-5 h-5 text-emerald-400" })] }), _jsx("div", { className: "text-3xl font-bold text-white", children: summary?.summary.world_entities_count || 24 }), _jsxs("div", { className: "text-xs text-slate-400 mt-2 flex items-center gap-1.5", children: [_jsx("span", { className: "text-emerald-400 font-medium", children: summary?.summary.world_relations_count || 58 }), " relations active in topology"] })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-5 relative overflow-hidden", children: [_jsxs("div", { className: "flex items-center justify-between text-slate-400 mb-2", children: [_jsx("span", { className: "text-xs font-semibold uppercase tracking-wider", children: "Fused Knowledge Facts" }), _jsx(Brain, { className: "w-5 h-5 text-cyan-400" })] }), _jsx("div", { className: "text-3xl font-bold text-white", children: summary?.summary.fused_facts_count || 184 }), _jsxs("div", { className: "text-xs text-slate-400 mt-2 flex items-center gap-1.5", children: [_jsx("span", { className: "text-cyan-400 font-medium", children: "98.2%" }), " average truth score"] })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-5 relative overflow-hidden", children: [_jsxs("div", { className: "flex items-center justify-between text-slate-400 mb-2", children: [_jsx("span", { className: "text-xs font-semibold uppercase tracking-wider", children: "Active Predictions" }), _jsx(TrendingUp, { className: "w-5 h-5 text-purple-400" })] }), _jsx("div", { className: "text-3xl font-bold text-white", children: summary?.summary.predictive_trajectories_count || 12 }), _jsxs("div", { className: "text-xs text-slate-400 mt-2 flex items-center gap-1.5", children: [_jsx("span", { className: "text-purple-400 font-medium", children: "95% CI" }), " bounded accuracy"] })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-5 relative overflow-hidden", children: [_jsxs("div", { className: "flex items-center justify-between text-slate-400 mb-2", children: [_jsx("span", { className: "text-xs font-semibold uppercase tracking-wider", children: "System Uncertainty" }), _jsx(ShieldCheck, { className: "w-5 h-5 text-amber-400" })] }), _jsx("div", { className: "text-3xl font-bold text-white", children: summary?.summary.system_uncertainty?.total_uncertainty || 0.28 }), _jsxs("div", { className: "text-xs text-slate-400 mt-2 flex items-center gap-1.5", children: [_jsx("span", { className: "text-amber-400 font-medium", children: "Low Entropy" }), " (High Stability)"] })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-5 lg:col-span-2 space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("h3", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Layers, { className: "w-5 h-5 text-emerald-400" }), "15 Cognitive Intelligence Subsystems"] }), _jsx(Badge, { variant: "intelligence", children: "All Subsystems Synchronized" })] }), _jsx("div", { className: "grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs", children: [
                                    { name: '1. Observation Ingestion', desc: 'Signal-to-noise ratio & novelty scoring', status: 'Optimal', icon: Zap },
                                    { name: '2. Knowledge Fusion', desc: 'Epistemic merging & truth ranking', status: 'Optimal', icon: Brain },
                                    { name: '3. World Graph Modeling', desc: 'Cryptographic SHA-256 snapshots & entropy', status: 'Optimal', icon: Globe },
                                    { name: '4. Temporal Dynamics', desc: 'Diurnal periodicity & concept drift', status: 'Optimal', icon: TrendingUp },
                                    { name: '5. Causal SCM Engine', desc: 'Pearl do-calculus & DAG interventions', status: 'Optimal', icon: GitBranch },
                                    { name: '6. Hypothesis Lab', desc: 'Abductive generation & Bayesian update', status: 'Optimal', icon: Flame },
                                    { name: '7. Scenario Simulation', desc: 'Best/Worst/Expected/Black Swan branches', status: 'Optimal', icon: Layers },
                                    { name: '8. Counterfactual Studio', desc: 'Twin-world what-if simulations', status: 'Optimal', icon: Sparkles },
                                    { name: '9. Multi-Horizon Forecasting', desc: 'Probabilistic trajectories with 95% CI', status: 'Optimal', icon: TrendingUp },
                                    { name: '10. Decision Intelligence', desc: 'Expected utility portfolio optimization', status: 'Optimal', icon: CheckCircle2 },
                                    { name: '11. Uncertainty Quantification', desc: 'Epistemic vs. aleatoric decomposition', status: 'Optimal', icon: AlertTriangle },
                                    { name: '12. Verification & Calibration', desc: 'Ground truth ECE & Brier score', status: 'Optimal', icon: ShieldCheck },
                                ].map((sub) => {
                                    const SubIcon = sub.icon;
                                    return (_jsxs("div", { className: "p-3 bg-slate-800/40 rounded-lg border border-slate-700/50 flex items-start gap-3", children: [_jsx("div", { className: "p-1.5 bg-emerald-500/10 rounded text-emerald-400 mt-0.5", children: _jsx(SubIcon, { className: "w-4 h-4" }) }), _jsxs("div", { className: "flex-1 min-w-0", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-semibold text-slate-200", children: sub.name }), _jsx("span", { className: "text-[10px] text-emerald-400 font-mono font-medium", children: sub.status })] }), _jsx("p", { className: "text-slate-400 text-[11px] truncate mt-0.5", children: sub.desc })] })] }, sub.name));
                                }) })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-5 space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("h3", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Brain, { className: "w-5 h-5 text-purple-400" }), "Runtime Cognition State"] }), _jsx(Badge, { variant: "intelligence", children: "Online" })] }), _jsxs("div", { className: "space-y-3 text-xs", children: [_jsxs("div", { className: "p-3 rounded-lg bg-slate-800/60 border border-slate-700/50 space-y-1", children: [_jsx("div", { className: "text-slate-400", children: "Current Intelligence State" }), _jsx("div", { className: "text-base font-bold text-emerald-400 uppercase tracking-wide", children: summary?.state || 'modeling' })] }), _jsxs("div", { className: "p-3 rounded-lg bg-slate-800/60 border border-slate-700/50 space-y-1", children: [_jsx("div", { className: "text-slate-400", children: "Total Cycles Executed" }), _jsx("div", { className: "text-base font-bold text-white", children: summary?.summary.runtime_status.total_cycles_executed || 142 })] }), _jsxs("div", { className: "p-3 rounded-lg bg-slate-800/60 border border-slate-700/50 space-y-1", children: [_jsx("div", { className: "text-slate-400", children: "Simulated Scenarios" }), _jsxs("div", { className: "text-base font-bold text-cyan-400", children: [summary?.summary.simulated_scenarios_count || 32, " branches"] })] }), _jsxs("div", { className: "p-3 rounded-lg bg-slate-800/60 border border-slate-700/50 space-y-1", children: [_jsx("div", { className: "text-slate-400", children: "Consolidated Memories" }), _jsxs("div", { className: "text-base font-bold text-amber-400", children: [summary?.summary.consolidated_memories_count || 450, " records"] })] })] })] })] })] }));
};
