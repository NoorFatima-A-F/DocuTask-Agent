import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 8: Counterfactual Studio
 */
import { useEffect, useState } from 'react';
import { Sparkles, RefreshCw, GitCompare, Sliders, Zap, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
export const CounterfactualStudio = () => {
    const [simulations, setSimulations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [queryTarget, setQueryTarget] = useState('P99 Document Extraction Latency');
    const [intervention, setIntervention] = useState('autoscaling_threshold_cpu = 0.6');
    const [simulating, setSimulating] = useState(false);
    const fetchSimulations = async () => {
        setLoading(true);
        try {
            const res = await WorldModelApiClient.getCounterfactuals();
            setSimulations(res.counterfactuals || []);
        }
        catch (err) {
            console.error('Error fetching counterfactuals:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        fetchSimulations();
    }, []);
    const handleSimulate = async (e) => {
        e.preventDefault();
        setSimulating(true);
        try {
            await WorldModelApiClient.simulateCounterfactual({
                base_snapshot_id: 'snap-01',
                interventions: { threshold: 0.6 },
                query_target: queryTarget,
                factual_outcome: '2.4 seconds',
            });
            await fetchSimulations();
        }
        catch (err) {
            console.error('Error running counterfactual:', err);
        }
        finally {
            setSimulating(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 border border-teal-500/30 rounded-xl p-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-teal-500/10 border border-teal-500/30 rounded-lg text-teal-400", children: _jsx(GitCompare, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold text-white tracking-tight", children: "Counterfactual Studio" }), _jsx(Badge, { variant: "intelligence", children: "Twin-World Simulation" })] }), _jsx("p", { className: "text-sm text-slate-400", children: "Evaluates retrospective and prospective \"what-if\" branches, computing outcome divergence and causal attribution." })] })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsx(Button, { variant: "outline", onClick: fetchSimulations, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "lg:col-span-2 space-y-4", children: [_jsxs("h3", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-5 h-5 text-teal-400" }), "Simulated Twin-World Counterfactuals"] }), _jsx("div", { className: "space-y-4", children: simulations.map((sim) => (_jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-5 space-y-4 hover:border-teal-500/40 transition-all", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx("span", { className: "text-xs font-mono text-teal-400 bg-teal-950/60 px-2 py-0.5 rounded border border-teal-500/30", children: sim.simulation_id }), _jsx("h4", { className: "text-base font-bold text-white mt-1.5", children: sim.query_target })] }), _jsxs(Badge, { variant: "success", children: ["Divergence: ", sim.divergence_score] })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs", children: [_jsxs("div", { className: "p-3 bg-slate-950/80 rounded border border-slate-800 space-y-1", children: [_jsx("span", { className: "text-slate-400 font-semibold uppercase text-[10px]", children: "Factual Outcome (Observed)" }), _jsx("div", { className: "text-base font-bold text-slate-200", children: String(sim.factual_outcome) })] }), _jsxs("div", { className: "p-3 bg-teal-950/30 rounded border border-teal-500/30 space-y-1", children: [_jsx("span", { className: "text-teal-400 font-semibold uppercase text-[10px]", children: "Counterfactual Outcome (Twin World)" }), _jsx("div", { className: "text-base font-bold text-teal-300", children: String(sim.counterfactual_outcome) })] })] }), _jsxs("div", { className: "p-3 bg-slate-950/80 rounded border border-slate-800 text-xs", children: [_jsx("span", { className: "text-slate-400 block mb-1 font-semibold", children: "Causal Attribution:" }), _jsx("span", { className: "text-emerald-300", children: sim.causal_attribution })] })] }, sim.simulation_id))) })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-5 space-y-4", children: [_jsxs("h3", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Sliders, { className: "w-5 h-5 text-teal-400" }), "Query Counterfactual"] }), _jsxs("form", { onSubmit: handleSimulate, className: "space-y-4 text-xs", children: [_jsxs("div", { children: [_jsx("label", { className: "block text-slate-300 font-semibold mb-1", children: "Query Metric / Target" }), _jsx("input", { type: "text", required: true, value: queryTarget, onChange: (e) => setQueryTarget(e.target.value), className: "w-full bg-slate-800 border border-slate-700 rounded p-2 text-white text-xs" })] }), _jsxs("div", { children: [_jsx("label", { className: "block text-slate-300 font-semibold mb-1", children: "Intervention Hypothesis" }), _jsx("input", { type: "text", required: true, value: intervention, onChange: (e) => setIntervention(e.target.value), className: "w-full bg-slate-800 border border-slate-700 rounded p-2 text-white text-xs font-mono" })] }), _jsx(Button, { variant: "intelligence", type: "submit", disabled: simulating, className: "w-full", children: _jsxs("span", { className: "flex items-center justify-center gap-2", children: [_jsx(Zap, { className: "w-4 h-4" }), simulating ? 'Simulating Twin World...' : 'Simulate Counterfactual'] }) })] })] })] })] }));
};
