import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { BrainCircuit, Clock } from 'lucide-react';
export const PlannerEventsView = () => {
    const plannerState = {
        state: 'EXECUTION_READY',
        activeMissionId: 'mission-fin-001',
        totalPlansGenerated: 42,
        totalReplansExecuted: 3,
        currentGoal: 'Process and validate 2026 Q3 vendor audit invoices',
        generatedTasksCount: 6,
        estimatedCostUsd: 0.0032,
        criticalPathMs: 185.4,
    };
    const plannerEvents = [
        {
            id: 'evt-pl-001',
            time: '14:20:00.350',
            type: 'PlannerStarted',
            goal: 'Process and validate 2026 Q3 vendor audit invoices',
            strategy: 'DYNAMIC_DAG_SYNTHESIS',
            actor: 'ChiefPlanner',
            details: 'Evaluated 4 sub-goal decomposition heuristics. Selected optimal DAG topology.',
        },
        {
            id: 'evt-pl-002',
            time: '14:20:00.520',
            type: 'PlannerHeuristicEvaluated',
            goal: 'Invoice Ingestion Sub-Graph',
            strategy: 'PARETO_UTILITY_MAXIMIZATION',
            actor: 'ChiefPlanner',
            details: 'Utility score U=0.985 for Gemini 1.5 Flash parallel routing.',
        },
        {
            id: 'evt-pl-003',
            time: '14:20:00.890',
            type: 'PlannerFinished',
            goal: 'DAG Synthesis Complete',
            strategy: 'DAG_COMPOSED',
            actor: 'ChiefPlanner',
            details: 'Synthesized 6 DAG execution nodes with critical path of 185.4ms.',
        },
        {
            id: 'evt-pl-004',
            time: '14:20:01.300',
            type: 'PlannerReplanned',
            goal: 'OCR Chunk 2 Worker Timeout',
            strategy: 'BRANCH_MUTATION_AND_REROUTE',
            actor: 'ChiefPlanner',
            details: 'Pruned stalled branch on worker-ocr-02 and spawned redundant replica.',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Planner Domain Events & Projections" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Read Model" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Real-time projection of autonomous planning events, DAG synthesis decisions, and dynamic replanning triggers." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Badge, { variant: "success", size: "md", children: ["Planner Status: ", plannerState.state] }) })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 bg-emerald-950/10 border-emerald-500/20", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Plans Generated" }), _jsxs("div", { className: "text-2xl font-bold font-mono text-emerald-400 mt-1", children: [plannerState.totalPlansGenerated, " Plans"] }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Cumulative lifecycle" })] }), _jsxs(Card, { className: "p-4 bg-blue-950/10 border-blue-500/20", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Dynamic Replans" }), _jsxs("div", { className: "text-2xl font-bold font-mono text-blue-400 mt-1", children: [plannerState.totalReplansExecuted, " Replans"] }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Fault-induced re-routes" })] }), _jsxs(Card, { className: "p-4 bg-purple-950/10 border-purple-500/20", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Critical Path Latency" }), _jsxs("div", { className: "text-2xl font-bold font-mono text-purple-400 mt-1", children: [plannerState.criticalPathMs, " ms"] }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Parallel execution bound" })] }), _jsxs(Card, { className: "p-4 bg-cyan-950/10 border-cyan-500/20", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Estimated Plan Cost" }), _jsxs("div", { className: "text-2xl font-bold font-mono text-cyan-400 mt-1", children: ["$", plannerState.estimatedCostUsd] }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "6 Active tasks" })] })] }), _jsxs("div", { className: "space-y-3", children: [_jsx("h2", { className: "text-sm font-semibold tracking-wider text-muted-foreground uppercase", children: "Planner Domain Event Log" }), _jsx("div", { className: "grid grid-cols-1 gap-3", children: plannerEvents.map(ev => (_jsxs(Card, { className: "p-4 border-border/60 hover:border-border transition-all space-y-2", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(BrainCircuit, { className: "w-4 h-4 text-primary" }), _jsx("span", { className: "text-sm font-bold text-foreground", children: ev.type }), _jsx(Badge, { variant: "outline", size: "sm", children: ev.strategy })] }), _jsxs("div", { className: "flex items-center gap-2 font-mono text-[11px] text-muted-foreground", children: [_jsx(Clock, { className: "w-3.5 h-3.5" }), _jsxs("span", { children: [ev.time, " UTC"] })] })] }), _jsx("p", { className: "text-xs text-muted-foreground", children: ev.details }), _jsxs("div", { className: "text-[11px] text-muted-foreground font-mono pt-1 border-t border-border/30", children: ["Actor: ", _jsx("strong", { className: "text-foreground", children: ev.actor }), " \u2022 Goal: ", _jsx("strong", { className: "text-primary", children: ev.goal })] })] }, ev.id))) })] })] }));
};
