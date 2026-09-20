import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Users, PlusCircle, } from 'lucide-react';
export const TaskMarketplaceView = () => {
    const [auctions] = useState([
        {
            id: 'auc-001',
            name: 'Batch Document OCR & Entity Extraction (50 Pages)',
            type: 'WEIGHTED_UTILITY',
            maxBudget: 100.0,
            deadlineSec: 10.0,
            status: 'AWARDED',
            bids: [
                { bidder: 'agent-spec-ocr', cost: 65.0, latencyMs: 140, score: 0.942, status: 'ACCEPTED' },
                { bidder: 'agent-res-opt', cost: 80.0, latencyMs: 220, score: 0.810, status: 'REJECTED' },
            ],
        },
        {
            id: 'auc-002',
            name: 'Cryptographic Merkle Tree Proof Generator',
            type: 'FIRST_PRICE_SEALED',
            maxBudget: 45.0,
            deadlineSec: 5.0,
            status: 'AWARDED',
            bids: [
                { bidder: 'agent-val-sec', cost: 30.0, latencyMs: 80, score: 0.985, status: 'ACCEPTED' },
            ],
        },
    ]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Task Auction Marketplace" }), _jsx(Badge, { variant: "success", size: "sm", children: "MARKET LIQUID" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Decentralized task auctions, competitive agent bidding, Pareto-optimal utility scoring, and contract settlement." })] }), _jsxs(Button, { variant: "primary", size: "sm", children: [_jsx(PlusCircle, { className: "w-3.5 h-3.5 mr-1.5" }), "Publish Auction Task"] })] }), _jsx("div", { className: "space-y-4", children: auctions.map(auc => (_jsxs(Card, { className: "p-5 border-border/60 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border/40 pb-3", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "outline", size: "sm", className: "font-mono", children: auc.id }), _jsx("h3", { className: "font-bold text-sm", children: auc.name })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: auc.type }), _jsx(Badge, { variant: "success", size: "sm", children: auc.status })] })] }), _jsxs("div", { className: "grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono", children: [_jsxs("div", { className: "p-2.5 rounded bg-muted/20 border border-border/30", children: [_jsx("span", { className: "text-[10px] text-muted-foreground block", children: "Max Budget Cap" }), _jsxs("span", { className: "font-bold text-emerald-400", children: ["$", auc.maxBudget, " USD"] })] }), _jsxs("div", { className: "p-2.5 rounded bg-muted/20 border border-border/30", children: [_jsx("span", { className: "text-[10px] text-muted-foreground block", children: "SLA Deadline" }), _jsxs("span", { className: "font-bold text-blue-400", children: [auc.deadlineSec, "s"] })] }), _jsxs("div", { className: "p-2.5 rounded bg-muted/20 border border-border/30", children: [_jsx("span", { className: "text-[10px] text-muted-foreground block", children: "Total Bids" }), _jsxs("span", { className: "font-bold text-purple-400", children: [auc.bids.length, " Submitted"] })] }), _jsxs("div", { className: "p-2.5 rounded bg-muted/20 border border-border/30", children: [_jsx("span", { className: "text-[10px] text-muted-foreground block", children: "Award Status" }), _jsx("span", { className: "font-bold text-emerald-400", children: "Settled & Locked" })] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground block mb-2", children: "Agent Bidding Log" }), _jsx("div", { className: "space-y-2", children: auc.bids.map(b => (_jsxs("div", { className: `flex items-center justify-between p-3 rounded-lg border text-xs font-mono ${b.status === 'ACCEPTED'
                                            ? 'bg-emerald-950/20 border-emerald-500/30 text-emerald-300'
                                            : 'bg-muted/10 border-border/20 text-muted-foreground'}`, children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Users, { className: "w-3.5 h-3.5" }), _jsx("span", { className: "font-bold", children: b.bidder })] }), _jsxs("div", { className: "flex items-center gap-4", children: [_jsxs("span", { children: ["Cost: $", b.cost] }), _jsxs("span", { children: ["Latency: ", b.latencyMs, "ms"] }), _jsxs("span", { className: "font-semibold", children: ["Utility: ", (b.score * 100).toFixed(1), "%"] }), _jsx(Badge, { variant: b.status === 'ACCEPTED' ? 'success' : 'default', size: "sm", children: b.status })] })] }, b.bidder))) })] })] }, auc.id))) })] }));
};
