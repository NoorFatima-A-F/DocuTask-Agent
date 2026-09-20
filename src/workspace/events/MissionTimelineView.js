import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Clock, RefreshCw, Hash, ShieldCheck } from 'lucide-react';
export const MissionTimelineView = () => {
    const [selectedEventId, setSelectedEventId] = useState('evt-m01-001');
    const [isRefreshing, setIsRefreshing] = useState(false);
    const events = [
        {
            id: 'evt-m01-001',
            offset: 0,
            time: '14:20:00.120 UTC',
            type: 'MissionCreated',
            subsystem: 'MISSION_CONTROL',
            actor: 'HumanOperator',
            actorType: 'HUMAN',
            correlationId: 'corr-mission-fin-001',
            causationId: 'cause-user-submit',
            evidenceHash: '9f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069',
            truthLedgerHash: '8a1b2c3d4e5f60017a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f',
            severity: 'INFO',
            payload: { goal: 'Process and validate 2026 Q3 vendor audit invoices', document_count: 4, sla_seconds: 30 },
        },
        {
            id: 'evt-m01-002',
            offset: 1,
            time: '14:20:00.350 UTC',
            type: 'PlannerStarted',
            subsystem: 'PLANNER',
            actor: 'ChiefPlanner',
            actorType: 'PLANNER',
            correlationId: 'corr-mission-fin-001',
            causationId: 'cause-evt-m01-001',
            evidenceHash: '4a5b6c7d8e9f00112233445566778899aabbccddeeff00112233445566778899',
            truthLedgerHash: '3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c',
            severity: 'INFO',
            payload: { strategy: 'DYNAMIC_DAG_SYNTHESIS', model: 'gemini-1.5-pro', priority: 'HIGH' },
        },
        {
            id: 'evt-m01-003',
            offset: 2,
            time: '14:20:00.890 UTC',
            type: 'PlannerFinished',
            subsystem: 'PLANNER',
            actor: 'ChiefPlanner',
            actorType: 'PLANNER',
            correlationId: 'corr-mission-fin-001',
            causationId: 'cause-evt-m01-002',
            evidenceHash: '11223344556677889900aabbccddeeff00112233445566778899aabbccddeeff',
            truthLedgerHash: '5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d',
            severity: 'INFO',
            payload: { generated_task_count: 6, estimated_cost_usd: 0.0032, critical_path_latency_ms: 185.4 },
        },
        {
            id: 'evt-m01-004',
            offset: 3,
            time: '14:20:01.100 UTC',
            type: 'TaskAssigned',
            subsystem: 'WORKER_POOL',
            actor: 'DAGScheduler',
            actorType: 'SYSTEM',
            correlationId: 'corr-mission-fin-001',
            causationId: 'cause-evt-m01-003',
            evidenceHash: '778899aabbccddeeff00112233445566778899aabbccddeeff00112233445566',
            truthLedgerHash: '7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f',
            severity: 'INFO',
            payload: { task_id: 'task-ocr-chunk-1', worker_id: 'worker-ocr-01', task_type: 'OCR_EXTRACTION' },
        },
        {
            id: 'evt-m01-005',
            offset: 4,
            time: '14:20:01.420 UTC',
            type: 'OCRCompleted',
            subsystem: 'OCR_SERVICE',
            actor: 'worker-ocr-01',
            actorType: 'WORKER',
            correlationId: 'corr-mission-fin-001',
            causationId: 'cause-evt-m01-004',
            evidenceHash: 'aabbccddeeff00112233445566778899aabbccddeeff00112233445566778899',
            truthLedgerHash: '9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b',
            severity: 'INFO',
            payload: { extracted_text_length: 4520, confidence: 0.994, duration_ms: 320.0 },
        },
        {
            id: 'evt-m01-006',
            offset: 5,
            time: '14:20:01.750 UTC',
            type: 'ValidationPassed',
            subsystem: 'VALIDATION_ENGINE',
            actor: 'ScientificValidator',
            actorType: 'SYSTEM',
            correlationId: 'corr-mission-fin-001',
            causationId: 'cause-evt-m01-005',
            evidenceHash: 'bbccddee00112233445566778899aabbccddeeff00112233445566778899aabb',
            truthLedgerHash: '1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d',
            severity: 'INFO',
            payload: { schema_valid: true, business_rules_passed: 12, invariant_checks: 6 },
        },
        {
            id: 'evt-m01-007',
            offset: 6,
            time: '14:20:02.100 UTC',
            type: 'MissionCompleted',
            subsystem: 'MISSION_CONTROL',
            actor: 'MissionCommander',
            actorType: 'SYSTEM',
            correlationId: 'corr-mission-fin-001',
            causationId: 'cause-evt-m01-006',
            evidenceHash: 'ccddee00112233445566778899aabbccddeeff00112233445566778899aabbcc',
            truthLedgerHash: '2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e',
            severity: 'INFO',
            payload: { total_tasks_completed: 6, duration_seconds: 1.98, total_cost_usd: 0.0031, status: 'SUCCESS' },
        },
    ];
    const currentEvent = (events.find(e => e.id === selectedEventId) || events[0]);
    const handleRefresh = () => {
        setIsRefreshing(true);
        setTimeout(() => setIsRefreshing(false), 300);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Mission Domain Event Timeline" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Immutable Event Stream" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Chronological, cryptographically linked domain event stream for the active mission partition." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Button, { variant: "outline", size: "sm", onClick: handleRefresh, disabled: isRefreshing, children: [_jsx(RefreshCw, { className: `w-3.5 h-3.5 mr-1.5 ${isRefreshing ? 'animate-spin' : ''}` }), "Refresh Stream"] }), _jsx(Badge, { variant: "success", size: "md", children: "7/7 Events Verified" })] })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 bg-emerald-950/10 border-emerald-500/20", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Partition Stream Length" }), _jsxs("div", { className: "text-2xl font-bold font-mono text-emerald-400 mt-1", children: [events.length, " Events"] }), _jsxs("div", { className: "text-[11px] text-muted-foreground mt-1", children: ["Offsets 0..", events.length - 1] })] }), _jsxs(Card, { className: "p-4 bg-blue-950/10 border-blue-500/20", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Execution Latency" }), _jsx("div", { className: "text-2xl font-bold font-mono text-blue-400 mt-1", children: "1.98s Total" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Within 30s SLA budget" })] }), _jsxs(Card, { className: "p-4 bg-purple-950/10 border-purple-500/20", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Merkle Continuity" }), _jsx("div", { className: "text-2xl font-bold font-mono text-purple-400 mt-1", children: "100.0%" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "SHA-256 parent linked" })] }), _jsxs(Card, { className: "p-4 bg-cyan-950/10 border-cyan-500/20", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Total Incurred Cost" }), _jsx("div", { className: "text-2xl font-bold font-mono text-cyan-400 mt-1", children: "$0.0031" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Optimized utility path" })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "lg:col-span-2 space-y-3", children: [_jsx("h2", { className: "text-sm font-semibold tracking-wider text-muted-foreground uppercase", children: "Chronological Event Stream" }), _jsx("div", { className: "space-y-2", children: events.map(ev => (_jsx(Card, { onClick: () => setSelectedEventId(ev.id), className: `p-3.5 cursor-pointer transition-all border ${selectedEventId === ev.id
                                        ? 'border-primary bg-primary/5 shadow-md'
                                        : 'border-border/60 hover:border-border'}`, children: _jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2", children: [_jsxs("div", { className: "flex items-center gap-2.5", children: [_jsxs("span", { className: "w-6 h-6 rounded-full bg-primary/10 text-primary flex items-center justify-center text-xs font-mono font-bold", children: ["#", ev.offset] }), _jsxs("div", { children: [_jsxs("div", { className: "text-xs font-bold text-foreground flex items-center gap-2", children: [_jsx("span", { children: ev.type }), _jsx(Badge, { variant: "outline", size: "sm", children: ev.subsystem })] }), _jsxs("div", { className: "text-[10px] text-muted-foreground font-mono mt-0.5", children: [ev.id, " \u2022 ", ev.actor, " (", ev.actorType, ")"] })] })] }), _jsxs("div", { className: "flex items-center gap-2 font-mono text-[11px] text-muted-foreground self-end sm:self-center", children: [_jsx(Clock, { className: "w-3.5 h-3.5" }), _jsx("span", { children: ev.time })] })] }) }, ev.id))) })] }), _jsxs("div", { className: "space-y-4", children: [_jsx("h2", { className: "text-sm font-semibold tracking-wider text-muted-foreground uppercase", children: "Event Inspector" }), _jsxs(Card, { className: "p-5 border-border/60 space-y-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs(Badge, { variant: "intelligence", size: "sm", children: ["Offset #", currentEvent.offset] }), _jsx(Badge, { variant: "success", size: "sm", children: currentEvent.severity })] }), _jsx("div", { className: "text-base font-bold text-foreground mt-2", children: currentEvent.type }), _jsx("div", { className: "text-xs font-mono text-muted-foreground", children: currentEvent.id })] }), _jsxs("div", { className: "space-y-2.5 pt-2 border-t border-border/40 text-xs", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsx("span", { className: "text-muted-foreground", children: "Subsystem:" }), _jsx("span", { className: "font-mono text-foreground font-semibold", children: currentEvent.subsystem })] }), _jsxs("div", { className: "flex justify-between items-center", children: [_jsx("span", { className: "text-muted-foreground", children: "Actor:" }), _jsxs("span", { className: "font-mono text-foreground", children: [currentEvent.actor, " (", currentEvent.actorType, ")"] })] }), _jsxs("div", { className: "flex justify-between items-center", children: [_jsx("span", { className: "text-muted-foreground", children: "Correlation ID:" }), _jsx("span", { className: "font-mono text-primary text-[11px]", children: currentEvent.correlationId })] }), _jsxs("div", { className: "flex justify-between items-center", children: [_jsx("span", { className: "text-muted-foreground", children: "Causation ID:" }), _jsx("span", { className: "font-mono text-muted-foreground text-[11px]", children: currentEvent.causationId })] })] }), _jsxs("div", { className: "space-y-2 pt-2 border-t border-border/40", children: [_jsxs("div", { className: "text-[11px] font-semibold text-muted-foreground uppercase flex items-center gap-1.5", children: [_jsx(ShieldCheck, { className: "w-3.5 h-3.5 text-emerald-400" }), " Evidence Hash (SHA-256)"] }), _jsx("div", { className: "p-2 bg-muted/40 rounded font-mono text-[10px] text-primary break-all border border-border/30", children: currentEvent.evidenceHash }), _jsxs("div", { className: "text-[11px] font-semibold text-muted-foreground uppercase flex items-center gap-1.5 pt-1", children: [_jsx(Hash, { className: "w-3.5 h-3.5 text-blue-400" }), " Ledger Block Hash"] }), _jsx("div", { className: "p-2 bg-muted/40 rounded font-mono text-[10px] text-foreground break-all border border-border/30", children: currentEvent.truthLedgerHash })] }), _jsxs("div", { className: "space-y-1.5 pt-2 border-t border-border/40", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground uppercase", children: "Event Payload" }), _jsx("pre", { className: "p-3 bg-muted/50 rounded font-mono text-[11px] text-foreground overflow-x-auto border border-border/30 max-h-48", children: JSON.stringify(currentEvent.payload, null, 2) })] })] })] })] })] }));
};
