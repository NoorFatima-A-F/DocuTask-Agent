import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Layers, ShieldCheck, Play, RefreshCw, Flame, CheckCircle2, } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
export const EvolutionSimulationStudio = () => {
    const [latestReport, setLatestReport] = useState(null);
    const [loading, setLoading] = useState(true);
    const [simulating, setSimulating] = useState(false);
    // Simulation controls
    const [mode, setMode] = useState('SHADOW_REPLAY');
    const [traceCount, setTraceCount] = useState(2000);
    useEffect(() => {
        loadSimulations();
    }, []);
    const loadSimulations = async () => {
        setLoading(true);
        try {
            const data = await EvolutionPlatformApiClient.listSimulations();
            if (data.length > 0) {
                const last = data[data.length - 1];
                if (last)
                    setLatestReport(last);
            }
        }
        catch (err) {
            console.error('Failed to load simulations:', err);
        }
        finally {
            setLoading(false);
        }
    };
    const handleRunSimulation = async () => {
        setSimulating(true);
        try {
            const res = await EvolutionPlatformApiClient.runSimulation({
                simulation_mode: mode,
                traces_count: traceCount,
            });
            setLatestReport(res);
        }
        catch (err) {
            console.error('Simulation error:', err);
        }
        finally {
            setSimulating(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-cyan-500/10 border border-cyan-500/20 rounded-xl", children: _jsx(Layers, { className: "w-6 h-6 text-cyan-400" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-xl font-bold text-slate-100", children: "Evolution Simulation & Digital Twin Sandbox" }), _jsx(Badge, { variant: "info", size: "sm", children: "Shadow Replay & Chaos" })] }), _jsx("p", { className: "text-sm text-slate-400 mt-0.5", children: "Simulates candidate architecture modifications against thousands of production traces and chaos injections before rollout." })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: loadSimulations, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: handleRunSimulation, disabled: simulating, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Play, { className: `w-4 h-4 ${simulating ? 'animate-spin' : ''}` }), simulating ? 'Simulating Replay...' : 'Run Digital Twin Simulation'] }) })] })] }), _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4", children: [_jsx("h2", { className: "text-sm font-semibold text-slate-200", children: "Simulation Configuration" }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-5", children: [_jsxs("div", { children: [_jsx("label", { className: "text-xs font-medium text-slate-400 block mb-1", children: "Simulation Mode" }), _jsxs("select", { value: mode, onChange: (e) => setMode(e.target.value), className: "w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-cyan-500", children: [_jsx("option", { value: "SHADOW_REPLAY", children: "Shadow Replay (Historical Real Traces)" }), _jsx("option", { value: "DIGITAL_TWIN", children: "Digital Twin Predictive World Model" }), _jsx("option", { value: "CHAOS_FAULT_INJECTION", children: "Chaos Fault Injection (Worker Crashes & Lag)" }), _jsx("option", { value: "MONTE_CARLO", children: "Monte Carlo Extreme Stress Load" })] })] }), _jsxs("div", { children: [_jsxs("div", { className: "flex justify-between text-xs font-medium text-slate-400 mb-1", children: [_jsx("span", { children: "Historical Request Traces" }), _jsxs("span", { className: "font-mono text-cyan-400", children: [traceCount, " Traces"] })] }), _jsx("input", { type: "range", min: "500", max: "10000", step: "500", value: traceCount, onChange: (e) => setTraceCount(parseInt(e.target.value)), className: "w-full accent-cyan-400 cursor-pointer mt-2" })] })] })] }), latestReport && (_jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-5", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-3 pb-4 border-b border-slate-800", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsxs("h2", { className: "text-base font-bold text-slate-100", children: ["Simulation Report: ", latestReport.simulation_id] }), _jsx(Badge, { variant: latestReport.verified_safe ? 'success' : 'warning', size: "sm", children: latestReport.verified_safe ? 'Verified Safe' : 'Safety Warning' })] }), _jsxs("span", { className: "text-xs text-slate-400 font-mono mt-0.5 block", children: ["Mode: ", latestReport.simulation_mode, " \u2022 Traces: ", latestReport.traces_replayed] })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs text-slate-400", children: "Confidence:" }), _jsxs("span", { className: "text-xl font-bold text-cyan-400 font-mono", children: [(latestReport.stability_confidence * 100).toFixed(1), "%"] })] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4 font-mono", children: [_jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-4 space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-slate-400", children: [_jsxs("span", { className: "flex items-center gap-1.5", children: [_jsx(CheckCircle2, { className: "w-4 h-4 text-emerald-400" }), "Success Rate"] }), _jsxs("span", { className: "text-emerald-400 font-bold", children: [(latestReport.success_rate * 100).toFixed(2), "%"] })] }), _jsx("div", { className: "w-full bg-slate-800 h-1.5 rounded-full overflow-hidden", children: _jsx("div", { className: "bg-emerald-400 h-full rounded-full", style: { width: `${latestReport.success_rate * 100}%` } }) })] }), _jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-4 space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-slate-400", children: [_jsxs("span", { className: "flex items-center gap-1.5", children: [_jsx(Flame, { className: "w-4 h-4 text-amber-400" }), "Chaos Resilience"] }), _jsxs("span", { className: "text-amber-400 font-bold", children: [(latestReport.chaos_resilience_score * 100).toFixed(1), "%"] })] }), _jsx("div", { className: "w-full bg-slate-800 h-1.5 rounded-full overflow-hidden", children: _jsx("div", { className: "bg-amber-400 h-full rounded-full", style: { width: `${latestReport.chaos_resilience_score * 100}%` } }) })] }), _jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-4 space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-slate-400", children: [_jsxs("span", { className: "flex items-center gap-1.5", children: [_jsx(ShieldCheck, { className: "w-4 h-4 text-purple-400" }), "Invariant Violations"] }), _jsxs("span", { className: "text-emerald-400 font-bold", children: [latestReport.safety_invariant_violations, " Violations"] })] }), _jsx("div", { className: "text-[11px] text-slate-500 pt-0.5", children: "Zero security guardrail boundary breaches" })] })] }), _jsxs("div", { className: "p-3 bg-slate-950/80 border border-slate-800/80 rounded-lg text-xs font-mono text-slate-400", children: [_jsx("span", { className: "text-slate-300 font-bold block mb-1", children: "Execution Notes:" }), latestReport.execution_notes] })] }))] }));
};
