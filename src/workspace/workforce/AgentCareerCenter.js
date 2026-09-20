import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { workforceApiClient } from '../../services/workforceApiClient';
import { CheckCircle, ArrowUpRight } from 'lucide-react';
export const AgentCareerCenter = () => {
    const [paths, setPaths] = useState([]);
    useEffect(() => {
        workforceApiClient.getCareerPaths().then(setPaths);
    }, []);
    const handlePromote = async (id) => {
        const res = await workforceApiClient.executePromotion(id);
        setPaths(paths.map(p => p.id === id ? res : p));
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "bg-slate-900/60 p-5 rounded-2xl border border-slate-800", children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx("span", { className: "p-2 bg-emerald-500/20 text-emerald-400 rounded-xl", children: "\uD83C\uDF93" }), "Agent Career Center & Skill Progression"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Autonomous Role Advancement, Skill Certification, and Career Track Progression" })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6", children: paths.map((p) => (_jsxs(Card, { className: "p-5 bg-slate-900/50 border-slate-800", children: [_jsxs("div", { className: "flex justify-between items-start mb-3", children: [_jsxs("div", { children: [_jsx("div", { className: "text-base font-bold text-white", children: p.employee_id }), _jsxs("div", { className: "text-xs text-indigo-400 mt-0.5 flex items-center gap-1.5", children: [_jsx("span", { children: p.current_role }), _jsx("span", { children: "\u2192" }), _jsx("span", { className: "text-emerald-400 font-bold", children: p.target_role })] })] }), _jsx(Badge, { variant: p.status === 'PROMOTED' ? 'default' : 'outline', children: p.status })] }), _jsxs("div", { className: "my-4 p-3 bg-slate-950/60 rounded-xl border border-slate-800/80", children: [_jsxs("div", { className: "flex justify-between text-xs text-slate-400 mb-1", children: [_jsx("span", { children: "Eligibility Score" }), _jsxs("strong", { className: "text-emerald-400", children: [Math.round(p.eligibility_score * 100), "%"] })] }), _jsx("div", { className: "w-full bg-slate-800 h-1.5 rounded-full overflow-hidden", children: _jsx("div", { className: "bg-emerald-500 h-full", style: { width: `${p.eligibility_score * 100}%` } }) })] }), _jsxs("div", { className: "space-y-1.5 mb-4", children: [_jsx("div", { className: "text-[11px] font-semibold text-slate-400 uppercase tracking-wider", children: "Milestone Verification" }), p.completed_milestones.map((m, idx) => (_jsxs("div", { className: "text-xs text-slate-300 flex items-center gap-2", children: [_jsx(CheckCircle, { className: "w-3.5 h-3.5 text-emerald-400 shrink-0" }), _jsx("span", { children: m })] }, idx)))] }), _jsx("div", { className: "pt-2 flex justify-end", children: _jsx(Button, { size: "sm", variant: p.status === 'PROMOTED' ? 'outline' : 'primary', disabled: p.status === 'PROMOTED', onClick: () => handlePromote(p.id), children: _jsxs("span", { className: "flex items-center gap-1", children: [_jsx(ArrowUpRight, { className: "w-4 h-4" }), " ", p.status === 'PROMOTED' ? 'Promoted' : 'Authorize Promotion'] }) }) })] }, p.id))) })] }));
};
