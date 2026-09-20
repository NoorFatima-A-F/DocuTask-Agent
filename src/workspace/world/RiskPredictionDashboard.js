import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AlertTriangle, ShieldAlert, ArrowRight, PlusCircle, } from 'lucide-react';
export const RiskPredictionDashboard = () => {
    const risks = [
        {
            id: 'risk-01',
            type: 'DEADLOCK_CASCADE',
            severity: 'MEDIUM',
            probability: 0.035,
            impactScore: 0.65,
            description: 'High burst ingestion (> 50 simultaneous PDF tasks) could saturate OCR worker thread pool.',
            affected: ['OCR_WORKER_POOL', 'APDLE_DAG_SCHEDULER'],
            mitigation: 'Enable dynamic DAG chunk fan-out and worker auto-scaling.',
        },
        {
            id: 'risk-02',
            type: 'RESOURCE_STARVATION',
            severity: 'LOW',
            probability: 0.012,
            impactScore: 0.40,
            description: 'Shared token cache memory limit reached after 10,000 unique document layouts.',
            affected: ['RUNTIME_MEMORY_CACHE'],
            mitigation: 'Activate LRU memory eviction policy on token embeddings.',
        },
        {
            id: 'risk-03',
            type: 'POLICY_BREACH_DRIFT',
            severity: 'LOW',
            probability: 0.005,
            impactScore: 0.20,
            description: 'Budget SLA threshold near limit during heavy multi-page financial ledger audits.',
            affected: ['BUDGET_GOVERNOR'],
            mitigation: 'Dynamic budget headroom allocation for verified enterprise tier users.',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Risk Prediction Dashboard" }), _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: true, children: "FAILURE FORECASTING ACTIVE" }), _jsx(Badge, { variant: "outline", size: "sm", children: "AWM-PSDTIP Phase 13.10" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Predictive modeling of deadlock cascades, resource starvation, policy breaches, and failure heatmaps before execution begins." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "intelligence", size: "sm", children: [_jsx(PlusCircle, { className: "w-3.5 h-3.5 mr-1.5" }), "Analyze New Risk"] }) })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 bg-emerald-950/10 border-emerald-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider", children: "Overall Platform Status" }), _jsx(ShieldAlert, { className: "w-4 h-4 text-emerald-400" })] }), _jsx("div", { className: "text-2xl font-bold font-mono text-emerald-400 mt-2", children: "STABLE" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Composite Risk Index: 0.045" })] }), _jsxs(Card, { className: "p-4 bg-amber-950/10 border-amber-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider", children: "Active Forecasted Risks" }), _jsx(AlertTriangle, { className: "w-4 h-4 text-amber-400" })] }), _jsxs("div", { className: "text-2xl font-bold font-mono text-amber-400 mt-2", children: [risks.length, " Monitored"] }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "0 Critical risks identified" })] }), _jsxs(Card, { className: "p-4 bg-purple-950/10 border-purple-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider", children: "Max Failure Probability" }), _jsx(AlertTriangle, { className: "w-4 h-4 text-purple-400" })] }), _jsx("div", { className: "text-2xl font-bold font-mono text-purple-400 mt-2", children: "3.5%" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "OCR pool burst load" })] }), _jsxs(Card, { className: "p-4 bg-blue-950/10 border-blue-500/20", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider", children: "Automated Mitigations" }), _jsx(ShieldAlert, { className: "w-4 h-4 text-blue-400" })] }), _jsx("div", { className: "text-2xl font-bold font-mono text-blue-400 mt-2", children: "100% Ready" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Pre-computed recovery paths" })] })] }), _jsx("div", { className: "space-y-4", children: risks.map((r) => (_jsxs(Card, { className: "p-5 border-border/40 space-y-3 hover:border-purple-500/30 transition-colors", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2", children: [_jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono font-bold text-foreground", children: r.id }), _jsx(Badge, { variant: r.severity === 'MEDIUM' ? 'warning' : 'default', size: "sm", children: r.severity }), _jsx("span", { className: "text-xs font-semibold text-purple-300", children: r.type.replace(/_/g, ' ') })] }), _jsx("p", { className: "text-xs text-muted-foreground", children: r.description })] }), _jsx("div", { className: "flex items-center gap-2 text-xs font-mono", children: _jsxs("span", { className: "text-muted-foreground", children: ["Probability: ", _jsxs("strong", { className: "text-foreground", children: [(r.probability * 100).toFixed(1), "%"] })] }) })] }), _jsxs("div", { className: "flex items-center gap-2 text-xs text-emerald-400 bg-emerald-950/20 p-2.5 rounded border border-emerald-500/30", children: [_jsx(ArrowRight, { className: "w-3.5 h-3.5 flex-shrink-0" }), _jsxs("span", { children: ["Mitigation Directive: ", r.mitigation] })] })] }, r.id))) })] }));
};
