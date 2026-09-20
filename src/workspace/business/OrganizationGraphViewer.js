import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Users, RefreshCw, Building, Shield, Server, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { BusinessApiClient } from '../../services/businessApiClient';
export const OrganizationGraphViewer = () => {
    const [org, setOrg] = useState(null);
    const [loading, setLoading] = useState(true);
    const loadOrg = async () => {
        try {
            setLoading(true);
            const res = await BusinessApiClient.getOrganization();
            setOrg(res);
        }
        catch (err) {
            console.error('Failed to load organization graph:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadOrg();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(Users, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "Enterprise Knowledge Graph" }), _jsx("p", { className: "text-sm text-slate-400", children: "Departmental ontology, employee/agent role hierarchies, and approval matrices" })] })] }), _jsx(Button, { variant: "outline", onClick: loadOrg, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] }), _jsxs("div", { children: [_jsxs("h2", { className: "text-base font-semibold text-white mb-3 flex items-center gap-2", children: [_jsx(Building, { className: "w-4 h-4 text-indigo-400" }), "Enterprise Business Units & Departments"] }), _jsx("div", { className: "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4", children: org?.departments.map((d) => (_jsxs(Card, { className: "p-5 bg-slate-900/40 border-slate-800 space-y-3", children: [_jsxs("div", { className: "flex justify-between items-start", children: [_jsxs("div", { children: [_jsx("h3", { className: "font-bold text-white text-sm", children: d.name }), _jsxs("span", { className: "text-xs text-slate-400 font-mono", children: ["Head: ", d.head_role] })] }), _jsxs(Badge, { variant: "outline", children: [d.members_count, " Staff"] })] }), _jsxs("div", { className: "pt-2 border-t border-slate-800/80 text-xs text-slate-300 flex justify-between", children: [_jsx("span", { children: "Active Workflows:" }), _jsx("span", { className: "font-bold text-indigo-300 font-mono", children: d.active_processes_count })] })] }, d.department_id))) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-2 gap-6", children: [_jsxs(Card, { className: "p-6 bg-slate-900/40 border-slate-800 space-y-4", children: [_jsxs("h2", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Shield, { className: "w-4 h-4 text-emerald-400" }), "Roles, Delegations & Approval Limits"] }), _jsx("div", { className: "space-y-3 text-xs", children: org?.roles.map((r) => (_jsxs("div", { className: "p-3 bg-slate-800/40 rounded-xl border border-slate-700/60 flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-bold text-white text-xs", children: r.title }), _jsx(Badge, { variant: r.is_autonomous_agent ? 'intelligence' : 'default', children: r.is_autonomous_agent ? 'AI Agent' : 'Human' })] }), _jsxs("span", { className: "text-slate-400 text-[11px] block mt-0.5", children: ["Limit: $", r.approval_limit_amount.toLocaleString(), " USD"] })] }), _jsx("span", { className: "text-cyan-300 font-mono text-[11px]", children: r.department_id })] }, r.role_id))) })] }), _jsxs(Card, { className: "p-6 bg-slate-900/40 border-slate-800 space-y-4", children: [_jsxs("h2", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Server, { className: "w-4 h-4 text-cyan-400" }), "Connected Enterprise IT Systems"] }), _jsx("div", { className: "space-y-3 text-xs", children: org?.systems.map((s) => (_jsxs("div", { className: "p-3 bg-slate-800/40 rounded-xl border border-slate-700/60 flex items-center justify-between", children: [_jsxs("div", { children: [_jsx("span", { className: "font-bold text-white text-xs block", children: s.name }), _jsxs("span", { className: "text-slate-400 text-[11px]", children: ["Type: ", s.system_type] })] }), _jsx(Badge, { variant: "success", children: s.status })] }, s.system_id))) })] })] })] }));
};
