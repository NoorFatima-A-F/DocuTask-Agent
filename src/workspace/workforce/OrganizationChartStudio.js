import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { workforceApiClient } from '../../services/workforceApiClient';
import { Layers, RefreshCw } from 'lucide-react';
export const OrganizationChartStudio = () => {
    const [departments, setDepartments] = useState([]);
    const [loading, setLoading] = useState(false);
    const loadData = async () => {
        setLoading(true);
        try {
            const depts = await workforceApiClient.getDepartments();
            setDepartments(depts);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadData();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex justify-between items-center bg-slate-900/60 p-5 rounded-2xl border border-slate-800", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx("span", { className: "p-2 bg-emerald-500/20 text-emerald-400 rounded-xl", children: "\uD83C\uDF33" }), "Organization Chart Studio"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Hierarchical Reporting Trees, Matrix Units, and Reporting Lines" })] }), _jsx(Button, { variant: "outline", onClick: loadData, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh Hierarchy"] }) })] }), _jsx("div", { className: "flex justify-center", children: _jsxs(Card, { className: "p-6 bg-indigo-950/40 border-indigo-500/50 max-w-md w-full text-center relative shadow-lg shadow-indigo-500/10", children: [_jsx(Badge, { variant: "default", className: "mb-2", children: "CHIEF EXECUTIVE OFFICER" }), _jsx("div", { className: "text-lg font-bold text-white", children: "Astraea Core (CEO)" }), _jsx("p", { className: "text-xs text-indigo-300 mt-1", children: "Master Autonomous Orchestration & Governance" }), _jsx("div", { className: "mt-3 text-[11px] text-slate-400", children: "Clearance: TOP_SECRET \u2022 Trust: 0.99" })] }) }), _jsx("div", { className: "flex justify-center my-2", children: _jsx("div", { className: "w-0.5 h-8 bg-slate-700" }) }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-6", children: departments.map((d) => (_jsxs(Card, { className: "p-5 bg-slate-900/50 border-slate-800", children: [_jsxs("div", { className: "flex justify-between items-start mb-3", children: [_jsx("div", { className: "text-base font-bold text-white", children: d.name }), _jsx(Badge, { variant: "outline", children: d.dept_type })] }), _jsxs("div", { className: "text-xs text-slate-400 space-y-2 mb-4", children: [_jsxs("div", { className: "flex justify-between", children: [_jsx("span", { children: "Headcount:" }), _jsxs("strong", { className: "text-white", children: [d.headcount, " Agents"] })] }), _jsxs("div", { className: "flex justify-between", children: [_jsx("span", { children: "Monthly Budget:" }), _jsxs("strong", { className: "text-emerald-400", children: ["$", d.monthly_budget_usd.toLocaleString()] })] })] }), _jsxs("div", { className: "border-t border-slate-800 pt-3", children: [_jsxs("div", { className: "text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5", children: [_jsx(Layers, { className: "w-3.5 h-3.5 text-indigo-400" }), " Active OKRs"] }), _jsx("ul", { className: "space-y-1", children: d.okrs.map((okr, idx) => (_jsxs("li", { className: "text-xs text-slate-300 flex items-center gap-2", children: [_jsx("span", { className: "text-emerald-400", children: "\u2713" }), " ", okr] }, idx))) })] })] }, d.id))) })] }));
};
