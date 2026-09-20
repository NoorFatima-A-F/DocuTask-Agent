import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { ShieldCheck, ArrowDown, Lock } from 'lucide-react';
export const KnowledgeLineageExplorer = () => {
    const lineageChain = [
        {
            id: 'lin-001',
            recordId: 'kn-ocr-shard',
            version: '1.0.0',
            parentHash: 'GENESIS_ROOT',
            lineageHash: 'sha256:7f9a2b1c4e0d98',
            sourceMission: 'mission-001',
            mutationNote: 'Initial knowledge extraction from high-throughput PDF batch execution.',
            timestamp: '2026-09-12 00:05 UTC',
        },
        {
            id: 'lin-002',
            recordId: 'kn-ocr-shard',
            version: '1.1.0',
            parentHash: 'sha256:7f9a2b1c4e0d98',
            lineageHash: 'sha256:8e1a3b5c7d9f02',
            sourceMission: 'mission-002',
            mutationNote: 'Added adaptive jitter retry parameter to prevent OCR 429 rate limit drops.',
            timestamp: '2026-09-12 00:18 UTC',
        },
        {
            id: 'lin-003',
            recordId: 'kn-ocr-shard',
            version: '1.2.0',
            parentHash: 'sha256:8e1a3b5c7d9f02',
            lineageHash: 'sha256:9c2b4e8a1f3d5e',
            sourceMission: 'mission-003',
            mutationNote: 'Calibrated worker concurrency ceiling from 6 to 8 based on low-drift wavefronts.',
            timestamp: '2026-09-12 00:32 UTC',
        },
    ];
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 rounded-xl text-emerald-400", children: _jsx(Lock, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Cryptographic Knowledge Lineage Explorer", _jsx(Badge, { variant: "intelligence", size: "sm", children: "Tamper Evident" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] font-mono", children: "Inspect SHA-256 parent-child cryptographic provenance chains proving verifiable knowledge evolution" })] })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx(Badge, { variant: "success", size: "md", children: "Chain Integrity: 100% Valid" }) })] }), _jsx("div", { className: "space-y-4 font-mono max-w-4xl mx-auto", children: lineageChain.map((entry, idx) => (_jsxs(React.Fragment, { children: [_jsxs(Card, { className: "p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] space-y-3", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-2 border-b border-[#1E293B] pb-3 text-xs", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-white font-bold", children: entry.recordId }), _jsxs(Badge, { variant: "outline", size: "sm", children: ["v", entry.version] })] }), _jsxs("div", { className: "flex items-center gap-2 text-emerald-400 font-bold", children: [_jsx(ShieldCheck, { className: "w-3.5 h-3.5" }), "Tamper Proof"] })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs", children: [_jsxs("div", { className: "space-y-1", children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "PARENT HASH" }), _jsx("span", { className: "text-amber-400 font-bold block", children: entry.parentHash })] }), _jsxs("div", { className: "space-y-1", children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "LINEAGE HASH" }), _jsx("span", { className: "text-cyan-400 font-bold block", children: entry.lineageHash })] })] }), _jsxs("div", { className: "p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl text-xs space-y-1", children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "MUTATION RATIONALE:" }), _jsx("p", { className: "text-[#94A3B8]", children: entry.mutationNote }), _jsxs("div", { className: "text-[10px] text-[#64748B] pt-1", children: ["Source Mission: ", _jsx("span", { className: "text-indigo-400", children: entry.sourceMission }), " | Recorded: ", entry.timestamp] })] })] }), idx < lineageChain.length - 1 && (_jsx("div", { className: "flex justify-center my-2", children: _jsx("div", { className: "p-1.5 rounded-full bg-[#1E293B] text-cyan-400", children: _jsx(ArrowDown, { className: "w-4 h-4" }) }) }))] }, entry.id))) })] }));
};
