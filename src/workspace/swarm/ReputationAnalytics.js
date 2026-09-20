import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Award, } from 'lucide-react';
export const ReputationAnalytics = () => {
    const [scorecards] = useState([
        {
            agentId: 'agent-exec-01',
            name: 'Executive Director Alpha',
            compositeScore: 0.990,
            accuracyScore: 0.995,
            slaAdherenceScore: 0.990,
            collaborationQuality: 0.980,
            governanceCompliance: 1.000,
            evaluations: 142,
        },
        {
            agentId: 'agent-spec-ocr',
            name: 'Vision & OCR Specialist',
            compositeScore: 0.982,
            accuracyScore: 0.988,
            slaAdherenceScore: 0.975,
            collaborationQuality: 0.965,
            governanceCompliance: 1.000,
            evaluations: 1250,
        },
        {
            agentId: 'agent-val-sec',
            name: 'Cryptographic Security Validator',
            compositeScore: 0.994,
            accuracyScore: 0.998,
            slaAdherenceScore: 0.992,
            collaborationQuality: 0.990,
            governanceCompliance: 1.000,
            evaluations: 890,
        },
        {
            agentId: 'agent-plan-01',
            name: 'Lead DAG Planner',
            compositeScore: 0.976,
            accuracyScore: 0.980,
            slaAdherenceScore: 0.970,
            collaborationQuality: 0.960,
            governanceCompliance: 1.000,
            evaluations: 310,
        },
        {
            agentId: 'agent-res-opt',
            name: 'Resource & Token Governor',
            compositeScore: 0.964,
            accuracyScore: 0.965,
            slaAdherenceScore: 0.955,
            collaborationQuality: 0.970,
            governanceCompliance: 1.000,
            evaluations: 620,
        },
    ]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Reputation & Trust Analytics" }), _jsx(Badge, { variant: "success", size: "sm", children: "MATHEMATICALLY CALIBRATED" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Multi-dimensional reputation scoring across accuracy, SLA fulfillment, collaboration synergy, and zero-fabrication compliance." })] }) }), _jsx("div", { className: "space-y-4", children: scorecards.map(sc => (_jsxs(Card, { className: "p-5 border-border/60 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border/40 pb-3", children: [_jsxs("div", { className: "flex items-center gap-2.5", children: [_jsx(Award, { className: "w-5 h-5 text-emerald-400" }), _jsxs("div", { children: [_jsx("h3", { className: "font-bold text-sm", children: sc.name }), _jsx("span", { className: "text-[11px] font-mono text-muted-foreground", children: sc.agentId })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsxs("span", { className: "text-xs text-muted-foreground", children: [sc.evaluations, " Verified Missions"] }), _jsxs("div", { className: "px-3 py-1 rounded bg-emerald-950/20 border border-emerald-500/30 text-emerald-400 font-mono font-bold text-sm", children: [(sc.compositeScore * 100).toFixed(1), "% Score"] })] })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4", children: [_jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/30", children: [_jsxs("div", { className: "flex items-center justify-between text-xs mb-1.5", children: [_jsx("span", { className: "text-muted-foreground", children: "Accuracy" }), _jsxs("span", { className: "font-mono font-bold text-emerald-400", children: [(sc.accuracyScore * 100).toFixed(1), "%"] })] }), _jsx("div", { className: "w-full bg-background h-1.5 rounded-full overflow-hidden", children: _jsx("div", { className: "bg-emerald-400 h-full rounded-full", style: { width: `${sc.accuracyScore * 100}%` } }) })] }), _jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/30", children: [_jsxs("div", { className: "flex items-center justify-between text-xs mb-1.5", children: [_jsx("span", { className: "text-muted-foreground", children: "SLA Adherence" }), _jsxs("span", { className: "font-mono font-bold text-blue-400", children: [(sc.slaAdherenceScore * 100).toFixed(1), "%"] })] }), _jsx("div", { className: "w-full bg-background h-1.5 rounded-full overflow-hidden", children: _jsx("div", { className: "bg-blue-400 h-full rounded-full", style: { width: `${sc.slaAdherenceScore * 100}%` } }) })] }), _jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/30", children: [_jsxs("div", { className: "flex items-center justify-between text-xs mb-1.5", children: [_jsx("span", { className: "text-muted-foreground", children: "Collaboration" }), _jsxs("span", { className: "font-mono font-bold text-purple-400", children: [(sc.collaborationQuality * 100).toFixed(1), "%"] })] }), _jsx("div", { className: "w-full bg-background h-1.5 rounded-full overflow-hidden", children: _jsx("div", { className: "bg-purple-400 h-full rounded-full", style: { width: `${sc.collaborationQuality * 100}%` } }) })] }), _jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/30", children: [_jsxs("div", { className: "flex items-center justify-between text-xs mb-1.5", children: [_jsx("span", { className: "text-muted-foreground", children: "Compliance" }), _jsxs("span", { className: "font-mono font-bold text-teal-400", children: [(sc.governanceCompliance * 100).toFixed(1), "%"] })] }), _jsx("div", { className: "w-full bg-background h-1.5 rounded-full overflow-hidden", children: _jsx("div", { className: "bg-teal-400 h-full rounded-full", style: { width: `${sc.governanceCompliance * 100}%` } }) })] })] })] }, sc.agentId))) })] }));
};
