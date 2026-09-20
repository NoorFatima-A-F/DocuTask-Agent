import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { TrendingUp, Cpu, Clock, AlertOctagon, CheckCircle2, RefreshCw, Sliders, } from 'lucide-react';
import { DecisionIntelligenceApiClient } from '../../services/decisionIntelligenceApiClient';
export const WorldPredictionDashboard = () => {
    const [forecasts, setForecasts] = useState({});
    const [loading, setLoading] = useState(true);
    const [loadFactor, setLoadFactor] = useState(1.2);
    const [concurrency, setConcurrency] = useState(6);
    useEffect(() => {
        loadForecast();
    }, [loadFactor, concurrency]);
    const loadForecast = async () => {
        setLoading(true);
        try {
            const data = await DecisionIntelligenceApiClient.getWorldForecast();
            setForecasts(data.horizons);
        }
        catch (e) {
            console.error('Failed to load world forecasts:', e);
        }
        finally {
            setLoading(false);
        }
    };
    const horizonKeys = ['5m', '10m', '30m'];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-bold font-mono text-cyan-300 flex items-center gap-2", children: [_jsx(TrendingUp, { className: "w-4 h-4 text-cyan-400" }), "World Model Forward Simulator"] }), _jsx("p", { className: "text-xs text-slate-400 mt-0.5", children: "Simulates forward cluster physics across 5m, 10m, and 30m prediction horizons using Queuing Theory & Markov Chains." })] }), _jsxs("button", { onClick: loadForecast, disabled: loading, className: "flex items-center gap-2 px-3 py-1.5 bg-cyan-950/40 hover:bg-cyan-900/50 border border-cyan-800 text-cyan-300 rounded-lg text-xs font-mono transition-all disabled:opacity-50 self-start sm:self-auto", children: [_jsx(RefreshCw, { className: `w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}` }), "Re-simulate Physics"] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6 pt-1", children: [_jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between text-xs font-mono", children: [_jsxs("span", { className: "text-slate-300 flex items-center gap-1.5", children: [_jsx(Sliders, { className: "w-3.5 h-3.5 text-purple-400" }), "Mission Arrival Load Factor"] }), _jsxs("span", { className: "text-purple-300 font-bold", children: [loadFactor.toFixed(1), "x"] })] }), _jsx("input", { type: "range", min: "0.5", max: "3.0", step: "0.1", value: loadFactor, onChange: (e) => setLoadFactor(parseFloat(e.target.value)), className: "w-full accent-purple-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg" }), _jsxs("div", { className: "flex justify-between text-[10px] text-slate-500 font-mono", children: [_jsx("span", { children: "0.5x (Idle)" }), _jsx("span", { children: "1.0x (Nominal)" }), _jsx("span", { children: "3.0x (Peak Burst)" })] })] }), _jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between text-xs font-mono", children: [_jsxs("span", { className: "text-slate-300 flex items-center gap-1.5", children: [_jsx(Cpu, { className: "w-3.5 h-3.5 text-cyan-400" }), "Active Worker Concurrency"] }), _jsxs("span", { className: "text-cyan-300 font-bold", children: [concurrency, " Nodes"] })] }), _jsx("input", { type: "range", min: "1", max: "16", step: "1", value: concurrency, onChange: (e) => setConcurrency(parseInt(e.target.value)), className: "w-full accent-cyan-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg" }), _jsxs("div", { className: "flex justify-between text-[10px] text-slate-500 font-mono", children: [_jsx("span", { children: "1 Node" }), _jsx("span", { children: "8 Nodes" }), _jsx("span", { children: "16 Nodes" })] })] })] })] }), _jsx("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: horizonKeys.map((key) => {
                    const f = forecasts[key];
                    if (!f)
                        return null;
                    const isWarning = f.predicted_gpu_utilization > 0.8 || f.predicted_budget_exhaustion_probability > 0.05;
                    const gpuPct = (f.predicted_gpu_utilization * 100).toFixed(1);
                    const exhaustPct = (f.predicted_budget_exhaustion_probability * 100).toFixed(1);
                    return (_jsxs("div", { className: `bg-slate-900/90 border rounded-xl p-5 space-y-4 transition-all ${isWarning
                            ? 'border-amber-500/50 shadow-lg shadow-amber-950/20'
                            : 'border-slate-800 hover:border-slate-700'}`, children: [_jsxs("div", { className: "flex items-center justify-between border-b border-slate-800 pb-3", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Clock, { className: "w-4 h-4 text-cyan-400" }), _jsxs("span", { className: "text-base font-bold font-mono text-slate-100", children: ["T + ", f.horizon_minutes, "m Horizon"] })] }), _jsx("span", { className: `px-2 py-0.5 rounded text-[10px] font-mono border ${isWarning
                                            ? 'bg-amber-950/60 text-amber-300 border-amber-800'
                                            : 'bg-emerald-950/60 text-emerald-300 border-emerald-800'}`, children: isWarning ? 'CAPACITY STRAIN' : 'STABLE STATE' })] }), _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between text-xs font-mono mb-1", children: [_jsxs("span", { className: "text-slate-400 flex items-center gap-1", children: [_jsx(Cpu, { className: "w-3.5 h-3.5 text-cyan-400" }), "Predicted GPU Load"] }), _jsxs("span", { className: "font-bold text-slate-200", children: [gpuPct, "%"] })] }), _jsx("div", { className: "w-full bg-slate-800 h-2 rounded-full overflow-hidden", children: _jsx("div", { className: `h-full rounded-full transition-all duration-500 ${f.predicted_gpu_utilization > 0.8
                                                        ? 'bg-gradient-to-r from-amber-500 to-rose-500'
                                                        : 'bg-gradient-to-r from-cyan-500 to-emerald-400'}`, style: { width: `${Math.min(100, f.predicted_gpu_utilization * 100)}%` } }) })] }), _jsxs("div", { className: "grid grid-cols-2 gap-2 pt-1", children: [_jsxs("div", { className: "bg-slate-950/70 border border-slate-800 rounded-lg p-2.5", children: [_jsx("div", { className: "text-[10px] font-mono text-slate-400 uppercase", children: "Queue Depth" }), _jsxs("div", { className: "text-base font-bold font-mono text-slate-200 mt-0.5", children: [f.predicted_queue_depth, " ", _jsx("span", { className: "text-[10px] text-slate-500 font-normal", children: "items" })] })] }), _jsxs("div", { className: "bg-slate-950/70 border border-slate-800 rounded-lg p-2.5", children: [_jsx("div", { className: "text-[10px] font-mono text-slate-400 uppercase", children: "Token Velocity" }), _jsxs("div", { className: "text-base font-bold font-mono text-purple-300 mt-0.5", children: [f.predicted_token_burn_velocity.toFixed(0), ' ', _jsx("span", { className: "text-[10px] text-slate-500 font-normal", children: "t/s" })] })] })] }), _jsxs("div", { className: "bg-slate-950/70 border border-slate-800 rounded-lg p-2.5", children: [_jsxs("div", { className: "flex items-center justify-between text-[10px] font-mono", children: [_jsx("span", { className: "text-slate-400 uppercase", children: "Budget Breach Risk" }), _jsxs("span", { className: `font-bold ${f.predicted_budget_exhaustion_probability > 0.05
                                                            ? 'text-rose-400'
                                                            : 'text-emerald-400'}`, children: [exhaustPct, "%"] })] }), _jsxs("div", { className: "text-[9px] text-slate-500 font-mono mt-1", children: ["95% CI: [", (f.confidence_interval_lower * 100).toFixed(0), "% -", ' ', (f.confidence_interval_upper * 100).toFixed(0), "%]"] })] })] }), _jsx("div", { className: "pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] font-mono text-slate-400", children: _jsxs("span", { className: "flex items-center gap-1", children: [isWarning ? (_jsx(AlertOctagon, { className: "w-3.5 h-3.5 text-amber-400" })) : (_jsx(CheckCircle2, { className: "w-3.5 h-3.5 text-emerald-400" })), isWarning ? 'Auto-scaling triggered' : 'Nominal headroom'] }) })] }, key));
                }) })] }));
};
