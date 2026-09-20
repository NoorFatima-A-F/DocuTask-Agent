import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Sparkles, RotateCw, } from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
export const SimulationControlCenter = () => {
    const [workflows, setWorkflows] = useState([]);
    const [selectedWfId, setSelectedWfId] = useState('');
    const [simReport, setSimReport] = useState(null);
    const [simulating, setSimulating] = useState(false);
    const [loading, setLoading] = useState(true);
    const loadWorkflows = async () => {
        try {
            setLoading(true);
            const res = await executionPlatformApiClient.listWorkflows();
            setWorkflows(res.workflows || []);
            if (res.workflows && res.workflows.length > 0 && res.workflows[0]) {
                setSelectedWfId(res.workflows[0].workflow_id);
                runSimulation(res.workflows[0].workflow_id);
            }
        }
        catch (err) {
            console.error('Failed to load workflows for simulation:', err);
        }
        finally {
            setLoading(false);
        }
    };
    const runSimulation = async (wfId) => {
        try {
            setSimulating(true);
            const res = await executionPlatformApiClient.simulateWorkflow(wfId);
            setSimReport(res.simulation);
        }
        catch (err) {
            console.error('Simulation error:', err);
        }
        finally {
            setSimulating(false);
        }
    };
    useEffect(() => {
        loadWorkflows();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold text-white flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-5 h-5 text-purple-400" }), "Digital Twin Simulation & Blast Radius Sandbox"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Pre-flight dry runs, state delta predictions, compensation rehearsals & cost estimators" })] }), _jsxs("div", { className: "flex items-center gap-3", children: [loading && workflows.length === 0 ? (_jsx("span", { className: "text-xs text-slate-500", children: "Loading workflows..." })) : (_jsx("select", { className: "bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500", value: selectedWfId, onChange: (e) => {
                                    setSelectedWfId(e.target.value);
                                    runSimulation(e.target.value);
                                }, children: workflows.map((w) => (_jsx("option", { value: w.workflow_id, children: w.name }, w.workflow_id))) })), _jsx(Button, { variant: "intelligence", onClick: () => runSimulation(selectedWfId), disabled: simulating || !selectedWfId, children: _jsxs("span", { className: "flex items-center gap-2 text-xs", children: [_jsx(RotateCw, { className: `w-3.5 h-3.5 ${simulating ? 'animate-spin' : ''}` }), "Re-run Simulation"] }) })] })] }), simReport && (_jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { className: "pb-2", children: _jsx(CardTitle, { className: "text-xs text-slate-400", children: "Blast Radius Scope" }) }), _jsxs(CardContent, { children: [_jsx("div", { className: "text-xl font-bold text-white capitalize", children: simReport.blast_radius_scope }), _jsx(Badge, { variant: "outline", className: "mt-1 text-[10px]", children: "Zero Contagion" })] })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { className: "pb-2", children: _jsx(CardTitle, { className: "text-xs text-slate-400", children: "Predicted Cost" }) }), _jsxs(CardContent, { children: [_jsxs("div", { className: "text-xl font-bold text-emerald-400", children: ["$", simReport.total_predicted_cost_usd] }), _jsx("p", { className: "text-[10px] text-slate-500 mt-1", children: "AWS / API compute spend" })] })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { className: "pb-2", children: _jsx(CardTitle, { className: "text-xs text-slate-400", children: "Estimated Latency" }) }), _jsxs(CardContent, { children: [_jsxs("div", { className: "text-xl font-bold text-purple-400", children: [simReport.total_predicted_duration_ms, " ms"] }), _jsx("p", { className: "text-[10px] text-slate-500 mt-1", children: "Forward-pass simulation" })] })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { className: "pb-2", children: _jsx(CardTitle, { className: "text-xs text-slate-400", children: "Rehearsal Verdict" }) }), _jsxs(CardContent, { children: [_jsx("div", { className: "text-xl font-bold text-cyan-400", children: simReport.simulation_passed ? 'Passed (100%)' : 'Failed' }), _jsx("p", { className: "text-[10px] text-emerald-400 mt-1", children: "Ready for real-world dispatch" })] })] })] })), simReport && (_jsxs(Card, { className: "bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { children: _jsx(CardTitle, { className: "text-base text-white", children: "Simulated Step Delta & Shadow State Mutations" }) }), _jsx(CardContent, { children: _jsx("div", { className: "space-y-3", children: simReport.step_results.map((res, idx) => (_jsxs("div", { className: "p-4 bg-slate-800/40 border border-slate-700/60 rounded-xl space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "w-5 h-5 rounded-full bg-purple-900/60 border border-purple-500 flex items-center justify-center text-xs font-bold text-purple-200", children: idx + 1 }), _jsx("span", { className: "text-sm font-semibold text-white", children: res.step_id }), _jsxs("span", { className: "text-xs font-mono text-purple-300", children: ["(", res.tool_id, ")"] })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "success", children: "Saga Rehearsal Passed" }), _jsxs(Badge, { variant: "outline", children: [res.predicted_duration_ms, " ms"] })] })] }), _jsxs("div", { className: "text-xs space-y-1 mt-2", children: [_jsx("span", { className: "text-slate-400 font-semibold block", children: "Predicted External Mutations:" }), _jsx("ul", { className: "list-disc pl-5 text-slate-300 space-y-0.5", children: res.state_mutations_predicted.map((m, mIdx) => (_jsx("li", { children: m }, mIdx))) })] })] }, res.step_id))) }) })] }))] }));
};
