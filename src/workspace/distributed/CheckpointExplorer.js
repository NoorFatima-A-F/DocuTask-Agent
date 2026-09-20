import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Shield, RefreshCw, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { DistributedApiClient } from '../../services/distributedApiClient';
export const CheckpointExplorer = () => {
    const [workflows, setWorkflows] = useState([]);
    const [selectedWorkflowId, setSelectedWorkflowId] = useState('');
    const [checkpoints, setCheckpoints] = useState([]);
    const [selectedCheckpoint, setSelectedCheckpoint] = useState(null);
    const [loading, setLoading] = useState(true);
    const loadWorkflows = async () => {
        try {
            setLoading(true);
            const res = await DistributedApiClient.getDurableWorkflows();
            setWorkflows(res);
            if (res.length > 0) {
                const firstWf = res[0];
                if (firstWf) {
                    setSelectedWorkflowId(firstWf.workflow_id);
                    const chks = await DistributedApiClient.getCheckpoints(firstWf.workflow_id);
                    const fullList = chks.length > 0 ? chks : firstWf.checkpoints || [];
                    setCheckpoints(fullList);
                    if (fullList.length > 0) {
                        setSelectedCheckpoint(fullList[0] || null);
                    }
                }
            }
        }
        catch (err) {
            console.error('Failed to load checkpoints:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadWorkflows();
    }, []);
    const handleSelectWorkflow = async (wfId) => {
        setSelectedWorkflowId(wfId);
        try {
            const chks = await DistributedApiClient.getCheckpoints(wfId);
            const matched = workflows.find((w) => w.workflow_id === wfId);
            const list = chks.length > 0 ? chks : matched?.checkpoints || [];
            setCheckpoints(list);
            setSelectedCheckpoint(list[0] || null);
        }
        catch (err) {
            console.error('Failed to load checkpoints for workflow:', err);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(Shield, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "Checkpoint & State Explorer" }), _jsx("p", { className: "text-sm text-slate-400", children: "Immutable snapshot verification, monotonic fencing tokens & crash-recovery state audits" })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("select", { value: selectedWorkflowId, onChange: (e) => handleSelectWorkflow(e.target.value), className: "bg-slate-800 border border-slate-700 text-slate-200 text-sm rounded-lg px-3 py-2", children: workflows.map((w) => (_jsxs("option", { value: w.workflow_id, children: [w.title, " (", w.workflow_id, ")"] }, w.workflow_id))) }), _jsx(Button, { variant: "outline", onClick: loadWorkflows, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsx("div", { className: "lg:col-span-1 space-y-3", children: checkpoints.map((chk) => {
                            const isSelected = selectedCheckpoint?.checkpoint_id === chk.checkpoint_id;
                            return (_jsxs(Card, { onClick: () => setSelectedCheckpoint(chk), className: `p-4 cursor-pointer border transition-all ${isSelected
                                    ? 'bg-slate-800/80 border-indigo-500 shadow-md'
                                    : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'}`, children: [_jsxs("div", { className: "flex items-center justify-between mb-1", children: [_jsx("span", { className: "font-mono font-bold text-indigo-300 text-xs", children: chk.checkpoint_id }), _jsxs(Badge, { variant: "intelligence", children: ["Token #", chk.fencing_token] })] }), _jsxs("div", { className: "text-xs text-slate-400 flex justify-between", children: [_jsxs("span", { children: ["Step ", chk.step_index + 1] }), _jsx("span", { children: new Date(chk.timestamp).toLocaleTimeString() })] })] }, chk.checkpoint_id));
                        }) }), _jsx("div", { className: "lg:col-span-2", children: selectedCheckpoint ? (_jsxs(Card, { className: "p-6 bg-slate-900/60 border-slate-800 space-y-5", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsx("h3", { className: "text-base font-bold text-white", children: "Snapshot Details" }), _jsxs("p", { className: "text-xs font-mono text-slate-400", children: ["ID: ", selectedCheckpoint.checkpoint_id] })] }), _jsx(Badge, { variant: "success", children: "Cryptographically Sealed" })] }), _jsxs("div", { className: "grid grid-cols-2 gap-4 text-xs font-mono", children: [_jsxs("div", { className: "p-3 bg-slate-800/40 rounded-lg border border-slate-700/60", children: [_jsx("span", { className: "text-slate-500 block", children: "Fencing Token" }), _jsxs("span", { className: "text-white font-bold text-sm", children: ["#", selectedCheckpoint.fencing_token] })] }), _jsxs("div", { className: "p-3 bg-slate-800/40 rounded-lg border border-slate-700/60", children: [_jsx("span", { className: "text-slate-500 block", children: "SHA-256 State Hash" }), _jsx("span", { className: "text-emerald-400 text-xs truncate block", children: selectedCheckpoint.state_hash })] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-xs font-semibold text-slate-300 block mb-2", children: "Workflow Variables" }), _jsx("pre", { className: "p-3 bg-slate-950/80 rounded-lg border border-slate-800 text-xs font-mono text-indigo-300 overflow-x-auto", children: JSON.stringify(selectedCheckpoint.variables, null, 2) })] }), _jsxs("div", { children: [_jsx("span", { className: "text-xs font-semibold text-slate-300 block mb-2", children: "Memory Context" }), _jsx("pre", { className: "p-3 bg-slate-950/80 rounded-lg border border-slate-800 text-xs font-mono text-amber-300 overflow-x-auto", children: JSON.stringify(selectedCheckpoint.memory_context, null, 2) })] })] })) : (_jsx(Card, { className: "p-6 bg-slate-900/40 border-slate-800 text-center text-slate-500 text-sm", children: "No checkpoint selected." })) })] })] }));
};
