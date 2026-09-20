import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Zap, PlusCircle, CheckCircle2, } from 'lucide-react';
export const OpportunityDiscoveryCenter = () => {
    const opportunities = [
        {
            id: 'opp-01',
            title: 'Shared Corporate Invoice Header Caching',
            category: 'CACHING_OPTIMIZATION',
            description: 'Recurring corporate invoice formats share 85% identical header tokens across vendor documents.',
            latencyGainPct: 28.0,
            costSavingPct: 22.0,
            confidence: 0.985,
            directive: 'Enable zero-copy speculative embedding cache for top 50 corporate invoice schemas.',
        },
        {
            id: 'opp-02',
            title: 'Triadic Extraction Strike Team Template',
            category: 'WORKFLOW_REUSE',
            description: 'Pre-compose specialist agent coalitions for multi-column balance sheets to bypass auction renegotiation latency.',
            latencyGainPct: 19.5,
            costSavingPct: 8.0,
            confidence: 0.992,
            directive: 'Deploy pre-warmed triadic agent coalition template on high-volume accounting queues.',
        },
        {
            id: 'opp-03',
            title: 'Lock-Free Memory Buffer Migration',
            category: 'AGENT_SPECIALIZATION',
            description: 'Transition hot fact telemetry from mutex locks to atomic circular ring buffers.',
            latencyGainPct: 15.0,
            costSavingPct: 5.0,
            confidence: 0.978,
            directive: 'Activate zero-lock ring buffer in event routing subsystem.',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Opportunity Discovery Center" }), _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: true, children: "SYNERGY MINER ACTIVE" }), _jsx(Badge, { variant: "outline", size: "sm", children: "AWM-PSDTIP Phase 13.10" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Autonomous discovery of unexploited capability synergies, workflow reuse, caching potential, and proactive execution accelerations." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "intelligence", size: "sm", children: [_jsx(PlusCircle, { className: "w-3.5 h-3.5 mr-1.5" }), "Discover New Opportunities"] }) })] }), _jsx("div", { className: "space-y-4", children: opportunities.map((opp) => (_jsxs(Card, { className: "p-5 border-border/40 space-y-4 hover:border-purple-500/30 transition-colors", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2", children: [_jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: opp.category.replace(/_/g, ' ') }), _jsx("h2", { className: "text-base font-semibold text-foreground", children: opp.title })] }), _jsx("p", { className: "text-xs text-muted-foreground", children: opp.description })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Badge, { variant: "success", size: "sm", children: ["+", opp.latencyGainPct, "% Speed"] }), _jsxs(Badge, { variant: "info", size: "sm", children: ["-", opp.costSavingPct, "% Cost"] })] })] }), _jsxs("div", { className: "flex items-center gap-2 text-xs text-purple-300 bg-purple-950/20 p-2.5 rounded border border-purple-500/30", children: [_jsx(Zap, { className: "w-3.5 h-3.5 text-purple-400 flex-shrink-0" }), _jsxs("span", { children: ["Actionable Directive: ", opp.directive] })] }), _jsxs("div", { className: "flex items-center justify-between text-xs pt-2 border-t border-border/30", children: [_jsxs("div", { className: "flex items-center gap-1.5 text-muted-foreground font-mono", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5 text-emerald-400" }), _jsxs("span", { children: ["Confidence: ", (opp.confidence * 100).toFixed(1), "%"] })] }), _jsx(Button, { variant: "outline", size: "sm", children: "Apply Recommended Optimization" })] })] }, opp.id))) })] }));
};
