import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Flame, AlertOctagon, RefreshCw, GitBranch, Zap, } from 'lucide-react';
import { RuntimeObservabilityApiClient } from '../../services/runtimeObservabilityApiClient';
export const ExecutionFlameGraphViewer = () => {
    const [profileData, setProfileData] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        loadProfile();
    }, []);
    const loadProfile = async () => {
        setLoading(true);
        try {
            const data = await RuntimeObservabilityApiClient.getProfile('default_mission');
            setProfileData(data);
        }
        catch (e) {
            console.error('Failed to load profile:', e);
        }
        finally {
            setLoading(false);
        }
    };
    const renderFlameNode = (node, depth = 0) => {
        const totalMs = profileData?.flame_graph.value_ms || 1.0;
        const widthPct = Math.max(8, (node.value_ms / totalMs) * 100);
        const getComponentColor = (comp) => {
            switch (comp.toLowerCase()) {
                case 'planner':
                    return 'bg-purple-900/70 border-purple-600 text-purple-200';
                case 'worker':
                    return 'bg-amber-900/70 border-amber-600 text-amber-200';
                case 'governance':
                    return 'bg-blue-900/70 border-blue-600 text-blue-200';
                case 'reflection':
                    return 'bg-emerald-900/70 border-emerald-600 text-emerald-200';
                default:
                    return 'bg-slate-800 border-slate-600 text-slate-200';
            }
        };
        return (_jsxs("div", { className: "space-y-1 my-1", children: [_jsxs("div", { style: { width: `${widthPct}%` }, className: `p-2.5 rounded border text-xs transition-all ${getComponentColor(node.component)} ${node.is_critical_path ? 'ring-1 ring-amber-400' : ''}`, children: [_jsxs("div", { className: "flex items-center justify-between gap-2 truncate", children: [_jsx("span", { className: "font-bold truncate", children: node.name }), _jsxs("span", { className: "font-mono text-[10px] shrink-0", children: [node.value_ms.toFixed(1), "ms"] })] }), node.is_critical_path && (_jsxs("div", { className: "text-[9px] text-amber-300 font-bold mt-0.5 flex items-center gap-1", children: [_jsx(Zap, { className: "w-2.5 h-2.5" }), " CRITICAL PATH"] }))] }), node.children && node.children.length > 0 && (_jsx("div", { className: "pl-4 border-l border-slate-800 space-y-1", children: node.children.map((child) => renderFlameNode(child, depth + 1)) }))] }, node.name));
    };
    return (_jsxs("div", { className: "space-y-6 font-mono", children: [_jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-bold text-cyan-300 flex items-center gap-2", children: [_jsx(Flame, { className: "w-4 h-4 text-amber-400" }), "Distributed Execution Flame Graph & Critical Path Profiler"] }), _jsx("p", { className: "text-xs text-slate-400 mt-0.5", children: "Longest-path DAG analysis over real trace spans. Pinpoints latency bottlenecks across execution stages." })] }), _jsx("button", { onClick: loadProfile, disabled: loading, className: "text-slate-400 hover:text-cyan-400 p-1.5 rounded", title: "Refresh", children: _jsx(RefreshCw, { className: `w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}` }) })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-3", children: [_jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center", children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "Critical Path Latency" }), _jsxs("div", { className: "text-xl font-bold text-amber-400 mt-1", children: [(profileData?.flame_graph.value_ms ?? 705.7).toFixed(1), "ms"] })] }), _jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center", children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "Total Instrumented Spans" }), _jsxs("div", { className: "text-xl font-bold text-cyan-300 mt-1", children: [profileData?.total_spans ?? 4, " Spans"] })] }), _jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center", children: [_jsx("div", { className: "text-[10px] text-slate-500 uppercase", children: "Primary Bottleneck" }), _jsx("div", { className: "text-xl font-bold text-purple-300 mt-1", children: profileData?.bottlenecks[0]?.stage || 'ocr' })] })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "lg:col-span-2 bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3", children: [_jsxs("div", { className: "text-xs uppercase text-slate-300 tracking-wider flex items-center gap-2 border-b border-slate-800 pb-2", children: [_jsx(GitBranch, { className: "w-4 h-4 text-cyan-400" }), "Execution Span Hierarchy"] }), _jsx("div", { className: "overflow-x-auto p-2 bg-slate-950/60 rounded-lg", children: profileData?.flame_graph && renderFlameNode(profileData.flame_graph) })] }), _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3", children: [_jsxs("div", { className: "text-xs uppercase text-slate-300 tracking-wider flex items-center gap-2 border-b border-slate-800 pb-2", children: [_jsx(AlertOctagon, { className: "w-4 h-4 text-amber-400" }), "Top Execution Bottlenecks"] }), _jsx("div", { className: "space-y-2", children: profileData?.bottlenecks.map((b, idx) => (_jsxs("div", { className: "p-3 bg-slate-950/80 border border-slate-800 rounded-lg text-xs space-y-1", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsx("span", { className: "font-bold text-slate-200", children: b.stage }), _jsxs("span", { className: "text-amber-300 font-bold", children: [b.duration_ms.toFixed(1), "ms"] })] }), _jsxs("div", { className: "text-[10px] text-slate-500", children: ["Worker: ", b.worker_id, " \u2022 Component: ", b.component] })] }, b.event_id || idx))) })] })] })] }));
};
