import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Sliders, RefreshCw, Sparkles, Calculator, } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
export const ArchitectureOptimizerStudio = () => {
    const [candidates, setCandidates] = useState([]);
    const [loading, setLoading] = useState(true);
    const [generating, setGenerating] = useState(false);
    // Optimizer tuning parameters
    const [targetSubsystem, setTargetSubsystem] = useState('llm_cognition');
    const [objective, setObjective] = useState('TOKEN_EFFICIENCY');
    const [riskTolerance, setRiskTolerance] = useState(0.15);
    useEffect(() => {
        loadCandidates();
    }, []);
    const loadCandidates = async () => {
        setLoading(true);
        try {
            const data = await EvolutionPlatformApiClient.listOptimizationCandidates();
            setCandidates(data);
        }
        catch (err) {
            console.error('Failed to load optimization candidates:', err);
        }
        finally {
            setLoading(false);
        }
    };
    const handleGenerate = async () => {
        setGenerating(true);
        try {
            const newCand = await EvolutionPlatformApiClient.generateCandidate({
                target_subsystem: targetSubsystem,
                objective: objective,
                custom_risk_tolerance: riskTolerance,
            });
            setCandidates((prev) => [newCand, ...prev]);
        }
        catch (err) {
            console.error('Candidate generation failed:', err);
        }
        finally {
            setGenerating(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-amber-500/10 border border-amber-500/20 rounded-xl", children: _jsx(Sliders, { className: "w-6 h-6 text-amber-400" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-xl font-bold text-slate-100", children: "Multi-Objective Pareto Optimizer Studio" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Bayesian & Genetic Search" })] }), _jsx("p", { className: "text-sm text-slate-400 mt-0.5", children: "Simultaneously optimizes latency, token economy, and accuracy with mathematical proofs and Pareto ranking." })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: loadCandidates, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: handleGenerate, disabled: generating, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Sparkles, { className: `w-4 h-4 ${generating ? 'animate-spin' : ''}` }), generating ? 'Optimizing Frontier...' : 'Generate Pareto Candidate'] }) })] })] }), _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4", children: [_jsx("h2", { className: "text-sm font-semibold text-slate-200", children: "Hyperparameter & Subsystem Target Configuration" }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-5", children: [_jsxs("div", { children: [_jsx("label", { className: "text-xs font-medium text-slate-400 block mb-1", children: "Target Subsystem" }), _jsxs("select", { value: targetSubsystem, onChange: (e) => setTargetSubsystem(e.target.value), className: "w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-amber-500", children: [_jsx("option", { value: "llm_cognition", children: "LLM Cognition Layer" }), _jsx("option", { value: "memory_layer", children: "Episodic Vector Memory" }), _jsx("option", { value: "swarm_orchestrator", children: "Swarm Coordination Ring" }), _jsx("option", { value: "governance_sentinel", children: "Governance & Sentinel" })] })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs font-medium text-slate-400 block mb-1", children: "Primary Optimization Objective" }), _jsxs("select", { value: objective, onChange: (e) => setObjective(e.target.value), className: "w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-amber-500", children: [_jsx("option", { value: "TOKEN_EFFICIENCY", children: "Token Efficiency (Min Context Waste)" }), _jsx("option", { value: "LATENCY_REDUCTION", children: "Latency Reduction (Lock-Free SIMD)" }), _jsx("option", { value: "ACCURACY_MAXIMIZATION", children: "Accuracy Maximization" }), _jsx("option", { value: "COST_MINIMIZATION", children: "Cost Minimization" }), _jsx("option", { value: "SAFETY_COMPLIANCE", children: "Safety & Guardrail Compliance" })] })] }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between text-xs font-medium text-slate-400 mb-1", children: [_jsx("span", { children: "Risk Tolerance Threshold" }), _jsxs("span", { className: "font-mono text-amber-400", children: [(riskTolerance * 100).toFixed(0), "%"] })] }), _jsx("input", { type: "range", min: "0.05", max: "0.40", step: "0.01", value: riskTolerance, onChange: (e) => setRiskTolerance(parseFloat(e.target.value)), className: "w-full accent-amber-400 cursor-pointer mt-2" }), _jsxs("div", { className: "flex justify-between text-[10px] text-slate-500 font-mono mt-1", children: [_jsx("span", { children: "Strict Zero-Risk (5%)" }), _jsx("span", { children: "Aggressive (40%)" })] })] })] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5", children: candidates.map((c) => (_jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4 hover:border-slate-700 transition-all flex flex-col justify-between", children: [_jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-mono text-xs font-bold text-slate-300", children: c.candidate_id }), _jsxs(Badge, { variant: c.pareto_rank === 1 ? 'intelligence' : 'outline', size: "sm", children: ["Pareto Rank #", c.pareto_rank] })] }), _jsx("div", { className: "text-sm font-semibold text-slate-100", children: c.target_subsystem }), _jsxs("div", { className: "text-xs text-amber-400 font-mono", children: ["Objective: ", c.objective] })] }), _jsxs("div", { className: "p-3 bg-slate-950/80 border border-slate-800/80 rounded-lg text-xs text-slate-400 font-mono space-y-1", children: [_jsxs("div", { className: "flex items-center gap-1.5 text-slate-300 font-bold", children: [_jsx(Calculator, { className: "w-3.5 h-3.5 text-amber-400" }), _jsx("span", { children: "Mathematical Proof" })] }), _jsx("p", { className: "line-clamp-3 text-[11px] text-slate-400", children: c.mathematical_proof })] }), _jsxs("div", { className: "pt-3 border-t border-slate-800/80 grid grid-cols-3 gap-2 text-center text-xs font-mono", children: [_jsxs("div", { className: "bg-slate-950/60 p-2 rounded", children: [_jsx("div", { className: "text-slate-500 text-[10px]", children: "GAIN" }), _jsxs("div", { className: "text-emerald-400 font-semibold", children: ["+", c.expected_gain_pct.toFixed(1), "%"] })] }), _jsxs("div", { className: "bg-slate-950/60 p-2 rounded", children: [_jsx("div", { className: "text-slate-500 text-[10px]", children: "FITNESS" }), _jsxs("div", { className: "text-indigo-300 font-semibold", children: [(c.fitness_score * 100).toFixed(1), "%"] })] }), _jsxs("div", { className: "bg-slate-950/60 p-2 rounded", children: [_jsx("div", { className: "text-slate-500 text-[10px]", children: "RISK" }), _jsxs("div", { className: "text-amber-300 font-semibold", children: [(c.estimated_risk * 100).toFixed(1), "%"] })] })] })] }, c.candidate_id))) })] }));
};
