import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const ExecutiveControlCenter = () => {
    const [activeTab, setActiveTab] = useState('MISSIONS');
    const missions = [
        {
            id: 'mission_live_001',
            title: 'Enterprise Financial Document Processing',
            priority: 'CRITICAL',
            status: 'IN_PROGRESS',
            budget: '$0.050',
            spent: '$0.018',
            departments: ['dept_executive', 'dept_ocr', 'dept_extraction', 'dept_validation', 'dept_governance'],
            stages: [
                { name: 'Strategic Intake & Policy Check', dept: 'Executive', status: 'COMPLETED', dur: '35 ms' },
                { name: 'Optical Ingestion & Bounding Box Layout', dept: 'OCR', status: 'COMPLETED', dur: '180 ms' },
                { name: 'Structured Semantic Extraction', dept: 'Extraction', status: 'IN_PROGRESS', dur: '420 ms' },
                { name: 'Mathematical Cross-Field Invariant Check', dept: 'Validation', status: 'PENDING', dur: '—' },
                { name: 'Cryptographic Sign-off & Audit Vault', dept: 'Governance', status: 'PENDING', dur: '—' },
            ],
        },
    ];
    const decisions = [
        {
            id: 'exec_dec_001',
            title: 'Authorize Q3 Enterprise Invoices Multi-Department Processing',
            type: 'MISSION_INTAKE',
            rationale: 'Approved high-priority invoice corpus execution with target SLA < 1000ms and budget ceiling $0.05.',
            departments: ['Executive', 'OCR', 'Extraction', 'Validation', 'Governance'],
            authorizer: 'Chief Executive Agent',
            hash: 'sha256_exec_88a91f4c',
            time: '12 min ago',
        },
        {
            id: 'exec_dec_002',
            title: 'Grant Extraction Department Additional 4 Worker Threads',
            type: 'RESOURCE_REALLOCATION',
            rationale: 'Pre-emptive capacity boost to meet P95 latency guarantees during high throughput burst.',
            departments: ['Extraction', 'Research'],
            authorizer: 'Chief Executive Agent',
            hash: 'sha256_exec_31b0e9a2',
            time: '5 min ago',
        },
    ];
    const barriers = [
        {
            id: 'bar_ocr_extraction_01',
            title: 'Perception Handoff Barrier',
            participating: ['dept_ocr', 'dept_memory'],
            arrived: ['dept_ocr', 'dept_memory'],
            isReleased: true,
        },
        {
            id: 'bar_val_gov_02',
            title: 'Audit Sign-off Barrier',
            participating: ['dept_validation', 'dept_qa'],
            arrived: ['dept_validation'],
            isReleased: false,
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-2xl", children: "\uD83D\uDC54" }), _jsx("h2", { className: "text-xl font-bold text-[#F8FAFC]", children: "Executive Coordination & Strategy Control Center" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "C-Suite Autonomous Planner" })] }), _jsx("p", { className: "text-sm text-[#94A3B8] mt-1", children: "Top-level organizational steering: mission intake, inter-department conflict arbitration, and strategic priority governance." })] }), _jsxs("div", { className: "flex gap-2", children: [_jsx("button", { onClick: () => setActiveTab('MISSIONS'), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${activeTab === 'MISSIONS' ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'}`, children: "Active Missions" }), _jsx("button", { onClick: () => setActiveTab('DECISIONS'), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${activeTab === 'DECISIONS' ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'}`, children: "Executive Decisions" }), _jsx("button", { onClick: () => setActiveTab('BARRIERS'), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${activeTab === 'BARRIERS' ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'}`, children: "Coordination Barriers" })] })] }), activeTab === 'MISSIONS' && (_jsx("div", { className: "space-y-4", children: missions.map((m) => (_jsxs(Card, { className: "p-5 bg-[#0F172A] border-[#1E293B] space-y-4", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-base font-bold text-[#F8FAFC]", children: m.title }), _jsx(Badge, { variant: "error", size: "sm", children: m.priority }), _jsx(Badge, { variant: "warning", size: "sm", children: m.status })] }), _jsxs("div", { className: "text-xs text-[#94A3B8] font-mono mt-1", children: ["Mission ID: ", m.id, " | Budget Spent: ", _jsx("span", { className: "text-[#F59E0B]", children: m.spent }), " / ", m.budget] })] }), _jsxs("div", { className: "text-right", children: [_jsx("div", { className: "text-xs text-[#64748B] font-mono uppercase", children: "Assigned Departments" }), _jsxs("div", { className: "text-xs text-[#38BDF8] font-mono font-semibold mt-0.5", children: [m.departments.length, " Departments Active"] })] })] }), _jsxs("div", { className: "space-y-2", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8] uppercase", children: "Departmental Stage Pipeline" }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-5 gap-2", children: m.stages.map((st, idx) => (_jsxs("div", { className: `p-3 rounded-lg border text-xs font-mono ${st.status === 'COMPLETED'
                                            ? 'bg-[#10B981]/10 border-[#10B981]/30 text-[#10B981]'
                                            : st.status === 'IN_PROGRESS'
                                                ? 'bg-[#00D2FF]/10 border-[#00D2FF]/40 text-[#00D2FF] shadow-[0_0_10px_rgba(0,210,255,0.15)]'
                                                : 'bg-[#020617] border-[#1E293B] text-[#64748B]'}`, children: [_jsxs("div", { className: "flex items-center justify-between text-[10px] mb-1", children: [_jsxs("span", { children: ["STAGE 0", idx + 1] }), _jsx("span", { children: st.dur })] }), _jsx("div", { className: "font-semibold text-[#F8FAFC] line-clamp-1", children: st.name }), _jsxs("div", { className: "text-[10px] text-[#94A3B8] mt-1", children: ["Dept: ", st.dept] })] }, idx))) })] })] }, m.id))) })), activeTab === 'DECISIONS' && (_jsx("div", { className: "space-y-3", children: decisions.map((dec) => (_jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B] flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: [_jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-sm font-bold text-[#F8FAFC]", children: dec.title }), _jsx(Badge, { variant: "intelligence", size: "sm", children: dec.type })] }), _jsx("div", { className: "text-xs text-[#94A3B8]", children: dec.rationale }), _jsxs("div", { className: "flex items-center gap-3 text-[11px] text-[#64748B] font-mono pt-1", children: [_jsxs("span", { children: ["Authorizer: ", _jsx("span", { className: "text-[#38BDF8]", children: dec.authorizer })] }), _jsx("span", { children: "\u2022" }), _jsxs("span", { children: ["Affected: ", _jsx("span", { className: "text-[#F8FAFC]", children: dec.departments.join(', ') })] }), _jsx("span", { children: "\u2022" }), _jsxs("span", { children: ["Hash: ", _jsx("span", { className: "text-[#10B981]", children: dec.hash })] })] })] }), _jsx("div", { className: "text-xs text-[#64748B] font-mono whitespace-nowrap", children: dec.time })] }, dec.id))) })), activeTab === 'BARRIERS' && (_jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: barriers.map((b) => (_jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B] space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-sm font-bold text-[#F8FAFC]", children: b.title }), _jsx(Badge, { variant: b.isReleased ? 'success' : 'warning', size: "sm", children: b.isReleased ? 'RELEASED' : 'WAITING_ON_BARRIER' })] }), _jsxs("div", { className: "text-xs text-[#94A3B8] font-mono", children: ["Required Departments: ", _jsx("span", { className: "text-[#F8FAFC]", children: b.participating.join(', ') })] }), _jsxs("div", { className: "text-xs text-[#94A3B8] font-mono", children: ["Arrived Departments: ", _jsx("span", { className: "text-[#00D2FF]", children: b.arrived.join(', ') })] })] }, b.id))) }))] }));
};
