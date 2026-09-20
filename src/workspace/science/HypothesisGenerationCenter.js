import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Compass, Plus, CheckCircle2, HelpCircle, Filter, } from 'lucide-react';
export const HypothesisGenerationCenter = () => {
    const [selectedDomain, setSelectedDomain] = useState('all');
    const [notice, setNotice] = useState(null);
    const hypotheses = [
        {
            id: 'hyp-spec-tensor-01',
            title: 'Speculative Layout Cache Invariant',
            statement: 'Retaining speculative tensor embeddings for corporate invoice headers with >=5 hits/hr reduces P95 extraction latency by >=25%.',
            domain: 'performance',
            rationale: 'Analysis of 50,000 corporate invoices indicates 85% header spatial layout redundancy.',
            prior: 0.82,
            eig: 0.915,
            status: 'EXPERIMENTING',
            variables: ['tensor_cache_ttl', 'header_entropy', 'vram_allocation_mb'],
            ageDays: 1,
        },
        {
            id: 'hyp-triadic-coalition-02',
            title: 'Triadic Specialization Scaling Invariant',
            statement: 'Grouping agents into 3-member specialist triadic teams (Parser, Segmenter, Validator) eliminates 90% of auction negotiation jitter.',
            domain: 'swarm_dynamics',
            rationale: 'Auction bidding protocols experience 42ms scheduling overhead under high concurrency.',
            prior: 0.78,
            eig: 0.860,
            status: 'PROPOSED',
            variables: ['cluster_size', 'auction_round_count', 'task_throughput'],
            ageDays: 3,
        },
        {
            id: 'hyp-lockfree-ring-03',
            title: 'Lock-Free Ring Buffer Telemetry Invariant',
            statement: 'Migrating memory telemetry from mutex locks to atomic circular buffers reduces state synchronization stalls to zero across 64 concurrent workers.',
            domain: 'resilience',
            rationale: 'Mutex contention caused 180ms stalls in historical stress runs.',
            prior: 0.95,
            eig: 0.940,
            status: 'CONFIRMED',
            variables: ['buffer_lock_type', 'worker_concurrency', 'commit_latency'],
            ageDays: 7,
        },
        {
            id: 'hyp-quant-memory-04',
            title: 'Int8 Vector Quantization Recall Invariant',
            statement: 'Quantizing scratchpad vector representations from FP32 to Int8 retains >=99% semantic accuracy while reducing memory bandwidth by 50%.',
            domain: 'memory',
            rationale: 'High-dimensional embeddings exhibit significant sparsity in intermediate layers.',
            prior: 0.88,
            eig: 0.890,
            status: 'CONFIRMED',
            variables: ['quantization_bits', 'semantic_recall_pct', 'memory_bandwidth'],
            ageDays: 5,
        },
    ];
    const filteredHypotheses = selectedDomain === 'all'
        ? hypotheses
        : hypotheses.filter(h => h.domain === selectedDomain);
    const handleFormulateHypothesis = () => {
        setNotice('Autonomous Knowledge Gap Scanner formulated 1 new hypothesis for Memory Caching with EIG = 0.892.');
        setTimeout(() => setNotice(null), 4000);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(Compass, { className: "w-6 h-6 text-indigo-500" }), "Hypothesis Generation & Knowledge Gap Studio"] }), _jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: "Formulates testable scientific propositions driven by Expected Information Gain (EIG), Bayesian priors, and causal assumption mining." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "intelligence", size: "sm", onClick: handleFormulateHypothesis, children: [_jsx(Plus, { className: "w-3.5 h-3.5 mr-1.5" }), "Mine Knowledge Gaps & Formulate"] }) })] }), notice && (_jsxs("div", { className: "p-4 bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800 rounded-lg text-sm text-indigo-800 dark:text-indigo-300 flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-5 h-5 flex-shrink-0" }), _jsx("span", { children: notice })] })), _jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Filter, { className: "w-4 h-4 text-gray-400" }), _jsx("span", { className: "text-xs text-gray-500", children: "Domain Filter:" }), ['all', 'performance', 'swarm_dynamics', 'resilience', 'memory'].map(d => (_jsx("button", { onClick: () => setSelectedDomain(d), className: `px-2.5 py-1 text-xs rounded-full border transition-colors ${selectedDomain === d
                                    ? 'bg-indigo-600 text-white border-indigo-600'
                                    : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 border-gray-200 dark:border-gray-700 hover:bg-gray-50'}`, children: d.replace('_', ' ').toUpperCase() }, d)))] }), _jsxs("div", { className: "flex items-center gap-3 text-xs text-gray-500", children: [_jsxs("span", { children: ["Active Hypotheses: ", _jsx("strong", { className: "text-gray-900 dark:text-white", children: filteredHypotheses.length })] }), _jsxs("span", { children: ["Mean Prior: ", _jsx("strong", { className: "text-emerald-600", children: "85.7%" })] }), _jsxs("span", { children: ["Mean EIG: ", _jsx("strong", { className: "text-indigo-600", children: "0.901" })] })] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: filteredHypotheses.map(hypo => (_jsxs(Card, { className: "p-5 space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between gap-2", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-xs text-indigo-500", children: hypo.id }), _jsx(Badge, { variant: hypo.status === 'CONFIRMED' ? 'success' :
                                                        hypo.status === 'EXPERIMENTING' ? 'warning' : 'info', size: "sm", children: hypo.status })] }), _jsx("h3", { className: "font-semibold text-gray-900 dark:text-white mt-1", children: hypo.title })] }), _jsxs(Badge, { variant: "outline", size: "sm", children: ["EIG: ", hypo.eig.toFixed(3)] })] }), _jsxs("p", { className: "text-xs text-gray-600 dark:text-gray-300 bg-gray-50 dark:bg-gray-800/50 p-2.5 rounded border border-gray-100 dark:border-gray-700/60", children: ["\"", hypo.statement, "\""] }), _jsxs("div", { className: "text-xs text-gray-500 dark:text-gray-400", children: [_jsx("strong", { className: "text-gray-700 dark:text-gray-300", children: "Empirical Premise:" }), " ", hypo.rationale] }), _jsxs("div", { className: "flex flex-wrap items-center gap-1.5 pt-1", children: [_jsx("span", { className: "text-[10px] text-gray-400", children: "Variables:" }), hypo.variables.map(v => (_jsx("span", { className: "text-[10px] font-mono px-1.5 py-0.5 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded", children: v }, v)))] }), _jsxs("div", { className: "flex items-center justify-between pt-2 border-t border-gray-100 dark:border-gray-800 text-xs", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-gray-400", children: "Prior:" }), _jsxs("span", { className: "font-medium text-emerald-600 dark:text-emerald-400", children: [(hypo.prior * 100).toFixed(0), "%"] })] }), _jsxs("span", { className: "text-gray-400", children: ["Age: ", hypo.ageDays, "d"] })] })] }, hypo.id))) }), _jsxs(Card, { className: "p-5 space-y-4", children: [_jsxs("h3", { className: "font-semibold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(HelpCircle, { className: "w-4 h-4 text-amber-500" }), "Detected Knowledge Gaps & Uncharacterized Regimes"] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-3", children: [_jsxs("div", { className: "p-3 bg-amber-50/50 dark:bg-amber-950/20 rounded border border-amber-200 dark:border-amber-800/40", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-amber-900 dark:text-amber-300", children: "Layout Embedding Cache Pre-Warming" }), _jsx(Badge, { variant: "warning", size: "sm", children: "Severity: High" })] }), _jsx("p", { className: "text-xs text-gray-600 dark:text-gray-400 mt-1", children: "Optimal pre-warming batch size across multi-vendor accounting documents remains uncharacterized." })] }), _jsxs("div", { className: "p-3 bg-sky-50/50 dark:bg-sky-950/20 rounded border border-sky-200 dark:border-sky-800/40", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-sky-900 dark:text-sky-300", children: "Inter-Agent Comm Burst Latency" }), _jsx(Badge, { variant: "info", size: "sm", children: "Severity: Medium" })] }), _jsx("p", { className: "text-xs text-gray-600 dark:text-gray-400 mt-1", children: "Inter-agent shared scratchpad communication latency under >1000 doc/sec bursts." })] })] })] })] }));
};
