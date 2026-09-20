import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import { Scale, Lock, RefreshCw } from 'lucide-react';
export const PolicyAdministrationCenter = () => {
    const [policies, setPolicies] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        const load = async () => {
            setLoading(true);
            const list = await SaaSApiClient.listPolicies('tenant_acme_corp');
            setPolicies(list);
            setLoading(false);
        };
        load();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx(Scale, { className: "w-7 h-7 text-indigo-400" }), "Tenant Policy & RBAC/ABAC Engine"] }), _jsx("p", { className: "text-sm text-slate-400 mt-1", children: "Fine-grained authorization, geo-fencing constraints, role bindings, and spend cap rules." })] }) }), _jsxs(Card, { className: "bg-slate-900/80 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base text-white flex items-center gap-2", children: [_jsx(Lock, { className: "w-4 h-4 text-cyan-400" }), " Active Authorization Policies (", policies.length, ")"] }) }), _jsx(CardContent, { className: "space-y-3", children: loading ? (_jsxs("div", { className: "p-8 text-center text-slate-400", children: [_jsx(RefreshCw, { className: "w-6 h-6 animate-spin mx-auto mb-2" }), " Loading policies..."] })) : (policies.map((p) => (_jsxs("div", { className: "p-4 bg-slate-800/40 rounded border border-slate-700/50 flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-sm font-semibold text-white", children: p.policy_name }), _jsx(Badge, { variant: p.effect === 'ALLOW' ? 'success' : 'error', children: p.effect })] }), _jsxs("span", { className: "text-xs text-slate-400 block mt-1", children: ["Role: ", _jsx("span", { className: "text-slate-200 font-mono", children: p.subject_role }), " \u2022 Resource: ", _jsx("span", { className: "text-slate-200 font-mono", children: p.resource_type }), " \u2022 Action: ", _jsx("span", { className: "text-slate-200 font-mono", children: p.action })] })] }), _jsx("div", { className: "text-right text-xs text-slate-500 font-mono", children: p.policy_id })] }, p.policy_id)))) })] })] }));
};
