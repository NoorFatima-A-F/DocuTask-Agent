import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const TruthLedgerExplorerView = () => {
    const [filterType, setFilterType] = useState('ALL');
    const entries = [
        {
            eventId: 'tle_001_plan',
            missionId: 'msn_1001',
            eventType: 'PLANNER_DECISION',
            timestamp: '14:20:00.124',
            plannerVer: 'v2.1.0',
            strategyVer: '2.1.0',
            model: 'gemini-1.5-pro',
            parentHash: '0x0000000000000000',
            entryHash: '0x8f2ac31b4e5d6a7b',
            evidenceRoot: '0x8f2ac31b4e5d6a7b',
            status: 'VERIFIED',
        },
        {
            eventId: 'tle_002_tool',
            missionId: 'msn_1001',
            eventType: 'TOOL_EXECUTION',
            timestamp: '14:20:00.350',
            plannerVer: 'v2.1.0',
            strategyVer: '2.1.0',
            model: 'tesseract_v2_optimized',
            parentHash: '0x8f2ac31b4e5d6a7b',
            entryHash: '0x3c7eb44a1d9e2f8c',
            evidenceRoot: '0x3c7eb44a1d9e2f8c',
            status: 'VERIFIED',
        },
        {
            eventId: 'tle_003_sign',
            missionId: 'msn_1001',
            eventType: 'EVIDENCE_SIGNED',
            timestamp: '14:20:00.780',
            plannerVer: 'v2.1.0',
            strategyVer: '2.1.0',
            model: 'ed25519_authority',
            parentHash: '0x3c7eb44a1d9e2f8c',
            entryHash: '0x991afe820b4c7d6e',
            evidenceRoot: '0x991afe820b4c7d6e',
            status: 'VERIFIED',
        },
        {
            eventId: 'tle_004_opt',
            missionId: 'msn_1001',
            eventType: 'OPTIMIZATION_PROMOTED',
            timestamp: '14:20:01.050',
            plannerVer: 'v2.1.0',
            strategyVer: '2.1.0',
            model: 'aislcop_optimizer',
            parentHash: '0x991afe820b4c7d6e',
            entryHash: '0x661d009ab5e4f3a2',
            evidenceRoot: '0x661d009ab5e4f3a2',
            status: 'VERIFIED',
        },
    ];
    const filtered = filterType === 'ALL' ? entries : entries.filter((e) => e.eventType === filterType);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Runtime Truth Ledger" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Pillar 1" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Immutable, append-only truth ledger with SHA-256 parent-child hash continuity linking every mission event to cryptographic evidence." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "success", size: "md", children: "Chain Continuity: 100% Verified" }), _jsxs(Badge, { variant: "outline", size: "md", children: ["Total Entries: ", entries.length] })] })] }), _jsx("div", { className: "flex items-center gap-2", children: ['ALL', 'PLANNER_DECISION', 'TOOL_EXECUTION', 'EVIDENCE_SIGNED', 'OPTIMIZATION_PROMOTED'].map((t) => (_jsx("button", { onClick: () => setFilterType(t), className: `text-xs px-2.5 py-1 rounded transition-colors font-medium ${filterType === t ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground hover:bg-muted/80'}`, children: t }, t))) }), _jsx(Card, { className: "p-0 overflow-hidden", children: _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left text-xs border-collapse", children: [_jsx("thead", { children: _jsxs("tr", { className: "border-b border-border/40 bg-muted/20 font-semibold text-muted-foreground", children: [_jsx("th", { className: "p-3", children: "Event ID" }), _jsx("th", { className: "p-3", children: "Event Type" }), _jsx("th", { className: "p-3", children: "Mission ID" }), _jsx("th", { className: "p-3", children: "Timestamp" }), _jsx("th", { className: "p-3", children: "Parent Hash" }), _jsx("th", { className: "p-3", children: "Entry Hash" }), _jsx("th", { className: "p-3", children: "Evidence Link" }), _jsx("th", { className: "p-3", children: "Audit Status" })] }) }), _jsx("tbody", { className: "divide-y divide-border/20", children: filtered.map((e) => (_jsxs("tr", { className: "hover:bg-muted/10 transition-colors", children: [_jsx("td", { className: "p-3 font-mono font-semibold text-primary", children: e.eventId }), _jsx("td", { className: "p-3 font-mono text-foreground", children: _jsx(Badge, { variant: "outline", size: "sm", children: e.eventType }) }), _jsx("td", { className: "p-3 font-mono text-foreground", children: e.missionId }), _jsx("td", { className: "p-3 font-mono text-muted-foreground", children: e.timestamp }), _jsxs("td", { className: "p-3 font-mono text-[11px] text-muted-foreground", children: [e.parentHash.slice(0, 10), "..."] }), _jsxs("td", { className: "p-3 font-mono text-[11px] text-emerald-400 font-semibold", children: [e.entryHash.slice(0, 10), "..."] }), _jsxs("td", { className: "p-3 font-mono text-[11px] text-muted-foreground", children: [e.evidenceRoot.slice(0, 10), "..."] }), _jsx("td", { className: "p-3", children: _jsx(Badge, { variant: "success", size: "sm", children: e.status }) })] }, e.eventId))) })] }) }) })] }));
};
