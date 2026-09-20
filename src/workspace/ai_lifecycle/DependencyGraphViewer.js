import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import { Network, CheckCircle2, RefreshCw } from 'lucide-react';
export const DependencyGraphViewer = () => {
    const [dependencies, setDependencies] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        const load = async () => {
            setLoading(true);
            const list = await AILifecycleApiClient.listDependencies('agt_acme_invoice_reconciler');
            setDependencies(list);
            setLoading(false);
        };
        load();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx(Network, { className: "w-7 h-7 text-indigo-400" }), "Agent Dependency DAG & Breaking Change Inspector"] }), _jsx("p", { className: "text-sm text-slate-400 mt-1", children: "Tracks relationships between agents, tools, models, connectors, datasets, and policies." })] }) }), _jsxs(Card, { className: "bg-slate-900/80 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsx(CardTitle, { className: "text-base text-white", children: "Dependency Graph for Autonomous Invoice Reconciler" }), _jsxs(Badge, { variant: "success", className: "flex items-center gap-1", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5" }), " No Breaking Changes"] })] }) }), _jsx(CardContent, { className: "space-y-3", children: loading ? (_jsxs("div", { className: "p-8 text-center text-slate-400", children: [_jsx(RefreshCw, { className: "w-6 h-6 animate-spin mx-auto mb-2" }), " Loading Dependency DAG..."] })) : (dependencies.map((dep) => (_jsxs("div", { className: "p-3 bg-slate-800/40 rounded border border-slate-700/50 flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "intelligence", children: dep.dependency_type }), _jsx("span", { className: "text-sm font-semibold text-white", children: dep.target_resource_name })] }), _jsx("span", { className: "text-xs text-slate-400 font-mono mt-1 block", children: dep.target_resource_id })] }), _jsx(Badge, { variant: dep.is_breaking_change ? 'error' : 'outline', children: dep.is_breaking_change ? 'BREAKING' : 'COMPATIBLE' })] }, dep.dep_id)))) })] })] }));
};
