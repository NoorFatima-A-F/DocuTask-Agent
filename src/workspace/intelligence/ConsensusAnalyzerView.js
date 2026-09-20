import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const ConsensusAnalyzerView = () => {
    const contributions = [
        {
            agent: 'ChiefPlanner',
            department: 'Planning Dept',
            confidence: 0.98,
            recommendation: 'APPROVE',
            riskScore: 0.02,
            weight: 1.2,
            evidenceHashes: ['0x8f2a...c31b', '0x3c7e...b44a'],
            rationale: 'Topological invariant verification satisfied all constraints with zero DAG cycle risk.',
        },
        {
            agent: 'ComplianceGuard',
            department: 'Governance Dept',
            confidence: 0.96,
            recommendation: 'APPROVE',
            riskScore: 0.04,
            weight: 1.1,
            evidenceHashes: ['0x8f2a...c31b'],
            rationale: 'Enterprise policy boundary checked: data retention SLA verified.',
        },
        {
            agent: 'ValidationWorker',
            department: 'QA Dept',
            confidence: 0.92,
            recommendation: 'APPROVE',
            riskScore: 0.08,
            weight: 1.0,
            evidenceHashes: ['0x991a...fe82'],
            rationale: 'Mathematical checksum and Merkle leaf verification passed.',
        },
        {
            agent: 'CostAuditor',
            department: 'Finance Dept',
            confidence: 0.88,
            recommendation: 'APPROVE',
            riskScore: 0.12,
            weight: 0.9,
            evidenceHashes: ['0x8f2a...c31b'],
            rationale: 'Token spend within $0.015 threshold ceiling.',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Consensus Intelligence & Deliberation" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Pillar 7" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Evidence-weighted multi-agent consensus synthesis replacing naive majority voting with mathematically grounded deliberation." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "success", size: "md", children: "Agreement Score: 98.4%" }), _jsx(Badge, { variant: "outline", size: "md", children: "Composite Conf: 96.2%" })] })] }), _jsxs(Card, { className: "p-5 border-emerald-500/30 bg-emerald-950/10", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-border/40 pb-3 mb-3", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground", children: "Winning Synthesis:" }), _jsx(Badge, { variant: "success", size: "md", children: "APPROVE WITH FULL ATTESTATION" })] }), _jsx("span", { className: "text-xs font-mono text-emerald-400", children: "Dominant Evidence: 0x8f2a...c31b" })] }), _jsx("p", { className: "text-xs text-foreground", children: "4 independent departments contributed weighted deliberation. 0 conflict edges detected across participating agents." })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: contributions.map((c) => (_jsxs(Card, { className: "p-4 border-border/60", children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-semibold text-xs text-foreground", children: c.agent }), _jsxs("span", { className: "text-[10px] text-muted-foreground font-mono", children: ["[", c.department, "]"] })] }), _jsx(Badge, { variant: "success", size: "sm", children: c.recommendation })] }), _jsx("p", { className: "text-xs text-muted-foreground mb-3", children: c.rationale }), _jsxs("div", { className: "grid grid-cols-3 gap-2 p-2 rounded bg-muted/20 border border-border/40 text-center text-xs", children: [_jsxs("div", { children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Confidence" }), _jsxs("div", { className: "font-mono font-bold text-emerald-400", children: [(c.confidence * 100).toFixed(1), "%"] })] }), _jsxs("div", { children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Risk Score" }), _jsxs("div", { className: "font-mono font-bold text-foreground", children: [(c.riskScore * 100).toFixed(1), "%"] })] }), _jsxs("div", { children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Weight Mult" }), _jsxs("div", { className: "font-mono font-bold text-primary", children: [c.weight.toFixed(1), "x"] })] })] })] }, c.agent))) })] }));
};
