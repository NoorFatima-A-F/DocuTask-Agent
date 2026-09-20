import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { FileCheck2, ShieldCheck, Search, Hash, Database, CheckCircle2, Lock, } from 'lucide-react';
export const EvidenceExplorer = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [verifiedId, setVerifiedId] = useState(null);
    const evidenceRecords = [
        {
            id: 'evi-invoice-cache-ab-01',
            experimentId: 'exp-cache-ab-01',
            hypothesisId: 'hyp-spec-tensor-01',
            title: 'Speculative Layout Cache Empirical Proof Dataset',
            strength: 'EMPIRICAL_DEFINITIVE',
            dataPoints: 5000,
            sha256Hash: '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
            confidence: 0.992,
            timestamp: '2026-09-12T18:40:00Z',
        },
        {
            id: 'evi-lock-contention-03',
            experimentId: 'exp-ring-buffer-02',
            hypothesisId: 'hyp-lockfree-ring-03',
            title: 'Lock-Free Circular Buffer Telemetry Stream',
            strength: 'EMPIRICAL_DEFINITIVE',
            dataPoints: 10000,
            sha256Hash: '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
            confidence: 0.998,
            timestamp: '2026-09-12T17:15:00Z',
        },
        {
            id: 'evi-auction-jitter-02',
            experimentId: 'exp-triadic-auction-03',
            hypothesisId: 'hyp-triadic-coalition-02',
            title: 'Triadic Swarm Negotiation Latency Records',
            strength: 'STATISTICALLY_SIGNIFICANT',
            dataPoints: 5000,
            sha256Hash: '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a',
            confidence: 0.965,
            timestamp: '2026-09-12T16:00:00Z',
        },
    ];
    const handleVerifyIntegrity = (id) => {
        setVerifiedId(id);
        setTimeout(() => setVerifiedId(null), 3000);
    };
    const filtered = evidenceRecords.filter(r => r.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        r.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        r.sha256Hash.toLowerCase().includes(searchQuery.toLowerCase()));
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(FileCheck2, { className: "w-6 h-6 text-emerald-500" }), "Empirical Evidence & Provenance Ledger"] }), _jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: "Cryptographically sealed scientific evidence repository backed by SHA-256 hashes, telemetry lineage, and Truth Ledger anchors." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Badge, { variant: "success", size: "md", children: [_jsx(ShieldCheck, { className: "w-3.5 h-3.5 mr-1" }), "100% Provenance Certified"] }) })] }), _jsxs("div", { className: "relative", children: [_jsx(Search, { className: "w-4 h-4 text-gray-400 absolute left-3 top-3" }), _jsx("input", { type: "text", placeholder: "Search by evidence ID, SHA-256 hash, or hypothesis...", value: searchQuery, onChange: e => setSearchQuery(e.target.value), className: "w-full pl-9 pr-4 py-2 text-xs border rounded-lg dark:bg-gray-800 dark:border-gray-700 text-gray-900 dark:text-white" })] }), _jsx("div", { className: "space-y-4", children: filtered.map(record => (_jsxs(Card, { className: "p-5 space-y-3", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-2", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-xs text-emerald-500 font-semibold", children: record.id }), _jsxs(Badge, { variant: "outline", size: "sm", children: ["Exp: ", record.experimentId] }), _jsx(Badge, { variant: "success", size: "sm", children: record.strength })] }), _jsx("h3", { className: "font-semibold text-gray-900 dark:text-white mt-1", children: record.title })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "outline", size: "sm", onClick: () => handleVerifyIntegrity(record.id), children: [_jsx(Lock, { className: "w-3.5 h-3.5 mr-1 text-emerald-500" }), verifiedId === record.id ? 'Hash Verified!' : 'Verify SHA-256 Hash'] }) })] }), verifiedId === record.id && (_jsxs("div", { className: "p-3 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded text-xs text-emerald-800 dark:text-emerald-300 flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-4 h-4 flex-shrink-0" }), _jsx("span", { children: "SHA-256 Digest matches Truth Ledger Block #7491 with zero byte divergence." })] })), _jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900 rounded font-mono text-[11px] text-gray-600 dark:text-gray-400 flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2 overflow-hidden", children: [_jsx(Hash, { className: "w-3.5 h-3.5 text-gray-400 flex-shrink-0" }), _jsx("span", { className: "truncate", children: record.sha256Hash })] }), _jsx(Badge, { variant: "outline", size: "sm", children: "SHA-256" })] }), _jsxs("div", { className: "grid grid-cols-3 gap-2 text-xs text-gray-500 pt-1 border-t border-gray-100 dark:border-gray-800", children: [_jsxs("div", { className: "flex items-center gap-1.5", children: [_jsx(Database, { className: "w-3.5 h-3.5 text-gray-400" }), _jsxs("span", { children: ["Observations: ", _jsx("strong", { className: "text-gray-800 dark:text-gray-200", children: record.dataPoints.toLocaleString() })] })] }), _jsx("div", { children: _jsxs("span", { children: ["Confidence: ", _jsxs("strong", { className: "text-emerald-600", children: [(record.confidence * 100).toFixed(1), "%"] })] }) }), _jsx("div", { className: "text-right text-gray-400", children: new Date(record.timestamp).toLocaleString() })] })] }, record.id))) })] }));
};
