import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Compass, Calendar, Layers, TrendingUp, PlusCircle, Clock, } from 'lucide-react';
export const StrategicPlanningStudio = () => {
    const [horizonFilter, setHorizonFilter] = useState('ALL');
    const milestones = [
        {
            id: 'mls-01',
            phase: 'Phase 1: Dynamic Partitioning',
            timeframe: 'T+2 Hours',
            title: 'Dynamic Fan-Out DAG Sub-Scheduler',
            objective: 'Split multi-page invoice documents into concurrent child DAG tasks executed across specialist swarm agents.',
            targetGain: '+38.5% Latency Reduction',
            status: 'COMPLETED',
            risk: 'LOW',
        },
        {
            id: 'mls-02',
            phase: 'Phase 2: Embedding Caching',
            timeframe: 'T+1 Day',
            title: 'Speculative Token Cache Layer',
            objective: 'Deploy in-memory zero-copy cache for recurrent invoice table templates and common document schemas.',
            targetGain: '+22.0% Compute Savings',
            status: 'IN_PROGRESS',
            risk: 'MEDIUM',
        },
        {
            id: 'mls-03',
            phase: 'Phase 3: Autonomous Coalition',
            timeframe: 'T+3 Days',
            title: 'Dynamic Strike Team Formation',
            objective: 'Autonomously compose multi-agent verification strike teams for complex multi-column balance sheets.',
            targetGain: '+45.0% Throughput',
            status: 'SCHEDULED',
            risk: 'LOW',
        },
        {
            id: 'mls-04',
            phase: 'Phase 4: Invariant Audit',
            timeframe: 'T+7 Days',
            title: 'Cryptographic SHA-256 Ledger Hardening',
            objective: 'Enforce dual-signature threshold voting on all policy evolutionary changes across the runtime operating system.',
            targetGain: '100% Anti-Usurpation Invariant',
            status: 'SCHEDULED',
            risk: 'LOW',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Strategic Planning Studio" }), _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: true, children: "LONG-HORIZON ROADMAP ACTIVE" }), _jsx(Badge, { variant: "outline", size: "sm", children: "Multi-Stage Planning" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Formulation, Pareto front evaluation, and milestone execution for multi-hour, multi-day, and multi-week strategic roadmaps." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Button, { variant: "outline", size: "sm", children: [_jsx(Calendar, { className: "w-3.5 h-3.5 mr-1.5" }), "Recalculate Horizons"] }), _jsxs(Button, { variant: "intelligence", size: "sm", children: [_jsx(PlusCircle, { className: "w-3.5 h-3.5 mr-1.5" }), "Formulate New Roadmap"] })] })] }), _jsxs(Card, { className: "p-5 bg-gradient-to-r from-blue-950/30 via-purple-950/20 to-background border-blue-500/30 space-y-3", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-blue-500/10 rounded-lg border border-blue-500/20 text-blue-400", children: _jsx(Compass, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsx("h2", { className: "text-sm font-bold text-foreground", children: "Enterprise Autonomous Platform High-Throughput & Zero-Fabrication Roadmap" }), _jsx("p", { className: "text-xs text-muted-foreground", children: "Primary Goal: Sub-200ms Document Processing with Verifiable Cryptographic Zero-Fabrication Guarantees" })] })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "success", size: "sm", children: "Pareto Frontier Optimal" }), _jsx(Badge, { variant: "outline", size: "sm", children: "Confidence 98.5%" })] })] }), _jsxs("div", { className: "space-y-1.5 pt-2", children: [_jsxs("div", { className: "flex justify-between text-xs text-muted-foreground", children: [_jsx("span", { children: "Overall Roadmap Completion" }), _jsx("span", { className: "font-mono text-foreground font-semibold", children: "50% Complete" })] }), _jsx("div", { className: "h-2 w-full bg-secondary/50 rounded-full overflow-hidden", children: _jsx("div", { className: "h-full bg-gradient-to-r from-blue-500 to-purple-500 w-1/2 rounded-full transition-all duration-500" }) })] })] }), _jsx("div", { className: "flex items-center gap-2 border-b border-border/40 pb-2", children: ['ALL', 'MULTI_HOUR', 'MULTI_DAY', 'MULTI_WEEK'].map((h) => (_jsx(Button, { variant: horizonFilter === h ? 'primary' : 'ghost', size: "sm", onClick: () => setHorizonFilter(h), children: h.replace('_', ' ') }, h))) }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: milestones.map((m) => (_jsxs(Card, { className: `p-5 border transition-all ${m.status === 'COMPLETED'
                        ? 'border-emerald-500/30 bg-emerald-950/10'
                        : m.status === 'IN_PROGRESS'
                            ? 'border-blue-500/30 bg-blue-950/10'
                            : 'border-border/40 bg-secondary/10'}`, children: [_jsxs("div", { className: "flex items-start justify-between gap-2", children: [_jsxs("div", { className: "space-y-1", children: [_jsx("span", { className: "text-[11px] font-mono text-muted-foreground", children: m.phase }), _jsx("h3", { className: "text-sm font-semibold text-foreground", children: m.title })] }), _jsx(Badge, { variant: m.status === 'COMPLETED'
                                        ? 'success'
                                        : m.status === 'IN_PROGRESS'
                                            ? 'info'
                                            : 'default', size: "sm", children: m.status })] }), _jsx("p", { className: "text-xs text-muted-foreground my-3", children: m.objective }), _jsxs("div", { className: "flex items-center justify-between text-xs pt-3 border-t border-border/30", children: [_jsxs("div", { className: "flex items-center gap-1.5 text-purple-400 font-mono", children: [_jsx(TrendingUp, { className: "w-3.5 h-3.5" }), _jsx("span", { children: m.targetGain })] }), _jsxs("div", { className: "flex items-center gap-1 text-muted-foreground font-mono", children: [_jsx(Clock, { className: "w-3.5 h-3.5" }), _jsx("span", { children: m.timeframe })] })] })] }, m.id))) }), _jsxs(Card, { className: "p-5 border-border/40 space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Layers, { className: "w-4 h-4 text-purple-400" }), _jsx("h2", { className: "text-base font-semibold", children: "Pareto Optimization Strategy Frontier" })] }), _jsx(Badge, { variant: "outline", size: "sm", children: "Optimal Configuration" })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-3 gap-4", children: [_jsxs("div", { className: "p-3.5 rounded-lg border border-purple-500/20 bg-purple-950/10 space-y-1", children: [_jsx("span", { className: "text-xs text-muted-foreground", children: "Throughput Acceleration" }), _jsx("div", { className: "text-xl font-bold font-mono text-purple-400", children: "+45.0%" }), _jsx("span", { className: "text-[11px] text-muted-foreground", children: "Parallel sub-DAG execution" })] }), _jsxs("div", { className: "p-3.5 rounded-lg border border-emerald-500/20 bg-emerald-950/10 space-y-1", children: [_jsx("span", { className: "text-xs text-muted-foreground", children: "Compute Cost Reduction" }), _jsx("div", { className: "text-xl font-bold font-mono text-emerald-400", children: "-22.0%" }), _jsx("span", { className: "text-[11px] text-muted-foreground", children: "Embedding cache hits" })] }), _jsxs("div", { className: "p-3.5 rounded-lg border border-blue-500/20 bg-blue-950/10 space-y-1", children: [_jsx("span", { className: "text-xs text-muted-foreground", children: "Zero-Fabrication Floor" }), _jsx("div", { className: "text-xl font-bold font-mono text-blue-400", children: "99.8%" }), _jsx("span", { className: "text-[11px] text-muted-foreground", children: "Triadic consensus verification" })] })] })] })] }));
};
