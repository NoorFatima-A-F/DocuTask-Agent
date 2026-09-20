import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Search, Sparkles, Sliders } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { knowledgeApiClient } from '../../services/knowledgeApiClient';
export const SemanticSearchStudio = () => {
    const [query, setQuery] = useState('procurement approval threshold for vendor contracts');
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [clearance, setClearance] = useState('CONFIDENTIAL');
    const handleSearch = async () => {
        if (!query.trim())
            return;
        setLoading(true);
        try {
            const data = await knowledgeApiClient.search(query, 5);
            setResults(data);
        }
        finally {
            setLoading(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Search, { className: "w-7 h-7 text-indigo-400" }), "Semantic Search & Hybrid Retrieval Studio"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Perform multi-modal vector similarity, keyword BM25 matching, and security-governed enterprise retrieval." })] }), _jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 space-y-4", children: [_jsxs("div", { className: "flex gap-3", children: [_jsxs("div", { className: "relative flex-1", children: [_jsx(Search, { className: "w-5 h-5 text-slate-400 absolute left-3 top-3" }), _jsx("input", { value: query, onChange: (e) => setQuery(e.target.value), placeholder: "Ask questions or enter search query across all organizational data...", className: "w-full pl-10 pr-4 py-2.5 bg-slate-800/80 border border-slate-700 rounded-lg text-slate-200 text-sm focus:outline-none focus:border-indigo-500", onKeyDown: (e) => e.key === 'Enter' && handleSearch() })] }), _jsx(Button, { variant: "intelligence", onClick: handleSearch, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4" }), loading ? 'Searching...' : 'Hybrid Search'] }) })] }), _jsxs("div", { className: "flex flex-wrap items-center justify-between pt-2 border-t border-slate-800 text-xs text-slate-400", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Sliders, { className: "w-4 h-4 text-slate-400" }), _jsx("span", { children: "Security Clearance:" }), ['PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED'].map((lvl) => (_jsx(Button, { variant: clearance === lvl ? 'primary' : 'outline', size: "sm", onClick: () => setClearance(lvl), children: lvl }, lvl)))] }), _jsx("span", { children: "Algorithm: Cosine Similarity (0.7) + BM25 Keyword Overlap (0.3)" })] })] }), _jsxs("div", { className: "space-y-3", children: [_jsxs("h2", { className: "text-lg font-semibold text-slate-200", children: ["Retrieved Grounded Snippets (", results.length, ")"] }), results.map((res, idx) => (_jsxs(Card, { className: "p-4 bg-slate-900/60 border-slate-800 hover:border-indigo-500/40 transition-colors", children: [_jsxs("div", { className: "flex justify-between items-start mb-2", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "outline", className: "text-indigo-400 border-indigo-500/30", children: res.matched_via }), _jsx(Badge, { variant: "info", children: res.source_type }), _jsx(Badge, { variant: res.security_classification === 'CONFIDENTIAL' ? 'warning' : 'outline', children: res.security_classification })] }), _jsxs("span", { className: "text-xs font-mono text-emerald-400", children: ["Score: ", (res.score * 100).toFixed(1), "%"] })] }), _jsx("h3", { className: "text-base font-semibold text-slate-200 mb-1", children: res.title }), _jsx("p", { className: "text-sm text-slate-300 bg-slate-800/40 p-3 rounded border border-slate-700/50", children: res.content })] }, idx)))] })] }));
};
