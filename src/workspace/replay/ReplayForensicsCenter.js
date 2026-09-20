import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { ShieldAlert, ArrowRight, Search, CheckCircle2 } from 'lucide-react';
export const ReplayForensicsCenter = () => {
    const findings = [
        {
            id: 'F-001',
            category: 'RECOVERY_TRIGGER',
            severity: 'WARNING',
            event: 'worker.step.retry',
            description: 'OCR scan contrast below threshold on page 2. Activated contrast auto-normalization recovery sub-graph.',
            causalChain: ['evt_004 (worker.started)', 'evt_005 (quality.checked)', 'evt_006 (worker.step.retry)'],
            remedy: 'Contrast equalization succeeded; nominal extraction continued.',
        },
        {
            id: 'F-002',
            category: 'CONFIDENCE_DRIFT',
            severity: 'INFO',
            event: 'confidence.evaluated',
            description: 'Epistemic uncertainty decreased by 0.014 following invariant verification satisfaction.',
            causalChain: ['evt_007 (confidence.evaluated)', 'evt_008 (truth.invariant.checked)'],
            remedy: 'Posterior belief updated to 98.42%.',
        },
    ];
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsx("div", { className: "space-y-1", children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-amber-500/20 to-red-500/20 border border-amber-500/30 rounded-xl text-amber-400", children: _jsx(ShieldAlert, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Replay Forensics & Root-Cause Center", _jsx(Badge, { variant: "warning", size: "sm", children: "Automated Causal Backtracking" })] }), _jsx("p", { className: "text-xs text-slate-400", children: "Post-mortem causal analysis, failure chain reconstruction, and anomaly attribution across mission lifecycles." })] })] }) }), _jsx("div", { className: "flex items-center gap-3", children: _jsx(Badge, { variant: "success", size: "sm", children: "0 Invariant Violations" }) })] }), _jsx("div", { className: "space-y-4 font-mono text-xs", children: findings.map((f) => (_jsxs(Card, { className: "p-5 bg-[#0F172A] border-[#1E293B] space-y-3", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("span", { className: "font-bold text-amber-400", children: f.id }), _jsx("span", { className: "font-bold text-white text-sm", children: f.category }), _jsx(Badge, { variant: "warning", size: "sm", children: f.severity })] }), _jsx(Badge, { variant: "outline", size: "sm", children: f.event })] }), _jsx("p", { className: "text-slate-300 text-xs", children: f.description }), _jsxs("div", { className: "p-3 bg-slate-900/60 rounded-lg border border-slate-800 space-y-1.5", children: [_jsxs("div", { className: "text-[11px] font-bold text-slate-400 flex items-center gap-1.5", children: [_jsx(Search, { className: "w-3.5 h-3.5 text-cyan-400" }), " Causal Dependency Chain:"] }), _jsx("div", { className: "flex flex-wrap items-center gap-2 text-slate-300", children: f.causalChain.map((step, idx) => (_jsxs(React.Fragment, { children: [_jsx("span", { className: "bg-slate-800 px-2 py-0.5 rounded text-cyan-300", children: step }), idx < f.causalChain.length - 1 && _jsx(ArrowRight, { className: "w-3 h-3 text-slate-500" })] }, idx))) })] }), _jsxs("div", { className: "flex items-center gap-2 text-emerald-400 text-[11px]", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5 shrink-0" }), _jsxs("span", { children: ["Attribution: ", f.remedy] })] })] }, f.id))) })] }));
};
