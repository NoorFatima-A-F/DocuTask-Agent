import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Database, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { cognitiveApiClient } from '../../services/cognitiveApiClient';
export const ExperienceMemoryExplorer = () => {
    const [experiences, setExperiences] = useState([]);
    const loadData = async () => {
        const data = await cognitiveApiClient.listExperiences();
        setExperiences(data);
    };
    useEffect(() => {
        loadData();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Database, { className: "w-7 h-7 text-indigo-400" }), "Cross-Agent Experience Memory Pool"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Enterprise pool of successful execution traces enabling instant zero-shot transfer across all agent fleets." })] }), _jsx(Button, { variant: "outline", onClick: loadData, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: "w-4 h-4" }), "Refresh Pool"] }) })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: experiences.map((exp) => (_jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 space-y-3", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsx(Badge, { variant: "outline", className: "text-indigo-400 border-indigo-500/30", children: exp.task_fingerprint }), _jsxs(Badge, { variant: "info", children: ["Reused: ", exp.reuse_count, "x"] })] }), _jsx("h3", { className: "text-sm font-semibold text-slate-200", children: exp.input_pattern }), _jsx("p", { className: "text-xs text-slate-300 bg-slate-800/40 p-3 rounded border border-slate-700/50", children: exp.reusable_knowledge }), _jsxs("div", { className: "pt-2 border-t border-slate-800 flex justify-between items-center text-xs text-slate-400", children: [_jsxs("span", { children: ["Agent Origin: ", exp.agent_id] }), _jsxs("span", { className: "font-mono text-emerald-400", children: ["Quality: ", ((exp.performance_metrics.quality_score || 0.99) * 100).toFixed(0), "%"] })] })] }, exp.id))) })] }));
};
