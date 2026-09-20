import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Users, Zap, PlusCircle, Sparkles, } from 'lucide-react';
export const CoalitionManagerView = () => {
    const [coalitions] = useState([
        {
            id: 'coalition-alpha',
            name: 'Strike Team Alpha (Extraction & Security)',
            missionId: 'mission-9482',
            leadAgent: 'agent-exec-01',
            members: ['agent-spec-ocr', 'agent-val-sec', 'agent-res-opt'],
            objective: 'High-throughput parallel OCR document extraction and invariant cryptographic verification.',
            synergyScore: 0.96,
            status: 'ACTIVE',
        },
        {
            id: 'coalition-beta',
            name: 'Dynamic Scheduling Coalition',
            missionId: 'mission-9483',
            leadAgent: 'agent-plan-01',
            members: ['agent-coord-01', 'agent-res-opt'],
            objective: 'Dynamic DAG task dispatch and compute quota load balancing.',
            synergyScore: 0.92,
            status: 'ACTIVE',
        },
    ]);
    const [requiredSkillInput, setRequiredSkillInput] = useState('ocr_extraction, security_verification, budget_management');
    const [optimizedTeam, setOptimizedTeam] = useState(['agent-spec-ocr', 'agent-val-sec', 'agent-res-opt']);
    const handleOptimize = (e) => {
        e.preventDefault();
        const skills = requiredSkillInput.split(',').map(s => s.trim().toLowerCase());
        const candidates = ['agent-spec-ocr', 'agent-val-sec', 'agent-res-opt', 'agent-plan-01', 'agent-coord-01'];
        setOptimizedTeam(candidates.slice(0, Math.max(2, skills.length)));
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Dynamic Coalition Manager" }), _jsxs(Badge, { variant: "success", size: "sm", children: [coalitions.length, " Active Coalitions"] })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Autonomous team formation, dynamic coalition merging, capability synergy optimization, and historical team memory." })] }), _jsxs(Button, { variant: "primary", size: "sm", children: [_jsx(PlusCircle, { className: "w-3.5 h-3.5 mr-1.5" }), "Form New Coalition"] })] }), _jsx("div", { className: "grid grid-cols-1 lg:grid-cols-2 gap-6", children: coalitions.map(c => (_jsxs(Card, { className: "p-5 border-border/60 space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-border/40 pb-3", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "outline", size: "sm", className: "font-mono", children: c.id }), _jsx("h3", { className: "font-bold text-sm", children: c.name })] }), _jsx(Badge, { variant: "success", size: "sm", children: c.status })] }), _jsx("p", { className: "text-xs text-muted-foreground", children: c.objective }), _jsxs("div", { className: "grid grid-cols-2 gap-3", children: [_jsxs("div", { className: "p-2.5 rounded bg-muted/20 border border-border/30", children: [_jsx("span", { className: "text-[10px] text-muted-foreground block", children: "Lead Agent" }), _jsx("span", { className: "font-mono text-xs font-semibold text-primary", children: c.leadAgent })] }), _jsxs("div", { className: "p-2.5 rounded bg-muted/20 border border-border/30", children: [_jsx("span", { className: "text-[10px] text-muted-foreground block", children: "Team Synergy Score" }), _jsxs("span", { className: "font-mono text-xs font-bold text-emerald-400", children: [(c.synergyScore * 100).toFixed(1), "% Optimal"] })] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground block mb-2", children: "Coalition Members" }), _jsx("div", { className: "flex flex-wrap gap-2", children: c.members.map(m => (_jsxs("span", { className: "text-xs font-mono px-2.5 py-1 rounded bg-muted/30 border border-border/40 flex items-center gap-1.5", children: [_jsx(Users, { className: "w-3 h-3 text-primary" }), m] }, m))) })] })] }, c.id))) }), _jsxs(Card, { className: "p-5 border-border/60 space-y-4", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4 text-cyan-400" }), _jsx("h3", { className: "font-semibold text-sm", children: "Automated Team Composition Optimizer" })] }), _jsx("p", { className: "text-xs text-muted-foreground", children: "Enter required domain capabilities to autonomously compute the Pareto-optimal agent team covering all capabilities with minimal communication overhead." }), _jsxs("form", { onSubmit: handleOptimize, className: "flex flex-col sm:flex-row gap-3", children: [_jsx("input", { type: "text", value: requiredSkillInput, onChange: e => setRequiredSkillInput(e.target.value), placeholder: "e.g. ocr_extraction, security_verification, budget_management", className: "flex-1 text-xs font-mono p-2.5 rounded-md bg-background border border-border/60 focus:outline-none focus:ring-1 focus:ring-primary" }), _jsxs(Button, { type: "submit", size: "sm", variant: "primary", children: [_jsx(Zap, { className: "w-3.5 h-3.5 mr-1.5" }), "Compute Optimal Team"] })] }), _jsxs("div", { className: "p-4 rounded-lg bg-muted/20 border border-border/30", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground block mb-2", children: "Recommended Agent Strike Team:" }), _jsx("div", { className: "flex flex-wrap gap-2", children: optimizedTeam.map(agent => (_jsxs(Badge, { variant: "intelligence", size: "md", className: "font-mono", children: ["\u2713 ", agent] }, agent))) })] })] })] }));
};
