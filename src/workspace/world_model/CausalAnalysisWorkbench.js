import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 5: Causal Analysis Workbench
 */
import { useEffect, useState } from 'react';
import { GitBranch, RefreshCw, Zap, CheckCircle2, Sliders, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
export const CausalAnalysisWorkbench = () => {
    const [graph, setGraph] = useState(null);
    const [loading, setLoading] = useState(true);
    const [targetNode, setTargetNode] = useState('k8s_replicas_count');
    const [interventionVal, setInterventionVal] = useState('6');
    const [simulating, setSimulating] = useState(false);
    const [interventionResult, setInterventionResult] = useState(null);
    const fetchCausal = async () => {
        setLoading(true);
        try {
            const res = await WorldModelApiClient.getCausalGraph();
            setGraph(res.graph || null);
        }
        catch (err) {
            console.error('Error fetching causal graph:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        fetchCausal();
    }, []);
    const handleSimulateIntervention = async (e) => {
        e.preventDefault();
        setSimulating(true);
        try {
            const res = await WorldModelApiClient.executeCausalIntervention({
                target_node: targetNode,
                interventions: { [targetNode]: parseFloat(interventionVal) || interventionVal },
            });
            setInterventionResult(res.causal_effect || res.intervention || res);
        }
        catch (err) {
            console.error('Error executing causal intervention:', err);
        }
        finally {
            setSimulating(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 border border-amber-500/30 rounded-xl p-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-amber-500/10 border border-amber-500/30 rounded-lg text-amber-400", children: _jsx(GitBranch, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold text-white tracking-tight", children: "Causal Analysis Workbench" }), _jsx(Badge, { variant: "intelligence", children: "Pearl's do-calculus" })] }), _jsx("p", { className: "text-sm text-slate-400", children: "Structural Causal Models (SCM), DAG edge discovery, confounder adjustments, and synthetic interventional simulations." })] })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsx(Button, { variant: "outline", onClick: fetchCausal, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-5 lg:col-span-2 space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("h3", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(GitBranch, { className: "w-5 h-5 text-amber-400" }), "Active Structural Causal DAG & Path Coefficients"] }), _jsxs(Badge, { variant: "intelligence", children: [graph?.edges?.length || 2, " Causal Paths"] })] }), _jsx("div", { className: "space-y-3", children: (graph?.edges || []).map((edge, idx) => (_jsxs("div", { className: "p-4 bg-slate-950/80 rounded-lg border border-slate-800 space-y-2 hover:border-amber-500/40 transition-all", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("span", { className: "text-amber-400 font-mono font-semibold text-sm", children: edge.source_id }), _jsx("span", { className: "text-slate-500 font-bold", children: "\u2015(do)\u2192" }), _jsx("span", { className: "text-cyan-400 font-mono font-semibold text-sm", children: edge.target_id })] }), _jsxs(Badge, { variant: "warning", children: ["Weight: ", edge.weight] })] }), _jsxs("div", { className: "flex items-center justify-between text-xs text-slate-400 pt-1", children: [_jsxs("div", { children: ["Strength: ", _jsx("strong", { className: "text-slate-200 capitalize", children: edge.strength })] }), _jsxs("div", { children: ["Mechanism: ", _jsx("span", { className: "text-slate-300 font-mono text-[11px]", children: edge.mechanism || 'Direct path' })] })] })] }, idx))) })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-5 space-y-4", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("h3", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Sliders, { className: "w-5 h-5 text-cyan-400" }), "Interventional do(X) Simulator"] }) }), _jsxs("form", { onSubmit: handleSimulateIntervention, className: "space-y-4 text-xs", children: [_jsxs("div", { children: [_jsx("label", { className: "block text-slate-300 font-semibold mb-1", children: "Target Action Variable" }), _jsx("input", { type: "text", value: targetNode, onChange: (e) => setTargetNode(e.target.value), className: "w-full bg-slate-800 border border-slate-700 rounded p-2 text-white font-mono text-xs focus:outline-none focus:border-amber-500" })] }), _jsxs("div", { children: [_jsx("label", { className: "block text-slate-300 font-semibold mb-1", children: "Forced Intervention Value" }), _jsx("input", { type: "text", value: interventionVal, onChange: (e) => setInterventionVal(e.target.value), className: "w-full bg-slate-800 border border-slate-700 rounded p-2 text-white font-mono text-xs focus:outline-none focus:border-amber-500" })] }), _jsx(Button, { variant: "intelligence", type: "submit", disabled: simulating, className: "w-full", children: _jsxs("span", { className: "flex items-center justify-center gap-2", children: [_jsx(Zap, { className: "w-4 h-4" }), simulating ? 'Computing do(X)...' : 'Simulate Intervention'] }) })] }), interventionResult && (_jsxs("div", { className: "p-3 bg-amber-950/40 border border-amber-500/40 rounded-lg space-y-2 text-xs text-amber-200 animate-in fade-in", children: [_jsxs("div", { className: "font-semibold text-amber-300 flex items-center gap-1.5", children: [_jsx(CheckCircle2, { className: "w-4 h-4 text-amber-400" }), "Causal Effect Estimated"] }), _jsx("pre", { className: "p-2 bg-slate-950/80 rounded font-mono text-[11px] text-slate-200 whitespace-pre-wrap overflow-x-auto", children: JSON.stringify(interventionResult, null, 2) })] }))] })] })] }));
};
