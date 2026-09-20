import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Zap, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { cognitiveApiClient } from '../../services/cognitiveApiClient';
export const AutonomousOptimizationCenter = () => {
    const [opportunities, setOpportunities] = useState([]);
    const loadData = async () => {
        const data = await cognitiveApiClient.listOptimizations();
        setOpportunities(data);
    };
    useEffect(() => {
        loadData();
    }, []);
    const handleApply = async (id) => {
        await cognitiveApiClient.applyOptimization(id);
        await loadData();
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Zap, { className: "w-7 h-7 text-indigo-400" }), "Autonomous Optimization Center"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Continuous auto-tuning of model routing, prompt templates, concurrency pools, and embedding caches." })] }), _jsx(Button, { variant: "outline", onClick: loadData, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: "w-4 h-4" }), "Refresh"] }) })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: opportunities.map((opt) => (_jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 space-y-3", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsx(Badge, { variant: "outline", className: "text-indigo-400 border-indigo-500/30", children: opt.subsystem }), _jsx(Badge, { variant: opt.status === 'APPLIED' ? 'success' : 'info', children: opt.status })] }), _jsx("h3", { className: "text-base font-semibold text-slate-200", children: opt.recommended_change }), _jsxs("div", { className: "p-3 bg-slate-800/40 rounded border border-slate-700/60 flex justify-between items-center text-xs", children: [_jsxs("span", { className: "text-slate-400", children: ["Target: ", opt.target_resource] }), _jsxs("span", { className: "text-emerald-400 font-mono font-bold", children: ["+$", opt.projected_savings_monthly_usd, "/mo savings"] })] }), _jsx("div", { className: "pt-2 flex justify-end", children: _jsx(Button, { variant: "intelligence", size: "sm", disabled: opt.status === 'APPLIED', onClick: () => handleApply(opt.id), children: opt.status === 'APPLIED' ? 'Applied' : 'Execute Auto-Tune' }) })] }, opt.id))) })] }));
};
