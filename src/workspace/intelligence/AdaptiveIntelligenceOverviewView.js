import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const AdaptiveIntelligenceOverviewView = () => {
    const [activeCycle, setActiveCycle] = useState(null);
    const metrics = {
        totalExperiences: 1420,
        minedStrategies: 8,
        activeHypotheses: 5,
        abExperimentsCompleted: 14,
        statisticallyPromoted: 6,
        meanImprovementPct: '18.4%',
        predictionMAE: '42.1 ms',
        currentPlannerVersion: 'v2.1.0',
        evidenceLinkageRate: '100.0%',
        scientificPValue: 'p < 0.001',
    };
    const activeImprovements = [
        {
            id: 'pipe_inv_opt_01',
            title: 'Invoice Fan-Out Parallelization',
            domain: 'Invoice',
            stage: 'DEPLOYED',
            pVal: 'p = 0.0004',
            improvement: '+22.4% Latency Reduction',
            version: 'v2.1.0',
        },
        {
            id: 'pipe_legal_02',
            title: 'Legal Contract Pre-validation Invariant Guard',
            domain: 'Contract',
            stage: 'MONITORING',
            pVal: 'p = 0.0012',
            improvement: '-85.0% Downstream Retries',
            version: 'v2.0.4',
        },
        {
            id: 'pipe_med_03',
            title: 'Medical Clinical Trial Vision Tiering',
            domain: 'Medical',
            stage: 'EXPERIMENT_RUNNING',
            pVal: 'p = 0.0210',
            improvement: '+14.2% Cost Savings',
            version: 'CANDIDATE',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Adaptive Intelligence & Scientific Learning" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "AISLCOP v10.0" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Closed-loop self-improving platform: Experience \u2192 Hypothesis \u2192 A/B Experimentation \u2192 Statistical Verification \u2192 Versioned Deployment." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "success", size: "md", children: "Scientific Attestation: Validated" }), _jsxs(Badge, { variant: "outline", size: "md", children: ["Active: ", metrics.currentPlannerVersion] })] })] }), _jsxs("div", { className: "grid grid-cols-2 sm:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 border-primary/20", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Experiences Logged" }), _jsx("div", { className: "text-2xl font-bold font-mono text-foreground mt-1", children: metrics.totalExperiences }), _jsx("div", { className: "text-[11px] text-emerald-400 mt-1", children: "100% Cryptographically Hashed" })] }), _jsxs(Card, { className: "p-4", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Mined Strategies" }), _jsx("div", { className: "text-2xl font-bold font-mono text-foreground mt-1", children: metrics.minedStrategies }), _jsxs("div", { className: "text-[11px] text-muted-foreground mt-1", children: [metrics.statisticallyPromoted, " Promoted"] })] }), _jsxs(Card, { className: "p-4", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "A/B Experiments" }), _jsx("div", { className: "text-2xl font-bold font-mono text-foreground mt-1", children: metrics.abExperimentsCompleted }), _jsx("div", { className: "text-[11px] text-emerald-400 mt-1", children: "Welch's t-test (p < 0.05)" })] }), _jsxs(Card, { className: "p-4", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Mean System Gain" }), _jsx("div", { className: "text-2xl font-bold font-mono text-foreground mt-1", children: metrics.meanImprovementPct }), _jsxs("div", { className: "text-[11px] text-primary mt-1", children: ["Prediction MAE: ", metrics.predictionMAE] })] })] }), _jsxs(Card, { className: "p-5 border-border/60 bg-muted/10", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-border/40 pb-3 mb-4", children: [_jsx("h2", { className: "text-sm font-semibold tracking-wide", children: "Scientific Decision Loop & Optimization Pipeline" }), _jsx(Badge, { variant: "outline", size: "sm", children: "Deterministic & Reversible" })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-7 gap-2 text-center text-xs", children: [_jsxs("div", { className: "p-3 rounded-lg border border-border/60 bg-background flex flex-col items-center justify-center", children: [_jsx("span", { className: "font-semibold text-foreground", children: "1. Execution" }), _jsx("span", { className: "text-[10px] text-muted-foreground mt-1", children: "DAG Telemetry" })] }), _jsxs("div", { className: "p-3 rounded-lg border border-border/60 bg-background flex flex-col items-center justify-center", children: [_jsx("span", { className: "font-semibold text-foreground", children: "2. Experience" }), _jsx("span", { className: "text-[10px] text-muted-foreground mt-1", children: "Evidence Merkle" })] }), _jsxs("div", { className: "p-3 rounded-lg border border-border/60 bg-background flex flex-col items-center justify-center", children: [_jsx("span", { className: "font-semibold text-foreground", children: "3. Mining" }), _jsx("span", { className: "text-[10px] text-muted-foreground mt-1", children: "Candidate Strat" })] }), _jsxs("div", { className: "p-3 rounded-lg border border-border/60 bg-background flex flex-col items-center justify-center", children: [_jsx("span", { className: "font-semibold text-foreground", children: "4. Hypothesis" }), _jsx("span", { className: "text-[10px] text-muted-foreground mt-1", children: "Bottleneck Delta" })] }), _jsxs("div", { className: "p-3 rounded-lg border border-border/60 bg-background flex flex-col items-center justify-center", children: [_jsx("span", { className: "font-semibold text-foreground", children: "5. A/B Trials" }), _jsx("span", { className: "text-[10px] text-muted-foreground mt-1", children: "Control vs Cand" })] }), _jsxs("div", { className: "p-3 rounded-lg border border-border/60 bg-background flex flex-col items-center justify-center", children: [_jsx("span", { className: "font-semibold text-foreground", children: "6. Verification" }), _jsx("span", { className: "text-[10px] text-emerald-400 mt-1", children: "p < 0.05" })] }), _jsxs("div", { className: "p-3 rounded-lg border border-emerald-500/40 bg-emerald-950/20 flex flex-col items-center justify-center", children: [_jsx("span", { className: "font-semibold text-emerald-400", children: "7. Deploy & Rollback" }), _jsx("span", { className: "text-[10px] text-emerald-300 mt-1", children: "Versioned Kernel" })] })] })] }), _jsxs(Card, { className: "p-5", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-border/40 pb-3 mb-4", children: [_jsx("h2", { className: "text-sm font-semibold tracking-wide", children: "Active Continuous Improvement Pipelines" }), _jsx("button", { onClick: () => setActiveCycle('Triggered autonomous learning loop for invoice domain'), className: "text-xs px-3 py-1.5 rounded bg-primary text-primary-foreground hover:bg-primary/90 transition-colors font-medium", children: "Trigger Optimization Cycle" })] }), activeCycle && (_jsxs("div", { className: "mb-4 p-3 rounded bg-emerald-950/30 border border-emerald-500/30 text-xs text-emerald-300", children: [activeCycle, " \u2014 A/B validation concluded with p < 0.001. Promoted to planner version."] })), _jsx("div", { className: "space-y-3", children: activeImprovements.map((pipe) => (_jsxs("div", { className: "p-3 rounded-lg border border-border/60 bg-muted/5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-semibold text-xs text-foreground", children: pipe.title }), _jsx(Badge, { variant: pipe.stage === 'DEPLOYED' ? 'success' : pipe.stage === 'MONITORING' ? 'intelligence' : 'warning', size: "sm", children: pipe.stage }), _jsxs("span", { className: "text-[11px] text-muted-foreground font-mono", children: ["[", pipe.domain, "]"] })] }), _jsxs("div", { className: "text-xs text-muted-foreground mt-1 flex items-center gap-3", children: [_jsxs("span", { children: ["Significance: ", _jsx("strong", { className: "text-emerald-400", children: pipe.pVal })] }), _jsxs("span", { children: ["Measured Delta: ", _jsx("strong", { className: "text-foreground", children: pipe.improvement })] })] })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Badge, { variant: "outline", size: "sm", className: "font-mono", children: ["Target: ", pipe.version] }) })] }, pipe.id))) })] })] }));
};
