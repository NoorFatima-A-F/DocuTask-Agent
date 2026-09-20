import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Workflow, Pause, Play, RefreshCw, ShieldCheck, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { DistributedApiClient } from '../../services/distributedApiClient';
export const DurableWorkflowInspector = () => {
    const [workflows, setWorkflows] = useState([]);
    const [selectedWorkflow, setSelectedWorkflow] = useState(null);
    const [loading, setLoading] = useState(true);
    const [actionLoading, setActionLoading] = useState(false);
    const loadWorkflows = async () => {
        try {
            setLoading(true);
            const res = await DistributedApiClient.getDurableWorkflows();
            setWorkflows(res);
            if (res.length > 0) {
                setSelectedWorkflow(res[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load durable workflows:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadWorkflows();
    }, []);
    const handlePause = async (id) => {
        try {
            setActionLoading(true);
            const updated = await DistributedApiClient.pauseWorkflow(id);
            setSelectedWorkflow(updated);
            await loadWorkflows();
        }
        catch (err) {
            console.error('Failed to pause workflow:', err);
        }
        finally {
            setActionLoading(false);
        }
    };
    const handleResume = async (id) => {
        try {
            setActionLoading(true);
            const updated = await DistributedApiClient.resumeWorkflow(id);
            setSelectedWorkflow(updated);
            await loadWorkflows();
        }
        catch (err) {
            console.error('Failed to resume workflow:', err);
        }
        finally {
            setActionLoading(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(Workflow, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "Durable Workflow Inspector" }), _jsx("p", { className: "text-sm text-slate-400", children: "Temporal-grade stateful saga orchestration with pause, resume, and checkpoint replay" })] })] }), _jsx(Button, { variant: "outline", onClick: loadWorkflows, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsx("div", { className: "lg:col-span-1 space-y-3", children: workflows.map((wf) => {
                            const isSelected = selectedWorkflow?.workflow_id === wf.workflow_id;
                            return (_jsxs(Card, { onClick: () => setSelectedWorkflow(wf), className: `p-4 cursor-pointer border transition-all ${isSelected
                                    ? 'bg-slate-800/80 border-indigo-500 shadow-md'
                                    : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'}`, children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx("span", { className: "font-bold text-white text-sm truncate", children: wf.title }), _jsx(Badge, { variant: wf.state === 'RUNNING' ? 'intelligence' : wf.state === 'PAUSED' ? 'warning' : 'success', children: wf.state })] }), _jsxs("div", { className: "flex items-center justify-between text-xs text-slate-400 font-mono", children: [_jsx("span", { children: wf.workflow_id }), _jsxs("span", { className: "text-indigo-400", children: ["Step ", wf.current_step_index + 1, " / ", wf.total_steps] })] })] }, wf.workflow_id));
                        }) }), _jsx("div", { className: "lg:col-span-2", children: selectedWorkflow ? (_jsxs(Card, { className: "p-6 bg-slate-900/60 border-slate-800 space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4", children: [_jsxs("div", { children: [_jsx("h2", { className: "text-lg font-bold text-white", children: selectedWorkflow.title }), _jsxs("p", { className: "text-xs text-slate-400 font-mono", children: ["ID: ", selectedWorkflow.workflow_id, " | Tenant: ", selectedWorkflow.tenant_id] })] }), _jsx("div", { className: "flex items-center gap-2", children: selectedWorkflow.state === 'RUNNING' ? (_jsx(Button, { variant: "outline", onClick: () => handlePause(selectedWorkflow.workflow_id), disabled: actionLoading, children: _jsxs("span", { className: "flex items-center gap-2 text-amber-400", children: [_jsx(Pause, { className: "w-4 h-4" }), " Pause Workflow"] }) })) : (_jsx(Button, { variant: "intelligence", onClick: () => handleResume(selectedWorkflow.workflow_id), disabled: actionLoading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Play, { className: "w-4 h-4" }), " Resume Workflow"] }) })) })] }), _jsxs("div", { children: [_jsx("span", { className: "text-xs text-slate-400 block mb-2", children: "Execution Pipeline Progress" }), _jsx("div", { className: "w-full bg-slate-800 h-2 rounded-full overflow-hidden", children: _jsx("div", { className: "bg-indigo-500 h-full rounded-full transition-all", style: {
                                                    width: `${((selectedWorkflow.current_step_index + 1) / selectedWorkflow.total_steps) * 100}%`,
                                                } }) })] }), _jsxs("div", { className: "space-y-3", children: [_jsxs("h3", { className: "text-sm font-semibold text-white flex items-center gap-2", children: [_jsx(ShieldCheck, { className: "w-4 h-4 text-emerald-400" }), "Durable Checkpoints Recorded (", selectedWorkflow.checkpoints?.length ?? 0, ")"] }), selectedWorkflow.checkpoints?.length ? (selectedWorkflow.checkpoints.map((chk) => (_jsxs("div", { className: "p-3 bg-slate-800/40 rounded-xl border border-slate-700 text-xs space-y-2", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsx("span", { className: "font-mono text-indigo-300 font-bold", children: chk.checkpoint_id }), _jsx("span", { className: "text-slate-400", children: new Date(chk.timestamp).toLocaleTimeString() })] }), _jsxs("div", { className: "flex justify-between items-center text-slate-300 font-mono text-[11px]", children: [_jsxs("span", { children: ["Fencing Token: #", chk.fencing_token] }), _jsxs("span", { className: "text-slate-400 truncate max-w-[200px]", children: ["SHA: ", chk.state_hash] })] })] }, chk.checkpoint_id)))) : (_jsx("p", { className: "text-xs text-slate-500 italic", children: "No checkpoints recorded yet." }))] })] })) : (_jsx(Card, { className: "p-6 bg-slate-900/40 border-slate-800 text-center text-slate-500 text-sm", children: "Select a workflow to inspect durable state details." })) })] })] }));
};
