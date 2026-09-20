import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { HelpCircle, ShieldCheck } from 'lucide-react';
export const PlannerDecisionExplorerView = () => {
    const decisions = [
        {
            id: 'dec-p01-001',
            type: 'STRATEGY_SELECTION',
            title: 'Select Parallel DAG Strategy',
            reason: 'Document length exceeds single-batch latency SLA (30s) requiring parallel chunking',
            evidence: 'Input batch contains 4 high-resolution PDF pages with multi-column financial tables',
            chosen: 'Dynamic Parallel Chunking',
            confidence: '98.5%',
            truthHash: 'hash-dec-001-c8a1',
            offset: 1,
        },
        {
            id: 'dec-p01-002',
            type: 'WORKER_ALLOCATION',
            title: 'Assign Table Extraction to Worker OCR 02',
            reason: 'Worker 02 exhibits specialized bounding-box table recognition capability matrix',
            evidence: 'Capability score 0.985 vs generalist worker score 0.812',
            chosen: 'worker-ocr-02 (Table Specialist)',
            confidence: '98.5%',
            truthHash: 'hash-dec-002-d9b2',
            offset: 3,
        },
        {
            id: 'dec-p01-003',
            type: 'VALIDATION_CIRCUIT',
            title: 'Enforce Multi-Layer Invariant Check',
            reason: 'Invoice subtotal sum arithmetic must be verified before truth ledger commitment',
            evidence: 'Financial audit governance policy GOV-FIN-009 enforces 100% arithmetic certainty',
            chosen: 'Deterministic Invariant Proof',
            confidence: '99.9%',
            truthHash: 'hash-dec-003-e0c3',
            offset: 6,
        },
    ];
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsx("div", { className: "space-y-1", children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 rounded-xl text-indigo-400", children: _jsx(HelpCircle, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Planner Decision Cards & Proof Ledger", _jsx(Badge, { variant: "success", size: "sm", children: "Auditable" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] font-mono", children: "Inspect rationale, alternatives considered, confidence scores, and cryptographic truth proofs" })] })] }) }), _jsx(Badge, { variant: "intelligence", size: "md", children: "Phase 11 Truth Verified" })] }), _jsx("div", { className: "space-y-4 font-mono", children: decisions.map(d => (_jsxs(Card, { className: "p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] space-y-4", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-2 border-b border-[#1E293B] pb-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h3", { className: "text-sm font-bold text-white", children: d.title }), _jsx(Badge, { variant: "info", size: "sm", children: d.type })] }), _jsxs("span", { className: "text-[10px] text-[#64748B]", children: [d.id, " \u2022 Replay Offset #", d.offset] })] }), _jsxs(Badge, { variant: "intelligence", size: "sm", children: ["Confidence: ", d.confidence] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-3 text-xs", children: [_jsxs("div", { className: "p-3 bg-[#131D35] rounded-xl border border-[#1E293B] space-y-1", children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "PLANNER RATIONALE" }), _jsx("p", { className: "text-white text-[11px]", children: d.reason })] }), _jsxs("div", { className: "p-3 bg-[#131D35] rounded-xl border border-[#1E293B] space-y-1", children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "EVIDENCE OBSERVED" }), _jsx("p", { className: "text-[#94A3B8] text-[11px]", children: d.evidence })] })] }), _jsxs("div", { className: "flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-[#1E293B] text-xs", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-[#64748B]", children: "Chosen Action:" }), _jsx("strong", { className: "text-cyan-400", children: d.chosen })] }), _jsxs("div", { className: "flex items-center gap-2 text-[11px]", children: [_jsx(ShieldCheck, { className: "w-4 h-4 text-emerald-400" }), _jsx("span", { className: "text-emerald-400", children: d.truthHash })] })] })] }, d.id))) })] }));
};
