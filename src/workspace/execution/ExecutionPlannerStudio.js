import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { GitBranch, RotateCw, Zap, } from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
export const ExecutionPlannerStudio = () => {
    const [plans, setPlans] = useState([]);
    const [selectedPlan, setSelectedPlan] = useState(null);
    const [goalPrompt, setGoalPrompt] = useState('Deploy autonomous hotfix to production kubernetes cluster');
    const [planning, setPlanning] = useState(false);
    const [loading, setLoading] = useState(true);
    const loadPlans = async () => {
        try {
            setLoading(true);
            const res = await executionPlatformApiClient.listPlans();
            setPlans(res.plans || []);
            if (res.plans && res.plans.length > 0 && !selectedPlan) {
                setSelectedPlan(res.plans[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load plans:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadPlans();
    }, []);
    const handleCreatePlan = async () => {
        if (!goalPrompt.trim())
            return;
        try {
            setPlanning(true);
            const res = await executionPlatformApiClient.planMission({ mission_goal: goalPrompt });
            await loadPlans();
            setSelectedPlan(res.plan);
        }
        catch (err) {
            console.error('Error creating plan:', err);
        }
        finally {
            setPlanning(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs(Card, { className: "bg-slate-900/80 border-purple-800/40", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-lg text-white flex items-center gap-2", children: [_jsx(GitBranch, { className: "w-5 h-5 text-purple-400" }), "Critical Path Method (CPM) Planner Studio"] }) }), _jsx(CardContent, { children: _jsxs("div", { className: "flex flex-col md:flex-row gap-3", children: [_jsx("input", { type: "text", className: "flex-1 bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-purple-500", placeholder: "Enter mission goal for CPM Critical Path graph synthesis...", value: goalPrompt, onChange: (e) => setGoalPrompt(e.target.value) }), _jsx(Button, { variant: "intelligence", onClick: handleCreatePlan, disabled: planning || !goalPrompt.trim(), children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Zap, { className: "w-4 h-4" }), planning ? 'Computing Critical Path...' : 'Compile Execution Plan'] }) })] }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "lg:col-span-1 bg-slate-900/60 border-slate-800", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between pb-3", children: [_jsxs(CardTitle, { className: "text-sm font-semibold text-white", children: ["Generated Plans (", plans.length, ")"] }), _jsx(Button, { variant: "ghost", onClick: loadPlans, children: _jsxs("span", { className: "flex items-center gap-1 text-xs text-slate-400", children: [_jsx(RotateCw, { className: "w-3.5 h-3.5" }), "Refresh"] }) })] }), _jsx(CardContent, { className: "space-y-2 max-h-[600px] overflow-y-auto", children: loading && plans.length === 0 ? (_jsx("p", { className: "text-xs text-slate-500 py-4 text-center", children: "Loading plans..." })) : plans.map((p) => (_jsxs("div", { onClick: () => setSelectedPlan(p), className: `p-3 rounded-lg border cursor-pointer transition-all ${selectedPlan?.plan_id === p.plan_id
                                        ? 'bg-purple-950/40 border-purple-600'
                                        : 'bg-slate-800/40 border-slate-800 hover:border-slate-700'}`, children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-white truncate max-w-[170px]", children: p.mission_goal }), _jsx(Badge, { variant: "outline", children: p.overall_risk })] }), _jsxs("div", { className: "flex items-center justify-between mt-2 text-[11px] text-slate-400 font-mono", children: [_jsxs("span", { children: [p.nodes.length, " Nodes"] }), _jsxs("span", { children: [p.total_estimated_duration_ms, "ms total"] })] })] }, p.plan_id))) })] }), _jsxs(Card, { className: "lg:col-span-2 bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsx(CardTitle, { className: "text-base text-white", children: selectedPlan ? selectedPlan.mission_goal : 'Select a Plan' }), selectedPlan && (_jsxs("span", { className: "text-xs font-mono text-purple-400", children: ["Critical Steps: ", selectedPlan.critical_path_steps.length] }))] }) }), _jsx(CardContent, { className: "space-y-4", children: selectedPlan && (_jsx(_Fragment, { children: _jsx("div", { className: "border border-slate-800 rounded-xl overflow-hidden", children: _jsxs("table", { className: "w-full text-left text-xs", children: [_jsx("thead", { className: "bg-slate-950 text-slate-400 font-mono", children: _jsxs("tr", { children: [_jsx("th", { className: "p-3", children: "Step / Tool" }), _jsx("th", { className: "p-3", children: "Est. Duration" }), _jsx("th", { className: "p-3", children: "Early (ES/EF)" }), _jsx("th", { className: "p-3", children: "Late (LS/LF)" }), _jsx("th", { className: "p-3", children: "Slack" }), _jsx("th", { className: "p-3", children: "Critical Path" })] }) }), _jsx("tbody", { className: "divide-y divide-slate-800 text-slate-300", children: selectedPlan.nodes.map((n) => (_jsxs("tr", { className: n.is_critical_path ? 'bg-purple-950/20' : 'hover:bg-slate-800/30', children: [_jsxs("td", { className: "p-3 font-medium", children: [_jsx("span", { className: "text-white block", children: n.name }), _jsx("span", { className: "text-[11px] font-mono text-purple-400", children: n.tool_id })] }), _jsxs("td", { className: "p-3 font-mono", children: [n.estimated_duration_ms, " ms"] }), _jsxs("td", { className: "p-3 font-mono text-slate-400", children: [n.early_start, " / ", n.early_finish] }), _jsxs("td", { className: "p-3 font-mono text-slate-400", children: [n.late_start, " / ", n.late_finish] }), _jsx("td", { className: "p-3 font-mono", children: _jsxs("span", { className: n.slack === 0 ? 'text-amber-400 font-bold' : 'text-slate-400', children: [n.slack, " ms"] }) }), _jsx("td", { className: "p-3", children: n.is_critical_path ? (_jsx(Badge, { variant: "intelligence", children: "CRITICAL" })) : (_jsx(Badge, { variant: "outline", children: "Buffer" })) })] }, n.step_id))) })] }) }) })) })] })] })] }));
};
