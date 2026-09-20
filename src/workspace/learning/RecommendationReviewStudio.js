import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Sparkles, CheckCircle2, Play } from 'lucide-react';
export const RecommendationReviewStudio = () => {
    const [promoted, setPromoted] = useState([]);
    const recommendations = [
        {
            id: 'rec-001',
            title: 'Auto-Promote Parallel OCR Sharding to Default Planner Template',
            target: 'planner',
            evidenceLesson: 'lsn-001 (Parallel Wavefront OCR)',
            projectedSpeedup: '+34.2%',
            confidence: 96.5,
            impact: 'Reduces document processing latency by ~850ms on batches > 10 pages.',
            parameters: { shard_size: 4, parallelism: 8, max_retries: 3 },
        },
        {
            id: 'rec-002',
            title: 'Enforce SMT Invariant Verification on Financial Entity Extractions',
            target: 'truth_ledger',
            evidenceLesson: 'lsn-002 (SMT Invariant Validation)',
            projectedSpeedup: 'Zero Schema Drift',
            confidence: 99.1,
            impact: 'Mathematically verifies total invoice balances before triggering downstream accounting events.',
            parameters: { solver: 'z3', timeout_ms: 150, confidence_floor: 0.88 },
        },
        {
            id: 'rec-003',
            title: 'Deploy Jittered Retry Strategy on Worker Rate Limit (429)',
            target: 'worker',
            evidenceLesson: 'lsn-003 (Exponential Backoff)',
            projectedSpeedup: '100% Task Resilience',
            confidence: 97.8,
            impact: 'Prevents dropped tasks during high-traffic OCR bursts without human operator intervention.',
            parameters: { base_delay_ms: 250, backoff_multiplier: 2.0, max_retries: 4 },
        },
    ];
    const handlePromote = (id) => {
        setPromoted((prev) => [...prev, id]);
    };
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsx("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 rounded-xl text-indigo-400", children: _jsx(Sparkles, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Autonomous Recommendation Review Studio", _jsx(Badge, { variant: "intelligence", size: "sm", children: "Phase 13.5" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] font-mono", children: "Evaluate, test, and safely promote machine-learned policy recommendations into production" })] })] }) }), _jsx("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6 font-mono", children: recommendations.map((rec) => {
                    const isDone = promoted.includes(rec.id);
                    return (_jsxs(Card, { className: "p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] space-y-4 flex flex-col justify-between", children: [_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between gap-2", children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: rec.target.toUpperCase() }), _jsxs("span", { className: "text-xs font-bold text-emerald-400", children: [rec.confidence, "% Conf"] })] }), _jsxs("div", { children: [_jsx("h3", { className: "text-sm font-bold text-white leading-snug", children: rec.title }), _jsx("span", { className: "text-xs text-cyan-400 font-bold mt-1 block", children: rec.projectedSpeedup })] }), _jsx("p", { className: "text-xs text-[#94A3B8] leading-relaxed", children: rec.impact }), _jsxs("div", { className: "p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl text-[11px] space-y-1", children: [_jsx("span", { className: "text-[#64748B] text-[10px] block", children: "PROPOSED PARAMETERS:" }), _jsx("pre", { className: "text-indigo-300 overflow-x-auto", children: JSON.stringify(rec.parameters, null, 2) })] })] }), _jsxs("div", { className: "pt-3 border-t border-[#1E293B] flex items-center justify-between", children: [_jsx("span", { className: "text-[10px] text-[#64748B]", children: rec.evidenceLesson }), _jsx("button", { onClick: () => handlePromote(rec.id), disabled: isDone, className: `flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono font-bold transition-colors ${isDone
                                            ? 'bg-emerald-600/20 text-emerald-300 border border-emerald-500/30 cursor-default'
                                            : 'bg-indigo-600 hover:bg-indigo-500 text-white'}`, children: isDone ? (_jsxs(_Fragment, { children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5" }), " Promoted"] })) : (_jsxs(_Fragment, { children: [_jsx(Play, { className: "w-3.5 h-3.5" }), " Promote Policy"] })) })] })] }, rec.id));
                }) })] }));
};
