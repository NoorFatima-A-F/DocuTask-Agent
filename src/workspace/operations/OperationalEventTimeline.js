import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Clock, RefreshCw, GitCommit } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
export const OperationalEventTimeline = ({ missionId = 'cluster-primary-master', }) => {
    const [events] = useState([
        {
            eventId: 'op-evt-001',
            type: 'RuntimeHeartbeatReceived',
            subsystem: 'PLANNER',
            description: 'Liveness heartbeat pulse #1042 received; 18 supervised worker threads healthy.',
            timestamp: '10:15:00 UTC',
            severity: 'INFO',
        },
        {
            eventId: 'op-evt-002',
            type: 'IncidentDetected',
            subsystem: 'WORKERS',
            description: 'Worker thread segfault detected in local Tesseract OCR node.',
            timestamp: '10:14:02 UTC',
            severity: 'MEDIUM',
        },
        {
            eventId: 'op-evt-003',
            type: 'DiagnosisCompleted',
            subsystem: 'WORKERS',
            description: 'Root cause inferred: Unhandled OCR memory exception (confidence: 96.5%).',
            timestamp: '10:14:02 UTC',
            severity: 'INFO',
        },
        {
            eventId: 'op-evt-004',
            type: 'HealingCompleted',
            subsystem: 'WORKERS',
            description: 'Worker restarted and state verified in 120ms (SHA-256 audit signed).',
            timestamp: '10:14:03 UTC',
            severity: 'INFO',
        },
        {
            eventId: 'op-evt-005',
            type: 'HealthEvaluated',
            subsystem: 'TELEMETRY',
            description: 'Platform composite health score recomputed: 98.9% (HEALTHY).',
            timestamp: '10:14:05 UTC',
            severity: 'INFO',
        },
    ]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Clock, { className: "w-5 h-5 text-indigo-400" }), "Unified Operational Event & Resilience Timeline"] }), _jsxs("p", { className: "text-sm text-slate-400", children: ["Immutable stream of heartbeats, incident detections, root-cause diagnoses, and self-healing actions for: ", _jsx("code", { className: "text-indigo-300 font-mono text-xs", children: missionId })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: "intelligence", size: "md", children: "Stream Status: LIVE_SSE" }), _jsxs("button", { className: "flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700", children: [_jsx(RefreshCw, { className: "w-3.5 h-3.5" }), "Sync Event Stream"] })] })] }), _jsx("div", { className: "space-y-3 font-mono", children: events.map((evt) => (_jsx(Card, { className: "p-4 bg-slate-900 border-slate-800 hover:border-slate-700 transition-all", children: _jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { className: "flex items-start gap-3", children: [_jsx("div", { className: "p-2 rounded-lg bg-slate-950 border border-slate-800 text-indigo-400 mt-0.5", children: _jsx(GitCommit, { className: "w-4 h-4" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2 mb-1", children: [_jsx("span", { className: "text-xs font-bold text-indigo-400", children: evt.eventId }), _jsx(Badge, { variant: "intelligence", size: "sm", children: evt.type }), _jsx(Badge, { variant: evt.severity === 'MEDIUM' ? 'warning' : 'outline', size: "sm", children: evt.subsystem })] }), _jsx("p", { className: "text-xs text-slate-200 font-semibold", children: evt.description })] })] }), _jsx("div", { className: "text-right text-xs text-slate-400", children: _jsxs("span", { className: "flex items-center gap-1", children: [_jsx(Clock, { className: "w-3 h-3 text-slate-500" }), evt.timestamp] }) })] }) }, evt.eventId))) })] }));
};
