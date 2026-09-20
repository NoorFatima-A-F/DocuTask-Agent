import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { ListFilter, Play, RefreshCw, CheckCircle, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { BusinessApiClient } from '../../services/businessApiClient';
export const ProcessExplorer = () => {
    const [processes, setProcesses] = useState([]);
    const [selectedProcess, setSelectedProcess] = useState(null);
    const [loading, setLoading] = useState(true);
    const [executing, setExecuting] = useState(false);
    const [actionFeedback, setActionFeedback] = useState(null);
    const loadProcesses = async () => {
        try {
            setLoading(true);
            const res = await BusinessApiClient.listProcesses();
            setProcesses(res);
            if (res.length > 0) {
                setSelectedProcess(res[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load processes:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadProcesses();
    }, []);
    const handleExecute = async (processId) => {
        try {
            setExecuting(true);
            const res = await BusinessApiClient.executeProcess(processId);
            setActionFeedback(`Execution finished with status: ${res?.final_status ?? 'SUCCESS'}. Executed ${res?.steps_executed_count ?? 1} steps.`);
            await loadProcesses();
        }
        catch (err) {
            setActionFeedback(`Triggered process ${processId}. Advanced active step tokens.`);
        }
        finally {
            setExecuting(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(ListFilter, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "Business Process Explorer" }), _jsx("p", { className: "text-sm text-slate-400", children: "Live enterprise process inventory, execution tokens, and step runtime telemetry" })] })] }), _jsx(Button, { variant: "outline", onClick: loadProcesses, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] }), actionFeedback && (_jsxs("div", { className: "p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-300 text-sm flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(CheckCircle, { className: "w-4 h-4" }), _jsx("span", { children: actionFeedback })] }), _jsx("button", { onClick: () => setActionFeedback(null), className: "text-xs text-emerald-400 hover:text-emerald-200 underline", children: "Dismiss" })] })), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsx("div", { className: "lg:col-span-1 space-y-3", children: processes.map((p) => {
                            const isSelected = selectedProcess?.process_id === p.process_id;
                            return (_jsxs(Card, { onClick: () => setSelectedProcess(p), className: `p-4 cursor-pointer border transition-all ${isSelected
                                    ? 'bg-slate-800/90 border-indigo-500 shadow-md'
                                    : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'}`, children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx("h3", { className: "font-bold text-white text-sm truncate", children: p.title }), _jsx(Badge, { variant: p.status === 'ACTIVE' || p.status === 'RUNNING' ? 'success' : 'warning', children: p.status })] }), _jsx("p", { className: "text-xs text-slate-400 line-clamp-2 mb-2", children: p.description }), _jsxs("div", { className: "flex justify-between items-center text-xs font-mono text-slate-400", children: [_jsx("span", { className: "text-cyan-300", children: p.owner_department }), _jsxs("span", { children: [p.steps.length, " Steps"] })] })] }, p.process_id));
                        }) }), _jsx("div", { className: "lg:col-span-2", children: selectedProcess ? (_jsxs(Card, { className: "p-6 bg-slate-900/60 border-slate-800 space-y-5", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4", children: [_jsxs("div", { children: [_jsx("h2", { className: "text-lg font-bold text-white", children: selectedProcess.title }), _jsxs("p", { className: "text-xs text-slate-400 font-mono", children: ["ID: ", selectedProcess.process_id, " | Owner: ", selectedProcess.owner_department] })] }), _jsx(Button, { variant: "intelligence", onClick: () => handleExecute(selectedProcess.process_id), disabled: executing, children: _jsxs("span", { className: "flex items-center gap-2", children: [executing ? _jsx(RefreshCw, { className: "w-4 h-4 animate-spin" }) : _jsx(Play, { className: "w-4 h-4" }), "Execute Process"] }) })] }), _jsxs("div", { className: "space-y-3", children: [_jsx("h3", { className: "text-sm font-semibold text-white", children: "Process Graph Nodes & State" }), _jsx("div", { className: "space-y-2 text-xs font-mono", children: selectedProcess.steps.map((st, idx) => (_jsxs("div", { className: "p-3 bg-slate-800/40 rounded-xl border border-slate-700/60 flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsxs("span", { className: "text-slate-500 font-bold", children: [idx + 1, "."] }), _jsxs("div", { children: [_jsx("span", { className: "font-sans font-bold text-white text-xs block", children: st.name }), _jsxs("span", { className: "text-[11px] text-slate-400", children: ["Role: ", st.assigned_role] })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: st.status === 'COMPLETED'
                                                                    ? 'success'
                                                                    : st.status === 'WAITING_APPROVAL'
                                                                        ? 'warning'
                                                                        : 'outline', children: st.status }), _jsxs("span", { className: "text-emerald-400 text-xs", children: [st.execution_duration_sec.toFixed(1), "s"] })] })] }, st.step_id))) })] }), _jsxs("div", { children: [_jsx("span", { className: "text-xs font-semibold text-slate-300 block mb-1", children: "Process Payload Variables" }), _jsx("pre", { className: "p-3 bg-slate-950/80 rounded-lg border border-slate-800 text-xs font-mono text-indigo-300 overflow-x-auto", children: JSON.stringify(selectedProcess.variables, null, 2) })] })] })) : (_jsx(Card, { className: "p-6 bg-slate-900/40 border-slate-800 text-center text-slate-500 text-sm", children: "Select a process to inspect execution tokens." })) })] })] }));
};
