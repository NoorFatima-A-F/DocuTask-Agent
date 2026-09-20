import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { History, BrainCircuit, Sparkles, Sliders, CheckCircle, Database, ShieldCheck } from 'lucide-react';
export const LearningTimeline = () => {
    const events = [
        {
            id: 'evt-01',
            type: 'learning.reflection.started',
            title: 'Mission Reflection Initiated',
            missionId: 'mission-001',
            time: '10:04:12.110',
            icon: BrainCircuit,
            color: 'text-indigo-400',
            description: 'Loaded immutable execution trace and 44 runtime domain events for multi-perspective reflection.',
        },
        {
            id: 'evt-02',
            type: 'learning.pattern.detected',
            title: 'Parallel Wavefront Pattern Detected',
            missionId: 'mission-001',
            time: '10:04:12.340',
            icon: Sparkles,
            color: 'text-cyan-400',
            description: 'Discovered high-frequency 4-worker sharding pattern yielding 34.2% throughput speedup.',
        },
        {
            id: 'evt-03',
            type: 'learning.knowledge.extracted',
            title: 'Institutional Rule Extracted',
            missionId: 'mission-001',
            time: '10:04:12.580',
            icon: Database,
            color: 'text-emerald-400',
            description: 'Extracted verifiable concurrency rule with 0.965 confidence score and sealed cryptographic hash.',
        },
        {
            id: 'evt-04',
            type: 'learning.policy.proposed',
            title: 'Candidate Policy Synthesized',
            missionId: 'mission-001',
            time: '10:04:12.820',
            icon: Sliders,
            color: 'text-purple-400',
            description: 'Synthesized High-Throughput Wavefront Partitioning Policy with concurrency=8 and backoff=250ms.',
        },
        {
            id: 'evt-05',
            type: 'learning.policy.approved',
            title: 'Governance Approval Granted',
            missionId: 'mission-001',
            time: '10:04:13.150',
            icon: ShieldCheck,
            color: 'text-teal-400',
            description: 'Automated Governance Gatekeeper confirmed 100 counterfactual replays passed with zero regressions.',
        },
        {
            id: 'evt-06',
            type: 'learning.cycle.completed',
            title: 'Self-Improvement Cycle Sealed',
            missionId: 'mission-001',
            time: '10:04:13.400',
            icon: CheckCircle,
            color: 'text-emerald-400',
            description: 'Promoted candidate policy into live production registry. Lineage chain anchored.',
        },
    ];
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 rounded-xl text-indigo-400", children: _jsx(History, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Autonomous Learning & Evolution Timeline", _jsx(Badge, { variant: "intelligence", size: "sm", children: "Phase 13.5" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] font-mono", children: "Chronological domain event ledger tracing continuous cognitive reflection, mining, simulation, and promotion" })] })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx(Badge, { variant: "success", size: "md", children: "6 Events Recorded" }) })] }), _jsx(Card, { className: "p-6 rounded-2xl border border-[#1E293B] bg-[#0F172A] font-mono space-y-6", children: _jsx("div", { className: "relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-3 before:bottom-3 before:w-0.5 before:bg-[#1E293B]", children: events.map((evt) => {
                        const Icon = evt.icon;
                        return (_jsxs("div", { className: "relative flex items-start gap-4", children: [_jsx("div", { className: `p-1.5 rounded-full bg-[#0B1120] border border-[#334155] ${evt.color} shrink-0 -ml-6`, children: _jsx(Icon, { className: "w-4 h-4" }) }), _jsxs("div", { className: "flex-1 p-4 bg-[#0B1120] border border-[#1E293B] rounded-xl space-y-1.5 text-xs", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-2", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-white font-bold", children: evt.title }), _jsx(Badge, { variant: "outline", size: "sm", children: evt.type })] }), _jsx("span", { className: "text-[11px] text-[#64748B]", children: evt.time })] }), _jsx("p", { className: "text-[#94A3B8] leading-relaxed", children: evt.description }), _jsxs("div", { className: "text-[10px] text-[#64748B] pt-1", children: ["Mission: ", _jsx("span", { className: "text-indigo-400", children: evt.missionId }), " | Event ID: ", evt.id] })] })] }, evt.id));
                    }) }) })] }));
};
