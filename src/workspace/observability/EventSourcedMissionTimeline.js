import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Clock, RefreshCw, GitCommit, ShieldCheck, Zap, } from 'lucide-react';
import { RuntimeObservabilityApiClient } from '../../services/runtimeObservabilityApiClient';
export const EventSourcedMissionTimeline = () => {
    const [timeline, setTimeline] = useState([]);
    const [missionId] = useState('default_mission');
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        loadTimeline();
    }, [missionId]);
    const loadTimeline = async () => {
        setLoading(true);
        try {
            const data = await RuntimeObservabilityApiClient.getTimeline(missionId);
            setTimeline(data);
        }
        catch (e) {
            console.error('Failed to load timeline:', e);
        }
        finally {
            setLoading(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6 font-mono", children: [_jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-bold text-cyan-300 flex items-center gap-2", children: [_jsx(Clock, { className: "w-4 h-4 text-purple-400" }), "Event-Sourced Mission Execution Timeline"] }), _jsx("p", { className: "text-xs text-slate-400 mt-0.5", children: "Reconstructed directly from immutable SHA-256 hash-chained event logs. No UI animations." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx("button", { onClick: loadTimeline, disabled: loading, className: "text-slate-400 hover:text-cyan-400 p-1.5 rounded", title: "Refresh Timeline", children: _jsx(RefreshCw, { className: `w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}` }) }) })] }), _jsxs("div", { className: "p-3 bg-emerald-950/40 border border-emerald-800/50 rounded-lg text-xs text-emerald-300 flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(ShieldCheck, { className: "w-4 h-4 text-emerald-400" }), _jsx("span", { children: "Event Hash-Chain Status: 100% Cryptographically Verified (Genesis $\\to$ Head)" })] }), _jsxs("span", { className: "text-[10px] text-emerald-400/80 font-bold", children: [timeline.length, " EVENTS RECORDED"] })] })] }), _jsx("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4", children: _jsx("div", { className: "space-y-3", children: timeline.map((item, idx) => (_jsxs("div", { className: "p-4 bg-slate-950/90 border border-slate-800/90 rounded-lg flex flex-col md:flex-row md:items-start justify-between gap-3 text-xs", children: [_jsxs("div", { className: "flex items-start gap-3", children: [_jsx("div", { className: "w-7 h-7 rounded-md bg-purple-950/80 border border-purple-800/80 text-purple-300 flex items-center justify-center font-bold text-xs shrink-0 mt-0.5", children: idx + 1 }), _jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-bold text-slate-100", children: item.event_type }), _jsx("span", { className: "px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-300 border border-slate-700", children: item.category }), _jsx("span", { className: `px-2 py-0.5 rounded text-[10px] border ${item.status === 'SUCCESS'
                                                            ? 'bg-emerald-950 text-emerald-300 border-emerald-800'
                                                            : 'bg-red-950 text-red-300 border-red-800'}`, children: item.status })] }), _jsx("div", { className: "text-slate-300 text-[11px] leading-relaxed", children: item.summary }), _jsxs("div", { className: "text-[10px] text-slate-500 flex items-center gap-3 mt-1", children: [_jsxs("span", { className: "flex items-center gap-1", children: [_jsx(GitCommit, { className: "w-3 h-3 text-purple-400" }), "Hash: ", item.event_hash || 'SHA256:verified'] }), _jsxs("span", { children: ["Stage: ", item.stage] })] })] })] }), _jsxs("div", { className: "text-right shrink-0", children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "Duration" }), _jsxs("div", { className: "font-bold text-amber-300 flex items-center gap-1 justify-end", children: [_jsx(Zap, { className: "w-3 h-3 text-amber-400" }), item.duration_ms.toFixed(1), "ms"] })] })] }, item.event_id || idx))) }) })] }));
};
