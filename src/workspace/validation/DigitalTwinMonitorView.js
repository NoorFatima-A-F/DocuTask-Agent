import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const DigitalTwinMonitorView = () => {
    const [activeShadowTraffic, setActiveShadowTraffic] = useState(true);
    const shadowRecords = [
        {
            shadowId: 'shw_99182',
            missionId: 'MIS-INV-8821',
            targetPolicy: 'v4.2-pareto (Production)',
            shadowPolicy: 'v5.0-bayesian (Candidate)',
            agreementScore: '99.4%',
            latencyDivergence: '+3.8%',
            tokenDelta: '+25 tokens',
            sandboxStatus: 'MUTATION_INTERCEPTED',
            fidelity: 'HIGH_FIDELITY',
        },
        {
            shadowId: 'shw_99183',
            missionId: 'MIS-TABLE-4412',
            targetPolicy: 'v4.2-pareto (Production)',
            shadowPolicy: 'v5.0-bayesian (Candidate)',
            agreementScore: '98.1%',
            latencyDivergence: '-12.4%',
            tokenDelta: '-150 tokens',
            sandboxStatus: 'ISOLATED_SUCCESS',
            fidelity: 'HIGH_FIDELITY',
        },
        {
            shadowId: 'shw_99184',
            missionId: 'MIS-KYC-0034',
            targetPolicy: 'v4.2-pareto (Production)',
            shadowPolicy: 'v5.0-bayesian (Candidate)',
            agreementScore: '100.0%',
            latencyDivergence: '+0.5%',
            tokenDelta: '0 tokens',
            sandboxStatus: 'ISOLATED_SUCCESS',
            fidelity: 'HIGH_FIDELITY',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\uD83D\uDC65" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Digital Twin Shadow Execution & Safety Sandbox" }), _jsx(Badge, { variant: "success", size: "sm", children: "SANDBOX ISOLATED" })] }), _jsx("p", { className: "text-sm font-mono text-[#94A3B8] mt-1", children: "Zero-risk mirrored execution of production traffic against experimental candidate models and policies." })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("span", { className: "text-xs font-mono text-[#94A3B8]", children: "Shadow Traffic Mirroring:" }), _jsx("button", { onClick: () => setActiveShadowTraffic(!activeShadowTraffic), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${activeShadowTraffic
                                        ? 'bg-emerald-600 text-white'
                                        : 'bg-[#1E293B] text-[#94A3B8]'}`, children: activeShadowTraffic ? '● 100% MIRRORED' : '○ PAUSED' })] })] }) }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Database Mutation Shield" }), _jsx("div", { className: "text-xl font-bold font-mono text-emerald-400 mt-1", children: "ACTIVE (100% BLOCKED)" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "Virtual state interceptors" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Average Output Agreement" }), _jsx("div", { className: "text-2xl font-bold font-mono text-cyan-400 mt-1", children: "99.1%" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "High fidelity mirroring" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Production Latency Impact" }), _jsx("div", { className: "text-2xl font-bold font-mono text-emerald-400 mt-1", children: "0.00 ms" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "Asynchronous sidecar execution" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Overall Twin Status" }), _jsx("div", { className: "text-xl font-bold font-mono text-indigo-400 mt-1", children: "HIGH_FIDELITY" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "Parity with prod environment" })] })] }), _jsxs(Card, { className: "p-6 bg-[#0F172A] border-[#1E293B]", children: [_jsx("h3", { className: "text-sm font-bold font-mono text-[#F8FAFC] mb-4", children: "Live Mirrored Shadow Execution Stream" }), _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left font-mono text-xs", children: [_jsx("thead", { children: _jsxs("tr", { className: "border-b border-[#1E293B] text-[#94A3B8]", children: [_jsx("th", { className: "pb-3", children: "Shadow Run ID" }), _jsx("th", { className: "pb-3", children: "Production vs Candidate Policy" }), _jsx("th", { className: "pb-3", children: "Output Agreement" }), _jsx("th", { className: "pb-3", children: "Latency Divergence" }), _jsx("th", { className: "pb-3", children: "Sandbox Security" }), _jsx("th", { className: "pb-3", children: "Fidelity Grade" })] }) }), _jsx("tbody", { className: "divide-y divide-[#1E293B]", children: shadowRecords.map((s) => (_jsxs("tr", { className: "hover:bg-[#1E293B]/40 transition-colors", children: [_jsx("td", { className: "py-3 font-bold text-[#F8FAFC]", children: s.shadowId }), _jsxs("td", { className: "py-3", children: [_jsx("div", { className: "text-[#E2E8F0]", children: s.targetPolicy }), _jsxs("div", { className: "text-indigo-400 text-[11px]", children: ["\u21B3 ", s.shadowPolicy] })] }), _jsx("td", { className: "py-3 text-cyan-400 font-bold", children: s.agreementScore }), _jsx("td", { className: "py-3 text-emerald-400", children: s.latencyDivergence }), _jsx("td", { className: "py-3", children: _jsx(Badge, { variant: "warning", size: "sm", children: s.sandboxStatus }) }), _jsx("td", { className: "py-3", children: _jsx(Badge, { variant: "success", size: "sm", children: s.fidelity }) })] }, s.shadowId))) })] }) })] })] }));
};
