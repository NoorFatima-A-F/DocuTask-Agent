import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const OrganizationalLearningView = () => {
    const departments = [
        {
            id: 'fin_ops',
            name: 'Financial Operations Department',
            missions: 1420,
            successRate: 0.992,
            specialization: 0.94,
            throughput: 58.0,
            bottleneck: 0.04,
            reviewQuality: 0.98,
            capabilities: ['Invoice Extraction', 'Tax Reconciliation', 'Receipt Parsing'],
        },
        {
            id: 'legal_qa',
            name: 'Legal & Compliance Department',
            missions: 680,
            successRate: 0.978,
            specialization: 0.91,
            throughput: 22.0,
            bottleneck: 0.12,
            reviewQuality: 0.97,
            capabilities: ['Contract Review', 'Clause Indemnity', 'NDA Redaction'],
        },
        {
            id: 'health_rec',
            name: 'Healthcare Records Department',
            missions: 410,
            successRate: 0.985,
            specialization: 0.88,
            throughput: 30.0,
            bottleneck: 0.09,
            reviewQuality: 0.95,
            capabilities: ['HIPAA Redaction', 'Clinical Lab Panels', 'Intake Forms'],
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Organizational Learning Curves" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Pillar 10" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Departmental expertise accumulation, throughput specialization indices, and routing performance benchmarks." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx(Badge, { variant: "success", size: "md", children: "Mean Success: 98.5%" }) })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: departments.map((d) => (_jsx(Card, { className: "p-5 flex flex-col justify-between", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx("span", { className: "font-mono text-xs text-primary font-semibold", children: d.id }), _jsxs(Badge, { variant: "outline", size: "sm", children: ["Spec: ", (d.specialization * 100).toFixed(0), "%"] })] }), _jsx("h3", { className: "text-sm font-semibold text-foreground mb-1", children: d.name }), _jsxs("div", { className: "text-xs text-muted-foreground mb-4", children: ["Total Missions: ", _jsx("strong", { className: "text-foreground", children: d.missions })] }), _jsxs("div", { className: "grid grid-cols-2 gap-2 p-2.5 rounded bg-muted/20 border border-border/40 mb-4 text-center text-xs", children: [_jsxs("div", { children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Success Rate" }), _jsxs("div", { className: "font-mono font-bold text-emerald-400", children: [(d.successRate * 100).toFixed(1), "%"] })] }), _jsxs("div", { children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Throughput" }), _jsxs("div", { className: "font-mono font-bold text-foreground", children: [d.throughput, " docs/min"] })] }), _jsxs("div", { children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Bottleneck Score" }), _jsxs("div", { className: "font-mono font-bold text-emerald-400", children: [(d.bottleneck * 100).toFixed(1), "%"] })] }), _jsxs("div", { children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Review Quality" }), _jsxs("div", { className: "font-mono font-bold text-primary", children: [(d.reviewQuality * 100).toFixed(1), "%"] })] })] }), _jsx("div", { className: "text-[11px] font-semibold text-muted-foreground mb-1.5", children: "Specialized Capabilities" }), _jsx("div", { className: "flex flex-wrap gap-1", children: d.capabilities.map((c) => (_jsx("span", { className: "text-[10px] px-2 py-0.5 rounded bg-muted text-muted-foreground", children: c }, c))) })] }) }, d.id))) })] }));
};
