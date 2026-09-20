import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { useMissionControl } from '../../context/MissionControlContext';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { StatusIndicator } from '../ui/StatusIndicator';
export const AgentCollaborationSection = () => {
    const { state } = useMissionControl();
    const { agentTeam, thoughtStream } = state;
    const [filterRole, setFilterRole] = useState('ALL');
    const filteredThoughts = filterRole === 'ALL'
        ? thoughtStream
        : thoughtStream.filter((t) => t.agentRole === filterRole);
    const getAgentStatusType = (stateVal) => {
        switch (stateVal) {
            case 'THINKING':
            case 'OBSERVING':
            case 'PLANNING':
                return 'thinking';
            case 'EXECUTING':
                return 'executing';
            case 'VERIFYING':
                return 'verifying';
            case 'LEARNING':
                return 'learning';
            case 'WAITING_FOR_HITL':
                return 'waiting';
            case 'IDLE':
            default:
                return 'idle';
        }
    };
    return (_jsx("section", { className: "w-full mt-8", children: _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-12 gap-6", children: [_jsx("div", { className: "lg:col-span-7", children: _jsxs(Card, { variant: "default", className: "border-[#1E293B] bg-[#0F172A]/80 backdrop-blur-md h-full", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between pb-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: "MULTI-AGENT FLEET" }), _jsx("span", { className: "text-xs text-[#94A3B8] font-mono", children: "10 Specialized Roles" })] }), _jsx(CardTitle, { className: "mt-2 text-lg font-bold text-[#F8FAFC]", children: "Autonomous Agent Team" })] }), _jsx("div", { className: "flex items-center gap-2 text-xs font-mono text-[#10B981] bg-[#131D35] px-3 py-1.5 rounded-lg border border-[#334155]/60", children: _jsx("span", { children: "Fleet Health: 100% OK" }) })] }), _jsx(CardContent, { className: "p-4 grid grid-cols-1 sm:grid-cols-2 gap-3 max-h-[560px] overflow-y-auto", children: agentTeam.map((agent) => (_jsxs("div", { onClick: () => setFilterRole(filterRole === agent.role ? 'ALL' : agent.role), className: `p-3.5 rounded-xl border transition-all cursor-pointer ${filterRole === agent.role
                                        ? 'bg-[#1E293B] border-cyan-400 shadow-[0_0_15px_rgba(0,210,255,0.25)]'
                                        : 'bg-[#131D35]/70 border-[#1E293B] hover:border-[#334155] hover:bg-[#1E293B]/40'}`, children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-bold text-[#F8FAFC]", children: agent.name }), _jsx(StatusIndicator, { status: getAgentStatusType(agent.state), showPulse: agent.state !== 'IDLE', size: "sm" })] }), _jsxs("p", { className: "mt-2 text-[11px] text-[#94A3B8] line-clamp-1", children: ["\uD83C\uDFAF ", agent.currentGoal] }), _jsxs("div", { className: "mt-3 pt-2 border-t border-[#1E293B]/80 flex items-center justify-between text-[10px] font-mono text-[#64748B]", children: [_jsxs("span", { children: [(agent.confidence * 100).toFixed(0), "% conf"] }), _jsxs("span", { children: [agent.thinkingDurationMs, "ms"] }), _jsxs("span", { children: ["Q: ", agent.queueSize] })] })] }, agent.agentId))) })] }) }), _jsx("div", { className: "lg:col-span-5", children: _jsxs(Card, { variant: "default", className: "border-[#1E293B] bg-[#0F172A]/80 backdrop-blur-md h-full flex flex-col", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between pb-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsxs("span", { className: "relative flex h-2 w-2", children: [_jsx("span", { className: "animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75" }), _jsx("span", { className: "relative inline-flex rounded-full h-2 w-2 bg-[#00D2FF]" })] }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "LIVE AGENT THOUGHTS" })] }), _jsx(CardTitle, { className: "mt-2 text-lg font-bold text-[#F8FAFC]", children: "Cognition Thought Stream" })] }), filterRole !== 'ALL' && (_jsxs("button", { onClick: () => setFilterRole('ALL'), className: "text-[11px] text-[#00D2FF] hover:underline font-mono", children: ["Clear (", filterRole, ")"] }))] }), _jsx(CardContent, { className: "p-4 flex-1 overflow-y-auto max-h-[560px] space-y-3", children: filteredThoughts.map((msg) => (_jsxs("div", { className: "p-3 rounded-xl bg-[#131D35]/90 border border-[#1E293B] hover:border-cyan-500/40 transition-colors", children: [_jsxs("div", { className: "flex items-center justify-between text-[11px]", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-bold text-[#00D2FF]", children: msg.agentName }), _jsx("span", { className: "text-[10px] font-mono bg-[#0A0F1D] text-[#94A3B8] px-1.5 py-0.5 rounded border border-[#1E293B]", children: msg.thoughtType })] }), _jsx("span", { className: "text-[10px] font-mono text-[#64748B]", children: msg.timestampUtc })] }), _jsxs("p", { className: "mt-1.5 text-xs text-[#F8FAFC] leading-relaxed font-mono", children: ["\"", msg.content, "\""] }), msg.confidence !== undefined && (_jsx("div", { className: "mt-2 flex items-center justify-end text-[10px] font-mono text-[#10B981]", children: _jsxs("span", { children: ["Confidence: ", (msg.confidence * 100).toFixed(1), "%"] }) }))] }, msg.id))) })] }) })] }) }));
};
