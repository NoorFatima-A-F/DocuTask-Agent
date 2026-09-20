import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { ShieldCheck, Check, X, Clock, FileCheck } from 'lucide-react';
export const GovernanceApprovalWorkflow = () => {
    const [reviews, setReviews] = useState([
        {
            id: 'rev-001',
            candidateId: 'cand_b5e79b7c',
            policyName: 'High-Throughput Wavefront Partitioning Policy (v1.1.0)',
            target: 'planner',
            projectedGain: '+14.2% Throughput',
            riskScore: 0.12,
            riskTier: 'LOW',
            confidence: 96.5,
            guardrailsPassed: true,
            decision: 'APPROVED',
            reviewer: 'Governance Gatekeeper Engine',
            comments: 'All 100 counterfactual replay simulations passed with zero invariant regressions.',
            timestamp: '2026-09-12 00:15 UTC',
        },
        {
            id: 'rev-002',
            candidateId: 'cand_c8f12a9e',
            policyName: 'Aggressive Concurrency Booster Policy (16 Workers)',
            target: 'worker',
            projectedGain: '+38.5% Throughput',
            riskScore: 0.38,
            riskTier: 'MEDIUM',
            confidence: 89.2,
            guardrailsPassed: true,
            decision: 'PENDING_REVIEW',
            reviewer: 'Pending Human Operator Review',
            comments: 'Requires confirmation of downstream rate limit quotas before live activation.',
            timestamp: '2026-09-12 00:28 UTC',
        },
    ]);
    const handleAction = (id, action) => {
        setReviews((prev) => prev.map((r) => r.id === id
            ? {
                ...r,
                decision: action,
                reviewer: 'Admin User (Pair Programming Console)',
                comments: `Manually ${action.toLowerCase()} via governance workflow console.`,
            }
            : r));
    };
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-teal-500/20 to-emerald-500/20 border border-teal-500/30 rounded-xl text-teal-400", children: _jsx(ShieldCheck, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Governance & Safety Approval Workflow", _jsx(Badge, { variant: "intelligence", size: "sm", children: "Phase 13.5" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] font-mono", children: "Enforce multi-tier governance gates, guardrail validation bounds, and human-in-the-loop policy promotions" })] })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx(Badge, { variant: "success", size: "md", children: "100% Guardrail Enforced" }) })] }), _jsxs("div", { className: "space-y-4 font-mono", children: [_jsxs("h2", { className: "text-sm font-bold text-white flex items-center gap-2", children: [_jsx(FileCheck, { className: "w-4 h-4 text-indigo-400" }), "Candidate Policy Review Queue"] }), _jsx("div", { className: "grid grid-cols-1 gap-4", children: reviews.map((rev) => (_jsxs(Card, { className: "p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] space-y-4", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-3 border-b border-[#1E293B] pb-3", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("h3", { className: "text-sm font-bold text-white", children: rev.policyName }), _jsx(Badge, { variant: rev.decision === 'APPROVED' ? 'success' : rev.decision === 'REJECTED' ? 'error' : 'warning', size: "sm", children: rev.decision })] }), _jsxs("div", { className: "text-xs text-[#94A3B8] flex items-center gap-3", children: [_jsxs("span", { className: "flex items-center gap-1", children: [_jsx(Clock, { className: "w-3.5 h-3.5" }), " ", rev.timestamp] }), _jsxs("span", { children: ["ID: ", rev.candidateId] })] })] }), _jsxs("div", { className: "grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs", children: [_jsxs("div", { className: "p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl", children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "Projected Gain" }), _jsx("span", { className: "text-cyan-400 font-bold mt-0.5 block", children: rev.projectedGain })] }), _jsxs("div", { className: "p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl", children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "Risk Score" }), _jsxs("span", { className: `font-bold mt-0.5 block ${rev.riskScore < 0.2 ? 'text-emerald-400' : 'text-amber-400'}`, children: [rev.riskScore, " (", rev.riskTier, ")"] })] }), _jsxs("div", { className: "p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl", children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "Posterior Certainty" }), _jsxs("span", { className: "text-indigo-400 font-bold mt-0.5 block", children: [rev.confidence, "%"] })] }), _jsxs("div", { className: "p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl", children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "Safety Guardrails" }), _jsx("span", { className: "text-emerald-400 font-bold mt-0.5 block", children: "Zero Violations" })] })] }), _jsxs("div", { className: "p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl text-xs space-y-1", children: [_jsx("div", { className: "flex justify-between text-[#64748B] text-[10px]", children: _jsxs("span", { children: ["REVIEWER: ", rev.reviewer] }) }), _jsx("p", { className: "text-[#94A3B8]", children: rev.comments })] }), rev.decision === 'PENDING_REVIEW' && (_jsxs("div", { className: "flex items-center justify-end gap-3 pt-2", children: [_jsxs("button", { onClick: () => handleAction(rev.id, 'REJECTED'), className: "flex items-center gap-1.5 px-3 py-1.5 bg-red-500/20 hover:bg-red-500/30 text-red-300 border border-red-500/30 rounded-lg text-xs font-mono transition-colors", children: [_jsx(X, { className: "w-3.5 h-3.5" }), " Reject Policy"] }), _jsxs("button", { onClick: () => handleAction(rev.id, 'APPROVED'), className: "flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-mono font-bold transition-colors", children: [_jsx(Check, { className: "w-3.5 h-3.5" }), " Approve & Promote"] })] }))] }, rev.id))) })] })] }));
};
