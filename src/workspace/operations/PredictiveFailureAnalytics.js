import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { TrendingUp, BrainCircuit, RefreshCw, Cpu, DollarSign, Layers, Sparkles } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
export const PredictiveFailureAnalytics = ({ missionId = 'cluster-primary-master', }) => {
    const [predictions] = useState([
        {
            id: 'pred-cap-01',
            type: 'CAPACITY_EXHAUSTION',
            subsystem: 'WORKERS',
            probability: 0.75,
            timeToFailureSec: 140.0,
            severity: 'HIGH',
            recommendation: 'AUTO_SCALE_WORKER_POOL_OR_BURST_LOCAL_OCR',
            icon: _jsx(Cpu, { className: "w-4 h-4 text-cyan-400" }),
        },
        {
            id: 'pred-bdg-02',
            type: 'BUDGET_EXHAUSTION',
            subsystem: 'OPTIMIZATION',
            probability: 0.30,
            timeToFailureSec: 620.0,
            severity: 'MEDIUM',
            recommendation: 'SWITCH_TO_QUANTIZED_LOCAL_MODEL_TO_HALT_SPEND',
            icon: _jsx(DollarSign, { className: "w-4 h-4 text-emerald-400" }),
        },
        {
            id: 'pred-ret-03',
            type: 'RETRY_STORM',
            subsystem: 'API',
            probability: 0.15,
            timeToFailureSec: 180.0,
            severity: 'LOW',
            recommendation: 'ENGAGE_ADAPTIVE_EXPONENTIAL_BACKOFF_AND_CIRCUIT_BREAKER',
            icon: _jsx(TrendingUp, { className: "w-4 h-4 text-amber-400" }),
        },
        {
            id: 'pred-cnf-04',
            type: 'CONFIDENCE_COLLAPSE',
            subsystem: 'PLANNER',
            probability: 0.10,
            timeToFailureSec: 300.0,
            severity: 'LOW',
            recommendation: 'ESCALATE_TO_MULTI_AGENT_CONSENSUS_AND_SMT_SYMBOLIC_VERIFIER',
            icon: _jsx(BrainCircuit, { className: "w-4 h-4 text-purple-400" }),
        },
    ]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(BrainCircuit, { className: "w-5 h-5 text-indigo-400" }), "Predictive Failure Intelligence & Risk Analytics"] }), _jsxs("p", { className: "text-sm text-slate-400", children: ["Forecasting capacity exhaustion, budget overruns, retry storms, and confidence collapse prior to manifestation for: ", _jsx("code", { className: "text-indigo-300 font-mono text-xs", children: missionId })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: "intelligence", size: "md", children: "Composite Risk: 0.18 (LOW)" }), _jsxs("button", { className: "flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700", children: [_jsx(RefreshCw, { className: "w-3.5 h-3.5" }), "Recalculate Priors"] })] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4 font-mono", children: predictions.map((p) => (_jsxs(Card, { className: "p-5 bg-slate-900 border-slate-800 space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [p.icon, _jsx("span", { className: "text-xs font-bold text-slate-200", children: p.type })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: p.severity === 'HIGH' ? 'error' : p.severity === 'MEDIUM' ? 'warning' : 'default', size: "sm", children: p.severity }), _jsxs("span", { className: "text-xs font-bold text-indigo-400", children: [(p.probability * 100).toFixed(0), "% Prob"] })] })] }), _jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex justify-between text-xs text-slate-400", children: [_jsx("span", { children: "Estimated Time to Failure:" }), _jsxs("span", { className: "text-amber-400 font-bold", children: [p.timeToFailureSec, " sec"] })] }), _jsx("div", { className: "w-full bg-slate-950 h-1.5 rounded-full overflow-hidden", children: _jsx("div", { className: `h-full rounded-full ${p.probability > 0.6 ? 'bg-rose-500' : p.probability > 0.3 ? 'bg-amber-500' : 'bg-emerald-500'}`, style: { width: `${p.probability * 100}%` } }) })] }), _jsxs("div", { className: "pt-2 border-t border-slate-800 text-[11px] text-slate-400", children: [_jsx("span", { className: "text-slate-500 block text-[10px]", children: "PREVENTATIVE ACTION:" }), _jsxs("span", { className: "text-emerald-400 font-bold flex items-center gap-1 mt-0.5", children: [_jsx(Sparkles, { className: "w-3 h-3" }), p.recommendation] })] })] }, p.id))) }), _jsxs(Card, { className: "p-5 bg-slate-900 border-slate-800 space-y-3 font-mono", children: [_jsxs("h3", { className: "text-sm font-semibold text-slate-200 flex items-center gap-2", children: [_jsx(Layers, { className: "w-4 h-4 text-purple-400" }), "Aggregate Risk Exposure & SLA Breach Horizon"] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-3 text-xs", children: [_jsxs("div", { className: "p-3.5 bg-slate-950 rounded-lg border border-slate-800", children: [_jsx("span", { className: "text-slate-400 block mb-1", children: "Financial Exposure (24h)" }), _jsx("span", { className: "text-lg font-bold text-emerald-400", children: "$0.00 USD" })] }), _jsxs("div", { className: "p-3.5 bg-slate-950 rounded-lg border border-slate-800", children: [_jsx("span", { className: "text-slate-400 block mb-1", children: "SLA Breach Probability" }), _jsx("span", { className: "text-lg font-bold text-cyan-400", children: "0.01%" })] }), _jsxs("div", { className: "p-3.5 bg-slate-950 rounded-lg border border-slate-800", children: [_jsx("span", { className: "text-slate-400 block mb-1", children: "Preemptive Actions Armed" }), _jsx("span", { className: "text-lg font-bold text-indigo-400", children: "4 Autonomic Handlers" })] })] })] })] }));
};
