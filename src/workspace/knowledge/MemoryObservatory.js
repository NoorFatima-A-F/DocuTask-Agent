import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Cpu, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { knowledgeApiClient } from '../../services/knowledgeApiClient';
export const MemoryObservatory = () => {
    const [memories, setMemories] = useState([]);
    const [filterTier, setFilterTier] = useState('ALL');
    const loadMemories = async () => {
        const data = await knowledgeApiClient.listMemories();
        setMemories(data);
    };
    useEffect(() => {
        loadMemories();
    }, []);
    const filtered = memories.filter(m => filterTier === 'ALL' || m.tier === filterTier);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Cpu, { className: "w-7 h-7 text-indigo-400" }), "Autonomous Agent Memory Observatory"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Observe working memory, episodic history, organizational knowledge, and procedural execution SOPs." })] }), _jsx(Button, { variant: "outline", onClick: loadMemories, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: "w-4 h-4" }), "Refresh Memories"] }) })] }), _jsx("div", { className: "flex gap-2", children: ['ALL', 'SHORT_TERM', 'LONG_TERM', 'ORGANIZATIONAL', 'PROCEDURAL'].map((tier) => (_jsx(Button, { variant: filterTier === tier ? 'primary' : 'outline', size: "sm", onClick: () => setFilterTier(tier), children: tier.replace('_', ' ') }, tier))) }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: filtered.map((mem) => (_jsxs(Card, { className: "p-4 bg-slate-900/60 border-slate-800 space-y-3", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsx(Badge, { variant: "outline", className: "text-indigo-400 border-indigo-500/30", children: mem.tier }), _jsxs("span", { className: "text-xs font-mono text-slate-400", children: ["Access: ", mem.access_count, "x"] })] }), _jsx("h3", { className: "text-base font-semibold text-slate-200", children: mem.key }), _jsx("p", { className: "text-xs text-slate-300 bg-slate-800/40 p-3 rounded border border-slate-700", children: mem.content })] }, mem.id))) })] }));
};
