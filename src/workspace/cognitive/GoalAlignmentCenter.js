import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Target, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { cognitiveApiClient } from '../../services/cognitiveApiClient';
export const GoalAlignmentCenter = () => {
    const [goals, setGoals] = useState([]);
    const loadData = async () => {
        const data = await cognitiveApiClient.getGoalAlignments();
        setGoals(data);
    };
    useEffect(() => {
        loadData();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Target, { className: "w-7 h-7 text-indigo-400" }), "Enterprise Goal Alignment & KPI Hierarchy"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Binds every autonomous agent directly to Department Goals, Business Objectives, and Corporate KPIs." })] }), _jsx(Button, { variant: "outline", onClick: loadData, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: "w-4 h-4" }), "Refresh"] }) })] }), _jsx("div", { className: "space-y-4", children: goals.map((g) => (_jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 space-y-4", children: [_jsxs("div", { className: "flex justify-between items-start", children: [_jsxs("div", { children: [_jsx(Badge, { variant: "outline", className: "text-indigo-400 border-indigo-500/30 mb-1", children: "Corporate KPI" }), _jsx("h3", { className: "text-lg font-bold text-slate-100", children: g.corporate_kpi })] }), _jsxs(Badge, { variant: "success", children: ["Progress: ", g.current_progress_pct, "%"] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4 text-xs", children: [_jsxs("div", { className: "p-3 bg-slate-800/40 rounded border border-slate-700/50", children: [_jsx("span", { className: "font-semibold text-slate-400 uppercase", children: "Business Objective:" }), _jsx("p", { className: "text-slate-200 mt-1", children: g.business_goal })] }), _jsxs("div", { className: "p-3 bg-slate-800/40 rounded border border-slate-700/50", children: [_jsx("span", { className: "font-semibold text-slate-400 uppercase", children: "Department Target:" }), _jsx("p", { className: "text-slate-200 mt-1", children: g.department_goal })] })] }), _jsxs("div", { className: "pt-2 border-t border-slate-800 flex justify-between items-center text-xs text-slate-400", children: [_jsxs("span", { children: ["Assigned Agents: ", g.assigned_agents.join(', ')] }), _jsxs("span", { className: "text-emerald-400 font-semibold", children: ["Health: ", g.alignment_health] })] })] }, g.id))) })] }));
};
