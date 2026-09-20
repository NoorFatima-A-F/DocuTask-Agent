import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { ArrowRight, } from 'lucide-react';
export const TrustNetworkExplorer = () => {
    const [edges] = useState([
        { source: 'agent-exec-01', target: 'agent-plan-01', trustScore: 0.995, totalCollaborations: 142, status: 'OPTIMAL' },
        { source: 'agent-plan-01', target: 'agent-coord-01', trustScore: 0.985, totalCollaborations: 310, status: 'OPTIMAL' },
        { source: 'agent-coord-01', target: 'agent-spec-ocr', trustScore: 0.978, totalCollaborations: 480, status: 'OPTIMAL' },
        { source: 'agent-spec-ocr', target: 'agent-val-sec', trustScore: 0.992, totalCollaborations: 760, status: 'OPTIMAL' },
        { source: 'agent-val-sec', target: 'agent-res-opt', trustScore: 0.965, totalCollaborations: 390, status: 'OPTIMAL' },
        { source: 'agent-res-opt', target: 'agent-coord-01', trustScore: 0.980, totalCollaborations: 240, status: 'OPTIMAL' },
    ]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Trust Network Explorer" }), _jsx(Badge, { variant: "success", size: "sm", children: "6 TRUST CHANNELS ACTIVE" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Pairwise trust graph edges between collaborating agents, adaptive Bayesian trust scoring, and historical synergy." })] }) }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: edges.map(e => (_jsxs(Card, { className: "p-4 border-border/60 space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs(Badge, { variant: "outline", size: "sm", className: "font-mono", children: [e.totalCollaborations, " Interactions"] }), _jsx(Badge, { variant: "success", size: "sm", children: e.status })] }), _jsxs("div", { className: "flex items-center justify-between p-3 rounded bg-muted/20 border border-border/30 text-xs font-mono", children: [_jsx("span", { className: "font-bold text-foreground", children: e.source }), _jsx(ArrowRight, { className: "w-3.5 h-3.5 text-primary" }), _jsx("span", { className: "font-bold text-foreground", children: e.target })] }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between text-xs mb-1.5 font-mono", children: [_jsx("span", { className: "text-muted-foreground", children: "Pairwise Trust Score" }), _jsxs("span", { className: "font-bold text-emerald-400", children: [(e.trustScore * 100).toFixed(1), "%"] })] }), _jsx("div", { className: "w-full bg-background h-2 rounded-full overflow-hidden", children: _jsx("div", { className: "bg-emerald-400 h-full rounded-full", style: { width: `${e.trustScore * 100}%` } }) })] })] }, `${e.source}-${e.target}`))) })] }));
};
