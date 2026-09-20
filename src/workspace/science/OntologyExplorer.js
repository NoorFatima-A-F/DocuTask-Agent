import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Network, Plus, Binary, Layers, Search, CheckCircle2, } from 'lucide-react';
export const OntologyExplorer = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [expandNotice, setExpandNotice] = useState(null);
    const concepts = [
        {
            id: 'concept_agent_latency',
            name: 'Agent Latency',
            domain: 'performance',
            definition: 'Turnaround response time of agent reasoning cycles.',
            confidence: 1.0,
        },
        {
            id: 'concept_memory_footprint',
            name: 'Memory Footprint',
            domain: 'resource',
            definition: 'RAM and context memory consumed by agent swarms.',
            confidence: 1.0,
        },
        {
            id: 'concept_swarm_throughput',
            name: 'Swarm Throughput',
            domain: 'throughput',
            definition: 'Completed autonomous operations per unit time.',
            confidence: 1.0,
        },
        {
            id: 'concept_context_entropy',
            name: 'Context Entropy',
            domain: 'cognition',
            definition: 'Information disorder and token drift in cognitive memory.',
            confidence: 0.95,
        },
        {
            id: 'concept_speculative_cache',
            name: 'Speculative Tensor Cache',
            domain: 'caching',
            definition: 'GPU tensor cache pre-warming for recurring document schemas.',
            confidence: 0.98,
        },
    ];
    const relations = [
        { id: 'rel_1', from: 'concept_speculative_cache', to: 'concept_agent_latency', type: 'optimizes', weight: 0.95 },
        { id: 'rel_2', from: 'concept_memory_footprint', to: 'concept_agent_latency', type: 'correlates_with', weight: 0.75 },
        { id: 'rel_3', from: 'concept_context_entropy', to: 'concept_speculative_cache', type: 'regulates', weight: 0.88 },
        { id: 'rel_4', from: 'concept_agent_latency', to: 'concept_swarm_throughput', type: 'causes', weight: 0.92 },
    ];
    const handleExpandOntology = () => {
        setExpandNotice('Ontology Engine expanded semantic graph: Discovered 1 new conceptual link [Speculative Cache -> Swarm Throughput] via transitive graph closure.');
        setTimeout(() => setExpandNotice(null), 4000);
    };
    const filteredConcepts = concepts.filter(c => c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.domain.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.definition.toLowerCase().includes(searchQuery.toLowerCase()));
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(Network, { className: "w-6 h-6 text-indigo-500" }), "Dynamic Semantic Ontology Explorer"] }), _jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: "Dynamically expands the platform's ontological taxonomy, conceptual relations, and causal pathways across discovered scientific laws." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "intelligence", size: "sm", onClick: handleExpandOntology, children: [_jsx(Plus, { className: "w-3.5 h-3.5 mr-1.5" }), "Discover Semantic Relations"] }) })] }), expandNotice && (_jsxs("div", { className: "p-4 bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800 rounded-lg text-sm text-indigo-800 dark:text-indigo-300 flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-5 h-5 flex-shrink-0" }), _jsx("span", { children: expandNotice })] })), _jsxs("div", { className: "relative", children: [_jsx(Search, { className: "w-4 h-4 text-gray-400 absolute left-3 top-3" }), _jsx("input", { type: "text", placeholder: "Search ontology concepts or domains...", value: searchQuery, onChange: e => setSearchQuery(e.target.value), className: "w-full pl-9 pr-4 py-2 text-xs border rounded-lg dark:bg-gray-800 dark:border-gray-700 text-gray-900 dark:text-white" })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "lg:col-span-2 space-y-3", children: [_jsxs("h3", { className: "text-xs font-semibold text-gray-500 uppercase tracking-wider flex items-center gap-1.5", children: [_jsx(Binary, { className: "w-4 h-4 text-indigo-500" }), "Ontological Concepts (", filteredConcepts.length, ")"] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-3", children: filteredConcepts.map(c => (_jsxs(Card, { className: "p-4 space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-semibold text-sm text-gray-900 dark:text-white", children: c.name }), _jsx(Badge, { variant: "outline", size: "sm", children: c.domain })] }), _jsx("p", { className: "text-xs text-gray-600 dark:text-gray-300", children: c.definition }), _jsxs("div", { className: "flex items-center justify-between text-[11px] text-gray-400 pt-1 border-t border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "font-mono text-[10px]", children: c.id }), _jsxs("span", { className: "text-emerald-600", children: [(c.confidence * 100).toFixed(0), "% Conf"] })] })] }, c.id))) })] }), _jsxs("div", { className: "space-y-3", children: [_jsxs("h3", { className: "text-xs font-semibold text-gray-500 uppercase tracking-wider flex items-center gap-1.5", children: [_jsx(Layers, { className: "w-4 h-4 text-purple-500" }), "Semantic Relations (", relations.length, ")"] }), _jsx("div", { className: "space-y-2", children: relations.map(rel => (_jsxs(Card, { className: "p-3 text-xs space-y-1", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-semibold text-purple-600 dark:text-purple-400 uppercase text-[10px] tracking-wider", children: rel.type }), _jsxs(Badge, { variant: "outline", size: "sm", children: ["Weight: ", rel.weight] })] }), _jsxs("div", { className: "text-gray-800 dark:text-gray-200 font-mono text-[11px] flex items-center gap-1", children: [_jsx("span", { children: rel.from.replace('concept_', '') }), _jsx("span", { className: "text-purple-400", children: "\u2192" }), _jsx("span", { children: rel.to.replace('concept_', '') })] })] }, rel.id))) })] })] })] }));
};
