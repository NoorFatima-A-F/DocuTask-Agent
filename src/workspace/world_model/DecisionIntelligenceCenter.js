import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 10: Decision Intelligence Center
 */
import { useEffect, useState } from 'react';
import { CheckCircle2, RefreshCw, Briefcase, Zap, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
export const DecisionIntelligenceCenter = () => {
    const [options, setOptions] = useState([]);
    const [portfolios, setPortfolios] = useState([]);
    const [loading, setLoading] = useState(true);
    const fetchDecisions = async () => {
        setLoading(true);
        try {
            const res = await WorldModelApiClient.getDecisions();
            setOptions(res.options || []);
            setPortfolios(res.portfolios || []);
        }
        catch (err) {
            console.error('Error fetching decisions:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        fetchDecisions();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 border border-emerald-500/30 rounded-xl p-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-emerald-400", children: _jsx(CheckCircle2, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold text-white tracking-tight", children: "Decision Intelligence Center" }), _jsx(Badge, { variant: "intelligence", children: "Expected Utility Optimization" })] }), _jsx("p", { className: "text-sm text-slate-400", children: "Evaluates candidate actions against probabilistic world states, ranking options by multi-objective Expected Utility." })] })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsx(Button, { variant: "outline", onClick: fetchDecisions, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }) })] }), _jsxs("div", { className: "space-y-4", children: [_jsxs("h3", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Briefcase, { className: "w-5 h-5 text-emerald-400" }), "Recommended Decision Portfolios"] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: portfolios.map((port) => (_jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-5 space-y-4", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx("span", { className: "text-xs font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-500/30", children: port.portfolio_id }), _jsx("h4", { className: "text-base font-bold text-white mt-1", children: port.objective })] }), _jsxs(Badge, { variant: "success", children: ["Utility: ", port.aggregate_utility] })] }), _jsxs("div", { className: "grid grid-cols-2 gap-2 text-xs", children: [_jsxs("div", { className: "p-2.5 bg-slate-950/80 rounded border border-slate-800", children: [_jsx("span", { className: "text-slate-400 block text-[10px] uppercase", children: "Risk Profile" }), _jsx("span", { className: "text-emerald-300 font-semibold uppercase", children: port.risk_profile })] }), _jsxs("div", { className: "p-2.5 bg-slate-950/80 rounded border border-slate-800", children: [_jsx("span", { className: "text-slate-400 block text-[10px] uppercase", children: "Estimated Cost" }), _jsxs("span", { className: "text-white font-mono font-bold", children: ["$", port.total_cost, "k/mo"] })] })] })] }, port.portfolio_id))) })] }), _jsxs("div", { className: "space-y-4", children: [_jsxs("h3", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Zap, { className: "w-5 h-5 text-emerald-400" }), "Evaluated Candidate Decisions"] }), _jsx("div", { className: "space-y-3", children: options.map((opt) => (_jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-5 space-y-3 hover:border-emerald-500/40 transition-all", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-500/30", children: opt.option_id }), _jsx(Badge, { variant: "intelligence", children: opt.risk_profile })] }), _jsx("h4", { className: "text-base font-bold text-white mt-1.5", children: opt.title })] }), _jsxs("div", { className: "text-right", children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "Expected Utility" }), _jsx("span", { className: "text-lg font-bold text-emerald-400", children: opt.expected_utility })] })] }), _jsx("p", { className: "text-sm text-slate-300", children: opt.description }), _jsxs("div", { className: "grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs pt-1", children: [_jsxs("div", { className: "p-2 bg-slate-950/80 rounded border border-slate-800", children: [_jsx("span", { className: "text-slate-400 block text-[10px]", children: "Cost" }), _jsxs("span", { className: "text-white font-bold font-mono", children: ["$", opt.cost, "k"] })] }), _jsxs("div", { className: "p-2 bg-slate-950/80 rounded border border-slate-800", children: [_jsx("span", { className: "text-slate-400 block text-[10px]", children: "Time Horizon" }), _jsx("span", { className: "text-slate-200 font-mono", children: opt.time_horizon_seconds ? `${opt.time_horizon_seconds / 3600}h` : '4h' })] }), _jsxs("div", { className: "p-2 bg-slate-950/80 rounded border border-slate-800 col-span-2", children: [_jsx("span", { className: "text-slate-400 block text-[10px]", children: "Actions Enqueued" }), _jsx("span", { className: "text-emerald-300 font-mono text-[11px] truncate block", children: JSON.stringify(opt.actions || []) })] })] })] }, opt.option_id))) })] })] }));
};
