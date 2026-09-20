import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Filter, Search, FileText, Shield, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { knowledgeApiClient } from '../../services/knowledgeApiClient';
export const KnowledgeExplorer = () => {
    const [assets, setAssets] = useState([]);
    const [search, setSearch] = useState('');
    const [filterType, setFilterType] = useState('ALL');
    const [loading, setLoading] = useState(false);
    const loadAssets = async () => {
        setLoading(true);
        try {
            const data = await knowledgeApiClient.listAssets();
            setAssets(data);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadAssets();
    }, []);
    const filtered = assets.filter(a => {
        const matchSearch = a.name.toLowerCase().includes(search.toLowerCase()) ||
            a.raw_content.toLowerCase().includes(search.toLowerCase());
        const matchType = filterType === 'ALL' || a.source_type === filterType;
        return matchSearch && matchType;
    });
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(FileText, { className: "w-7 h-7 text-indigo-400" }), "Enterprise Knowledge Explorer"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Browse, search, and inspect ingested organizational documents, datasets, policies, and metadata." })] }), _jsx(Button, { variant: "outline", onClick: loadAssets, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] }), _jsxs(Card, { className: "p-4 bg-slate-900/60 border-slate-800 flex flex-wrap gap-4 items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-3 flex-1 min-w-[280px]", children: [_jsx(Search, { className: "w-4 h-4 text-slate-400" }), _jsx("input", { placeholder: "Search documents, policies, or topics...", value: search, onChange: (e) => setSearch(e.target.value), className: "flex-1 px-3 py-2 bg-slate-800/80 border border-slate-700 rounded-lg text-slate-200 text-sm focus:outline-none focus:border-indigo-500" })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Filter, { className: "w-4 h-4 text-slate-400" }), _jsx("span", { className: "text-xs text-slate-400", children: "Source:" }), ['ALL', 'LOCAL_DOCUMENT', 'GOOGLE_DRIVE', 'CONFLUENCE'].map((type) => (_jsx(Button, { variant: filterType === type ? 'primary' : 'outline', size: "sm", onClick: () => setFilterType(type), children: type.replace('_', ' ') }, type)))] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: filtered.map((asset) => (_jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 flex flex-col justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex justify-between items-start mb-2", children: [_jsx(Badge, { variant: "outline", className: "text-indigo-400 border-indigo-500/30", children: asset.source_type }), _jsx(Badge, { variant: asset.security_classification === 'CONFIDENTIAL' ? 'warning' : 'info', children: asset.security_classification })] }), _jsx("h3", { className: "text-base font-semibold text-slate-200 mb-1", children: asset.name }), _jsx("p", { className: "text-xs text-slate-400 line-clamp-3 mb-3", children: asset.processed_content || asset.raw_content })] }), _jsxs("div", { className: "pt-3 border-t border-slate-800 text-xs text-slate-400 flex justify-between items-center", children: [_jsxs("span", { children: ["Tokens: ", asset.metadata.token_count || 320] }), _jsxs("div", { className: "flex items-center gap-1 text-emerald-400", children: [_jsx(Shield, { className: "w-3.5 h-3.5" }), _jsxs("span", { children: ["Reliability: ", ((asset.reliability_score || 0.95) * 100).toFixed(0), "%"] })] })] })] }, asset.id))) })] }));
};
