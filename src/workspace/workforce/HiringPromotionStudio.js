import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { workforceApiClient } from '../../services/workforceApiClient';
import { UserPlus } from 'lucide-react';
export const HiringPromotionStudio = () => {
    const [reqs, setReqs] = useState([]);
    useEffect(() => {
        workforceApiClient.getRequisitions().then(setReqs);
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "bg-slate-900/60 p-5 rounded-2xl border border-slate-800", children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx("span", { className: "p-2 bg-teal-500/20 text-teal-400 rounded-xl", children: "\uD83C\uDFAF" }), "Autonomous Hiring & Requisition Studio"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Demand-Triggered Agent Requisitions, Profile Generation & Fleet Expansion" })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6", children: reqs.map((r) => (_jsxs(Card, { className: "p-5 bg-slate-900/50 border-slate-800", children: [_jsxs("div", { className: "flex justify-between items-start mb-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "text-base font-bold text-white", children: [r.target_role, " Requisition"] }), _jsxs("div", { className: "text-xs text-slate-400", children: [r.department, " \u2022 Reason: ", r.reason] })] }), _jsx(Badge, { variant: "default", children: r.status })] }), _jsxs("div", { className: "space-y-2 my-4", children: [_jsx("div", { className: "text-[11px] font-semibold text-slate-400 uppercase", children: "Top Automated Candidates" }), r.candidate_profiles.map((c, idx) => (_jsxs("div", { className: "p-3 bg-slate-950/60 rounded-xl border border-slate-800 flex justify-between items-center text-xs", children: [_jsxs("div", { children: [_jsx("strong", { className: "text-white", children: c.name }), _jsxs("div", { className: "text-[10px] text-slate-400", children: ["Match Score: ", Math.round(c.score * 100), "%"] })] }), _jsx(Button, { size: "sm", variant: "outline", children: _jsxs("span", { className: "flex items-center gap-1", children: [_jsx(UserPlus, { className: "w-3.5 h-3.5" }), " Auto-Hire"] }) })] }, idx)))] })] }, r.id))) })] }));
};
