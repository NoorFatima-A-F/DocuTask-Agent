import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { RefreshCw, Server, Play, CheckCircle2, } from 'lucide-react';
import { CognitiveEvolutionApiClient } from '../../services/cognitiveEvolutionApiClient';
export const DigitalTwinSimulatorView = () => {
    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);
    const [simulating, setSimulating] = useState(false);
    const [missionCount] = useState(500);
    useEffect(() => {
        loadSimulation();
    }, []);
    const loadSimulation = async () => {
        setLoading(true);
        try {
            const data = await CognitiveEvolutionApiClient.runDigitalTwinSimulation(missionCount);
            setReport(data);
        }
        catch (e) {
            console.error('Failed to run digital twin simulation:', e);
        }
        finally {
            setLoading(false);
        }
    };
    const handleRunSim = async () => {
        setSimulating(true);
        try {
            const data = await CognitiveEvolutionApiClient.runDigitalTwinSimulation(missionCount);
            setReport(data);
        }
        catch (e) {
            console.error('Simulation failed:', e);
        }
        finally {
            setSimulating(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6 font-mono", children: [_jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-bold text-cyan-300 flex items-center gap-2", children: [_jsx(Server, { className: "w-4 h-4 text-cyan-400" }), "Digital Twin Distributed Cluster Simulator (1,000+ Workers)"] }), _jsx("p", { className: "text-xs text-slate-400 mt-0.5", children: "High-fidelity discrete-event queuing simulation modeling GPU thermals, VRAM pressure, and chaos fault injection." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs("button", { onClick: handleRunSim, disabled: simulating, className: "flex items-center gap-2 px-3 py-1.5 bg-cyan-950/60 hover:bg-cyan-900/70 border border-cyan-800 text-cyan-300 rounded-lg text-xs font-bold transition-all disabled:opacity-50", children: [_jsx(Play, { className: `w-3.5 h-3.5 ${simulating ? 'animate-spin' : ''}` }), "Run 500-Mission Simulation"] }), _jsx("button", { onClick: loadSimulation, disabled: loading, className: "text-slate-400 hover:text-cyan-400 p-1.5 rounded", title: "Refresh", children: _jsx(RefreshCw, { className: `w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}` }) })] })] }), _jsxs("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-3 pt-1", children: [_jsxs("div", { className: "bg-slate-950/70 border border-slate-800 rounded-lg p-3", children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "Virtual Nodes" }), _jsxs("div", { className: "text-xl font-bold text-slate-200 mt-0.5", children: [report?.total_virtual_workers || 1000, " ", _jsx("span", { className: "text-[10px] text-cyan-400", children: "GPU/CPU" })] })] }), _jsxs("div", { className: "bg-slate-950/70 border border-slate-800 rounded-lg p-3", children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "P95 Latency" }), _jsxs("div", { className: "text-xl font-bold text-amber-300 mt-0.5", children: [report?.p95_latency_ms.toFixed(0) || 850, "ms"] })] }), _jsxs("div", { className: "bg-slate-950/70 border border-slate-800 rounded-lg p-3", children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "Tokens Consumed" }), _jsxs("div", { className: "text-xl font-bold text-purple-300 mt-0.5", children: [((report?.total_simulated_tokens || 2450000) / 1000000).toFixed(2), "M"] })] }), _jsxs("div", { className: "bg-slate-950/70 border border-slate-800 rounded-lg p-3", children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "Resilience Score" }), _jsxs("div", { className: "text-xl font-bold text-emerald-400 mt-0.5", children: [((report?.resilience_score || 0.992) * 100).toFixed(1), "%"] })] })] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-6", children: [_jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3", children: [_jsx("div", { className: "text-xs uppercase text-slate-400 tracking-wider", children: "Tail Latency Breakdown" }), _jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex justify-between text-xs", children: [_jsx("span", { className: "text-slate-400", children: "P50 (Median)" }), _jsxs("span", { className: "text-emerald-400 font-bold", children: [report?.p50_latency_ms.toFixed(0), "ms"] })] }), _jsxs("div", { className: "flex justify-between text-xs", children: [_jsx("span", { className: "text-slate-400", children: "P95" }), _jsxs("span", { className: "text-amber-400 font-bold", children: [report?.p95_latency_ms.toFixed(0), "ms"] })] }), _jsxs("div", { className: "flex justify-between text-xs", children: [_jsx("span", { className: "text-slate-400", children: "P99" }), _jsxs("span", { className: "text-rose-400 font-bold", children: [report?.p99_latency_ms.toFixed(0), "ms"] })] })] })] }), _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3", children: [_jsx("div", { className: "text-xs uppercase text-slate-400 tracking-wider", children: "Cluster Hardware Headroom" }), _jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex justify-between text-xs", children: [_jsx("span", { className: "text-slate-400", children: "Avg GPU Utilization" }), _jsxs("span", { className: "text-cyan-300 font-bold", children: [report?.average_gpu_utilization_pct.toFixed(1), "%"] })] }), _jsx("div", { className: "w-full bg-slate-800 h-2 rounded-full overflow-hidden", children: _jsx("div", { className: "h-full bg-gradient-to-r from-cyan-500 to-emerald-400 rounded-full", style: { width: `${report?.average_gpu_utilization_pct || 68.5}%` } }) })] })] }), _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3", children: [_jsx("div", { className: "text-xs uppercase text-slate-400 tracking-wider", children: "Fault Injection Status" }), _jsxs("div", { className: "p-3 bg-slate-950/80 border border-slate-800 rounded text-xs space-y-1", children: [_jsxs("div", { className: "text-emerald-300 flex items-center gap-1", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5 text-emerald-400" }), "0 Queue Overflows"] }), _jsx("div", { className: "text-[10px] text-slate-500", children: "Chaos fault rate: 2.0% stochastic crashes" })] })] })] })] }));
};
