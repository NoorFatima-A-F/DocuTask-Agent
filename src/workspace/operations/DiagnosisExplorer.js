import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Compass, CheckCircle2, RefreshCw, Zap, HelpCircle } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
export const DiagnosisExplorer = ({ missionId = 'inc-9b2f1a', }) => {
    const [activeDiagnosis] = useState({
        diagnosisId: 'diag-4a1d8e',
        incidentId: missionId,
        primaryCulprit: 'WORKERS',
        errorPattern: 'WORKER_CRASH',
        confidence: 0.965,
        recommendedAction: 'WORKER_RESTART',
        summary: 'Root cause identified in [WORKERS] (WORKER_CRASH) causing downstream degradation in 2 subsystems.',
        causalChain: [
            'Anomaly originated in [WORKERS] characterized by unhandled OCR segfault in thread #4.',
            'Degradation propagated downstream from [WORKERS] to [PLANNER] queue listener.',
            'Cascading failure bounded; autonomous healing isolation engaged for [WORKERS].',
        ],
        evidenceSources: ['EventStore', 'ReplayEngine', 'RuntimeTelemetry', 'TruthLedger'],
    });
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Compass, { className: "w-5 h-5 text-indigo-400" }), "Autonomous Diagnosis & Explainable Root-Cause Explorer"] }), _jsxs("p", { className: "text-sm text-slate-400", children: ["Multi-source causal reasoning, failure propagation topology, and diagnostic confidence proofs for: ", _jsx("code", { className: "text-indigo-300 font-mono text-xs", children: activeDiagnosis.incidentId })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsxs(Badge, { variant: "intelligence", size: "md", children: ["Diagnosis Confidence: ", (activeDiagnosis.confidence * 100).toFixed(1), "%"] }), _jsxs("button", { className: "flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700", children: [_jsx(RefreshCw, { className: "w-3.5 h-3.5" }), "Re-infer Root Cause"] })] })] }), _jsxs(Card, { className: "p-5 bg-slate-900 border-slate-800 space-y-4 font-mono", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "PRIMARY ROOT CAUSE CULPRIT" }), _jsxs("span", { className: "text-lg font-bold text-rose-400 mt-0.5 block", children: [activeDiagnosis.primaryCulprit, " (", activeDiagnosis.errorPattern, ")"] })] }), _jsxs("div", { className: "text-right", children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "RECOMMENDED REMEDIATION" }), _jsxs("span", { className: "text-sm font-bold text-emerald-400 flex items-center gap-1 justify-end mt-0.5", children: [_jsx(Zap, { className: "w-3.5 h-3.5" }), activeDiagnosis.recommendedAction] })] })] }), _jsx("p", { className: "text-xs text-slate-300 leading-relaxed", children: activeDiagnosis.summary }), _jsxs("div", { className: "flex items-center gap-2 pt-2 border-t border-slate-800 text-xs", children: [_jsx("span", { className: "text-slate-400", children: "Verified Evidence Sources:" }), activeDiagnosis.evidenceSources.map((src, idx) => (_jsxs(Badge, { variant: "outline", size: "sm", children: [_jsx(CheckCircle2, { className: "w-3 h-3 text-emerald-400 mr-1" }), src] }, idx)))] })] }), _jsxs(Card, { className: "p-5 bg-slate-900 border-slate-800 space-y-4 font-mono", children: [_jsxs("h3", { className: "text-sm font-semibold text-slate-200 flex items-center gap-2", children: [_jsx(HelpCircle, { className: "w-4 h-4 text-cyan-400" }), "Explainable Causal Failure Propagation Chain"] }), _jsx("div", { className: "space-y-3", children: activeDiagnosis.causalChain.map((step, idx) => (_jsxs("div", { className: "p-3.5 rounded-lg bg-slate-950 border border-slate-800 flex items-start gap-3", children: [_jsxs("div", { className: "p-1.5 rounded-md bg-indigo-950/60 border border-indigo-500/30 text-indigo-400 text-xs font-bold mt-0.5", children: ["0", idx + 1] }), _jsx("div", { className: "space-y-1 text-xs", children: _jsx("span", { className: "text-slate-200 font-semibold", children: step }) })] }, idx))) })] })] }));
};
