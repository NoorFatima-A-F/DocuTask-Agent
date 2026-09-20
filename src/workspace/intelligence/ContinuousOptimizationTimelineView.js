import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const ContinuousOptimizationTimelineView = () => {
    const steps = [
        {
            time: '14:20:00',
            stage: 'DEPLOYED',
            title: 'Planner Kernel Updated to v2.1.0',
            description: 'Activated candidate strategy for Invoice domain with 22.4% latency drop.',
            evidence: '0x8f2a...c31b',
            status: 'success',
        },
        {
            time: '14:18:45',
            stage: 'EVIDENCE_VERIFIED',
            title: 'A/B Experiment #14 Concluded (p = 0.0004)',
            description: 'Welch t-test confirmed rejection of null hypothesis with t = -4.82 and Cohen d = -1.45.',
            evidence: '0x3c7e...b44a',
            status: 'success',
        },
        {
            time: '14:15:10',
            stage: 'EXPERIMENT_RUNNING',
            title: 'Initiated A/B Trial: Parallel vs Sequential DAG',
            description: 'Dispatched 20 shadow missions comparing Control (v2.0.4) against Candidate (v2.1.0).',
            evidence: '0x991a...fe82',
            status: 'info',
        },
        {
            time: '14:12:00',
            stage: 'HYPOTHESIS_FORMULATED',
            title: 'Synthesized Hypothesis: hyp_inv_parallel',
            description: 'Identified 240ms serialization overhead during OCR & table extraction.',
            evidence: '0x661d...009a',
            status: 'info',
        },
        {
            time: '14:00:00',
            stage: 'EXPERIENCE_EXTRACTED',
            title: 'Logged 50 Operational Experiences for Invoices',
            description: 'Compiled latency profiles, cost metrics, and error traces into append-only ledger.',
            evidence: '0x1122...3344',
            status: 'info',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Continuous Optimization Lifecycle Timeline" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Pillar 11" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Complete audit trail of every scientific transition: Observation \u2192 Hypothesis \u2192 Experiment \u2192 Verification \u2192 Deployment." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx(Badge, { variant: "success", size: "md", children: "Audit Immutable" }) })] }), _jsx(Card, { className: "p-5 border-border/60", children: _jsx("div", { className: "space-y-6 relative before:absolute before:inset-0 before:left-3.5 before:w-0.5 before:bg-border/60", children: steps.map((step, idx) => (_jsxs("div", { className: "relative flex items-start gap-4 pl-8", children: [_jsx("div", { className: "absolute left-2.5 top-1.5 w-2.5 h-2.5 rounded-full bg-primary ring-4 ring-background" }), _jsxs("div", { className: "flex-1 p-3.5 rounded-lg border border-border/40 bg-muted/10", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1 mb-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-semibold text-xs text-foreground", children: step.title }), _jsx(Badge, { variant: step.status === 'success' ? 'success' : 'outline', size: "sm", children: step.stage })] }), _jsx("span", { className: "text-[11px] font-mono text-muted-foreground", children: step.time })] }), _jsx("p", { className: "text-xs text-muted-foreground mb-2", children: step.description }), _jsxs("div", { className: "text-[11px] font-mono text-muted-foreground flex items-center gap-2", children: [_jsx("span", { children: "Merkle Root:" }), _jsx("span", { className: "text-emerald-400", children: step.evidence })] })] })] }, idx))) }) })] }));
};
