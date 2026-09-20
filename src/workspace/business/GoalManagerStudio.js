import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Target, RefreshCw, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { BusinessApiClient } from '../../services/businessApiClient';
export const GoalManagerStudio = () => {
    const [goals, setGoals] = useState([]);
    const [loading, setLoading] = useState(true);
    const loadGoals = async () => {
        try {
            setLoading(true);
            const res = await BusinessApiClient.listGoals();
            setGoals(res);
        }
        catch (err) {
            console.error('Failed to load goals:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadGoals();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(Target, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "Business Goal & OKR Manager" }), _jsx("p", { className: "text-sm text-slate-400", children: "HTN goal decomposition, milestone tracking, and autonomous KPI alignment" })] })] }), _jsx(Button, { variant: "outline", onClick: loadGoals, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] }), _jsx("div", { className: "space-y-5", children: goals.map((g) => (_jsxs(Card, { className: "p-6 bg-slate-900/40 border-slate-800 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h2", { className: "text-base font-bold text-white", children: g.title }), _jsx(Badge, { variant: "intelligence", children: g.category })] }), _jsxs("span", { className: "text-xs text-slate-400 font-mono", children: ["Department: ", g.target_department, " | Aligned: ", g.aligned_process_ids.join(', ')] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsxs("span", { className: "text-sm font-bold text-emerald-400 font-mono", children: [g.progress_pct.toFixed(1), "%"] }), _jsx(Badge, { variant: g.status === 'ACHIEVED' ? 'success' : 'default', children: g.status })] })] }), _jsx("div", { className: "w-full bg-slate-800 h-2 rounded-full overflow-hidden", children: _jsx("div", { className: "bg-emerald-500 h-full rounded-full transition-all", style: { width: `${g.progress_pct}%` } }) }), _jsxs("div", { className: "space-y-2 pt-2", children: [_jsx("span", { className: "text-xs font-semibold text-slate-400 block", children: "Quantitative Key Results (KRs)" }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono", children: g.key_results.map((kr) => (_jsxs("div", { className: "p-3 bg-slate-800/40 rounded-xl border border-slate-700/60 flex items-center justify-between", children: [_jsxs("div", { children: [_jsx("span", { className: "font-sans text-slate-200 block text-xs font-medium", children: kr.description }), _jsxs("span", { className: "text-slate-400 text-[11px]", children: ["Target: ", kr.target_value, " ", kr.unit, " | Current: ", kr.current_value, " ", kr.unit] })] }), _jsx(Badge, { variant: kr.achieved ? 'success' : 'outline', children: kr.achieved ? 'Achieved' : 'In Progress' })] }, kr.kr_id))) })] })] }, g.goal_id))) })] }));
};
