import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Activity, Cpu } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { knowledgeApiClient } from '../../services/knowledgeApiClient';
export const KnowledgeQualityCenter = () => {
    const [report, setReport] = useState(null);
    const loadReport = async () => {
        const data = await knowledgeApiClient.getQualityReport();
        setReport(data);
    };
    useEffect(() => {
        loadReport();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Activity, { className: "w-7 h-7 text-emerald-400" }), "Knowledge Quality & Conflict Intelligence"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Detect policy discrepancies, outdated versions, duplicate documents, and evaluate reliability index." })] }), _jsx(Button, { variant: "intelligence", onClick: () => knowledgeApiClient.runOptimization(), children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Cpu, { className: "w-4 h-4" }), "Auto-Reconcile Conflicts"] }) })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: [_jsxs(Card, { className: "p-4 bg-slate-900/60 border-slate-800", children: [_jsx("span", { className: "text-xs text-slate-400 uppercase font-semibold", children: "Freshness Score" }), _jsxs("p", { className: "text-2xl font-bold text-emerald-400 mt-1", children: [((report?.freshness_index || 0.96) * 100).toFixed(0), "%"] })] }), _jsxs(Card, { className: "p-4 bg-slate-900/60 border-slate-800", children: [_jsx("span", { className: "text-xs text-slate-400 uppercase font-semibold", children: "Reliability Index" }), _jsxs("p", { className: "text-2xl font-bold text-cyan-400 mt-1", children: [((report?.avg_reliability_score || 0.95) * 100).toFixed(0), "%"] })] }), _jsxs(Card, { className: "p-4 bg-slate-900/60 border-slate-800", children: [_jsx("span", { className: "text-xs text-slate-400 uppercase font-semibold", children: "Active Conflicts" }), _jsx("p", { className: "text-2xl font-bold text-slate-100 mt-1", children: report?.active_conflicts.length || 0 })] })] }), _jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 space-y-4", children: [_jsx("h2", { className: "text-base font-semibold text-slate-200", children: "Policy Conflict Audit Log" }), report?.active_conflicts.length === 0 ? (_jsx("div", { className: "p-4 text-center text-sm text-emerald-400 bg-emerald-950/20 border border-emerald-500/30 rounded-lg", children: "\u2713 Zero policy conflicts or version discrepancies detected." })) : (report?.active_conflicts.map((conf) => (_jsxs("div", { className: "p-4 rounded-lg bg-amber-950/20 border border-amber-500/30 space-y-2", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsxs(Badge, { variant: "warning", children: [conf.severity, " SEVERITY"] }), _jsx("span", { className: "text-xs text-slate-400 font-mono", children: conf.id })] }), _jsx("p", { className: "text-sm font-semibold text-amber-200", children: conf.conflict_topic }), _jsx("p", { className: "text-xs text-slate-300", children: conf.recommended_resolution })] }, conf.id))))] })] }));
};
