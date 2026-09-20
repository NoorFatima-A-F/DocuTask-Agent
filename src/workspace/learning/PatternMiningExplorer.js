import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { GitBranch, Search, TrendingUp, ArrowRight } from 'lucide-react';
export const PatternMiningExplorer = () => {
    const [selectedCategory, setSelectedCategory] = useState('ALL');
    const [searchTerm, setSearchTerm] = useState('');
    const patterns = [
        {
            id: 'pat-001',
            name: 'Parallel OCR Wavefront Pattern',
            type: 'PARALLEL_WAVEFRONT',
            frequency: 18,
            successRate: 98.6,
            throughputGain: '+34.2%',
            tasks: ['task-ocr-partition', 'task-ocr-shard-01', 'task-ocr-shard-02', 'task-schema-fusion'],
            description: 'Partitioning high-page count PDFs into independent worker batches yields near-linear throughput scaling.',
        },
        {
            id: 'pat-002',
            name: 'SMT Truth Gating Validation Pattern',
            type: 'INVARIANT_VERIFICATION',
            frequency: 24,
            successRate: 99.9,
            throughputGain: 'Zero Hallucinations',
            tasks: ['task-entity-extraction', 'task-smt-solver', 'task-truth-ledger-commit'],
            description: 'Invoking symbolic constraint solver before committing extraction outputs prevents schema hallucinations.',
        },
        {
            id: 'pat-003',
            name: 'Transient Rate Limit Fallback Cascade',
            type: 'FALLBACK_CASCADE',
            frequency: 9,
            successRate: 96.0,
            throughputGain: '100% Recovery',
            tasks: ['task-llm-call', 'task-rate-limiter', 'task-jitter-backoff'],
            description: 'Exponential jitter retry with 250ms base backoff recovers throttled worker nodes without planner intervention.',
        },
        {
            id: 'pat-004',
            name: 'Dual-LLM Cross Verification Wavefront',
            type: 'CONFIDENCE_RECOVERY',
            frequency: 12,
            successRate: 97.4,
            throughputGain: '+11.8% Posterior Conf',
            tasks: ['task-gemini-extract', 'task-counterfactual-verifier'],
            description: 'Triggering secondary referee model when primary confidence is between 0.80 and 0.88 resolves ambiguities.',
        },
    ];
    const filteredPatterns = patterns.filter((p) => {
        const matchesCategory = selectedCategory === 'ALL' || p.type === selectedCategory;
        const matchesSearch = p.name.toLowerCase().includes(searchTerm.toLowerCase()) || p.description.toLowerCase().includes(searchTerm.toLowerCase());
        return matchesCategory && matchesSearch;
    });
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-purple-500/20 to-indigo-500/20 border border-purple-500/30 rounded-xl text-purple-400", children: _jsx(GitBranch, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Execution Pattern Mining Explorer", _jsx(Badge, { variant: "intelligence", size: "sm", children: "Phase 13.5" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] font-mono", children: "Unsupervised and supervised pattern mining across mission replay logs to discover high-utility workflow wavefronts" })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsxs("div", { className: "relative", children: [_jsx(Search, { className: "w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-[#64748B]" }), _jsx("input", { type: "text", placeholder: "Search mined patterns...", value: searchTerm, onChange: (e) => setSearchTerm(e.target.value), className: "bg-[#0F172A] border border-[#334155] rounded-lg pl-9 pr-3 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-purple-500" })] }), _jsxs("select", { value: selectedCategory, onChange: (e) => setSelectedCategory(e.target.value), className: "bg-[#0F172A] border border-[#334155] rounded-lg px-3 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-purple-500", children: [_jsx("option", { value: "ALL", children: "All Pattern Types" }), _jsx("option", { value: "PARALLEL_WAVEFRONT", children: "Parallel Wavefront" }), _jsx("option", { value: "INVARIANT_VERIFICATION", children: "Invariant Verification" }), _jsx("option", { value: "FALLBACK_CASCADE", children: "Fallback Cascade" }), _jsx("option", { value: "CONFIDENCE_RECOVERY", children: "Confidence Recovery" })] })] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6 font-mono", children: filteredPatterns.map((p) => (_jsxs(Card, { className: "p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] space-y-4 flex flex-col justify-between", children: [_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between gap-2", children: [_jsx(Badge, { variant: "outline", size: "sm", children: p.type }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs("span", { className: "text-xs text-[#94A3B8]", children: [p.frequency, " Occurrences"] }), _jsxs(Badge, { variant: "success", size: "sm", children: [p.successRate, "% Success"] })] })] }), _jsxs("div", { children: [_jsx("h3", { className: "text-sm font-bold text-white", children: p.name }), _jsx("p", { className: "text-xs text-[#94A3B8] mt-1 leading-relaxed", children: p.description })] }), _jsxs("div", { className: "p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl space-y-1.5", children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "TASK EXECUTION WAVEFRONT:" }), _jsx("div", { className: "flex flex-wrap items-center gap-1.5 text-[11px]", children: p.tasks.map((task, idx) => (_jsxs(React.Fragment, { children: [_jsx("span", { className: "px-2 py-0.5 bg-purple-500/10 border border-purple-500/20 text-purple-300 rounded", children: task }), idx < p.tasks.length - 1 && _jsx(ArrowRight, { className: "w-3 h-3 text-[#64748B]" })] }, idx))) })] })] }), _jsxs("div", { className: "pt-3 border-t border-[#1E293B] flex items-center justify-between text-xs", children: [_jsxs("span", { className: "text-emerald-400 font-bold flex items-center gap-1", children: [_jsx(TrendingUp, { className: "w-3.5 h-3.5" }), "Gain: ", p.throughputGain] }), _jsxs("span", { className: "text-[11px] text-[#64748B]", children: ["Pattern ID: ", p.id] })] })] }, p.id))) })] }));
};
