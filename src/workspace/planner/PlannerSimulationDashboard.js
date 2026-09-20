import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { TrendingUp, Sliders, RefreshCw, } from 'lucide-react';
import { ApdlePlannerApiClient } from '../../services/apdlePlannerApiClient';
export const PlannerSimulationDashboard = () => {
    const [sim, setSim] = useState(null);
    const [trials, setTrials] = useState(100);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        loadSimulation();
    }, [trials]);
    const loadSimulation = async () => {
        setLoading(true);
        try {
            const data = await ApdlePlannerApiClient.getSimulation('default_mission', trials);
            setSim(data);
        }
        catch (e) {
            console.error('Failed to load simulation:', e);
        }
        finally {
            setLoading(false);
        }
    };
    return (_jsx("div", { className: "space-y-6 font-mono", children: _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-bold text-cyan-300 flex items-center gap-2", children: [_jsx(TrendingUp, { className: "w-4 h-4 text-cyan-400" }), "Pre-Execution Monte Carlo DAG Simulator"] }), _jsx("p", { className: "text-xs text-slate-400 mt-0.5", children: "Stochastic simulation over DAG variance. Estimates tail latencies (P90, P99), expected cost, and risk bottlenecks." })] }), _jsx("button", { onClick: loadSimulation, disabled: loading, className: "text-slate-400 hover:text-cyan-400 p-1.5 rounded", title: "Refresh", children: _jsx(RefreshCw, { className: `w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}` }) })] }), _jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-4 space-y-2 text-xs", children: [_jsx("div", { className: "flex justify-between items-center", children: _jsxs("span", { className: "text-slate-300 flex items-center gap-2", children: [_jsx(Sliders, { className: "w-3.5 h-3.5 text-purple-400" }), "Monte Carlo Sample Size: ", _jsxs("span", { className: "text-purple-300 font-bold", children: [trials, " Iterations"] })] }) }), _jsx("input", { type: "range", min: "20", max: "500", step: "20", value: trials, onChange: (e) => setTrials(parseInt(e.target.value)), className: "w-full accent-cyan-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg" })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-3", children: [_jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center", children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "Median Latency (P50)" }), _jsxs("div", { className: "text-xl font-bold text-emerald-400 mt-1", children: [(sim?.p50_completion_ms ?? 760).toFixed(0), "ms"] })] }), _jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center", children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "Tail Latency (P90)" }), _jsxs("div", { className: "text-xl font-bold text-amber-400 mt-1", children: [(sim?.p90_completion_ms ?? 880).toFixed(0), "ms"] })] }), _jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center", children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "Worst Case (P99)" }), _jsxs("div", { className: "text-xl font-bold text-red-400 mt-1", children: [(sim?.p99_completion_ms ?? 995).toFixed(0), "ms"] })] }), _jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center", children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "Expected Cost" }), _jsxs("div", { className: "text-xl font-bold text-cyan-300 mt-1", children: ["$", (sim?.expected_total_cost_usd ?? 0.0032).toFixed(4)] })] })] })] }) }));
};
