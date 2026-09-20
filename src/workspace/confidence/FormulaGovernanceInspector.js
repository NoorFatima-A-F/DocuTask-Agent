import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { ShieldCheck, CheckCircle2, Lock, FileCode, Check } from 'lucide-react';
const rules = [
    {
        id: 'GOV-001',
        rule: 'Monotonic Feature Response',
        category: 'MONOTONICITY',
        status: 'PASSED',
        enforcement: 'STRICT_BLOCK',
        details: 'Positive feature increments must never decrease resulting confidence score.',
    },
    {
        id: 'GOV-002',
        rule: 'Output Bounds Compliance [0, 1]',
        category: 'BOUNDS',
        status: 'PASSED',
        enforcement: 'STRICT_BLOCK',
        details: 'Calculated confidence and uncertainty must stay strictly within [0.0, 1.0].',
    },
    {
        id: 'GOV-003',
        rule: 'Dual Approval on Formula Promotion',
        category: 'APPROVAL',
        status: 'PASSED',
        enforcement: 'STRICT_BLOCK',
        details: 'Formula migration from v1.2.0 to v1.3.0 approved by Governance Committee & Chief Architect.',
    },
    {
        id: 'GOV-004',
        rule: 'Cryptographic Event Hash Lineage',
        category: 'IMMUTABILITY',
        status: 'PASSED',
        enforcement: 'STRICT_BLOCK',
        details: 'All feature inputs must resolve to immutable Event Store entries with valid hashes.',
    },
];
export const FormulaGovernanceInspector = () => {
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsx("div", { className: "space-y-1", children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 rounded-xl text-emerald-400", children: _jsx(ShieldCheck, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Formula Governance & Policy Inspector", _jsx(Badge, { variant: "success", size: "sm", children: "Governance Certified" })] }), _jsx("p", { className: "text-xs text-slate-400", children: "Enforcing mathematical validity, monotonicity, bounds safety, and dual-authorization on formulas." })] })] }) }), _jsx("div", { className: "flex items-center gap-3", children: _jsx(Badge, { variant: "outline", size: "sm", children: "Active Formula: WeightedEnsemble (v1.3.0)" }) })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4 font-mono", children: [_jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs text-slate-400", children: "Monotonic Invariance" }), _jsxs("div", { className: "text-lg font-bold text-emerald-400 mt-1 flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-4 h-4" }), " 100% Enforced"] }), _jsx("p", { className: "text-[11px] text-slate-500 mt-1", children: "Zero anti-monotonic regressions" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs text-slate-400", children: "Formula Immutability" }), _jsxs("div", { className: "text-lg font-bold text-cyan-400 mt-1 flex items-center gap-2", children: [_jsx(Lock, { className: "w-4 h-4" }), " Locked & Signed"] }), _jsx("p", { className: "text-[11px] text-slate-500 mt-1", children: "SHA256: 9e01fb3401..." })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs text-slate-400", children: "Audit Compliance" }), _jsxs("div", { className: "text-lg font-bold text-indigo-400 mt-1 flex items-center gap-2", children: [_jsx(FileCode, { className: "w-4 h-4" }), " ISO/IEC 42001"] }), _jsx("p", { className: "text-[11px] text-slate-500 mt-1", children: "Enterprise AI Governance Ready" })] })] }), _jsxs(Card, { className: "p-5 bg-[#0F172A] border-[#1E293B]", children: [_jsxs("div", { className: "flex items-center justify-between mb-4", children: [_jsx("h2", { className: "text-sm font-bold font-mono text-slate-200", children: "Enforced Governance Policies" }), _jsx(Badge, { variant: "success", size: "sm", children: "4 Policies Active" })] }), _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left text-xs font-mono", children: [_jsx("thead", { className: "bg-[#1E293B]/60 text-slate-400 border-b border-[#1E293B]", children: _jsxs("tr", { children: [_jsx("th", { className: "p-3", children: "Rule ID" }), _jsx("th", { className: "p-3", children: "Policy Name" }), _jsx("th", { className: "p-3", children: "Category" }), _jsx("th", { className: "p-3", children: "Enforcement Mode" }), _jsx("th", { className: "p-3", children: "Status" }), _jsx("th", { className: "p-3", children: "Verification Details" })] }) }), _jsx("tbody", { className: "divide-y divide-[#1E293B]/40", children: rules.map((r) => (_jsxs("tr", { className: "hover:bg-slate-800/30 transition-colors", children: [_jsx("td", { className: "p-3 font-semibold text-emerald-400", children: r.id }), _jsx("td", { className: "p-3 text-slate-100 font-bold", children: r.rule }), _jsx("td", { className: "p-3", children: _jsx(Badge, { variant: "outline", size: "sm", children: r.category }) }), _jsx("td", { className: "p-3 text-slate-300", children: r.enforcement }), _jsx("td", { className: "p-3", children: _jsxs(Badge, { variant: "success", size: "sm", className: "flex items-center gap-1", children: [_jsx(Check, { className: "w-3 h-3" }), r.status] }) }), _jsx("td", { className: "p-3 text-slate-400", children: r.details })] }, r.id))) })] }) })] })] }));
};
