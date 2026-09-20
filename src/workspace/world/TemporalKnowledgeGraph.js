import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Calendar, } from 'lucide-react';
export const TemporalKnowledgeGraph = () => {
    const [activeTab, setActiveTab] = useState('ALL');
    const nodes = [
        {
            id: 'tnode-01',
            label: 'Legacy Sequential APDLE DAG (T-24h)',
            type: 'MISSION_STATE',
            validFrom: '2026-09-11 00:00 UTC',
            validTo: '2026-09-12 00:00 UTC',
            isProjected: false,
            properties: { mean_latency_ms: 380.0, errors: 0 },
        },
        {
            id: 'tnode-02',
            label: 'Dynamic Fan-Out DAG + Cache (Present)',
            type: 'MISSION_STATE',
            validFrom: '2026-09-12 00:00 UTC',
            isProjected: false,
            properties: { mean_latency_ms: 180.0, cache_hit_rate: 0.82 },
        },
        {
            id: 'tnode-03',
            label: 'Projected Autonomous Strike Swarm (T+48h)',
            type: 'PREDICTED_FUTURE',
            validFrom: '2026-09-14 00:00 UTC',
            isProjected: true,
            properties: { predicted_latency_ms: 95.0, confidence: 0.985 },
        },
    ];
    const filteredNodes = nodes.filter((n) => {
        if (activeTab === 'HISTORICAL')
            return !n.isProjected;
        if (activeTab === 'PROJECTED')
            return n.isProjected;
        return true;
    });
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Temporal Knowledge Graph" }), _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: true, children: "4D TEMPORAL REASONING" }), _jsx(Badge, { variant: "outline", size: "sm", children: "AWM-PSDTIP Phase 13.10" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Time-aware graph linking historical state transitions, evolutionary trajectories, and projected future execution branches." })] }) }), _jsx("div", { className: "flex items-center gap-2 border-b border-border/40 pb-2", children: ['ALL', 'HISTORICAL', 'PROJECTED'].map((t) => (_jsx(Button, { variant: activeTab === t ? 'primary' : 'ghost', size: "sm", onClick: () => setActiveTab(t), children: t }, t))) }), _jsx("div", { className: "space-y-4", children: filteredNodes.map((n) => (_jsxs(Card, { className: `p-5 border transition-all ${n.isProjected
                        ? 'border-purple-500/50 bg-purple-950/20 shadow-sm'
                        : 'border-border/40 bg-secondary/10'}`, children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2", children: [_jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono font-bold text-foreground", children: n.id }), _jsx(Badge, { variant: n.isProjected ? 'intelligence' : 'outline', size: "sm", children: n.type }), n.isProjected && _jsx(Badge, { variant: "success", size: "sm", children: "Projected Future" })] }), _jsx("h3", { className: "text-sm font-semibold text-foreground", children: n.label })] }), _jsxs("div", { className: "text-xs font-mono text-muted-foreground flex items-center gap-1", children: [_jsx(Calendar, { className: "w-3.5 h-3.5" }), _jsxs("span", { children: ["Valid: ", n.validFrom, " ", n.validTo ? `→ ${n.validTo}` : '(Current)'] })] })] }), _jsx("div", { className: "p-3 rounded bg-secondary/20 border border-border/30 text-xs font-mono text-muted-foreground grid grid-cols-1 sm:grid-cols-3 gap-2 mt-3", children: Object.entries(n.properties).map(([k, v], idx) => (_jsxs("div", { className: "truncate", children: [_jsxs("span", { className: "text-foreground", children: [k, ":"] }), " ", String(v)] }, idx))) })] }, n.id))) })] }));
};
