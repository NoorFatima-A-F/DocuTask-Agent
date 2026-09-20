import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Cpu, Server } from 'lucide-react';
export const ResourceAllocationMonitor = () => {
    const activeAllocations = [
        {
            ticketId: 'tkt_7b9d3e',
            missionId: 'mission-001',
            resource: 'General Async Worker Pool',
            allocatedUnits: 6,
            status: 'ALLOCATED',
            timestamp: '10:14:22 UTC',
        },
        {
            ticketId: 'tkt_8a1f4c',
            missionId: 'mission-001',
            resource: 'Gemini 1.5 Flash Quota',
            allocatedUnits: 150,
            status: 'ALLOCATED',
            timestamp: '10:14:22 UTC',
        },
        {
            ticketId: 'tkt_2d0e9a',
            missionId: 'mission-002',
            resource: 'Local Tesseract OCR Cluster',
            allocatedUnits: 3,
            status: 'ALLOCATED',
            timestamp: '10:14:25 UTC',
        },
    ];
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-indigo-500/20 to-teal-500/20 border border-indigo-500/30 rounded-xl text-indigo-400", children: _jsx(Cpu, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Resource Allocation Monitor", _jsx(Badge, { variant: "intelligence", size: "sm", children: "Phase 13.6 ARIA-EOP" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] font-mono", children: "Live atomic reservation engine tracking active worker tickets, quota allocations, and concurrency headroom" })] })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx(Badge, { variant: "success", size: "md", children: "3 Active Reservation Tickets" }) })] }), _jsxs("div", { className: "space-y-4 font-mono", children: [_jsxs("h2", { className: "text-sm font-bold text-white flex items-center gap-2", children: [_jsx(Server, { className: "w-4 h-4 text-cyan-400" }), "Active Resource Allocation Tickets"] }), _jsx("div", { className: "grid grid-cols-1 gap-4", children: activeAllocations.map((alloc) => (_jsxs(Card, { className: "p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] flex flex-wrap items-center justify-between gap-4", children: [_jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-white font-bold", children: alloc.resource }), _jsx(Badge, { variant: "success", size: "sm", children: alloc.status })] }), _jsxs("div", { className: "text-xs text-[#64748B]", children: ["Mission: ", _jsx("span", { className: "text-indigo-400", children: alloc.missionId }), " | Ticket: ", alloc.ticketId] })] }), _jsxs("div", { className: "flex items-center gap-6 text-xs", children: [_jsxs("div", { className: "text-right", children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "ALLOCATED UNITS" }), _jsxs("span", { className: "text-cyan-400 font-bold", children: [alloc.allocatedUnits, " units"] })] }), _jsxs("div", { className: "text-right", children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "TIMESTAMP" }), _jsx("span", { className: "text-[#94A3B8]", children: alloc.timestamp })] })] })] }, alloc.ticketId))) })] })] }));
};
