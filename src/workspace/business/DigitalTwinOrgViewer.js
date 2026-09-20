import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Globe, RefreshCw, Activity, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { BusinessApiClient } from '../../services/businessApiClient';
export const DigitalTwinOrgViewer = () => {
    const [dto, setDto] = useState(null);
    const [loading, setLoading] = useState(true);
    const loadDto = async () => {
        try {
            setLoading(true);
            const res = await BusinessApiClient.getDigitalTwin();
            setDto(res);
        }
        catch (err) {
            console.error('Failed to load digital twin:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadDto();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(Globe, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "Digital Twin of the Organization (DTO)" }), _jsx("p", { className: "text-sm text-slate-400", children: "Live synchronized simulation model of enterprise departments, worker load & operational capacity" })] })] }), _jsx(Button, { variant: "outline", onClick: loadDto, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Sync Digital Twin"] }) })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-5 bg-slate-900/50 border-slate-800", children: [_jsx("span", { className: "text-xs text-slate-400 block mb-1", children: "Human Workforce" }), _jsxs("div", { className: "flex items-baseline gap-2", children: [_jsx("span", { className: "text-2xl font-bold text-white", children: dto?.active_human_workers ?? 90 }), _jsx("span", { className: "text-xs text-slate-400", children: "Employees" })] })] }), _jsxs(Card, { className: "p-5 bg-slate-900/50 border-slate-800", children: [_jsx("span", { className: "text-xs text-slate-400 block mb-1", children: "Autonomous Agent Fleet" }), _jsxs("div", { className: "flex items-baseline gap-2", children: [_jsx("span", { className: "text-2xl font-bold text-indigo-400", children: dto?.active_agent_workers ?? 24 }), _jsx("span", { className: "text-xs text-slate-400", children: "AI Agents" })] })] }), _jsxs(Card, { className: "p-5 bg-slate-900/50 border-slate-800", children: [_jsx("span", { className: "text-xs text-slate-400 block mb-1", children: "Active Sagas" }), _jsxs("div", { className: "flex items-baseline gap-2", children: [_jsx("span", { className: "text-2xl font-bold text-white", children: dto?.running_business_processes ?? 8 }), _jsx("span", { className: "text-xs text-slate-400", children: "Workflows" })] })] }), _jsxs(Card, { className: "p-5 bg-slate-900/50 border-slate-800", children: [_jsx("span", { className: "text-xs text-slate-400 block mb-1", children: "Mean Org SLA Compliance" }), _jsxs("div", { className: "flex items-baseline gap-2", children: [_jsxs("span", { className: "text-2xl font-bold text-emerald-400", children: [dto?.mean_org_sla_compliance_pct?.toFixed(1) ?? '99.2', "%"] }), _jsx(Badge, { variant: "success", children: "Optimal" })] })] })] }), _jsxs(Card, { className: "p-6 bg-slate-900/40 border-slate-800 space-y-4", children: [_jsxs("h2", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Activity, { className: "w-4 h-4 text-emerald-400" }), "Departmental Workload & Operational Capacity Heatmap"] }), _jsx("div", { className: "space-y-4 pt-2", children: Object.entries(dto?.department_workloads || {}).map(([dept, load]) => (_jsxs("div", { className: "space-y-1 text-xs", children: [_jsxs("div", { className: "flex justify-between", children: [_jsx("span", { className: "font-mono font-bold text-white uppercase", children: dept.replace('dept_', '') }), _jsxs("span", { className: "font-mono text-indigo-300", children: [load.toFixed(1), "% Load"] })] }), _jsx("div", { className: "w-full bg-slate-800 h-2.5 rounded-full overflow-hidden", children: _jsx("div", { className: `h-full rounded-full transition-all ${load > 80 ? 'bg-amber-500' : 'bg-indigo-500'}`, style: { width: `${load}%` } }) })] }, dept))) })] })] }));
};
