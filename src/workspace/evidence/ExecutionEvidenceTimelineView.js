import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const ExecutionEvidenceTimelineView = () => {
    const [filterType, setFilterType] = useState('ALL');
    const timelineEvents = [
        {
            timeOffsetMs: 0,
            timestamp: '18:22:10.142',
            type: 'PLANNER_DECISION',
            title: 'Optimal Trajectory Selection',
            summary: 'Chief Planner selected Gemini Flash with parallelism=3 across 4 candidate plans.',
            evidenceId: 'ev-node-001',
            costUsd: 0.0018,
            durationMs: 14.2,
            hash: 'a8f3b20c91e847ad3ef0192a83c7482910fae12089bb3c17820aedfa9102bc45',
        },
        {
            timeOffsetMs: 180,
            timestamp: '18:22:10.322',
            type: 'RESOURCE_AUCTION',
            title: 'GPU Compute Token Auction',
            summary: 'OCR Department won Vickrey auction for 4x GPU workers with $0.00042 bid.',
            evidenceId: 'ev-node-002',
            costUsd: 0.00042,
            durationMs: 4.8,
            hash: 'd4e9102fae89bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c748',
        },
        {
            timeOffsetMs: 380,
            timestamp: '18:22:10.522',
            type: 'TOOL_EXECUTION',
            title: 'Tesseract V5 OCR Execution',
            summary: 'Processed invoice image in 124.5ms; extracted 142 tokens and 28 bounding boxes.',
            evidenceId: 'ev-node-003',
            costUsd: 0.00042,
            durationMs: 124.5,
            hash: '7c3f810dae99120bc45a8f3b20c91e847ad3ef0192a83c748d4e9102fae89bb3c',
        },
        {
            timeOffsetMs: 520,
            timestamp: '18:22:10.662',
            type: 'VALIDATION_CHECK',
            title: 'Financial Invariant Reconciliation',
            summary: 'Reconciled subtotal + tax = $4,850.00 with p=0.0001 statistical confidence.',
            evidenceId: 'ev-node-004',
            costUsd: 0.0,
            durationMs: 18.2,
            hash: '3b20c91e847ad3ef0192a83c748d4e9102fae89bb3c7c3f810dae99120bc45a8f',
        },
        {
            timeOffsetMs: 650,
            timestamp: '18:22:10.792',
            type: 'ARTIFACT_MUTATION',
            title: 'Content-Addressable Registry Store',
            summary: 'Stored certified extraction JSON sealed with SHA-256 digest in artifact catalog.',
            evidenceId: 'ev-node-005',
            costUsd: 0.0,
            durationMs: 2.1,
            hash: 'f81d4fae7dec11d0a76500a0c91e6bf6012a8f3b20c91e847ad3ef0192a83c748',
        },
    ];
    const filtered = filterType === 'ALL' ? timelineEvents : timelineEvents.filter((e) => e.type === filterType);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Execution Evidence Timeline" }), _jsx(Badge, { variant: "success", size: "sm", children: "Millisecond Timestamped" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Chronological, high-resolution timeline of every runtime event linked directly to immutable evidence blocks." })] }), _jsx("div", { className: "flex items-center gap-2", children: ['ALL', 'PLANNER_DECISION', 'TOOL_EXECUTION', 'VALIDATION_CHECK'].map((f) => (_jsx("button", { onClick: () => setFilterType(f), className: `px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${filterType === f
                                ? 'bg-primary text-primary-foreground'
                                : 'bg-muted/40 text-muted-foreground hover:bg-muted/80'}`, children: f.replace('_', ' ') }, f))) })] }), _jsx("div", { className: "relative pl-6 space-y-4 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-border/60", children: filtered.map((ev) => (_jsxs("div", { className: "relative space-y-1", children: [_jsx("div", { className: "absolute -left-6 top-1.5 w-3 h-3 rounded-full bg-primary ring-4 ring-background" }), _jsxs(Card, { className: "p-4 space-y-2", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsxs("span", { className: "font-mono text-xs font-bold text-primary", children: ["+", ev.timeOffsetMs, "ms"] }), _jsx("span", { className: "text-sm font-semibold text-foreground", children: ev.title }), _jsx(Badge, { variant: "outline", size: "sm", children: ev.type })] }), _jsxs("div", { className: "flex items-center gap-3 text-xs font-mono text-muted-foreground", children: [_jsxs("span", { children: [ev.timestamp, " UTC"] }), _jsxs("span", { children: [ev.durationMs, " ms"] }), ev.costUsd > 0 && _jsxs("span", { className: "text-emerald-400 font-bold", children: ["$", ev.costUsd.toFixed(5)] })] })] }), _jsx("p", { className: "text-xs text-muted-foreground", children: ev.summary }), _jsxs("div", { className: "pt-2 border-t border-border/40 flex items-center justify-between text-[11px] font-mono text-muted-foreground", children: [_jsxs("span", { children: ["Evidence ID: ", _jsx("span", { className: "text-foreground", children: ev.evidenceId })] }), _jsxs("span", { className: "truncate max-w-xs", children: ["Hash: ", ev.hash.slice(0, 20), "..."] })] })] })] }, ev.evidenceId))) })] }));
};
