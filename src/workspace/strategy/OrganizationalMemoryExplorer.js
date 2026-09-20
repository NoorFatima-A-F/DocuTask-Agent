import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { BookOpen, Search, } from 'lucide-react';
export const OrganizationalMemoryExplorer = () => {
    const [selectedCategory, setSelectedCategory] = useState('ALL');
    const [searchQuery, setSearchQuery] = useState('');
    const knowledgeEntries = [
        {
            id: 'playbook-triadic-01',
            category: 'PLAYBOOK',
            title: 'Triadic Coalition Strategy for Complex Tables',
            description: 'Use a 3-agent team (Header Parser, Grid Segmenter, Data Validator) with shared scratchpad to bypass auction renegotiation.',
            tags: ['playbook', 'tables', 'coalition', 'throughput'],
            confidence: 0.992,
            usageCount: 380,
            successRate: 0.996,
        },
        {
            id: 'lesson-cache-warm-02',
            category: 'LESSON_LEARNED',
            title: 'Recurrent Corporate Invoice Header Redundancy',
            description: '85% of corporate invoices share identical token sequences in the upper 20% bounding region, yielding 28% latency reduction via caching.',
            tags: ['caching', 'invoices', 'latency', 'gpu'],
            confidence: 0.988,
            usageCount: 520,
            successRate: 0.991,
        },
        {
            id: 'antipattern-bidding-03',
            category: 'ANTI_PATTERN',
            title: 'Unbounded Inter-Agent Bidding in High-Concurrency Batches',
            description: 'Real-time multi-agent bidding during >500 doc/sec surges increases scheduling jitter by 42ms. Use pre-allocated task coalitions instead.',
            tags: ['bidding', 'swarm', 'latency', 'anti_pattern'],
            confidence: 0.975,
            usageCount: 95,
            successRate: 0.980,
        },
        {
            id: 'postmortem-lock-04',
            category: 'FAILURE_POSTMORTEM',
            title: 'State Lock Contention on Global Memory Stream',
            description: 'Simultaneous 32-worker telemetry commits locked memory table for 180ms. Resolved by migrating to lock-free ring buffers.',
            tags: ['resilience', 'locks', 'ring_buffer', 'postmortem'],
            confidence: 0.995,
            usageCount: 45,
            successRate: 1.0,
        },
        {
            id: 'strategy-zk-verify-05',
            category: 'SUCCESS_STRATEGY',
            title: 'Continuous SHA-256 Checkpoint Verification',
            description: 'Cryptographic hashing of state snapshots prior to destructive interventions enables zero-downtime micro-rollbacks.',
            tags: ['security', 'cryptography', 'governance', 'rollback'],
            confidence: 0.999,
            usageCount: 1240,
            successRate: 0.999,
        },
    ];
    const filteredEntries = knowledgeEntries.filter((k) => {
        const matchCategory = selectedCategory === 'ALL' || k.category === selectedCategory;
        const matchSearch = searchQuery === '' ||
            k.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            k.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
            k.tags.some((t) => t.toLowerCase().includes(searchQuery.toLowerCase()));
        return matchCategory && matchSearch;
    });
    const getCategoryBadgeVariant = (category) => {
        switch (category) {
            case 'PLAYBOOK':
                return 'intelligence';
            case 'SUCCESS_STRATEGY':
                return 'success';
            case 'LESSON_LEARNED':
                return 'default';
            case 'ANTI_PATTERN':
                return 'warning';
            case 'FAILURE_POSTMORTEM':
                return 'error';
            default:
                return 'default';
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(BookOpen, { className: "w-6 h-6 text-indigo-500" }), "Organizational Memory & Institutional Knowledge Center"] }), _jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: "Phase 13.11 \u2014 Collective knowledge repository preserving playbooks, empirical lessons, anti-patterns, and postmortems." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Badge, { variant: "intelligence", size: "md", children: [knowledgeEntries.length, " Verified Playbooks & Insights"] }) })] }), _jsxs("div", { className: "flex flex-col md:flex-row gap-3", children: [_jsxs("div", { className: "relative flex-1", children: [_jsx(Search, { className: "w-4 h-4 absolute left-3 top-3 text-gray-400" }), _jsx("input", { type: "text", placeholder: "Search playbooks, lessons, anti-patterns, tags...", value: searchQuery, onChange: (e) => setSearchQuery(e.target.value), className: "w-full pl-9 pr-4 py-2 text-xs rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500" })] }), _jsx("div", { className: "flex gap-1.5 flex-wrap", children: ['ALL', 'PLAYBOOK', 'LESSON_LEARNED', 'ANTI_PATTERN', 'FAILURE_POSTMORTEM', 'SUCCESS_STRATEGY'].map((cat) => (_jsx("button", { onClick: () => setSelectedCategory(cat), className: `px-3 py-1.5 text-xs font-semibold rounded-md transition-colors ${selectedCategory === cat
                                ? 'bg-indigo-600 text-white shadow-sm'
                                : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:text-indigo-600'}`, children: cat.replace('_', ' ') }, cat))) })] }), _jsx("div", { className: "grid grid-cols-1 gap-4", children: filteredEntries.map((k) => (_jsxs(Card, { className: "p-5 hover:shadow-md transition-shadow", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-xs text-indigo-600 dark:text-indigo-400 font-semibold", children: k.id }), _jsx(Badge, { variant: getCategoryBadgeVariant(k.category), size: "sm", children: k.category.replace('_', ' ') })] }), _jsx("h4", { className: "font-semibold text-gray-900 dark:text-white text-base mt-1", children: k.title })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsxs("div", { className: "text-right", children: [_jsx("span", { className: "text-xs text-gray-400 block", children: "Usage Replays" }), _jsxs("span", { className: "text-base font-bold text-gray-900 dark:text-white font-mono", children: [k.usageCount, " times"] })] }) })] }), _jsx("p", { className: "text-xs text-gray-600 dark:text-gray-300 mt-3", children: k.description }), _jsxs("div", { className: "mt-4 flex flex-col md:flex-row md:items-center justify-between gap-2 pt-3 border-t border-gray-100 dark:border-gray-800 text-xs", children: [_jsx("div", { className: "flex items-center gap-1.5 flex-wrap", children: k.tags.map((t, idx) => (_jsxs("span", { className: "px-2 py-0.5 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded-full font-mono text-[10px]", children: ["#", t] }, idx))) }), _jsxs("div", { className: "flex items-center gap-4 text-gray-400", children: [_jsxs("span", { children: ["Confidence: ", _jsxs("strong", { className: "text-purple-600 dark:text-purple-400", children: [(k.confidence * 100).toFixed(1), "%"] })] }), _jsx("span", { children: "\u2022" }), _jsxs("span", { children: ["Success Rate: ", _jsxs("strong", { className: "text-emerald-600 dark:text-emerald-400", children: [(k.successRate * 100).toFixed(1), "%"] })] })] })] })] }, k.id))) })] }));
};
