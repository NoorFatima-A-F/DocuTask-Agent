import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { BookOpen, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
export const OrganizationalLearningCenter = () => {
    const [insights, setInsights] = useState([]);
    const [loading, setLoading] = useState(false);
    const loadData = async () => {
        setLoading(true);
        try {
            const res = await fetch('/api/v1/cognitive/learning/insights?tenant_id=default-tenant');
            if (res.ok)
                setInsights(await res.json());
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadData();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(BookOpen, { className: "w-7 h-7 text-indigo-400" }), "Autonomous Organizational Learning Center"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Continuous distillation of cross-agent best practices, pattern mining, and emergent operational policies." })] }), _jsx(Button, { variant: "outline", onClick: loadData, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: insights.map((item, idx) => (_jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 space-y-3", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsx(Badge, { variant: "outline", className: "text-indigo-400 border-indigo-500/30", children: item.action || 'BEST_PRACTICE_DISTILLED' }), _jsx("span", { className: "text-[10px] text-slate-500 font-mono", children: item.discovered_at?.slice(0, 16) })] }), _jsx("h3", { className: "text-base font-semibold text-slate-200", children: item.topic }), _jsx("p", { className: "text-xs text-slate-300 bg-slate-800/40 p-3 rounded border border-slate-700/50", children: item.observation }), _jsx("div", { className: "pt-2 border-t border-slate-800 flex justify-between items-center text-xs text-emerald-400", children: _jsxs("span", { children: ["Policy: ", item.recommended_policy] }) })] }, idx))) })] }));
};
