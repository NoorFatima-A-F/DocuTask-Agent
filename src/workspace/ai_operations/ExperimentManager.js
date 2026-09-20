import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { TestTube2, Play, Clock, TrendingUp, RefreshCw, Award, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';
export const ExperimentManager = () => {
    const [experiments, setExperiments] = useState([]);
    const [selectedExp, setSelectedExp] = useState(null);
    const [loading, setLoading] = useState(true);
    const [runningNew, setRunningNew] = useState(false);
    const loadExperiments = async () => {
        try {
            setLoading(true);
            const data = await AIOperationsApiClient.getExperiments();
            setExperiments(data);
            if (data.length > 0 && !selectedExp) {
                setSelectedExp(data[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load experiments:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadExperiments();
    }, []);
    const handleLaunchExperiment = async () => {
        try {
            setRunningNew(true);
            const res = await AIOperationsApiClient.runExperiment({
                name: 'Manual Canary Test Run',
                agent_id: 'agent_chief_architect',
                control_version: 'v1.0.0',
                candidate_version: 'v1.1.0',
                sample_size: 100,
            });
            setSelectedExp(res);
            await loadExperiments();
        }
        catch (err) {
            console.error('Failed to run experiment:', err);
        }
        finally {
            setRunningNew(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-cyan-500/10 rounded-xl border border-cyan-500/20", children: _jsx(TestTube2, { className: "w-6 h-6 text-cyan-400" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-xl font-bold text-white", children: "A/B Canary Experiment Manager" }), _jsx("p", { className: "text-xs text-slate-400", children: "Statistical hypothesis testing (Welch's t-test, Cohen's d) for prompt & model deployments" })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: loadExperiments, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: handleLaunchExperiment, disabled: runningNew, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Play, { className: `w-4 h-4 ${runningNew ? 'animate-spin' : ''}` }), runningNew ? 'Running Canary...' : 'Launch Canary A/B Run'] }) })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-12 gap-6", children: [_jsxs("div", { className: "lg:col-span-4 space-y-3", children: [_jsx("h2", { className: "text-xs font-semibold text-slate-400 uppercase tracking-wider px-1", children: "Canary Experiment Runs" }), _jsx("div", { className: "space-y-2 max-h-[600px] overflow-y-auto pr-1", children: experiments.map((exp) => (_jsxs(Card, { className: `p-3.5 cursor-pointer transition-all border ${selectedExp?.experiment_id === exp.experiment_id
                                        ? 'bg-cyan-950/30 border-cyan-500/50 shadow-md shadow-cyan-950/20'
                                        : 'bg-slate-900/40 border-slate-800/80 hover:bg-slate-800/40'}`, onClick: () => setSelectedExp(exp), children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-semibold text-white text-xs", children: exp.agent_id }), _jsx(Badge, { variant: exp.statistically_significant ? 'success' : 'outline', children: exp.statistically_significant ? 'Stat Sig (p<0.05)' : 'Inconclusive' })] }), _jsx("h3", { className: "font-medium text-slate-200 text-xs mt-1 line-clamp-1", children: exp.name }), _jsxs("div", { className: "flex items-center justify-between mt-2.5 text-[11px] text-slate-400 border-t border-slate-800/60 pt-2", children: [_jsxs("span", { children: [(exp.control_success_rate * 100).toFixed(0), "% \u2192 ", (exp.candidate_success_rate * 100).toFixed(0), "%"] }), _jsxs("span", { children: ["n=", exp.sample_size] })] })] }, exp.experiment_id))) })] }), _jsx("div", { className: "lg:col-span-8 space-y-4", children: selectedExp ? (_jsxs(Card, { className: "p-6 bg-slate-900/50 border-slate-800 space-y-5", children: [_jsxs("div", { className: "flex items-start justify-between border-b border-slate-800 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "intelligence", children: selectedExp.agent_id }), _jsx("h2", { className: "text-lg font-bold text-white", children: selectedExp.name })] }), _jsxs("p", { className: "text-xs text-slate-400 font-mono mt-0.5", children: ["Experiment ID: ", selectedExp.experiment_id, " \u2022 Status: ", selectedExp.status] })] }), _jsx(Badge, { variant: selectedExp.statistically_significant ? 'success' : 'warning', children: selectedExp.statistically_significant ? 'Statistically Validated' : 'Not Significant' })] }), _jsxs("div", { className: "grid grid-cols-3 gap-3", children: [_jsxs("div", { className: "p-3 bg-slate-950/60 rounded-xl border border-slate-800/60", children: [_jsxs("span", { className: "text-xs text-slate-400 flex items-center gap-1", children: [_jsx(Award, { className: "w-3.5 h-3.5 text-cyan-400" }), " p-Value (Welch's t)"] }), _jsx("p", { className: "text-lg font-bold text-cyan-300 mt-1", children: selectedExp.p_value })] }), _jsxs("div", { className: "p-3 bg-slate-950/60 rounded-xl border border-slate-800/60", children: [_jsxs("span", { className: "text-xs text-slate-400 flex items-center gap-1", children: [_jsx(TrendingUp, { className: "w-3.5 h-3.5 text-indigo-400" }), " Cohen's d Effect Size"] }), _jsx("p", { className: "text-lg font-bold text-indigo-300 mt-1", children: selectedExp.effect_size_cohen_d })] }), _jsxs("div", { className: "p-3 bg-slate-950/60 rounded-xl border border-slate-800/60", children: [_jsxs("span", { className: "text-xs text-slate-400 flex items-center gap-1", children: [_jsx(Clock, { className: "w-3.5 h-3.5 text-amber-400" }), " Sample Trials"] }), _jsx("p", { className: "text-lg font-bold text-white mt-1", children: selectedExp.sample_size })] })] }), _jsxs("div", { className: "grid grid-cols-2 gap-4", children: [_jsxs("div", { className: "p-4 bg-slate-950/60 rounded-xl border border-slate-800/80", children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsxs("span", { className: "text-xs font-semibold text-slate-400", children: ["Control (", selectedExp.control_version, ")"] }), _jsx(Badge, { variant: "outline", children: "Baseline" })] }), _jsxs("div", { className: "text-2xl font-bold text-white", children: [(selectedExp.control_success_rate * 100).toFixed(1), "%"] }), _jsxs("p", { className: "text-xs text-slate-400 mt-1", children: ["Avg Latency: ", selectedExp.control_avg_latency_ms, " ms"] }), _jsxs("p", { className: "text-xs text-slate-500", children: ["Avg Cost: $", selectedExp.control_avg_cost_usd] })] }), _jsxs("div", { className: "p-4 bg-slate-950/60 rounded-xl border border-cyan-500/40", children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsxs("span", { className: "text-xs font-semibold text-cyan-300", children: ["Candidate (", selectedExp.candidate_version, ")"] }), _jsx(Badge, { variant: "success", children: "Candidate" })] }), _jsxs("div", { className: "text-2xl font-bold text-cyan-400", children: [(selectedExp.candidate_success_rate * 100).toFixed(1), "%"] }), _jsxs("p", { className: "text-xs text-slate-300 mt-1", children: ["Avg Latency: ", selectedExp.candidate_avg_latency_ms, " ms"] }), _jsxs("p", { className: "text-xs text-slate-400", children: ["Avg Cost: $", selectedExp.candidate_avg_cost_usd] })] })] })] })) : (_jsxs(Card, { className: "p-8 text-center text-slate-400 bg-slate-900/40 border-slate-800", children: [_jsx(TestTube2, { className: "w-8 h-8 text-slate-600 mx-auto mb-2" }), _jsx("p", { children: "Select a canary experiment run to inspect statistical significance metrics." })] })) })] })] }));
};
