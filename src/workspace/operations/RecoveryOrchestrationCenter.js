import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { RotateCcw, CheckCircle2, RefreshCw, Layers, Sparkles } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
export const RecoveryOrchestrationCenter = ({ missionId = 'mission-current', }) => {
    const [recoveries] = useState([
        {
            recoveryId: 'rec-chk-8b1a9c',
            missionId: missionId,
            strategy: 'CHECKPOINT_ROLLBACK',
            status: 'COMPLETED',
            restoredStep: 4,
            invariantsRestored: 12,
            elapsedMs: 180.0,
            timestamp: '2026-09-12T10:14:05Z',
        },
        {
            recoveryId: 'rec-opt-2f4e0d',
            missionId: 'mission-002',
            strategy: 'OPTIMIZATION_RETRY',
            status: 'COMPLETED',
            restoredStep: 1,
            invariantsRestored: 15,
            elapsedMs: 145.0,
            timestamp: '2026-09-12T09:30:12Z',
        },
    ]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(RotateCcw, { className: "w-5 h-5 text-indigo-400" }), "Recovery Orchestration & Mission Continuation Center"] }), _jsxs("p", { className: "text-sm text-slate-400", children: ["Multi-tier checkpoint restoration (Phase 13.4), policy rollback (Phase 13.5), dynamic re-optimization (Phase 13.6), and mission continuation for: ", _jsx("code", { className: "text-indigo-300 font-mono text-xs", children: missionId })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: "success", size: "md", children: "State Consistency: 100% VERIFIED" }), _jsxs("button", { className: "flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700", children: [_jsx(RefreshCw, { className: "w-3.5 h-3.5" }), "Scan Checkpoints"] })] })] }), _jsxs(Card, { className: "p-5 bg-slate-900 border-slate-800 space-y-4 font-mono", children: [_jsxs("h3", { className: "text-sm font-semibold text-slate-200 flex items-center gap-2", children: [_jsx(Layers, { className: "w-4 h-4 text-cyan-400" }), "Multi-Tier Recovery Orchestrator"] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-3 gap-3", children: [_jsxs("div", { className: "p-3.5 bg-slate-950 border border-slate-800 rounded-xl space-y-2", children: [_jsx("span", { className: "text-xs font-bold text-slate-200 block", children: "Tier 1: Checkpoint Snapshot" }), _jsx("p", { className: "text-[11px] text-slate-400", children: "Restores deterministic execution snapshot from Phase 13.4 timeline." }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Deterministic Restore" })] }), _jsxs("div", { className: "p-3.5 bg-slate-950 border border-slate-800 rounded-xl space-y-2", children: [_jsx("span", { className: "text-xs font-bold text-slate-200 block", children: "Tier 2: Policy Fallback" }), _jsx("p", { className: "text-[11px] text-slate-400", children: "Rolls back learned heuristics to safe baseline guardrails (Phase 13.5)." }), _jsx(Badge, { variant: "outline", size: "sm", children: "Policy Invariant" })] }), _jsxs("div", { className: "p-3.5 bg-slate-950 border border-slate-800 rounded-xl space-y-2", children: [_jsx("span", { className: "text-xs font-bold text-slate-200 block", children: "Tier 3: Dynamic Re-Optimization" }), _jsx("p", { className: "text-[11px] text-slate-400", children: "Re-solves Pareto frontier under degraded capacity (Phase 13.6)." }), _jsx(Badge, { variant: "success", size: "sm", children: "Pareto Frontier" })] })] })] }), _jsxs("div", { className: "space-y-3 font-mono", children: [_jsxs("h3", { className: "text-sm font-semibold text-slate-200 flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4 text-emerald-400" }), "Recent Mission Recovery Invocations"] }), recoveries.map((r) => (_jsxs(Card, { className: "p-4 bg-slate-900 border-slate-800 space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-bold text-indigo-400", children: r.recoveryId }), _jsx(Badge, { variant: "intelligence", size: "sm", children: r.strategy }), _jsxs("span", { className: "text-xs text-slate-300", children: ["Mission: ", r.missionId] })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Badge, { variant: "success", size: "sm", children: [_jsx(CheckCircle2, { className: "w-3 h-3 mr-1" }), r.status] }), _jsxs("span", { className: "text-xs text-slate-400", children: [r.elapsedMs, "ms"] })] })] }), _jsxs("div", { className: "grid grid-cols-3 gap-2 text-[11px] bg-slate-950 p-2.5 rounded border border-slate-800 text-slate-400", children: [_jsxs("span", { children: ["Restored Step: ", _jsx("strong", { className: "text-slate-200", children: r.restoredStep })] }), _jsxs("span", { children: ["Invariants Restored: ", _jsx("strong", { className: "text-emerald-400", children: r.invariantsRestored })] }), _jsxs("span", { children: ["Timestamp: ", _jsx("strong", { className: "text-slate-300", children: new Date(r.timestamp).toLocaleTimeString() })] })] })] }, r.recoveryId)))] })] }));
};
