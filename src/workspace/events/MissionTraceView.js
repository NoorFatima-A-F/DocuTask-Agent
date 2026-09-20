import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const MissionTraceView = () => {
    const spans = [
        { name: 'Mission Lifecycle (Root)', startMs: 0, durationMs: 1980, color: 'bg-emerald-500' },
        { name: 'Dynamic DAG Planning', startMs: 230, durationMs: 540, color: 'bg-blue-500' },
        { name: 'Task Queue & Worker Dispatch', startMs: 800, durationMs: 210, color: 'bg-purple-500' },
        { name: 'OCR Parallel Ingestion (Worker 1)', startMs: 1020, durationMs: 320, color: 'bg-amber-500' },
        { name: 'Scientific Invariant Validation', startMs: 1350, durationMs: 330, color: 'bg-cyan-500' },
        { name: 'Proof Commit & Finalization', startMs: 1690, durationMs: 290, color: 'bg-indigo-500' },
    ];
    const totalDuration = 1980;
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Mission Distributed Flame Trace" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Span Waterfall" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Deep waterfall trace breakdown of event latencies, child spans, and critical execution paths." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx(Badge, { variant: "success", size: "md", children: "Total Duration: 1.98s" }) })] }), _jsxs(Card, { className: "p-6 border-border/60 space-y-4", children: [_jsxs("div", { className: "flex justify-between items-center text-xs font-semibold text-muted-foreground uppercase", children: [_jsx("span", { children: "Execution Spans" }), _jsx("span", { children: "Timeline (0ms - 1980ms)" })] }), _jsx("div", { className: "space-y-3 pt-2", children: spans.map((s, idx) => {
                            const leftPct = (s.startMs / totalDuration) * 100;
                            const widthPct = Math.max(5, (s.durationMs / totalDuration) * 100);
                            return (_jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex justify-between text-xs", children: [_jsx("span", { className: "font-semibold text-foreground", children: s.name }), _jsxs("span", { className: "font-mono text-muted-foreground", children: [s.durationMs, " ms (+", s.startMs, "ms)"] })] }), _jsx("div", { className: "w-full bg-muted/40 h-4 rounded overflow-hidden relative border border-border/30", children: _jsx("div", { className: `${s.color} h-full rounded opacity-90 transition-all`, style: { marginLeft: `${leftPct}%`, width: `${widthPct}%` } }) })] }, idx));
                        }) })] })] }));
};
