import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Database, Search, ShieldCheck, Tag, CheckCircle2 } from 'lucide-react';
export const KnowledgeRegistryView = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('ALL');
    const records = [
        {
            id: 'kn_8ae86cf4',
            title: 'Parallel Wavefront Sharding for Large Document Sets',
            category: 'EXECUTION_RULE',
            version: '1.0.0',
            status: 'VERIFIED',
            confidence: 96.5,
            hash: 'sha256:4a9c1e7f',
            missionId: 'mission-001',
            tags: ['ocr', 'sharding', 'performance', 'wavefront'],
            content: { shard_size: 4, parallelism: 6, speedup_pct: 34.2 },
        },
        {
            id: 'kn_7b9d3e12',
            title: 'Dynamic SMT Verification on Ambiguous Entity Extractions',
            category: 'VALIDATION_STRATEGY',
            version: '1.0.0',
            status: 'VERIFIED',
            confidence: 94.2,
            hash: 'sha256:2d8f9a0c',
            missionId: 'mission-001',
            tags: ['smt', 'verification', 'confidence', 'truth'],
            content: { confidence_floor: 0.88, smt_timeout_ms: 120 },
        },
        {
            id: 'kn_3c8a91f5',
            title: 'Exponential Jitter Backoff on OCR Throttling',
            category: 'RESILIENCE_STRATEGY',
            version: '1.0.0',
            status: 'VERIFIED',
            confidence: 97.8,
            hash: 'sha256:8e1a3b5c',
            missionId: 'mission-001',
            tags: ['resilience', 'retry', 'throttling'],
            content: { base_delay_ms: 250, max_retries: 3, jitter: true },
        },
        {
            id: 'kn_1e9f4a6b',
            title: 'Dynamic DAG Wavefront Partitioning Heuristic',
            category: 'PLANNER_POLICY',
            version: '2.1.0',
            status: 'VERIFIED',
            confidence: 98.2,
            hash: 'sha256:9c2b4e8a',
            missionId: 'mission-002',
            tags: ['planner', 'dag', 'heuristics'],
            content: { max_fanout: 8, replan_threshold: 0.85 },
        },
    ];
    const filteredRecords = records.filter((r) => {
        const matchesCat = selectedCategory === 'ALL' || r.category === selectedCategory;
        const matchesSearch = r.title.toLowerCase().includes(searchTerm.toLowerCase()) || r.tags.some((t) => t.toLowerCase().includes(searchTerm.toLowerCase()));
        return matchesCat && matchesSearch;
    });
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 rounded-xl text-emerald-400", children: _jsx(Database, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Institutional Knowledge Registry", _jsx(Badge, { variant: "intelligence", size: "sm", children: "Version Controlled" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] font-mono", children: "Authoritative catalog of immutable, cryptographically sealed rules, strategies, and empirical knowledge records" })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsxs("div", { className: "relative", children: [_jsx(Search, { className: "w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-[#64748B]" }), _jsx("input", { type: "text", placeholder: "Search knowledge records...", value: searchTerm, onChange: (e) => setSearchTerm(e.target.value), className: "bg-[#0F172A] border border-[#334155] rounded-lg pl-9 pr-3 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-emerald-500" })] }), _jsxs("select", { value: selectedCategory, onChange: (e) => setSelectedCategory(e.target.value), className: "bg-[#0F172A] border border-[#334155] rounded-lg px-3 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-emerald-500", children: [_jsx("option", { value: "ALL", children: "All Categories" }), _jsx("option", { value: "EXECUTION_RULE", children: "Execution Rules" }), _jsx("option", { value: "VALIDATION_STRATEGY", children: "Validation Strategies" }), _jsx("option", { value: "RESILIENCE_STRATEGY", children: "Resilience Strategies" }), _jsx("option", { value: "PLANNER_POLICY", children: "Planner Policies" })] })] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6 font-mono", children: filteredRecords.map((rec) => (_jsxs(Card, { className: "p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] space-y-4 flex flex-col justify-between", children: [_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between gap-2", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: rec.category }), _jsxs(Badge, { variant: "outline", size: "sm", children: ["v", rec.version] })] }), _jsxs("div", { className: "flex items-center gap-1.5 text-emerald-400 text-xs font-bold", children: [_jsx(ShieldCheck, { className: "w-3.5 h-3.5" }), rec.confidence, "% Conf"] })] }), _jsxs("div", { children: [_jsx("h3", { className: "text-sm font-bold text-white", children: rec.title }), _jsxs("div", { className: "flex items-center gap-3 text-[11px] text-[#64748B] mt-1", children: [_jsxs("span", { children: ["Source: ", rec.missionId] }), _jsxs("span", { children: ["Hash: ", rec.hash] })] })] }), _jsxs("div", { className: "p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl text-[11px] space-y-1 font-mono", children: [_jsx("span", { className: "text-[#64748B] block text-[10px]", children: "RECORD PAYLOAD:" }), _jsx("pre", { className: "text-cyan-300 overflow-x-auto", children: JSON.stringify(rec.content, null, 2) })] }), _jsx("div", { className: "flex flex-wrap gap-1.5 pt-1", children: rec.tags.map((t, idx) => (_jsxs("span", { className: "px-2 py-0.5 bg-[#1E293B] text-[#94A3B8] rounded text-[10px] flex items-center gap-1", children: [_jsx(Tag, { className: "w-2.5 h-2.5 text-[#64748B]" }), t] }, idx))) })] }), _jsxs("div", { className: "pt-3 border-t border-[#1E293B] flex items-center justify-between text-xs", children: [_jsxs("span", { className: "text-emerald-400 font-bold flex items-center gap-1", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5" }), rec.status] }), _jsxs("span", { className: "text-[11px] text-[#64748B]", children: ["ID: ", rec.id] })] })] }, rec.id))) })] }));
};
