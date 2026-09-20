import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const PlannerEvolutionView = () => {
    const [activeVersion, setActiveVersion] = useState('v2.1.0');
    const versions = [
        {
            versionId: 'v2.1.0',
            parent: 'v2.0.4',
            status: 'ACTIVE',
            createdAt: 'Today, 14:20',
            justification: 'Promoted after A/B trial #14 proved 22.4% latency drop with p < 0.001.',
            params: {
                explorationWeight: 0.12,
                latencyPenaltyFactor: 0.48,
                costPenaltyFactor: 0.30,
                confidenceThreshold: 0.92,
                maxDagDepth: 6,
                defaultOcrEngine: 'tesseract_v2_optimized',
            },
        },
        {
            versionId: 'v2.0.4',
            parent: 'v1.0.0',
            status: 'ARCHIVED',
            createdAt: 'Yesterday, 18:00',
            justification: 'Contract invariant validation node integration.',
            params: {
                explorationWeight: 0.18,
                latencyPenaltyFactor: 0.42,
                costPenaltyFactor: 0.30,
                confidenceThreshold: 0.90,
                maxDagDepth: 5,
                defaultOcrEngine: 'tesseract_v2',
            },
        },
        {
            versionId: 'v1.0.0',
            parent: 'None',
            status: 'BASELINE',
            createdAt: 'Initial Release',
            justification: 'Initial factory configuration.',
            params: {
                explorationWeight: 0.25,
                latencyPenaltyFactor: 0.35,
                costPenaltyFactor: 0.30,
                confidenceThreshold: 0.88,
                maxDagDepth: 5,
                defaultOcrEngine: 'tesseract_v2',
            },
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Scientific Planner Evolution" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Pillar 3" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Auditable progression of versioned planner hyperparameters with 1-click deterministic rollback." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Badge, { variant: "success", size: "md", children: ["Active: ", activeVersion] }) })] }), _jsx("div", { className: "space-y-4", children: versions.map((ver) => (_jsxs(Card, { className: `p-5 border-border/60 ${ver.status === 'ACTIVE' ? 'ring-1 ring-primary/40 bg-primary/5' : ''}`, children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 mb-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-base font-bold text-foreground", children: ver.versionId }), _jsx(Badge, { variant: ver.status === 'ACTIVE' ? 'success' : 'outline', size: "sm", children: ver.status }), _jsxs("span", { className: "text-xs text-muted-foreground", children: ["Parent: ", _jsx("strong", { className: "font-mono", children: ver.parent })] })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: ver.justification })] }), _jsx("div", { className: "flex items-center gap-2", children: ver.status !== 'ACTIVE' && (_jsx("button", { onClick: () => setActiveVersion(ver.versionId), className: "text-xs px-3 py-1.5 rounded bg-muted hover:bg-muted/80 text-foreground font-medium transition-colors", children: "Rollback to this Version" })) })] }), _jsxs("div", { className: "grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 text-center text-xs", children: [_jsxs("div", { className: "p-2 rounded bg-muted/20 border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Exploration Weight" }), _jsx("div", { className: "font-mono font-bold text-foreground mt-0.5", children: ver.params.explorationWeight })] }), _jsxs("div", { className: "p-2 rounded bg-muted/20 border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Latency Penalty" }), _jsx("div", { className: "font-mono font-bold text-foreground mt-0.5", children: ver.params.latencyPenaltyFactor })] }), _jsxs("div", { className: "p-2 rounded bg-muted/20 border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Cost Penalty" }), _jsx("div", { className: "font-mono font-bold text-foreground mt-0.5", children: ver.params.costPenaltyFactor })] }), _jsxs("div", { className: "p-2 rounded bg-muted/20 border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Conf Threshold" }), _jsx("div", { className: "font-mono font-bold text-emerald-400 mt-0.5", children: ver.params.confidenceThreshold })] }), _jsxs("div", { className: "p-2 rounded bg-muted/20 border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Max DAG Depth" }), _jsx("div", { className: "font-mono font-bold text-foreground mt-0.5", children: ver.params.maxDagDepth })] }), _jsxs("div", { className: "p-2 rounded bg-muted/20 border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Default OCR Engine" }), _jsx("div", { className: "font-mono text-[11px] text-primary truncate mt-0.5", children: ver.params.defaultOcrEngine })] })] })] }, ver.versionId))) })] }));
};
