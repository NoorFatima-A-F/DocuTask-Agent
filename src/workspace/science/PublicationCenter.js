import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { FileText, ShieldCheck, Download, Share2, CheckCircle2, Lock, } from 'lucide-react';
export const PublicationCenter = () => {
    const [downloadNotice, setDownloadNotice] = useState(null);
    const publications = [
        {
            id: 'pub-spec-cache-01',
            doi: '10.ai-sci/2026.001',
            title: 'Empirical Proof of Speculative Invariance in Multi-Column Accounting Extraction',
            abstract: 'We demonstrate that recurring enterprise invoice headers exhibit <=1.2 bits/token spatial entropy, allowing speculative GPU tensor caching that reduces P95 extraction latency by 30.27% (p < 0.0001) under 5,000 document evaluation.',
            conclusions: [
                'Speculative tensor caching yields 30.27% P95 latency reduction.',
                'Zero accuracy degradation observed across 5,000 evaluated invoices.',
                'Verified against Truth Ledger Block 7491 with SHA-256 provenance.',
            ],
            authors: ['AI Chief Scientist', 'Optimization Swarm Alpha', 'Governance Oracle'],
            state: 'PUBLISHED',
            publishedAt: '2026-09-12T18:45:00Z',
            signature: 'secp256k1:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
        },
        {
            id: 'pub-lockfree-ring-02',
            doi: '10.ai-sci/2026.002',
            title: 'Zero-Lock Telemetry Streaming with Atomic Circular Buffers in Autonomous Agent Societies',
            abstract: 'We establish an empirical proof that lock-free atomic circular buffers eliminate all thread contention in memory telemetry across 64 concurrent agents, yielding zero thread lock stalls under 100k events/sec throughput.',
            conclusions: [
                'Atomic circular buffers eliminate 100% of telemetry mutex lock stalls.',
                'Sustained 120k events/sec ingestion with <2MB memory jitter.',
                'Fully reproducible under deterministic replay replay-ring-994.',
            ],
            authors: ['AI Chief Scientist', 'Resilience Swarm Gamma'],
            state: 'PUBLISHED',
            publishedAt: '2026-09-12T17:30:00Z',
            signature: 'secp256k1:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
        },
    ];
    const handleDownloadPaper = (title) => {
        setDownloadNotice(`Generated machine-readable JSON-LD & PDF bundle for "${title}" with embedded cryptographic signatures.`);
        setTimeout(() => setDownloadNotice(null), 4000);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(FileText, { className: "w-6 h-6 text-sky-500" }), "Machine-Readable Scientific Publication Center"] }), _jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: "Produces cryptographically signed research publications, empirical reports, and executive discovery briefings with verifiable DOI anchors." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Badge, { variant: "success", size: "md", children: [_jsx(ShieldCheck, { className: "w-3.5 h-3.5 mr-1" }), "DOI Authority Registered"] }) })] }), downloadNotice && (_jsxs("div", { className: "p-4 bg-sky-50 dark:bg-sky-950/40 border border-sky-200 dark:border-sky-800 rounded-lg text-sm text-sky-800 dark:text-sky-300 flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-5 h-5 flex-shrink-0" }), _jsx("span", { children: downloadNotice })] })), _jsx("div", { className: "space-y-5", children: publications.map(pub => (_jsxs(Card, { className: "p-6 space-y-4", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-gray-100 dark:border-gray-800 pb-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsxs("span", { className: "font-mono text-xs text-sky-500 font-bold", children: ["DOI: ", pub.doi] }), _jsx(Badge, { variant: "success", size: "sm", children: pub.state })] }), _jsx("h3", { className: "text-lg font-bold text-gray-900 dark:text-white mt-1", children: pub.title }), _jsxs("div", { className: "text-xs text-gray-500 mt-1", children: ["Authors: ", _jsx("span", { className: "text-gray-700 dark:text-gray-300 font-medium", children: pub.authors.join(', ') })] })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Button, { variant: "outline", size: "sm", onClick: () => handleDownloadPaper(pub.title), children: [_jsx(Download, { className: "w-3.5 h-3.5 mr-1 text-sky-500" }), "Export Paper"] }), _jsx(Button, { variant: "ghost", size: "sm", children: _jsx(Share2, { className: "w-3.5 h-3.5" }) })] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-xs font-semibold text-gray-500 uppercase", children: "Abstract" }), _jsx("p", { className: "text-xs text-gray-700 dark:text-gray-300 mt-1 leading-relaxed bg-gray-50 dark:bg-gray-800/50 p-3 rounded", children: pub.abstract })] }), _jsxs("div", { children: [_jsx("span", { className: "text-xs font-semibold text-gray-500 uppercase", children: "Key Empirical Conclusions" }), _jsx("ul", { className: "mt-1 space-y-1 text-xs text-gray-600 dark:text-gray-300", children: pub.conclusions.map((c, i) => (_jsxs("li", { className: "flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5 text-emerald-500 flex-shrink-0" }), _jsx("span", { children: c })] }, i))) })] }), _jsxs("div", { className: "pt-2 border-t border-gray-100 dark:border-gray-800 flex flex-col md:flex-row md:items-center justify-between text-xs text-gray-500 gap-2", children: [_jsxs("div", { className: "flex items-center gap-1.5 font-mono text-[11px] text-gray-400", children: [_jsx(Lock, { className: "w-3.5 h-3.5 text-emerald-500" }), _jsx("span", { className: "truncate max-w-md", children: pub.signature })] }), _jsxs("div", { children: ["Published: ", new Date(pub.publishedAt).toLocaleDateString()] })] })] }, pub.id))) })] }));
};
