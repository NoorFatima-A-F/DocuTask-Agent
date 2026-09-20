import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { ShieldCheck, Lock, UserCheck, } from 'lucide-react';
export const GovernanceApprovalCenter = () => {
    const approvals = [
        {
            id: 'appr-301',
            targetProposalId: 'pol-prop-701',
            proposalType: 'POLICY_UPGRADE',
            approverRole: 'EXECUTIVE_DIRECTOR',
            decision: 'APPROVED',
            rationale: 'Empirically proven via historical replay experiment with p < 0.001 and 44% latency reduction.',
            signature: '0x3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b',
            timestamp: '2026-09-12 09:30:15 UTC',
        },
        {
            id: 'appr-302',
            targetProposalId: 'arch-opt-601',
            proposalType: 'ARCHITECTURE_REFACTOR',
            approverRole: 'SECURITY_AUDITOR',
            decision: 'APPROVED',
            rationale: 'Multicast bus refactoring validated against chaos fault injection tests.',
            signature: '0x9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2e1f0d9c8b7a6e5f4d3c2b1a0f9e8d',
            timestamp: '2026-09-12 09:45:22 UTC',
        },
        {
            id: 'appr-303',
            targetProposalId: 'pol-prop-703',
            proposalType: 'SECURITY_QUORUM',
            approverRole: 'CHIEF_ARCHITECT',
            decision: 'PENDING',
            rationale: 'Pending second threshold cryptographic signature verification.',
            signature: '0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b',
            timestamp: '2026-09-12 10:05:00 UTC',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Governance Approval Center" }), _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: true, children: "DUAL-SIGNATURE THRESHOLD ACTIVE" }), _jsx(Badge, { variant: "outline", size: "sm", children: "AMRS-RSIP Phase 13.9" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Cryptographic digital signature verification, anti-usurpation guardrails, and audit ledger for autonomous platform mutations." })] }) }), _jsxs(Card, { className: "p-4 bg-purple-950/20 border-purple-500/30 flex flex-col sm:flex-row sm:items-center justify-between gap-3", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-purple-500/10 rounded-lg border border-purple-500/20 text-purple-400", children: _jsx(ShieldCheck, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsx("span", { className: "text-xs font-semibold text-purple-400 uppercase tracking-wider", children: "Anti-Usurpation Core Invariant" }), _jsx("div", { className: "text-xs text-foreground font-medium mt-0.5", children: "No autonomous policy or structural change may self-deploy without valid cryptographic multi-signature quorum." })] })] }), _jsx(Badge, { variant: "success", size: "sm", children: "Invariant 100% Intact" })] }), _jsx("div", { className: "space-y-4", children: approvals.map((appr) => (_jsxs(Card, { className: "p-5 border-border/40 space-y-3 hover:border-purple-500/30 transition-colors", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2", children: [_jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono font-bold text-foreground", children: appr.targetProposalId }), _jsx(Badge, { variant: appr.decision === 'APPROVED'
                                                        ? 'success'
                                                        : appr.decision === 'PENDING'
                                                            ? 'warning'
                                                            : 'error', size: "sm", children: appr.decision })] }), _jsx("span", { className: "text-xs text-purple-300 font-semibold", children: appr.proposalType })] }), _jsxs("div", { className: "flex items-center gap-2 text-xs font-mono text-muted-foreground", children: [_jsx(UserCheck, { className: "w-3.5 h-3.5 text-purple-400" }), _jsxs("span", { children: ["Approver: ", appr.approverRole] })] })] }), _jsx("p", { className: "text-xs text-muted-foreground", children: appr.rationale }), _jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between text-[11px] text-muted-foreground pt-3 border-t border-border/30 font-mono gap-2", children: [_jsxs("div", { className: "flex items-center gap-1.5 truncate max-w-md", children: [_jsx(Lock, { className: "w-3.5 h-3.5 text-purple-400 flex-shrink-0" }), _jsxs("span", { className: "truncate", children: ["Digital Signature: ", appr.signature] })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { children: appr.timestamp }), appr.decision === 'PENDING' && (_jsx(Button, { variant: "primary", size: "sm", children: "Sign & Authorize" }))] })] })] }, appr.id))) })] }));
};
