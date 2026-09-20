import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Server, RefreshCw, } from 'lucide-react';
import { ApdlePlannerApiClient } from '../../services/apdlePlannerApiClient';
export const WorkerAllocationView = () => {
    const [schedule, setSchedule] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        loadSchedule();
    }, []);
    const loadSchedule = async () => {
        setLoading(true);
        try {
            const data = await ApdlePlannerApiClient.getSchedule('default_mission');
            setSchedule(data);
        }
        catch (e) {
            console.error('Failed to load schedule:', e);
        }
        finally {
            setLoading(false);
        }
    };
    return (_jsx("div", { className: "space-y-6 font-mono", children: _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-bold text-cyan-300 flex items-center gap-2", children: [_jsx(Server, { className: "w-4 h-4 text-cyan-400" }), "Heterogeneous Worker Allocation & Capability Matching"] }), _jsx("p", { className: "text-xs text-slate-400 mt-0.5", children: "Multi-factor capability matching, load balancing, and active concurrency limits across dedicated worker pools." })] }), _jsx("button", { onClick: loadSchedule, disabled: loading, className: "text-slate-400 hover:text-cyan-400 p-1.5 rounded", title: "Refresh", children: _jsx(RefreshCw, { className: `w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}` }) })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: schedule?.workers.map((w) => {
                        const loadPct = (w.active_tasks / Math.max(1, w.max_concurrency)) * 100;
                        return (_jsxs("div", { className: "p-4 bg-slate-950/80 border border-slate-800 rounded-xl space-y-3 text-xs", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-bold text-slate-100", children: w.name }), _jsx("span", { className: `text-[9px] px-2 py-0.5 rounded border font-bold ${w.status === 'BUSY'
                                                ? 'bg-amber-950 text-amber-300 border-amber-800'
                                                : 'bg-emerald-950 text-emerald-300 border-emerald-800'}`, children: w.status })] }), _jsx("div", { className: "flex flex-wrap gap-1", children: w.capabilities.map((cap) => (_jsx("span", { className: "px-1.5 py-0.5 rounded text-[9px] bg-slate-800 text-cyan-300 border border-slate-700", children: cap }, cap))) }), _jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex justify-between text-[10px] text-slate-400", children: [_jsx("span", { children: "Concurrency Load" }), _jsxs("span", { children: [w.active_tasks, " / ", w.max_concurrency, " (", loadPct.toFixed(0), "%)"] })] }), _jsx("div", { className: "w-full bg-slate-800 h-1.5 rounded-full overflow-hidden", children: _jsx("div", { style: { width: `${loadPct}%` }, className: `h-full transition-all ${loadPct >= 75 ? 'bg-amber-500' : 'bg-cyan-500'}` }) })] }), _jsxs("div", { className: "grid grid-cols-2 gap-2 text-[10px] text-slate-400 pt-2 border-t border-slate-800/60", children: [_jsxs("div", { children: ["Success: ", _jsxs("span", { className: "text-emerald-400 font-bold", children: [(w.historical_success_rate * 100).toFixed(0), "%"] })] }), _jsxs("div", { children: ["Avg Latency: ", _jsxs("span", { className: "text-amber-300 font-bold", children: [w.average_latency_ms.toFixed(0), "ms"] })] })] })] }, w.worker_id));
                    }) })] }) }));
};
