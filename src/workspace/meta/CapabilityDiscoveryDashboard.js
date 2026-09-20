import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Search, Code2, Sparkles, CheckCircle2, } from 'lucide-react';
export const CapabilityDiscoveryDashboard = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [categoryFilter, setCategoryFilter] = useState('ALL');
    const capabilities = [
        {
            id: 'cap-801',
            name: 'Parallel Multi-Table Layout Extractor',
            category: 'WORKFLOW_TEMPLATE',
            description: 'Autonomous sub-DAG template that concurrently isolates, unmerges, and verifies multi-column tabular data in financial balance sheets.',
            synthesizedFrom: ['tesseract_engine', 'vision_transformer', 'sha256_verifier'],
            reusabilityScore: 0.985,
            inputContract: '{ document_pages: array, bounding_boxes: array }',
            outputContract: '{ structured_tables: array, confidence: float }',
            usageCount: 342,
        },
        {
            id: 'cap-802',
            name: 'Cryptographic Invariant Validator Agent Role',
            category: 'AGENT_ROLE',
            description: 'Specialized agent profile tailored for zero-fabrication mathematical auditing and schema consensus verification.',
            synthesizedFrom: ['VALIDATOR', 'REVIEWER', 'SECURITY'],
            reusabilityScore: 0.992,
            inputContract: '{ target_data: object, schema_hash: string }',
            outputContract: '{ audit_proof: string, passed: boolean }',
            usageCount: 890,
        },
        {
            id: 'cap-803',
            name: 'Triadic Verification Planner Pattern',
            category: 'PLANNER_PATTERN',
            description: 'Pattern orchestrating three independent specialized agents (Extractor, Verifier, Auditor) for high-stakes regulatory documents.',
            synthesizedFrom: ['APDLE_SCHEDULER', 'CONSENSUS_ENGINE'],
            reusabilityScore: 0.978,
            inputContract: '{ mission_goal: string, compliance_tier: string }',
            outputContract: '{ verified_dossier: object, merkle_hash: string }',
            usageCount: 154,
        },
    ];
    const filteredCapabilities = capabilities.filter((cap) => {
        const matchesSearch = cap.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            cap.description.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesCategory = categoryFilter === 'ALL' || cap.category === categoryFilter;
        return matchesSearch && matchesCategory;
    });
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Capability Discovery Dashboard" }), _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: true, children: "SYNTHESIS ACTIVE" }), _jsx(Badge, { variant: "outline", size: "sm", children: "AMRS-RSIP Phase 13.9" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Dynamic discovery of execution gaps, autonomous synthesis of composite tools, workflow templates, and specialized agent roles." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "intelligence", size: "sm", children: [_jsx(Sparkles, { className: "w-3.5 h-3.5 mr-1.5" }), "Synthesize Novel Capability"] }) })] }), _jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-4", children: [_jsx("div", { className: "flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0", children: ['ALL', 'WORKFLOW_TEMPLATE', 'AGENT_ROLE', 'PLANNER_PATTERN'].map((cat) => (_jsx(Button, { variant: categoryFilter === cat ? 'primary' : 'ghost', size: "sm", onClick: () => setCategoryFilter(cat), children: cat.replace('_', ' ') }, cat))) }), _jsxs("div", { className: "relative w-full sm:w-64", children: [_jsx(Search, { className: "w-3.5 h-3.5 absolute left-2.5 top-2.5 text-muted-foreground" }), _jsx("input", { type: "text", value: searchQuery, onChange: (e) => setSearchQuery(e.target.value), placeholder: "Search capabilities...", className: "w-full bg-secondary/50 text-xs rounded-md pl-8 pr-2 py-1.5 border border-border/40 focus:outline-none focus:border-primary" })] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: filteredCapabilities.map((cap) => (_jsxs(Card, { className: "p-5 border-border/40 space-y-4 hover:border-purple-500/30 transition-colors flex flex-col justify-between", children: [_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between gap-2", children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: cap.category.replace('_', ' ') }), _jsxs("span", { className: "text-xs font-mono text-muted-foreground", children: [cap.usageCount, " Executions"] })] }), _jsxs("div", { children: [_jsx("h2", { className: "text-sm font-semibold text-foreground", children: cap.name }), _jsx("p", { className: "text-xs text-muted-foreground mt-1 leading-relaxed", children: cap.description })] }), _jsxs("div", { className: "space-y-1.5 pt-1", children: [_jsx("span", { className: "text-[11px] text-muted-foreground", children: "Synthesized From Components:" }), _jsx("div", { className: "flex flex-wrap gap-1.5", children: cap.synthesizedFrom.map((src, idx) => (_jsx("span", { className: "text-[10px] font-mono px-2 py-0.5 rounded bg-secondary/60 text-secondary-foreground border border-border/40", children: src }, idx))) })] }), _jsxs("div", { className: "p-2.5 rounded bg-secondary/20 border border-border/30 space-y-1 text-[11px] font-mono text-muted-foreground", children: [_jsxs("div", { className: "flex items-center gap-1", children: [_jsx(Code2, { className: "w-3 h-3 text-purple-400" }), _jsxs("span", { children: ["Input: ", cap.inputContract] })] }), _jsxs("div", { className: "flex items-center gap-1", children: [_jsx(Code2, { className: "w-3 h-3 text-emerald-400" }), _jsxs("span", { children: ["Output: ", cap.outputContract] })] })] })] }), _jsxs("div", { className: "flex items-center justify-between text-xs pt-3 border-t border-border/30", children: [_jsxs("div", { className: "flex items-center gap-1 text-emerald-400 font-mono", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5" }), _jsxs("span", { children: ["Reusability: ", (cap.reusabilityScore * 100).toFixed(1), "%"] })] }), _jsx(Button, { variant: "outline", size: "sm", children: "Deploy Template" })] })] }, cap.id))) })] }));
};
