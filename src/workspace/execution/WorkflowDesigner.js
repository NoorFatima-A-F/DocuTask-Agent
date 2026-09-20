import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Workflow, RotateCw, ArrowRight, } from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
export const WorkflowDesigner = () => {
    const [workflows, setWorkflows] = useState([]);
    const [selectedWf, setSelectedWf] = useState(null);
    const [tiers, setTiers] = useState([]);
    const [loading, setLoading] = useState(true);
    const loadWorkflows = async () => {
        try {
            setLoading(true);
            const res = await executionPlatformApiClient.listWorkflows();
            setWorkflows(res.workflows || []);
            if (res.workflows && res.workflows.length > 0 && res.workflows[0]) {
                selectWorkflow(res.workflows[0].workflow_id);
            }
        }
        catch (err) {
            console.error('Failed to load workflows:', err);
        }
        finally {
            setLoading(false);
        }
    };
    const selectWorkflow = async (wfId) => {
        try {
            const res = await executionPlatformApiClient.getWorkflow(wfId);
            setSelectedWf(res.workflow);
            setTiers(res.tiers || []);
        }
        catch (err) {
            console.error('Failed to get workflow details:', err);
        }
    };
    useEffect(() => {
        loadWorkflows();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold text-white flex items-center gap-2", children: [_jsx(Workflow, { className: "w-5 h-5 text-purple-400" }), "Workflow DAG & Saga Designer"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Topological tier orchestrator, cycle detection engine, and automated compensation DAG inversion" })] }), _jsx(Button, { variant: "outline", onClick: loadWorkflows, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: "w-4 h-4" }), "Refresh"] }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "lg:col-span-1 bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-sm font-semibold text-white", children: ["Registered Pipelines (", workflows.length, ")"] }) }), _jsx(CardContent, { className: "space-y-2", children: loading && workflows.length === 0 ? (_jsx("p", { className: "text-xs text-slate-500 py-4 text-center", children: "Loading pipelines..." })) : workflows.map((wf) => (_jsxs("div", { onClick: () => selectWorkflow(wf.workflow_id), className: `p-3 rounded-lg border cursor-pointer transition-all ${selectedWf?.workflow_id === wf.workflow_id
                                        ? 'bg-purple-950/40 border-purple-600'
                                        : 'bg-slate-800/40 border-slate-800 hover:border-slate-700'}`, children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-white truncate max-w-[180px]", children: wf.name }), _jsx(Badge, { variant: "intelligence", children: wf.mode })] }), _jsx("p", { className: "text-[11px] text-slate-400 mt-1 line-clamp-2", children: wf.description })] }, wf.workflow_id))) })] }), _jsxs(Card, { className: "lg:col-span-2 bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsx(CardTitle, { className: "text-base text-white", children: selectedWf ? selectedWf.name : 'Select a Workflow' }), selectedWf && (_jsxs(Badge, { variant: "outline", className: "text-xs", children: [selectedWf.steps.length, " Steps \u2022 ", selectedWf.risk_level, " Risk"] }))] }) }), _jsx(CardContent, { className: "space-y-6", children: selectedWf && (_jsxs(_Fragment, { children: [_jsxs("div", { children: [_jsx("h4", { className: "text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3", children: "Topological Parallel Execution Tiers (Kahn's Sort)" }), _jsx("div", { className: "flex flex-wrap items-center gap-3", children: tiers.map((tier, idx) => (_jsxs("div", { className: "flex items-center gap-2", children: [_jsxs("div", { className: "p-3 bg-slate-950 border border-purple-800/50 rounded-lg", children: [_jsxs("span", { className: "text-[10px] text-purple-400 font-bold block mb-1", children: ["TIER ", idx + 1] }), _jsx("div", { className: "flex flex-wrap gap-1.5", children: tier.map((stepId) => (_jsx("span", { className: "px-2 py-0.5 bg-purple-900/40 text-purple-200 text-xs rounded", children: stepId }, stepId))) })] }), idx < tiers.length - 1 && _jsx(ArrowRight, { className: "w-4 h-4 text-slate-600" })] }, idx))) })] }), _jsxs("div", { className: "space-y-3", children: [_jsx("h4", { className: "text-xs font-semibold text-slate-400 uppercase tracking-wider", children: "Workflow Node Specifications" }), selectedWf.steps.map((step) => (_jsxs("div", { className: "p-3 bg-slate-800/40 border border-slate-700/60 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-sm font-semibold text-white", children: step.name }), _jsxs("span", { className: "text-xs font-mono text-purple-400", children: ["(", step.step_id, ")"] })] }), _jsxs("p", { className: "text-xs text-slate-400 mt-1", children: ["Tool: ", _jsx("span", { className: "font-mono text-slate-300", children: step.tool_id }), step.depends_on.length > 0 && ` • Depends on: ${step.depends_on.join(', ')}`] })] }), _jsx("div", { className: "flex items-center gap-2", children: step.is_compensable ? (_jsx(Badge, { variant: "success", children: "Compensable (Saga)" })) : (_jsx(Badge, { variant: "warning", children: "Non-Compensable" })) })] }, step.step_id)))] })] })) })] })] })] }));
};
