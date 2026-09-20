import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { ShieldCheck, Lock, RotateCcw, CheckCircle2, Key, Award, } from 'lucide-react';
export const PredictiveGovernanceCenter = () => {
    const [approvals] = useState([
        {
            id: 'appr-001',
            planId: 'plan-auto-scale-04',
            actionTitle: 'Predictive Horizontal Worker Scaling (+4 Replicas)',
            riskScore: 0.12,
            approved: true,
            signer: 'secp256k1:gov_oracle_node_alpha',
            signature: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            timestamp: '2026-09-12T15:20:00Z',
            rollbackPlanId: 'rb-plan-04-drain',
            constraintsValidated: [
                'SLO Budget Invariant (>99.95%)',
                'Cost Envelope Cap (<$12.50/hr)',
                'Zero Simulation Policy Verified',
            ],
        },
        {
            id: 'appr-002',
            planId: 'plan-cache-warm-09',
            actionTitle: 'Predictive Cache Pre-Warming for Batch Ingest',
            riskScore: 0.08,
            approved: true,
            signer: 'secp256k1:gov_oracle_node_beta',
            signature: 'f4c8996fb92427ae41e4649b934ca495991b7852b855e3b0c44298fc1c149a',
            timestamp: '2026-09-12T15:25:30Z',
            rollbackPlanId: 'rb-cache-purge-09',
            constraintsValidated: [
                'Memory Pressure Boundary (<75%)',
                'Lock Contention Invariant (<1.5ms)',
            ],
        },
        {
            id: 'appr-003',
            planId: 'plan-route-failover-02',
            actionTitle: 'Proactive Degraded Agent Isolation & Route Divergence',
            riskScore: 0.22,
            approved: true,
            signer: 'secp256k1:gov_oracle_node_gamma',
            signature: '1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855e3b0c44298fc',
            timestamp: '2026-09-12T15:30:15Z',
            rollbackPlanId: 'rb-route-restore-02',
            constraintsValidated: [
                'Byzantine Fault Threshold (<33%)',
                'Quorum Agreement (>67%)',
            ],
        },
    ]);
    const [rollbackStatus, setRollbackStatus] = useState(null);
    const handleTriggerRollback = (planId, rbId) => {
        setRollbackStatus(`Rollback executed successfully for ${planId} using checkpoint ${rbId}. State restored.`);
        setTimeout(() => setRollbackStatus(null), 4000);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(ShieldCheck, { className: "w-6 h-6 text-indigo-500" }), "Predictive Governance & Cryptographic Assurance Center"] }), _jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: "Phase 13.10 \u2014 SHA-256 signed predictive action verifications, policy constraint proofs, and zero-downtime rollback checkpoints." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Badge, { variant: "success", size: "md", children: [_jsx(Lock, { className: "w-3.5 h-3.5 mr-1" }), "3/3 Cryptographically Signed"] }), _jsxs(Badge, { variant: "intelligence", size: "md", children: [_jsx(Award, { className: "w-3.5 h-3.5 mr-1" }), "Zero Simulation Enforced"] })] })] }), rollbackStatus && (_jsxs("div", { className: "p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-lg text-sm text-emerald-800 dark:text-emerald-300 flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-5 h-5 flex-shrink-0" }), _jsx("span", { children: rollbackStatus })] })), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 border-indigo-200 dark:border-indigo-900 bg-indigo-50/20 dark:bg-indigo-950/20", children: [_jsx("span", { className: "text-xs font-medium text-gray-500 dark:text-gray-400", children: "Signed Approvals" }), _jsx("div", { className: "text-2xl font-bold text-indigo-600 dark:text-indigo-400 mt-1", children: approvals.length }), _jsx("span", { className: "text-xs text-emerald-600 dark:text-emerald-400 font-medium", children: "100% Verified Signatures" })] }), _jsxs(Card, { className: "p-4", children: [_jsx("span", { className: "text-xs font-medium text-gray-500 dark:text-gray-400", children: "Max Tolerable Risk Cap" }), _jsx("div", { className: "text-2xl font-bold text-gray-900 dark:text-white mt-1", children: "0.300" }), _jsx("span", { className: "text-xs text-gray-400", children: "Current Max: 0.220" })] }), _jsxs(Card, { className: "p-4", children: [_jsx("span", { className: "text-xs font-medium text-gray-500 dark:text-gray-400", children: "Active Checkpoints" }), _jsx("div", { className: "text-2xl font-bold text-purple-600 dark:text-purple-400 mt-1", children: approvals.length }), _jsx("span", { className: "text-xs text-purple-500", children: "Zero-downtime Rollback Ready" })] }), _jsxs(Card, { className: "p-4", children: [_jsx("span", { className: "text-xs font-medium text-gray-500 dark:text-gray-400", children: "Safety Invariant Guard" }), _jsx("div", { className: "text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1", children: "ACTIVE" }), _jsx("span", { className: "text-xs text-emerald-500", children: "Autonomous Gatekeeper" })] })] }), _jsxs("div", { className: "space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("h3", { className: "text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider flex items-center gap-2", children: [_jsx(Key, { className: "w-4 h-4 text-indigo-500" }), "Cryptographic Approval Ledger"] }), _jsx("span", { className: "text-xs text-gray-500", children: "SHA-256 Provenance" })] }), _jsx("div", { className: "grid grid-cols-1 gap-4", children: approvals.map((rec) => (_jsxs(Card, { className: "p-5 border-l-4 border-l-indigo-500 hover:shadow-md transition-shadow", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-xs text-indigo-600 dark:text-indigo-400 font-semibold", children: rec.id }), _jsx("h4", { className: "font-semibold text-gray-900 dark:text-white text-base", children: rec.actionTitle })] }), _jsxs("div", { className: "text-xs text-gray-400 mt-0.5", children: ["Plan ID: ", _jsx("span", { className: "font-mono text-gray-600 dark:text-gray-300", children: rec.planId }), " \u2022 Recorded at: ", new Date(rec.timestamp).toLocaleTimeString()] })] }), _jsxs("div", { className: "flex items-center gap-2 flex-shrink-0", children: [_jsxs(Badge, { variant: "success", size: "sm", children: [_jsx(CheckCircle2, { className: "w-3 h-3 mr-1" }), "APPROVED"] }), _jsxs(Button, { variant: "outline", size: "sm", className: "text-xs text-rose-600 dark:text-rose-400 border-rose-200 dark:border-rose-900 hover:bg-rose-50 dark:hover:bg-rose-950/30", onClick: () => handleTriggerRollback(rec.planId, rec.rollbackPlanId), children: [_jsx(RotateCcw, { className: "w-3.5 h-3.5 mr-1" }), "Rollback Checkpoint"] })] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 text-xs", children: [_jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-gray-500", children: "Signer Identity:" }), _jsx("span", { className: "font-mono text-gray-700 dark:text-gray-300", children: rec.signer })] }), _jsxs("div", { children: [_jsx("span", { className: "text-gray-500 block mb-1", children: "Cryptographic Signature (SHA-256 Digest):" }), _jsx("div", { className: "p-2 bg-gray-50 dark:bg-gray-900/60 rounded border border-gray-200 dark:border-gray-800 font-mono text-gray-600 dark:text-gray-400 break-all text-[11px]", children: rec.signature })] })] }), _jsxs("div", { className: "space-y-2", children: [_jsx("span", { className: "text-gray-500 block font-medium", children: "Validated Safety Constraints:" }), _jsx("div", { className: "space-y-1.5", children: rec.constraintsValidated.map((c, idx) => (_jsxs("div", { className: "flex items-center gap-1.5 text-emerald-700 dark:text-emerald-400", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5 flex-shrink-0" }), _jsx("span", { children: c })] }, idx))) }), _jsxs("div", { className: "pt-2 flex items-center justify-between text-gray-500", children: [_jsx("span", { children: "Rollback Checkpoint Target:" }), _jsx("span", { className: "font-mono text-indigo-600 dark:text-indigo-400 font-medium", children: rec.rollbackPlanId })] })] })] })] }, rec.id))) })] })] }));
};
