import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
const CANONICAL_INCIDENTS = [
    {
        id: 'inc_2026_001',
        title: 'Transient Gemini 429 Quota Exhaustion During Batch Burst',
        severity: 'SEV2_HIGH',
        status: 'RESOLVED',
        commander: 'Chief Executive Agent',
        affected: ['Structured Extraction', 'Optical Perception'],
        rootCause: 'Upstream LLM burst exceeded 10,000 RPM concurrent token limit on single API key.',
        mitigation: 'Auto-switched extraction traffic to Gemini Flash Lite with exponential jitter backoff.',
        impact: '14 tasks delayed by 420ms; zero data loss; 100% invariant math verified.',
        timeline: [
            { time: '16:05:00Z', phase: 'DETECTED', action: 'HTTP 429 spike detected in Extraction Department.', actor: 'WorkerMonitor' },
            { time: '16:05:02Z', phase: 'TRIAGING', action: 'Incident Commander assigned; war room #incident-war-room opened.', actor: 'IncidentCommander' },
            { time: '16:05:05Z', phase: 'MITIGATING', action: 'Traffic routed to Flash Lite fallback pool; prompt compression applied.', actor: 'Lead Extraction Specialist' },
            { time: '16:05:12Z', phase: 'RESOLVED', action: 'Quota recovered; nominal queue latency restored.', actor: 'IncidentCommander' },
        ],
        postmortem: {
            whys: [
                'Why 1: Extraction tasks queued up -> upstream LLM returned HTTP 429.',
                'Why 2: Burst of 20 dense invoices arrived concurrently.',
                'Why 3: Single Gemini Pro API quota pool was shared without rate-smoothing.',
                'Why 4: Leaky-bucket token rate limiter threshold was set too loose.',
                'Why 5: Proactive prompt caching was not pre-warmed for this vendor template.',
            ],
            actionItems: [
                'Enable proactive token rate-smoothing on Extraction Department queue (COMPLETED)',
                'Pre-warm prompt caches on vendor batch ingestion (IN_PROGRESS)',
                'Add automatic Fallback-to-Flash-Lite circuit breaker rule (COMPLETED)',
            ],
        },
    },
];
export const IncidentCommandCenter = () => {
    const [selectedIncidentId, setSelectedIncidentId] = useState('inc_2026_001');
    const inc = CANONICAL_INCIDENTS.find((i) => i.id === selectedIncidentId) || CANONICAL_INCIDENTS[0];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-2xl", children: "\uD83D\uDEA8" }), _jsx("h2", { className: "text-xl font-bold text-[#F8FAFC]", children: "Enterprise Incident Command Center & War Room" }), _jsx(Badge, { variant: "error", size: "sm", children: "Automated Triage" })] }), _jsx("p", { className: "text-sm text-[#94A3B8] mt-1", children: "Automated incident lifecycle: DETECTED \u2192 TRIAGING \u2192 MITIGATING \u2192 RESOLVED \u2192 POSTMORTEM with 5-Whys root cause analysis." })] }), _jsx("div", { className: "flex items-center gap-2", children: CANONICAL_INCIDENTS.map((i) => (_jsx("button", { onClick: () => setSelectedIncidentId(i.id), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${selectedIncidentId === i.id ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'}`, children: i.id }, i.id))) })] }), _jsxs(Card, { className: "p-5 bg-[#0F172A] border-[#1E293B] space-y-5", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-[#1E293B] pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-base font-bold text-[#F8FAFC]", children: inc.title }), _jsx(Badge, { variant: "warning", size: "sm", children: inc.severity }), _jsx(Badge, { variant: "success", size: "sm", children: inc.status })] }), _jsxs("div", { className: "text-xs text-[#94A3B8] font-mono mt-1", children: ["Incident ID: ", inc.id, " | Commander: ", _jsx("span", { className: "text-[#38BDF8] font-semibold", children: inc.commander })] })] }), _jsxs("div", { className: "text-right text-xs font-mono", children: [_jsx("span", { className: "text-[#64748B] block", children: "AFFECTED DEPARTMENTS" }), _jsx("span", { className: "text-[#F8FAFC] font-semibold", children: inc.affected.join(', ') })] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: [_jsxs("div", { className: "p-4 rounded-xl bg-[#020617] border border-[#1E293B] space-y-1", children: [_jsx("div", { className: "text-xs font-mono text-[#EF4444] font-bold", children: "Root Cause Assessment" }), _jsx("p", { className: "text-xs text-[#CBD5E1]", children: inc.rootCause })] }), _jsxs("div", { className: "p-4 rounded-xl bg-[#020617] border border-[#1E293B] space-y-1", children: [_jsx("div", { className: "text-xs font-mono text-[#10B981] font-bold", children: "Mitigation Executed" }), _jsx("p", { className: "text-xs text-[#CBD5E1]", children: inc.mitigation })] })] }), _jsxs("div", { className: "space-y-3", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8] uppercase", children: "Automated Response Timeline" }), _jsx("div", { className: "space-y-2", children: inc.timeline.map((t, idx) => (_jsxs("div", { className: "flex items-center justify-between p-3 rounded-lg bg-[#020617]/60 border border-[#1E293B]/60 text-xs font-mono", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: t.phase === 'RESOLVED' ? 'success' : (t.phase === 'MITIGATING' ? 'warning' : 'info'), size: "sm", children: t.phase }), _jsx("span", { className: "text-[#F8FAFC]", children: t.action })] }), _jsxs("div", { className: "text-[11px] text-[#64748B]", children: ["Actor: ", _jsx("span", { className: "text-[#38BDF8]", children: t.actor }), " | ", t.time] })] }, idx))) })] }), _jsxs("div", { className: "space-y-3 pt-2", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8] uppercase", children: "Blameless 5-Whys Postmortem & Action Items" }), _jsxs("div", { className: "p-4 rounded-xl bg-[#020617] border border-[#1E293B] space-y-3 text-xs font-mono", children: [_jsx("div", { className: "space-y-1 text-[#CBD5E1]", children: inc.postmortem.whys.map((why, idx) => (_jsxs("div", { className: "flex items-start gap-2", children: [_jsx("span", { className: "text-[#00D2FF]", children: "\u21B3" }), _jsx("span", { children: why })] }, idx))) }), _jsxs("div", { className: "pt-2 border-t border-[#1E293B]/60 space-y-1", children: [_jsx("div", { className: "text-[11px] text-[#94A3B8] uppercase", children: "Corrective Prevention Rules:" }), inc.postmortem.actionItems.map((act, idx) => (_jsxs("div", { className: "text-[#10B981] flex items-center gap-2", children: [_jsx("span", { children: "\u2713" }), _jsx("span", { children: act })] }, idx)))] })] })] })] })] }));
};
