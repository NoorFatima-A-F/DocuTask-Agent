import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { GitBranch, ShieldCheck, CheckCircle2, ArrowRight } from 'lucide-react';
const lineageHistory = [
    {
        hash: 'c8a1f492...e109',
        parentHash: 'b712c980...f881',
        timestamp: '2026-09-11T22:45:21Z',
        operation: 'FINAL_POSTERIOR_EVALUATION',
        formulaVersion: 'WeightedEnsemble (v1.3.0)',
        resultingScore: 98.42,
        evidenceCount: 14,
        verified: true,
    },
    {
        hash: 'b712c980...f881',
        parentHash: 'a90184aa...c234',
        timestamp: '2026-09-11T22:45:15Z',
        operation: 'INVARIANT_CHECK_UPDATE',
        formulaVersion: 'WeightedEnsemble (v1.3.0)',
        resultingScore: 97.50,
        evidenceCount: 11,
        verified: true,
    },
    {
        hash: 'a90184aa...c234',
        parentHash: 'f0023da9...8812',
        timestamp: '2026-09-11T22:45:08Z',
        operation: 'SCHEMA_EXTRACTION_UPDATE',
        formulaVersion: 'WeightedEnsemble (v1.3.0)',
        resultingScore: 94.20,
        evidenceCount: 8,
        verified: true,
    },
    {
        hash: 'f0023da9...8812',
        parentHash: null,
        timestamp: '2026-09-11T22:45:00Z',
        operation: 'PRIOR_INITIALIZATION',
        formulaVersion: 'WeightedEnsemble (v1.3.0)',
        resultingScore: 85.00,
        evidenceCount: 2,
        verified: true,
    },
];
export const ConfidenceLineageExplorer = () => {
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsx("div", { className: "space-y-1", children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-amber-500/20 to-orange-500/20 border border-amber-500/30 rounded-xl text-amber-400", children: _jsx(GitBranch, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Confidence Lineage & Provenance Chain", _jsx(Badge, { variant: "success", size: "sm", children: "Merkle Root Verified" })] }), _jsx("p", { className: "text-xs text-slate-400", children: "Cryptographically linked hash chains proving the exact computational history of every confidence metric." })] })] }) }), _jsx("div", { className: "flex items-center gap-3", children: _jsx(Badge, { variant: "outline", size: "sm", children: "Chain Length: 4 Blocks" }) })] }), _jsx("div", { className: "space-y-4", children: lineageHistory.map((node, idx) => (_jsx(Card, { className: "p-5 bg-[#0F172A] border-[#1E293B] hover:border-amber-500/40 transition-all font-mono", children: _jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4", children: [_jsxs("div", { className: "space-y-1.5", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsxs("span", { className: "text-amber-400 font-bold text-sm", children: ["#", lineageHistory.length - idx] }), _jsx("span", { className: "text-white font-bold text-sm", children: node.operation }), _jsx(Badge, { variant: "intelligence", size: "sm", children: node.formulaVersion })] }), _jsxs("div", { className: "flex flex-wrap items-center gap-3 text-xs text-slate-400", children: [_jsxs("span", { children: ["Current Hash: ", _jsx("span", { className: "text-slate-200 bg-slate-900 px-1.5 py-0.5 rounded border border-slate-700", children: node.hash })] }), node.parentHash && (_jsxs("span", { className: "flex items-center gap-1", children: [_jsx(ArrowRight, { className: "w-3 h-3 text-slate-500" }), "Parent: ", _jsx("span", { className: "text-slate-400 bg-slate-900 px-1.5 py-0.5 rounded border border-slate-800", children: node.parentHash })] }))] })] }), _jsxs("div", { className: "flex items-center gap-6", children: [_jsxs("div", { className: "text-right", children: [_jsxs("div", { className: "text-lg font-bold text-white", children: [node.resultingScore.toFixed(2), "%"] }), _jsxs("div", { className: "text-[11px] text-slate-400", children: [node.evidenceCount, " Evidences"] })] }), node.verified ? (_jsxs(Badge, { variant: "success", size: "sm", className: "flex items-center gap-1", children: [_jsx(CheckCircle2, { className: "w-3 h-3" }), "Verified"] })) : (_jsx(Badge, { variant: "warning", size: "sm", children: "Unverified" }))] })] }) }, node.hash))) }), _jsx(Card, { className: "p-4 bg-gradient-to-r from-amber-950/20 to-slate-900/60 border border-amber-500/30 flex items-center justify-between", children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(ShieldCheck, { className: "w-5 h-5 text-amber-400 shrink-0" }), _jsxs("div", { className: "text-xs text-slate-300", children: [_jsx("span", { className: "font-bold text-white", children: "Truth Ledger Seal: " }), "Root Hash ", _jsx("code", { className: "text-amber-300 bg-black/40 px-1 py-0.5 rounded", children: "sha256:c8a1f492e109..." }), " confirmed immutable in event store."] })] }) })] }));
};
