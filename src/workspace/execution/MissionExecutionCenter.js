import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Play, RotateCw, Clock, Send, Workflow, } from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
export const MissionExecutionCenter = () => {
    const [missions, setMissions] = useState([]);
    const [selectedMission, setSelectedMission] = useState(null);
    const [goalInput, setGoalInput] = useState('Deploy autonomous hotfix to canary and broadcast status');
    const [dryRun, setDryRun] = useState(false);
    const [executing, setExecuting] = useState(false);
    const [loading, setLoading] = useState(true);
    const loadMissions = async () => {
        try {
            setLoading(true);
            const res = await executionPlatformApiClient.listMissions();
            setMissions(res.missions || []);
            if (res.missions && res.missions.length > 0 && !selectedMission) {
                setSelectedMission(res.missions[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load missions:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadMissions();
    }, []);
    const handleExecute = async () => {
        if (!goalInput.trim())
            return;
        try {
            setExecuting(true);
            const res = await executionPlatformApiClient.executeGoal({
                goal: goalInput,
                dry_run: dryRun,
                initiated_by: 'Mission Execution Control Room',
            });
            await loadMissions();
            setSelectedMission(res.mission);
        }
        catch (err) {
            console.error('Error executing mission:', err);
        }
        finally {
            setExecuting(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs(Card, { className: "bg-slate-900/80 border-purple-800/40 shadow-lg", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-lg text-white flex items-center gap-2", children: [_jsx(Send, { className: "w-5 h-5 text-purple-400" }), "Dispatch Real-World Execution Mission"] }) }), _jsx(CardContent, { children: _jsxs("div", { className: "flex flex-col md:flex-row gap-4", children: [_jsx("input", { type: "text", className: "flex-1 bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-purple-500", placeholder: "Enter natural language mission goal...", value: goalInput, onChange: (e) => setGoalInput(e.target.value) }), _jsxs("div", { className: "flex items-center gap-4", children: [_jsxs("label", { className: "flex items-center gap-2 text-xs text-slate-300 cursor-pointer", children: [_jsx("input", { type: "checkbox", checked: dryRun, onChange: (e) => setDryRun(e.target.checked), className: "rounded bg-slate-950 border-slate-700 text-purple-600 focus:ring-0" }), "Dry Run Simulation Only"] }), _jsx(Button, { variant: "intelligence", onClick: handleExecute, disabled: executing || !goalInput.trim(), children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Play, { className: "w-4 h-4" }), executing ? 'Executing Mission Pipeline...' : 'Dispatch Mission'] }) })] })] }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "lg:col-span-1 bg-slate-900/60 border-slate-800", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between pb-3", children: [_jsxs(CardTitle, { className: "text-sm font-semibold text-white flex items-center gap-2", children: [_jsx(Clock, { className: "w-4 h-4 text-slate-400" }), "Mission Registry (", missions.length, ")"] }), _jsx(Button, { variant: "ghost", onClick: loadMissions, children: _jsxs("span", { className: "flex items-center gap-1 text-xs text-slate-400 hover:text-white", children: [_jsx(RotateCw, { className: "w-3.5 h-3.5" }), "Refresh"] }) })] }), _jsx(CardContent, { className: "space-y-2 max-h-[600px] overflow-y-auto", children: loading && missions.length === 0 ? (_jsx("p", { className: "text-xs text-slate-500 py-4 text-center", children: "Loading missions..." })) : missions.length === 0 ? (_jsx("p", { className: "text-xs text-slate-500 py-4 text-center", children: "No missions registered yet." })) : (missions.map((m) => (_jsxs("div", { onClick: () => setSelectedMission(m), className: `p-3 rounded-lg border cursor-pointer transition-all ${selectedMission?.mission_id === m.mission_id
                                        ? 'bg-purple-950/40 border-purple-600'
                                        : 'bg-slate-800/40 border-slate-800 hover:border-slate-700'}`, children: [_jsxs("div", { className: "flex items-center justify-between gap-2", children: [_jsx("span", { className: "text-xs font-medium text-white truncate max-w-[180px]", children: m.goal }), _jsx(Badge, { variant: m.status === 'completed'
                                                        ? 'success'
                                                        : m.status === 'executing'
                                                            ? 'intelligence'
                                                            : m.status === 'rolled_back'
                                                                ? 'warning'
                                                                : 'error', children: m.status })] }), _jsxs("div", { className: "flex items-center justify-between mt-2 text-[11px] text-slate-400", children: [_jsxs("span", { children: [m.steps.length, " Steps"] }), _jsxs("span", { children: [m.total_execution_time_ms, "ms"] })] })] }, m.mission_id)))) })] }), _jsxs(Card, { className: "lg:col-span-2 bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsxs(CardTitle, { className: "text-base text-white flex items-center gap-2", children: [_jsx(Workflow, { className: "w-5 h-5 text-purple-400" }), selectedMission ? selectedMission.goal : 'Select a Mission'] }), selectedMission && (_jsxs(Badge, { variant: "outline", className: "text-xs", children: [selectedMission.risk_level.toUpperCase(), " RISK"] }))] }) }), _jsx(CardContent, { children: !selectedMission ? (_jsx("p", { className: "text-sm text-slate-500 py-12 text-center", children: "Select a mission from the list to view step traces and execution certificates." })) : (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "grid grid-cols-2 sm:grid-cols-4 gap-3 p-3 bg-slate-950/60 rounded-lg border border-slate-800 text-xs", children: [_jsxs("div", { children: [_jsx("span", { className: "text-slate-500 block", children: "Mission ID" }), _jsx("span", { className: "text-slate-300 font-mono", children: selectedMission.mission_id })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500 block", children: "Initiated By" }), _jsx("span", { className: "text-slate-300", children: selectedMission.initiated_by })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500 block", children: "Status" }), _jsx("span", { className: "text-emerald-400 font-semibold", children: selectedMission.status })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500 block", children: "Execution Latency" }), _jsxs("span", { className: "text-purple-300", children: [selectedMission.total_execution_time_ms, " ms"] })] })] }), _jsxs("div", { className: "space-y-4", children: [_jsx("h3", { className: "text-sm font-semibold text-slate-200", children: "Execution Stepper" }), _jsx("div", { className: "space-y-3", children: selectedMission.steps.map((step, idx) => (_jsxs("div", { className: "p-3.5 bg-slate-800/40 border border-slate-700/60 rounded-xl space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2.5", children: [_jsx("span", { className: "w-6 h-6 rounded-full bg-purple-900/60 border border-purple-600 flex items-center justify-center text-xs font-bold text-purple-200", children: idx + 1 }), _jsx("span", { className: "text-sm font-medium text-white", children: step.name }), _jsx("span", { className: "text-xs font-mono text-purple-400 bg-purple-950/50 px-2 py-0.5 rounded border border-purple-800/40", children: step.tool_id })] }), _jsx(Badge, { variant: step.status === 'success'
                                                                            ? 'success'
                                                                            : step.status === 'running'
                                                                                ? 'intelligence'
                                                                                : 'warning', children: step.status })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-2 text-xs font-mono mt-2", children: [_jsxs("div", { className: "p-2 bg-slate-950 rounded border border-slate-800", children: [_jsx("span", { className: "text-slate-500 block text-[10px]", children: "INPUTS" }), _jsx("pre", { className: "text-slate-300 text-[11px] overflow-x-auto whitespace-pre-wrap", children: JSON.stringify(step.inputs, null, 2) })] }), _jsxs("div", { className: "p-2 bg-slate-950 rounded border border-slate-800", children: [_jsx("span", { className: "text-emerald-500 block text-[10px]", children: "OUTPUT" }), _jsx("pre", { className: "text-emerald-300 text-[11px] overflow-x-auto whitespace-pre-wrap", children: step.output ? JSON.stringify(step.output, null, 2) : '(no output)' })] })] })] }, step.step_id))) })] })] })) })] })] })] }));
};
