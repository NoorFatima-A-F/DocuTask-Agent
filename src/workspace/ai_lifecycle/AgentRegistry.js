import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import { Box, User, Tag, Calendar, RefreshCw } from 'lucide-react';
export const AgentRegistry = () => {
    const [agents, setAgents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filterCategory, setFilterCategory] = useState('ALL');
    useEffect(() => {
        const load = async () => {
            setLoading(true);
            const list = await AILifecycleApiClient.listAgents();
            setAgents(list);
            setLoading(false);
        };
        load();
    }, []);
    const filtered = filterCategory === 'ALL' ? agents : agents.filter((a) => a.category === filterCategory);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx(Box, { className: "w-7 h-7 text-indigo-400" }), "Enterprise Agent Registry & Asset Catalog"] }), _jsx("p", { className: "text-sm text-slate-400 mt-1", children: "Centralized inventory of all governed AI applications, owners, version tags, and lifecycle states." })] }), _jsx("div", { className: "flex gap-2", children: ['ALL', 'FINANCIAL_AUDIT', 'COMPLIANCE', 'LEGAL_ANALYSIS', 'AUTOMATION'].map((cat) => (_jsx("button", { onClick: () => setFilterCategory(cat), className: `px-3 py-1 text-xs rounded-lg border transition ${filterCategory === cat
                                ? 'bg-indigo-600 text-white border-indigo-500'
                                : 'bg-slate-800 text-slate-400 border-slate-700 hover:text-white'}`, children: cat }, cat))) })] }), loading ? (_jsxs("div", { className: "p-12 text-center text-slate-400", children: [_jsx(RefreshCw, { className: "w-6 h-6 animate-spin mx-auto mb-2" }), " Loading Registry..."] })) : (_jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6", children: filtered.map((agent) => (_jsxs(Card, { className: "bg-slate-900/80 border-slate-800 flex flex-col justify-between", children: [_jsxs(CardHeader, { children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx(Badge, { variant: "intelligence", children: agent.category }), _jsx(Badge, { variant: agent.lifecycle_state === 'DEPLOYED' ? 'success' : 'warning', children: agent.lifecycle_state })] }), _jsx(CardTitle, { className: "text-lg text-white", children: agent.name }), _jsx("span", { className: "text-xs font-mono text-slate-400", children: agent.agent_id })] }), _jsxs(CardContent, { className: "space-y-4", children: [_jsx("p", { className: "text-xs text-slate-300", children: agent.description }), _jsxs("div", { className: "grid grid-cols-2 gap-2 text-xs bg-slate-800/40 p-3 rounded border border-slate-700/50", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(User, { className: "w-4 h-4 text-indigo-400" }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-400 block text-[10px]", children: "Owner" }), _jsx("span", { className: "text-slate-200 font-medium truncate block", children: agent.owner_email })] })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Calendar, { className: "w-4 h-4 text-cyan-400" }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-400 block text-[10px]", children: "Version" }), _jsxs("span", { className: "text-slate-200 font-mono font-medium", children: ["v", agent.current_version] })] })] })] }), _jsx("div", { className: "flex flex-wrap gap-1.5 pt-2 border-t border-slate-800", children: agent.tags.map((t) => (_jsxs("span", { className: "text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded border border-slate-700 flex items-center gap-1", children: [_jsx(Tag, { className: "w-2.5 h-2.5" }), " ", t] }, t))) })] })] }, agent.agent_id))) }))] }));
};
