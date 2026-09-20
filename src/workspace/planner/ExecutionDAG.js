import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Layers, RefreshCw, } from 'lucide-react';
import { ApdlePlannerApiClient } from '../../services/apdlePlannerApiClient';
export const ExecutionDAG = () => {
    const [dag, setDag] = useState(null);
    const [schedule, setSchedule] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        loadData();
    }, []);
    const loadData = async () => {
        setLoading(true);
        try {
            const [dagRes, schedRes] = await Promise.all([
                ApdlePlannerApiClient.getGraph('default_mission'),
                ApdlePlannerApiClient.getSchedule('default_mission'),
            ]);
            setDag(dagRes);
            setSchedule(schedRes);
        }
        catch (e) {
            console.error('Failed to load execution DAG:', e);
        }
        finally {
            setLoading(false);
        }
    };
    return (_jsx("div", { className: "space-y-6 font-mono", children: _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-bold text-cyan-300 flex items-center gap-2", children: [_jsx(Layers, { className: "w-4 h-4 text-cyan-400" }), "Dynamic Wavefront Execution DAG"] }), _jsx("p", { className: "text-xs text-slate-400 mt-0.5", children: "Visualizes concurrent execution wavefronts. Nodes in the same layer execute in parallel across worker pools." })] }), _jsx("button", { onClick: loadData, disabled: loading, className: "text-slate-400 hover:text-cyan-400 p-1.5 rounded", title: "Refresh", children: _jsx(RefreshCw, { className: `w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}` }) })] }), _jsx("div", { className: "space-y-4", children: schedule?.wavefronts.map((wave, layerIdx) => (_jsxs("div", { className: "bg-slate-950/80 border border-slate-800/90 rounded-lg p-4 space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between text-xs border-b border-slate-800 pb-2", children: [_jsxs("span", { className: "font-bold text-purple-300 flex items-center gap-2", children: [_jsxs("span", { children: ["Wavefront Layer ", layerIdx + 1] }), _jsx("span", { className: "text-[10px] px-2 py-0.5 rounded bg-purple-950 text-purple-400 border border-purple-800", children: wave.length > 1 ? 'PARALLEL CONCURRENCY' : 'SEQUENTIAL BARRIER' })] }), _jsxs("span", { className: "text-slate-500", children: [wave.length, " Tasks"] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-3", children: wave.map((nodeId) => {
                                    const node = dag?.nodes.find((n) => n.id === nodeId);
                                    if (!node)
                                        return null;
                                    return (_jsxs("div", { className: "p-3 bg-slate-900/70 border border-slate-800 rounded-lg text-xs space-y-2", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsx("span", { className: "font-bold text-slate-200", children: node.label }), _jsx("span", { className: `text-[9px] px-1.5 py-0.5 rounded border ${node.status === 'COMPLETED'
                                                            ? 'bg-emerald-950 text-emerald-300 border-emerald-800'
                                                            : node.status === 'RUNNING'
                                                                ? 'bg-cyan-950 text-cyan-300 border-cyan-800'
                                                                : 'bg-slate-800 text-slate-400 border-slate-700'}`, children: node.status })] }), _jsxs("div", { className: "text-[10px] text-slate-500 flex justify-between", children: [_jsxs("span", { children: ["Worker: ", node.assigned_worker || 'Pending'] }), _jsxs("span", { children: [node.estimated_runtime_ms.toFixed(0), "ms"] })] })] }, nodeId));
                                }) })] }, layerIdx))) })] }) }));
};
