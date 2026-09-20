import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { workforceApiClient } from '../../services/workforceApiClient';
import { Users, Zap, Plus } from 'lucide-react';
export const TeamFormationCenter = () => {
    const [teams, setTeams] = useState([]);
    const [teamName, setTeamName] = useState('');
    const [mission, setMission] = useState('');
    const [skills, setSkills] = useState('');
    const [budget, setBudget] = useState('200');
    useEffect(() => {
        workforceApiClient.getTeams().then(setTeams);
    }, []);
    const handleFormTeam = async () => {
        if (!teamName || !mission)
            return;
        const reqSkills = skills.split(',').map(s => s.trim()).filter(Boolean);
        const newTeam = await workforceApiClient.formTeam({
            team_name: teamName,
            mission,
            required_skills: reqSkills.length ? reqSkills : ['Document Extraction', 'OCR Verification'],
            max_budget_usd: parseFloat(budget) || 200
        });
        setTeams([...teams, newTeam]);
        setTeamName('');
        setMission('');
        setSkills('');
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "bg-slate-900/60 p-5 rounded-2xl border border-slate-800", children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx("span", { className: "p-2 bg-purple-500/20 text-purple-400 rounded-xl", children: "\u26A1" }), "Dynamic Team Formation Center"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Constraint-Optimized Autonomous Multi-Agent Task Forces" })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "p-5 bg-slate-900/50 border-slate-800 lg:col-span-1", children: [_jsxs("h3", { className: "text-base font-bold text-white mb-4 flex items-center gap-2", children: [_jsx(Zap, { className: "w-4 h-4 text-amber-400" }), " Assemble Task Force"] }), _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { children: [_jsx("label", { className: "text-xs text-slate-400 block mb-1", children: "Team Name" }), _jsx("input", { placeholder: "e.g. Audit Rapid Strike Force", value: teamName, onChange: (e) => setTeamName(e.target.value), className: "bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 text-sm w-full" })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs text-slate-400 block mb-1", children: "Mission Objective" }), _jsx("input", { placeholder: "e.g. Validate 5,000 PDF invoices with zero fabrication", value: mission, onChange: (e) => setMission(e.target.value), className: "bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 text-sm w-full" })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs text-slate-400 block mb-1", children: "Required Skills (comma-separated)" }), _jsx("input", { placeholder: "Document Extraction, OCR Verification", value: skills, onChange: (e) => setSkills(e.target.value), className: "bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 text-sm w-full" })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs text-slate-400 block mb-1", children: "Max Budget (USD)" }), _jsx("input", { placeholder: "200", value: budget, onChange: (e) => setBudget(e.target.value), className: "bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 text-sm w-full" })] }), _jsx(Button, { className: "w-full mt-2", onClick: handleFormTeam, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Plus, { className: "w-4 h-4" }), " Form Autonomous Team"] }) })] })] }), _jsxs("div", { className: "lg:col-span-2 space-y-4", children: [_jsxs("h3", { className: "text-base font-bold text-white flex items-center gap-2", children: [_jsx(Users, { className: "w-4 h-4 text-indigo-400" }), " Active Dynamic Teams"] }), _jsx("div", { className: "space-y-4", children: teams.map((t) => (_jsxs(Card, { className: "p-5 bg-slate-900/50 border-slate-800", children: [_jsxs("div", { className: "flex justify-between items-start mb-2", children: [_jsxs("div", { children: [_jsx("div", { className: "text-base font-bold text-white", children: t.team_name }), _jsx("div", { className: "text-xs text-slate-400 mt-0.5", children: t.mission })] }), _jsxs(Badge, { variant: "default", children: [Math.round(t.team_health_score * 100), "% Health"] })] }), _jsxs("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-3 my-4 p-3 bg-slate-950/60 rounded-xl border border-slate-800/80 text-xs", children: [_jsxs("div", { children: [_jsx("span", { className: "text-slate-500 block", children: "Team Lead" }), _jsx("strong", { className: "text-indigo-400", children: t.team_lead_id })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500 block", children: "Members" }), _jsxs("strong", { className: "text-white", children: [t.member_ids.length, " Agents"] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500 block", children: "Budget" }), _jsxs("strong", { className: "text-emerald-400", children: ["$", t.max_budget_usd] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500 block", children: "Target SLA" }), _jsxs("strong", { className: "text-amber-400", children: [t.sla_hours, "h"] })] })] }), _jsx("div", { className: "flex flex-wrap gap-1.5", children: t.required_skills.map((s, idx) => (_jsx("span", { className: "text-[10px] px-2 py-0.5 bg-slate-800 rounded border border-slate-700 text-slate-300", children: s }, idx))) })] }, t.id))) })] })] })] }));
};
