import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const DecisionProofExplorerView = () => {
    const [selectedProof, setSelectedProof] = useState('prf_001_inv');
    const proofs = [
        {
            proofId: 'prf_001_inv',
            missionId: 'msn_1001',
            domain: 'Invoice',
            plannerVer: 'v2.1.0',
            formula: 'U(s) = 0.50 * Acc(s) - 0.30 * (Lat(s)/1000) - 0.20 * (Cost(s)/0.01)',
            selectedStrategy: 'Invoice Parallel Fan-Out Strategy',
            selectedStrategyId: 'strat_inv_fanout',
            winningScore: 0.1245,
            evidenceHash: '0x8f2ac31b4e5d6a7b',
            candidates: [
                {
                    name: 'Invoice Parallel Fan-Out Strategy',
                    acc: 0.994,
                    lat: 730.0,
                    cost: 0.0078,
                    utility: 0.1245,
                    feasible: true,
                    rejection: null,
                },
                {
                    name: 'Sequential Single-Pass Baseline',
                    acc: 0.978,
                    lat: 940.0,
                    cost: 0.0084,
                    utility: 0.0390,
                    feasible: true,
                    rejection: null,
                },
                {
                    name: 'Heavy Vision Multi-Pass OCR',
                    acc: 0.996,
                    lat: 2800.0,
                    cost: 0.0450,
                    utility: -1.2420,
                    feasible: false,
                    rejection: 'Exceeded cost SLA ceiling ($0.0450 > $0.0200)',
                },
            ],
        },
    ];
    const current = proofs.find((p) => p.proofId === selectedProof) || proofs[0];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Decision Proof Explorer" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Pillar 2" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Formal mathematical decision proofs capturing evaluated alternatives, utility scores, constraints, and rejection justifications." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [proofs.map((p) => (_jsx("button", { onClick: () => setSelectedProof(p.proofId), className: `text-xs px-2.5 py-1 rounded transition-colors font-mono font-medium ${selectedProof === p.proofId ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground hover:bg-muted/80'}`, children: p.proofId }, p.proofId))), _jsx(Badge, { variant: "success", size: "md", children: "Proof Status: Cryptographically Bound" })] })] }), current && (_jsx("div", { className: "space-y-4", children: _jsxs(Card, { className: "p-5 border-border/60", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 border-b border-border/40 pb-3 mb-4", children: [_jsxs("div", { children: [_jsx("span", { className: "font-mono text-xs text-primary font-semibold", children: current.proofId }), _jsxs("h2", { className: "text-sm font-semibold text-foreground mt-0.5", children: ["Planner Strategy Selection for Mission ", _jsx("strong", { className: "font-mono text-primary", children: current.missionId })] }), _jsxs("div", { className: "text-xs text-muted-foreground mt-1 font-mono", children: ["Objective Function: ", _jsx("strong", { className: "text-foreground", children: current.formula })] })] }), _jsxs("div", { className: "text-right", children: [_jsxs(Badge, { variant: "success", size: "sm", children: ["WINNER: ", current.selectedStrategyId] }), _jsxs("div", { className: "text-[11px] font-mono text-emerald-400 mt-1", children: ["Score: +", current.winningScore.toFixed(4)] })] })] }), _jsx("h3", { className: "text-xs font-semibold text-muted-foreground mb-2", children: "Evaluated Alternatives & Objective Scores" }), _jsx("div", { className: "overflow-x-auto border border-border/40 rounded-lg", children: _jsxs("table", { className: "w-full text-left text-xs border-collapse", children: [_jsx("thead", { children: _jsxs("tr", { className: "border-b border-border/40 bg-muted/20 font-semibold text-muted-foreground", children: [_jsx("th", { className: "p-3", children: "Candidate Strategy" }), _jsx("th", { className: "p-3", children: "Accuracy" }), _jsx("th", { className: "p-3", children: "Latency (ms)" }), _jsx("th", { className: "p-3", children: "Cost ($)" }), _jsx("th", { className: "p-3", children: "Utility Score" }), _jsx("th", { className: "p-3", children: "Feasibility" }), _jsx("th", { className: "p-3", children: "Rejection / Selection Rationale" })] }) }), _jsx("tbody", { className: "divide-y divide-border/20", children: current.candidates.map((c, idx) => (_jsxs("tr", { className: c.name === current.selectedStrategy ? 'bg-primary/5' : 'hover:bg-muted/10', children: [_jsxs("td", { className: "p-3 font-semibold text-foreground", children: [c.name, c.name === current.selectedStrategy && (_jsx("span", { className: "ml-2 text-[10px] text-emerald-400 font-mono font-bold", children: "\u2190 SELECTED" }))] }), _jsxs("td", { className: "p-3 font-mono text-emerald-400", children: [(c.acc * 100).toFixed(1), "%"] }), _jsxs("td", { className: "p-3 font-mono", children: [c.lat.toFixed(0), " ms"] }), _jsxs("td", { className: "p-3 font-mono", children: ["$", c.cost.toFixed(4)] }), _jsx("td", { className: "p-3 font-mono font-bold text-foreground", children: c.utility.toFixed(4) }), _jsx("td", { className: "p-3", children: _jsx(Badge, { variant: c.feasible ? 'success' : 'error', size: "sm", children: c.feasible ? 'FEASIBLE' : 'REJECTED' }) }), _jsx("td", { className: "p-3 text-[11px] text-muted-foreground", children: c.rejection || 'Selected: Global Maximum Utility Score' })] }, idx))) })] }) })] }) }))] }));
};
