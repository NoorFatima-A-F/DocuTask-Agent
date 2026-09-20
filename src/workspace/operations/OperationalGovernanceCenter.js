import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { ShieldAlert, CheckCircle2, RefreshCw, Lock, Award } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
export const OperationalGovernanceCenter = ({ missionId = 'cluster-primary-master', }) => {
    const [policies] = useState([
        {
            id: 'POL-OP-001',
            name: 'Automated Sub-Second Self-Healing',
            rule: 'Execute automated restarts on single worker thread failure without human blocking',
            isHardGuardrail: true,
            enforced: true,
            violations: 0,
        },
        {
            id: 'POL-OP-002',
            name: 'Zero Data Loss Checkpoint Guarantee',
            rule: 'Rollback only to verified cryptographic SHA-256 snapshots from Phase 13.4',
            isHardGuardrail: true,
            enforced: true,
            violations: 0,
        },
        {
            id: 'POL-OP-003',
            name: 'SLA Latency Circuit Breaker',
            rule: 'Engage quantized fallback models when P99 latency exceeds 3000ms for 3 consecutive minutes',
            isHardGuardrail: false,
            enforced: true,
            violations: 0,
        },
    ]);
    const [compliance] = useState({
        soc2Pct: 100.0,
        iso27001Pct: 100.0,
        iso42001Pct: 98.5,
        nistAiRmfPct: 99.0,
        merkleRoot: '0x8f1a029cb384ef7a91c55d015a3bf4f1b2b0b822cd15d6c15b0f00a08',
        auditedEvents: 1420,
    });
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(ShieldAlert, { className: "w-5 h-5 text-emerald-400" }), "Operational Governance & SRE Compliance Center"] }), _jsxs("p", { className: "text-sm text-slate-400", children: ["Automated safety boundaries, multi-standard compliance scoring (SOC2, ISO 27001, ISO 42001, NIST AI RMF), and append-only cryptographic audits for: ", _jsx("code", { className: "text-emerald-300 font-mono text-xs", children: missionId })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: "success", size: "md", children: "Governance Status: 100% COMPLIANT" }), _jsxs("button", { className: "flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700", children: [_jsx(RefreshCw, { className: "w-3.5 h-3.5" }), "Audit Merkle Root"] })] })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-mono", children: [_jsxs(Card, { className: "p-4 bg-slate-900 border-slate-800 space-y-1", children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "SOC 2 Type II" }), _jsxs("span", { className: "text-2xl font-bold text-emerald-400", children: [compliance.soc2Pct, "%"] }), _jsx("span", { className: "text-[10px] text-slate-500 block", children: "Security & Availability" })] }), _jsxs(Card, { className: "p-4 bg-slate-900 border-slate-800 space-y-1", children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "ISO / IEC 27001" }), _jsxs("span", { className: "text-2xl font-bold text-cyan-400", children: [compliance.iso27001Pct, "%"] }), _jsx("span", { className: "text-[10px] text-slate-500 block", children: "Information Security" })] }), _jsxs(Card, { className: "p-4 bg-slate-900 border-slate-800 space-y-1", children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "ISO / IEC 42001" }), _jsxs("span", { className: "text-2xl font-bold text-purple-400", children: [compliance.iso42001Pct, "%"] }), _jsx("span", { className: "text-[10px] text-slate-500 block", children: "AI Governance System" })] }), _jsxs(Card, { className: "p-4 bg-slate-900 border-slate-800 space-y-1", children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "NIST AI RMF 1.0" }), _jsxs("span", { className: "text-2xl font-bold text-indigo-400", children: [compliance.nistAiRmfPct, "%"] }), _jsx("span", { className: "text-[10px] text-slate-500 block", children: "AI Risk Management" })] })] }), _jsxs(Card, { className: "p-4 bg-slate-900 border-slate-800 flex items-center justify-between font-mono", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 rounded-lg bg-indigo-950/60 border border-indigo-500/30 text-indigo-400", children: _jsx(Lock, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "Append-Only Merkle Audit Root" }), _jsx("code", { className: "text-xs font-bold text-slate-200", children: compliance.merkleRoot })] })] }), _jsxs("div", { className: "text-right", children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "Audited Operations" }), _jsxs("span", { className: "text-xs font-bold text-emerald-400", children: [compliance.auditedEvents, " Events Logged"] })] })] }), _jsxs("div", { className: "space-y-3 font-mono", children: [_jsxs("h3", { className: "text-sm font-semibold text-slate-200 flex items-center gap-2", children: [_jsx(Award, { className: "w-4 h-4 text-emerald-400" }), "Enforced Operational SRE Policies & Guardrails"] }), policies.map((pol) => (_jsxs(Card, { className: "p-4 bg-slate-900 border-slate-800 flex items-center justify-between", children: [_jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-bold text-indigo-400", children: pol.id }), _jsx("span", { className: "text-xs font-bold text-slate-200", children: pol.name }), pol.isHardGuardrail && _jsx(Badge, { variant: "error", size: "sm", children: "Hard Guardrail" })] }), _jsx("p", { className: "text-xs text-slate-400", children: pol.rule })] }), _jsxs("div", { className: "text-right space-y-1", children: [_jsxs(Badge, { variant: "success", size: "sm", children: [_jsx(CheckCircle2, { className: "w-3 h-3 mr-1" }), "ENFORCED"] }), _jsxs("span", { className: "text-[10px] text-slate-500 block", children: [pol.violations, " Violations"] })] })] }, pol.id)))] })] }));
};
