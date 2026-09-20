import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const GovernanceApprovalCenterView = () => {
    const approvalStages = [
        {
            stage: 'STAGE 1: Automated Test & Invariant Verification',
            status: 'PASSED',
            approver: 'CI/CD Automated Daemon',
            timestamp: '2 hours ago',
            details: '10/10 test suites passed. Residual errors within ±5% bounds.',
            isDone: true,
        },
        {
            stage: 'STAGE 2: Principal AI Engineer Peer Review',
            status: 'APPROVED',
            approver: 'lead-architect@enterprise.internal',
            timestamp: '1 hour ago',
            details: 'Verified Pearl SCM backdoor adjustment and Bayesian regret bounds.',
            isDone: true,
        },
        {
            stage: 'STAGE 3: Enterprise Compliance & Model Safety Signoff',
            status: 'APPROVED',
            approver: 'compliance-officer@enterprise.internal',
            timestamp: '30 mins ago',
            details: 'Audited deterministic audit logs and zero-data-loss rollback plans.',
            isDone: true,
        },
        {
            stage: 'STAGE 4: Production Rollout Authorization',
            status: 'READY_TO_DEPLOY',
            approver: 'Release Gatekeeper',
            timestamp: 'Pending Final Trigger',
            details: 'Canary staging health check optimal; ready for 100% production traffic promotion.',
            isDone: false,
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\uD83D\uDEE1\uFE0F" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Governance Approval Center & Multi-Stage Gatekeeper" }), _jsx(Badge, { variant: "success", size: "sm", children: "3/4 GATES APPROVED" })] }), _jsx("p", { className: "text-sm font-mono text-[#94A3B8] mt-1", children: "Multi-stakeholder compliance verification before promoting evolved model weights and policies to production." })] }), _jsx("button", { className: "px-4 py-2 rounded-xl text-xs font-mono font-bold bg-emerald-600 text-white hover:bg-emerald-500 transition-all shadow-lg shadow-emerald-600/20", children: "\u2713 AUTHORIZE FINAL PRODUCTION PROMOTION" })] }) }), _jsx("div", { className: "space-y-4", children: approvalStages.map((st, idx) => (_jsx(Card, { className: `p-6 border ${st.isDone
                        ? 'bg-[#0F172A] border-[#1E293B]'
                        : 'bg-blue-950/20 border-blue-500/50 shadow-lg shadow-blue-500/10'}`, children: _jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsx("div", { className: "flex items-center gap-2", children: _jsx("span", { className: "text-sm font-bold font-mono text-[#F8FAFC]", children: st.stage }) }), _jsxs("div", { className: "text-xs font-mono text-[#64748B] mt-1", children: ["Signed by: ", _jsx("span", { className: "text-[#94A3B8] font-bold", children: st.approver }), " \u2022 ", st.timestamp] }), _jsx("p", { className: "text-xs font-mono text-[#E2E8F0] mt-3", children: st.details })] }), _jsx(Badge, { variant: st.isDone ? 'success' : 'info', size: "sm", children: st.status })] }) }, idx))) })] }));
};
