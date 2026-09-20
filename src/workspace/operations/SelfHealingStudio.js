import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Zap, CheckCircle2, RefreshCw, Lock, RotateCcw, Sparkles } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
export const SelfHealingStudio = ({ missionId = 'cluster-primary-master', }) => {
    const [healingHistory] = useState([
        {
            healingId: 'heal-7c2a1e',
            incidentId: 'inc-9b2f1a',
            actionType: 'WORKER_RESTART',
            target: 'worker-th-04',
            status: 'COMPLETED',
            executionTimeMs: 120.0,
            validationPassed: true,
            auditHash: 'a7162acf5f9c4f74d081c70e28d4ec0cf4bf49f0ec1fc93ff06460395fa3fa74',
            timestamp: '10:14:02 UTC',
        },
        {
            healingId: 'heal-1e8d9c',
            incidentId: 'inc-3e7c8d',
            actionType: 'FALLBACK_MODEL_ENGAGE',
            target: 'gemini-1.5-pro',
            status: 'COMPLETED',
            executionTimeMs: 75.0,
            validationPassed: true,
            auditHash: '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b',
            timestamp: '09:42:16 UTC',
        },
    ]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Zap, { className: "w-5 h-5 text-emerald-400" }), "Autonomous Self-Healing Studio & Actuation Center"] }), _jsxs("p", { className: "text-sm text-slate-400", children: ["Real-time execution of automated worker restarts, planner rollbacks, dynamic resource reallocation, and cryptographic audit proofs for: ", _jsx("code", { className: "text-emerald-300 font-mono text-xs", children: missionId })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: "success", size: "md", children: "Healing Efficacy: 100%" }), _jsxs("button", { className: "flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700", children: [_jsx(RefreshCw, { className: "w-3.5 h-3.5" }), "Sync Ledger"] })] })] }), _jsxs(Card, { className: "p-5 bg-slate-900 border-slate-800 space-y-4 font-mono", children: [_jsxs("h3", { className: "text-sm font-semibold text-slate-200 flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4 text-indigo-400" }), "Autonomous Remediation Actions"] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-3 gap-3", children: [_jsxs("button", { className: "p-3.5 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-xl text-left space-y-1 transition-all", children: [_jsxs("span", { className: "text-xs font-bold text-slate-200 block flex items-center gap-1.5", children: [_jsx(RotateCcw, { className: "w-3.5 h-3.5 text-emerald-400" }), " Restart Worker Pool"] }), _jsx("span", { className: "text-[11px] text-slate-400 block", children: "Restarts unpinned async threads" })] }), _jsxs("button", { className: "p-3.5 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-xl text-left space-y-1 transition-all", children: [_jsxs("span", { className: "text-xs font-bold text-slate-200 block flex items-center gap-1.5", children: [_jsx(Zap, { className: "w-3.5 h-3.5 text-amber-400" }), " Reallocate Concurrency"] }), _jsx("span", { className: "text-[11px] text-slate-400 block", children: "Dynamically scales worker slots" })] }), _jsxs("button", { className: "p-3.5 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-xl text-left space-y-1 transition-all", children: [_jsxs("span", { className: "text-xs font-bold text-slate-200 block flex items-center gap-1.5", children: [_jsx(Lock, { className: "w-3.5 h-3.5 text-indigo-400" }), " Repair Vector Cache"] }), _jsx("span", { className: "text-[11px] text-slate-400 block", children: "Evicts stale memory partitions" })] })] })] }), _jsxs("div", { className: "space-y-3 font-mono", children: [_jsxs("h3", { className: "text-sm font-semibold text-slate-200 flex items-center gap-2", children: [_jsx(Lock, { className: "w-4 h-4 text-purple-400" }), "Cryptographic SHA-256 Self-Healing Audit Ledger"] }), healingHistory.map((h) => (_jsxs(Card, { className: "p-4 bg-slate-900 border-slate-800 space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: h.actionType }), _jsxs("span", { className: "text-xs font-bold text-slate-200", children: ["Target: ", h.target] })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Badge, { variant: "success", size: "sm", children: [_jsx(CheckCircle2, { className: "w-3 h-3 mr-1" }), h.status] }), _jsxs("span", { className: "text-xs text-slate-400", children: [h.executionTimeMs, "ms"] })] })] }), _jsxs("div", { className: "flex items-center justify-between text-[11px] bg-slate-950 p-2.5 rounded border border-slate-800 text-slate-400", children: [_jsxs("span", { children: ["SHA-256 Audit: ", _jsx("code", { className: "text-indigo-300 font-bold truncate", children: h.auditHash })] }), _jsx("span", { children: h.timestamp })] })] }, h.healingId)))] })] }));
};
