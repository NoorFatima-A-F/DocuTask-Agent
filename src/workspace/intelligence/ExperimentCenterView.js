import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const ExperimentCenterView = () => {
    const [selectedRun, setSelectedRun] = useState('exp_run_01');
    const experiments = [
        {
            id: 'exp_run_01',
            title: 'A/B Trial: Parallel vs Sequential DAG on Invoices',
            hypothesisId: 'hyp_inv_parallel',
            sampleSize: 20,
            status: 'CONCLUDED',
            promotesCandidate: true,
            verdict: 'Statistically significant latency reduction of 22.4% (p = 0.0004, Welch t-test).',
            metrics: {
                controlLatency: 940.5,
                candidateLatency: 730.0,
                controlCost: 0.0084,
                candidateCost: 0.0086,
                controlConfidence: 0.978,
                candidateConfidence: 0.982,
                pValue: 0.0004,
                tStat: -4.82,
                cohensD: -1.45,
            },
        },
        {
            id: 'exp_run_02',
            title: 'A/B Trial: Pre-validation Invariant Guard on Contracts',
            hypothesisId: 'hyp_con_preval',
            sampleSize: 15,
            status: 'CONCLUDED',
            promotesCandidate: true,
            verdict: 'Statistically significant retry reduction from 18% to 2% (p = 0.0012).',
            metrics: {
                controlLatency: 2150.0,
                candidateLatency: 1980.0,
                controlCost: 0.0342,
                candidateCost: 0.0315,
                controlConfidence: 0.942,
                candidateConfidence: 0.965,
                pValue: 0.0012,
                tStat: -3.94,
                cohensD: -1.12,
            },
        },
    ];
    const current = experiments.find((e) => e.id === selectedRun) || experiments[0];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "A/B Experimentation & Statistical Center" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Pillar 5" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Randomized trials and shadow replays evaluated using Welch's t-test, Cohen's d effect sizes, and p-value significance filters." })] }), _jsx("div", { className: "flex items-center gap-2", children: experiments.map((exp) => (_jsx("button", { onClick: () => setSelectedRun(exp.id), className: `text-xs px-2.5 py-1 rounded transition-colors font-mono font-medium ${selectedRun === exp.id ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground'}`, children: exp.id }, exp.id))) })] }), current && (_jsx("div", { className: "space-y-4", children: _jsxs(Card, { className: "p-5 border-border/60", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-border/40 pb-3 mb-4", children: [_jsxs("div", { children: [_jsx("span", { className: "font-mono text-xs text-primary font-semibold", children: current.id }), _jsx("h2", { className: "text-sm font-semibold text-foreground mt-0.5", children: current.title })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx(Badge, { variant: current.promotesCandidate ? 'success' : 'error', size: "sm", children: current.promotesCandidate ? 'PROMOTION GRANTED' : 'REJECTED' }) })] }), _jsxs("div", { className: "p-3 rounded bg-emerald-950/30 border border-emerald-500/30 text-xs text-emerald-300 mb-4", children: [_jsx("strong", { children: "Verdict:" }), " ", current.verdict] }), _jsxs("div", { className: "grid grid-cols-2 sm:grid-cols-4 gap-3 text-center mb-4", children: [_jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Control Latency" }), _jsxs("div", { className: "text-sm font-mono font-bold text-foreground mt-1", children: [current.metrics.controlLatency, " ms"] }), _jsx("div", { className: "text-[10px] text-muted-foreground mt-0.5", children: "Baseline" })] }), _jsxs("div", { className: "p-3 rounded bg-emerald-950/20 border border-emerald-500/30", children: [_jsx("div", { className: "text-[10px] text-emerald-400", children: "Candidate Latency" }), _jsxs("div", { className: "text-sm font-mono font-bold text-emerald-400 mt-1", children: [current.metrics.candidateLatency, " ms"] }), _jsxs("div", { className: "text-[10px] text-emerald-300 mt-0.5", children: ["-", (((current.metrics.controlLatency - current.metrics.candidateLatency) / current.metrics.controlLatency) * 100).toFixed(1), "%"] })] }), _jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Welch's t-Statistic" }), _jsx("div", { className: "text-sm font-mono font-bold text-primary mt-1", children: current.metrics.tStat }), _jsxs("div", { className: "text-[10px] text-muted-foreground mt-0.5", children: ["d = ", current.metrics.cohensD] })] }), _jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Significance (p-value)" }), _jsx("div", { className: "text-sm font-mono font-bold text-emerald-400 mt-1", children: current.metrics.pValue }), _jsx("div", { className: "text-[10px] text-emerald-300 mt-0.5", children: "\u03B1 = 0.05 Passed" })] })] })] }) }))] }));
};
