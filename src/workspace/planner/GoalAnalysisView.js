import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Target, CheckCircle2 } from 'lucide-react';
export const GoalAnalysisView = () => {
    const [activeTab, setActiveTab] = useState('OBJECTIVES');
    const goalData = {
        goalId: 'goal-m01-fin-audit',
        title: 'Process and validate 2026 Q3 vendor audit invoices with arithmetic invariant checks',
        priority: 'HIGH',
        deadline: '30.0s SLA',
        estimatedCostUsd: 0.0032,
        confidence: 0.985,
        objectives: [
            { id: 'obj-1', name: 'Rasterize & Segment Invoices', worker: 'OCR Workers', latency: '320ms', status: 'COMPLETED' },
            { id: 'obj-2', name: 'Extract Structured Vendor Line Items', worker: 'Extract Worker', latency: '250ms', status: 'RUNNING' },
            { id: 'obj-3', name: 'Verify Mathematical Arithmetic Invariant', worker: 'Scientific Validator', latency: '180ms', status: 'PENDING' },
            { id: 'obj-4', name: 'Commit Merkle Proof to Truth Ledger', worker: 'Truth Authenticator', latency: '110ms', status: 'PENDING' },
        ],
        constraints: [
            'Total mission latency must remain strictly below 30.0 seconds.',
            'Arithmetic invariant: sum(item_subtotals) + tax == total_amount_due.',
            'Zero hallucinations: Confidence score >= 0.95 across invoice tax IDs.',
            'Immutable cryptographic hash chain must link raw document to final extracted JSON.',
        ],
        resources: [
            { name: 'Google Cloud Document AI (Primary)', type: 'CLOUD_OCR', quota: '50 req/min' },
            { name: 'Tesseract OCR Fallback (Edge Engine)', type: 'LOCAL_FALLBACK', quota: 'Unlimited' },
            { name: 'Deterministic Schema Regex Engine', type: 'SCHEMA_NORMALIZER', quota: 'In-Memory' },
            { name: 'Hardware Merkle Hash Ring', type: 'LEDGER_SIGNER', quota: '1000 ops/sec' },
        ],
    };
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsx("div", { className: "space-y-1", children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 rounded-xl text-cyan-400", children: _jsx(Target, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Autonomous Goal Analysis & Constraint Extractor", _jsx(Badge, { variant: "success", size: "sm", children: "Decomposed" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] font-mono", children: "Inspect structured objectives, deterministic constraints, and discovered capabilities" })] })] }) }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "intelligence", size: "md", children: "Confidence 98.5%" }), _jsx(Badge, { variant: "outline", size: "md", children: "SLA: 30.0s" })] })] }), _jsxs(Card, { className: "p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] space-y-3 font-mono", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("span", { className: "text-xs text-[#64748B]", children: ["MISSION GOAL IDENTIFIER: ", goalData.goalId] }), _jsxs(Badge, { variant: "info", size: "sm", children: ["Priority: ", goalData.priority] })] }), _jsx("p", { className: "text-sm font-semibold text-white", children: goalData.title }), _jsxs("div", { className: "flex flex-wrap gap-4 text-xs text-[#94A3B8] pt-2 border-t border-[#1E293B]", children: [_jsxs("span", { children: ["Estimated Cost: ", _jsxs("strong", { className: "text-emerald-400", children: ["$", goalData.estimatedCostUsd] })] }), _jsxs("span", { children: ["Target SLA: ", _jsx("strong", { className: "text-cyan-400", children: goalData.deadline })] }), _jsxs("span", { children: ["Decomposed Sub-Tasks: ", _jsx("strong", { className: "text-purple-400", children: goalData.objectives.length })] })] })] }), _jsx("div", { className: "flex gap-2 border-b border-[#1E293B] pb-2 font-mono text-xs", children: ['OBJECTIVES', 'CONSTRAINTS', 'RESOURCES'].map(tab => (_jsx("button", { onClick: () => setActiveTab(tab), className: `px-4 py-2 rounded-xl transition-all font-semibold ${activeTab === tab ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' : 'text-[#94A3B8] hover:bg-[#131D35]'}`, children: tab }, tab))) }), activeTab === 'OBJECTIVES' && (_jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: goalData.objectives.map((obj, i) => (_jsxs(Card, { className: "p-4 rounded-xl border border-[#1E293B] bg-[#0F172A] space-y-2 font-mono", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("span", { className: "text-[10px] text-[#64748B]", children: ["OBJECTIVE #", i + 1] }), _jsx(Badge, { variant: obj.status === 'COMPLETED' ? 'success' : obj.status === 'RUNNING' ? 'intelligence' : 'outline', size: "sm", children: obj.status })] }), _jsx("h3", { className: "text-xs font-bold text-white", children: obj.name }), _jsxs("div", { className: "flex items-center justify-between text-[11px] text-[#94A3B8] pt-2 border-t border-[#1E293B]", children: [_jsxs("span", { children: ["Target: ", obj.worker] }), _jsxs("span", { children: ["Latency Est: ", obj.latency] })] })] }, obj.id))) })), activeTab === 'CONSTRAINTS' && (_jsx("div", { className: "space-y-3 font-mono", children: goalData.constraints.map((c, i) => (_jsxs(Card, { className: "p-4 rounded-xl border border-[#1E293B] bg-[#0F172A] flex items-center gap-3", children: [_jsx(CheckCircle2, { className: "w-5 h-5 text-emerald-400 shrink-0" }), _jsx("div", { className: "text-xs text-[#F8FAFC]", children: c })] }, i))) })), activeTab === 'RESOURCES' && (_jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4 font-mono", children: goalData.resources.map((r, i) => (_jsxs(Card, { className: "p-4 rounded-xl border border-[#1E293B] bg-[#0F172A] space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx(Badge, { variant: "info", size: "sm", children: r.type }), _jsxs("span", { className: "text-[10px] text-[#64748B]", children: ["Quota: ", r.quota] })] }), _jsx("h3", { className: "text-xs font-bold text-white", children: r.name })] }, i))) }))] }));
};
