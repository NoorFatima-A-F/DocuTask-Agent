import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const PlannerDecisionLedgerView = () => {
    const [selectedEntry, setSelectedEntry] = useState('pde-0001');
    const ledgerEntries = [
        {
            id: 'pde-0001',
            decisionId: 'dec-opt-8891',
            missionId: 'mission-alpha-889',
            timestamp: '2026-09-10T18:22:10Z',
            selectedPlan: {
                candidateId: 'cand-flash-p3',
                model: 'gemini-2.5-flash',
                dagDepth: 3,
                parallelism: 3,
                predictedCost: 0.0018,
                predictedLatency: 380,
                predictedAccuracy: 0.985,
                estimatedUtility: 0.892,
            },
            candidatePlans: [
                {
                    candidateId: 'cand-flash-p3',
                    model: 'gemini-2.5-flash',
                    dagDepth: 3,
                    parallelism: 3,
                    predictedCost: 0.0018,
                    predictedLatency: 380,
                    predictedAccuracy: 0.985,
                    estimatedUtility: 0.892,
                    isOptimal: true,
                },
                {
                    candidateId: 'cand-pro-p1',
                    model: 'gemini-2.5-pro',
                    dagDepth: 2,
                    parallelism: 1,
                    predictedCost: 0.012,
                    predictedLatency: 1150,
                    predictedAccuracy: 0.994,
                    estimatedUtility: 0.741,
                    isOptimal: false,
                },
                {
                    candidateId: 'cand-hybrid-p2',
                    model: 'gemini-2.5-flash+heuristics',
                    dagDepth: 4,
                    parallelism: 2,
                    predictedCost: 0.0009,
                    predictedLatency: 420,
                    predictedAccuracy: 0.962,
                    estimatedUtility: 0.824,
                    isOptimal: false,
                },
            ],
            regretReport: {
                optimalCandidateId: 'cand-flash-p3',
                predictedUtility: 0.892,
                realizedUtility: 0.904,
                empiricalRegret: 0.0,
                counterfactualGap: 0.012,
                isBoundedOptimal: true,
            },
            previousHash: 'genesis_decision_block_00000000000000000000000000000000',
            entryHash: 'b7c891e45da092a83c7482910fae12089bb3c17820aedfa9102bc45a8f3b20c9',
            rationale: 'Flash with parallelism=3 provides optimal utility with 98.5% accuracy under 400ms latency envelope.',
        },
        {
            id: 'pde-0002',
            decisionId: 'dec-opt-8892',
            missionId: 'mission-alpha-889',
            timestamp: '2026-09-10T18:22:11Z',
            selectedPlan: {
                candidateId: 'cand-dense-ocr-v2',
                model: 'tesseract-v5-enhanced',
                dagDepth: 2,
                parallelism: 4,
                predictedCost: 0.0004,
                predictedLatency: 125,
                predictedAccuracy: 0.991,
                estimatedUtility: 0.945,
            },
            candidatePlans: [
                {
                    candidateId: 'cand-dense-ocr-v2',
                    model: 'tesseract-v5-enhanced',
                    dagDepth: 2,
                    parallelism: 4,
                    predictedCost: 0.0004,
                    predictedLatency: 125,
                    predictedAccuracy: 0.991,
                    estimatedUtility: 0.945,
                    isOptimal: true,
                },
                {
                    candidateId: 'cand-cloud-vision',
                    model: 'google-cloud-vision-v1',
                    dagDepth: 1,
                    parallelism: 1,
                    predictedCost: 0.0025,
                    predictedLatency: 650,
                    predictedAccuracy: 0.993,
                    estimatedUtility: 0.812,
                    isOptimal: false,
                },
            ],
            regretReport: {
                optimalCandidateId: 'cand-dense-ocr-v2',
                predictedUtility: 0.945,
                realizedUtility: 0.948,
                empiricalRegret: 0.0,
                counterfactualGap: 0.003,
                isBoundedOptimal: true,
            },
            previousHash: 'b7c891e45da092a83c7482910fae12089bb3c17820aedfa9102bc45a8f3b20c9',
            entryHash: 'f4102bc45a8f3b20c9b7c891e45da092a83c7482910fae12089bb3c17820aedf',
            rationale: 'Local enhanced OCR satisfies 99% accuracy constraint at 1/6th cost and 5x lower latency than cloud API.',
        },
    ];
    const activeEntry = ledgerEntries.find((e) => e.id === selectedEntry) || ledgerEntries[0];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Planner Decision Ledger" }), _jsx(Badge, { variant: "success", size: "sm", children: "Hash-Chained & Immutable" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Complete audit trail of all candidate plans considered, Pareto frontiers evaluated, and empirical regret calculations." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "intelligence", size: "md", children: "Max Regret: 0.0000" }), _jsx(Badge, { variant: "outline", size: "md", children: "Chain Valid: TRUE" })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: ["Decision Ledger Entries (", ledgerEntries.length, ")"] }), ledgerEntries.map((entry) => {
                                const isSelected = entry.id === selectedEntry;
                                return (_jsxs(Card, { className: `p-4 cursor-pointer transition-all ${isSelected ? 'border-primary ring-1 ring-primary/40 bg-primary/5' : 'hover:border-border/80'}`, onClick: () => setSelectedEntry(entry.id), children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx("span", { className: "font-mono text-xs font-bold text-foreground", children: entry.id }), _jsx("div", { className: "text-xs font-medium text-muted-foreground mt-0.5", children: entry.decisionId })] }), _jsx(Badge, { variant: "success", size: "sm", children: "Bounded Optimal" })] }), _jsxs("div", { className: "mt-2 text-xs font-mono text-foreground/80", children: ["Selected: ", _jsx("span", { className: "text-primary font-bold", children: entry.selectedPlan.model })] }), _jsxs("div", { className: "mt-2 font-mono text-[10px] text-muted-foreground truncate", children: ["Hash: ", entry.entryHash.slice(0, 18), "..."] })] }, entry.id));
                            })] }), _jsx("div", { className: "lg:col-span-2 space-y-6", children: _jsxs(Card, { className: "p-6 space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsx("h2", { className: "text-lg font-bold", children: activeEntry.decisionId }), _jsxs("div", { className: "text-xs text-muted-foreground mt-0.5", children: ["Mission: ", _jsx("span", { className: "font-mono text-foreground", children: activeEntry.missionId }), " | Timestamp: ", _jsx("span", { className: "font-mono text-foreground", children: activeEntry.timestamp })] })] }), _jsxs(Badge, { variant: "intelligence", size: "md", children: ["Selected: ", activeEntry.selectedPlan.candidateId] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: [_jsxs("div", { className: "p-4 bg-muted/30 border border-border/40 rounded-lg space-y-2", children: [_jsx("div", { className: "text-xs font-semibold text-foreground", children: "Selection Rationale" }), _jsx("p", { className: "text-xs text-muted-foreground leading-relaxed", children: activeEntry.rationale })] }), _jsxs("div", { className: "p-4 bg-muted/30 border border-border/40 rounded-lg space-y-2", children: [_jsxs("div", { className: "text-xs font-semibold text-foreground flex items-center justify-between", children: [_jsx("span", { children: "Empirical Regret Analysis" }), _jsxs(Badge, { variant: "success", size: "sm", children: ["Regret: ", activeEntry.regretReport.empiricalRegret.toFixed(4)] })] }), _jsxs("div", { className: "text-xs font-mono space-y-1 text-muted-foreground", children: [_jsxs("div", { children: ["Predicted Utility: ", _jsx("span", { className: "text-foreground", children: activeEntry.regretReport.predictedUtility })] }), _jsxs("div", { children: ["Realized Utility: ", _jsx("span", { className: "text-emerald-400 font-bold", children: activeEntry.regretReport.realizedUtility })] }), _jsxs("div", { children: ["Counterfactual Gap: ", _jsx("span", { className: "text-foreground", children: activeEntry.regretReport.counterfactualGap })] })] })] })] }), _jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: ["Evaluated Candidate Plans (", activeEntry.candidatePlans.length, ")"] }), _jsx("div", { className: "border border-border/40 rounded-lg overflow-hidden", children: _jsxs("table", { className: "w-full text-left text-xs font-mono", children: [_jsx("thead", { className: "bg-muted/50 border-b border-border/40 text-muted-foreground", children: _jsxs("tr", { children: [_jsx("th", { className: "p-2.5", children: "Candidate ID" }), _jsx("th", { className: "p-2.5", children: "Model" }), _jsx("th", { className: "p-2.5", children: "Cost" }), _jsx("th", { className: "p-2.5", children: "Latency" }), _jsx("th", { className: "p-2.5", children: "Accuracy" }), _jsx("th", { className: "p-2.5", children: "Utility" }), _jsx("th", { className: "p-2.5", children: "Status" })] }) }), _jsx("tbody", { className: "divide-y divide-border/40", children: activeEntry.candidatePlans.map((cand) => (_jsxs("tr", { className: cand.isOptimal ? 'bg-primary/10 font-bold' : '', children: [_jsx("td", { className: "p-2.5", children: cand.candidateId }), _jsx("td", { className: "p-2.5 text-foreground", children: cand.model }), _jsxs("td", { className: "p-2.5", children: ["$", cand.predictedCost.toFixed(4)] }), _jsxs("td", { className: "p-2.5", children: [cand.predictedLatency, " ms"] }), _jsxs("td", { className: "p-2.5", children: [(cand.predictedAccuracy * 100).toFixed(1), "%"] }), _jsx("td", { className: "p-2.5 text-primary", children: cand.estimatedUtility.toFixed(3) }), _jsx("td", { className: "p-2.5", children: _jsx(Badge, { variant: cand.isOptimal ? 'success' : 'outline', size: "sm", children: cand.isOptimal ? 'SELECTED' : 'REJECTED' }) })] }, cand.candidateId))) })] }) })] }), _jsxs("div", { className: "p-3 bg-card border border-border/40 rounded font-mono text-[11px] text-muted-foreground space-y-1", children: [_jsxs("div", { children: [_jsx("span", { className: "text-foreground", children: "Previous Entry Hash: " }), activeEntry.previousHash] }), _jsxs("div", { children: [_jsx("span", { className: "text-foreground", children: "Current Entry Hash: " }), _jsx("span", { className: "text-emerald-400 font-bold", children: activeEntry.entryHash })] })] })] }) })] })] }));
};
