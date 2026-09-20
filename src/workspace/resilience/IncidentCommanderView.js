import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { CheckCircle2 } from 'lucide-react';
export const IncidentCommanderView = () => {
    const [activeTab, setActiveTab] = useState('INCIDENTS');
    const [selectedIncidentId, setSelectedIncidentId] = useState('inc-202609-001');
    const incidents = [
        {
            id: 'inc-202609-001',
            title: 'Upstream Gemini 1.5 Pro 504 Timeout Spike',
            severity: 'SEV2_HIGH',
            state: 'RESOLVED',
            rootCause: 'node-gemini (Google Cloud Gateway)',
            blastRadius: ['node-workers', 'node-planner'],
            duration: '90 seconds',
            mttr: '45.0 ms',
            strategy: 'strat-gemini-flash-fallback',
            postMortem: 'Upstream cloud gateway experienced momentary latency spike to 5.2s. Autonomous Incident Commander declared SEV2, tripped circuit breaker, and routed 100% of pending DAG worker prompts to Gemini 1.5 Flash in 45ms with 0 state loss.',
            timeline: [
                { time: '14:20:00 UTC', state: 'DETECTED', actor: 'COMMANDER', msg: 'Anomalous error rate (85%) detected on Gemini provider endpoint.' },
                { time: '14:20:12 UTC', state: 'TRIAGING', actor: 'DIAGNOSTIC_AGENT', msg: 'Diagnostic subagent confirmed upstream 504 Gateway Timeout.' },
                { time: '14:20:25 UTC', state: 'ISOLATING', actor: 'COMMANDER', msg: 'Circuit breaker tripped for node-gemini. In-flight requests rerouted.' },
                { time: '14:20:40 UTC', state: 'RECOVERING', actor: 'COMMANDER', msg: 'Activated strat-gemini-flash-fallback. Model swapped to Flash.' },
                { time: '14:20:70 UTC', state: 'VERIFYING', actor: 'COMMANDER', msg: 'Invariant check passed: replay parity 99.98%, zero data drop.' },
                { time: '14:21:30 UTC', state: 'RESOLVED', actor: 'COMMANDER', msg: 'Incident resolved autonomously. Health score restored to 100.0.' },
            ],
        },
        {
            id: 'inc-202609-002',
            title: 'OCR Worker Subsystem Memory Pressure',
            severity: 'SEV3_MEDIUM',
            state: 'RESOLVED',
            rootCause: 'node-workers (DAG Worker Pool)',
            blastRadius: ['node-planner'],
            duration: '45 seconds',
            mttr: '180.0 ms',
            strategy: 'strat-ocr-chunk-respawn',
            postMortem: 'Worker pool reached 85% memory threshold during large raster PDF processing. Commander isolated corrupted chunk, respawned sandboxed worker replica, and resumed pipeline.',
            timeline: [
                { time: '11:15:00 UTC', state: 'DETECTED', actor: 'COMMANDER', msg: 'Worker node-workers reported heap usage > 85%.' },
                { time: '11:15:10 UTC', state: 'ISOLATING', actor: 'COMMANDER', msg: 'Worker process isolated from active scheduler queue.' },
                { time: '11:15:25 UTC', state: 'RECOVERING', actor: 'COMMANDER', msg: 'Respawned worker sandbox. Chunk re-allocated.' },
                { time: '11:15:45 UTC', state: 'RESOLVED', actor: 'COMMANDER', msg: 'Worker heap stabilized at 18%. Zero document data dropped.' },
            ],
        },
    ];
    const currentInc = (incidents.find(i => i.id === selectedIncidentId) || incidents[0]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Autonomous Incident Commander" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Auto-Triage & Recovery" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Self-governing incident commander that detects anomalies, isolates failing components, executes verified fallbacks, and authors formal post-mortems." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs("div", { className: "flex bg-muted/40 p-1 rounded-lg border border-border/40 text-xs", children: [_jsxs("button", { onClick: () => setActiveTab('INCIDENTS'), className: `px-3 py-1 rounded font-medium transition-colors ${activeTab === 'INCIDENTS' ? 'bg-primary text-primary-foreground' : 'text-muted-foreground hover:text-foreground'}`, children: ["Live Incidents (", incidents.length, ")"] }), _jsx("button", { onClick: () => setActiveTab('POSTMORTEMS'), className: `px-3 py-1 rounded font-medium transition-colors ${activeTab === 'POSTMORTEMS' ? 'bg-primary text-primary-foreground' : 'text-muted-foreground hover:text-foreground'}`, children: "Post-Mortems" })] }), _jsx(Badge, { variant: "success", size: "md", children: "All Incidents Resolved (100%)" })] })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 bg-emerald-950/10 border-emerald-500/20", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Autonomous Resolution Rate" }), _jsx("div", { className: "text-2xl font-bold font-mono text-emerald-400 mt-1", children: "100.0%" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "0 Human escalations needed" })] }), _jsxs(Card, { className: "p-4 bg-blue-950/10 border-blue-500/20", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Mean Time To Triage" }), _jsx("div", { className: "text-2xl font-bold font-mono text-blue-400 mt-1", children: "11.5 sec" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Autonomous diagnostic agent" })] }), _jsxs(Card, { className: "p-4 bg-purple-950/10 border-purple-500/20", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Mean Time To Recovery" }), _jsx("div", { className: "text-2xl font-bold font-mono text-purple-400 mt-1", children: "67.5 sec" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "End-to-end self-healing" })] }), _jsxs(Card, { className: "p-4 bg-cyan-950/10 border-cyan-500/20", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Data Loss Under Incidents" }), _jsx("div", { className: "text-2xl font-bold font-mono text-cyan-400 mt-1", children: "0 Bytes" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Truth ledger unbroken" })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "space-y-3", children: [_jsx("h2", { className: "text-sm font-semibold tracking-wider text-muted-foreground uppercase", children: "Incident Log" }), incidents.map(inc => (_jsxs(Card, { onClick: () => setSelectedIncidentId(inc.id), className: `p-4 cursor-pointer transition-all border ${selectedIncidentId === inc.id ? 'border-primary bg-primary/5 shadow-md' : 'border-border/60 hover:border-border'}`, children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx("div", { className: "text-xs font-bold text-foreground", children: inc.title }), _jsx("div", { className: "text-[10px] text-muted-foreground font-mono mt-0.5", children: inc.id })] }), _jsx(Badge, { variant: inc.severity === 'SEV2_HIGH' ? 'warning' : 'default', size: "sm", children: inc.severity })] }), _jsxs("div", { className: "flex items-center justify-between text-[11px] text-muted-foreground mt-3 pt-2 border-t border-border/40", children: [_jsxs("span", { children: ["Duration: ", _jsx("strong", { className: "text-foreground", children: inc.duration })] }), _jsx(Badge, { variant: "success", size: "sm", children: inc.state })] })] }, inc.id)))] }), _jsxs("div", { className: "lg:col-span-2 space-y-4", children: [_jsx("h2", { className: "text-sm font-semibold tracking-wider text-muted-foreground uppercase", children: "Incident Mitigation Timeline & Forensics" }), _jsxs(Card, { className: "p-5 border-border/60 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border/40 pb-3", children: [_jsxs("div", { children: [_jsx("div", { className: "text-base font-bold text-foreground", children: currentInc.title }), _jsxs("div", { className: "text-xs text-muted-foreground font-mono mt-0.5", children: ["Root Cause: ", _jsx("strong", { className: "text-red-400", children: currentInc.rootCause }), " \u2022 Failover: ", _jsx("strong", { className: "text-primary", children: currentInc.strategy })] })] }), _jsxs(Badge, { variant: "success", size: "md", children: ["Status: ", currentInc.state] })] }), _jsxs("div", { className: "space-y-3 pt-2", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground uppercase", children: "Chronological Action Ledger" }), _jsx("div", { className: "space-y-2 font-mono text-xs", children: currentInc.timeline.map((entry, idx) => (_jsxs("div", { className: "flex items-start gap-3 p-2.5 rounded bg-muted/30 border border-border/30", children: [_jsx("div", { className: "text-[11px] text-muted-foreground whitespace-nowrap pt-0.5", children: entry.time }), _jsx(Badge, { variant: "intelligence", size: "sm", children: entry.state }), _jsxs("div", { className: "text-xs text-foreground flex-1", children: [_jsxs("strong", { className: "text-primary", children: ["[", entry.actor, "]"] }), " ", entry.msg] })] }, idx))) })] }), _jsxs("div", { className: "p-4 bg-muted/40 rounded-lg border border-border/40 space-y-1.5 mt-4", children: [_jsxs("div", { className: "text-xs font-bold text-foreground flex items-center gap-1.5", children: [_jsx(CheckCircle2, { className: "w-4 h-4 text-emerald-400" }), " Autonomous Post-Mortem Summary"] }), _jsx("p", { className: "text-xs text-muted-foreground leading-relaxed", children: currentInc.postMortem })] })] })] })] })] }));
};
