import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const WorkflowDSLEditorView = () => {
    const defaultDSL = `mission_id: dsl-invoice-audit-001
title: Declarative Invoice Processing Pipeline
steps:
  - name: optical_perception
    capability: perception.ocr
    retry_max: 2
    timeout_ms: 3000
  - name: financial_extraction
    capability: extraction.invoice
    depends_on: [optical_perception]
  - name: invariant_reconciliation
    capability: validation.reconciliation
    depends_on: [financial_extraction]
retry_policy:
  max_attempts: 3
  backoff_multiplier: 1.5
reflection: true
policies:
  - pol-sec-001
  - pol-cost-002`;
    const [dslText, setDslText] = useState(defaultDSL);
    const [compiledSummary, setCompiledSummary] = useState(null);
    const handleCompile = () => {
        setCompiledSummary({
            workflowId: 'dsl-invoice-audit-001',
            totalSteps: 3,
            criticalPathDurationMs: 420.0,
            estimatedCostUsd: 0.0019,
            capabilitiesRequired: ['perception.ocr', 'extraction.invoice', 'validation.reconciliation'],
            policiesChecked: ['pol-sec-001 (Privacy)', 'pol-cost-002 (Cost Ceiling)'],
            status: 'COMPILED_AND_VALIDATED',
        });
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Workflow DSL Editor & Compiler" }), _jsx(Badge, { variant: "success", size: "sm", children: "Declarative YAML" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Write declarative YAML/JSON workflows. The compiler translates high-level intents into CPM task graphs." })] }), _jsx("button", { onClick: handleCompile, className: "px-4 py-2 bg-primary hover:bg-primary/90 text-primary-foreground font-semibold text-xs rounded-lg transition-all flex items-center gap-2 shadow-sm cursor-pointer", children: "\u26A1 Compile DSL to Task Graph" })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-2 gap-6", children: [_jsxs("div", { className: "space-y-3", children: [_jsx("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: "YAML Workflow Specification" }), _jsx(Card, { className: "p-4 bg-black/90 border-border/40", children: _jsx("textarea", { value: dslText, onChange: (e) => setDslText(e.target.value), rows: 18, className: "w-full bg-transparent text-emerald-400 font-mono text-xs focus:outline-none resize-none leading-relaxed" }) })] }), _jsxs("div", { className: "space-y-3", children: [_jsx("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: "Compiler Output & Critical Path" }), _jsx(Card, { className: "p-6 space-y-4", children: compiledSummary ? (_jsxs("div", { className: "space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-border/40 pb-3", children: [_jsxs("div", { children: [_jsx("span", { className: "font-mono text-sm font-bold text-foreground", children: compiledSummary.workflowId }), _jsx("div", { className: "text-xs text-muted-foreground mt-0.5", children: "3 Steps Compiled" })] }), _jsx(Badge, { variant: "success", size: "sm", children: compiledSummary.status })] }), _jsxs("div", { className: "grid grid-cols-2 gap-3 font-mono text-xs", children: [_jsxs("div", { className: "p-3 bg-muted/30 rounded border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Critical Path (CPM)" }), _jsxs("div", { className: "text-base font-bold text-foreground mt-1", children: [compiledSummary.criticalPathDurationMs, " ms"] })] }), _jsxs("div", { className: "p-3 bg-muted/30 rounded border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Estimated Spend" }), _jsxs("div", { className: "text-base font-bold text-emerald-400 mt-1", children: ["$", compiledSummary.estimatedCostUsd] })] })] }), _jsxs("div", { className: "space-y-2", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Resolved Capabilities" }), _jsx("div", { className: "flex flex-wrap gap-1.5", children: compiledSummary.capabilitiesRequired.map((cap) => (_jsx(Badge, { variant: "intelligence", size: "sm", children: cap }, cap))) })] }), _jsxs("div", { className: "space-y-2", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Enforced Governance Policies" }), _jsx("div", { className: "flex flex-wrap gap-1.5", children: compiledSummary.policiesChecked.map((pol) => (_jsx(Badge, { variant: "outline", size: "sm", children: pol }, pol))) })] })] })) : (_jsx("div", { className: "py-16 text-center text-muted-foreground text-xs font-mono", children: "Click \"Compile DSL to Task Graph\" to compile and analyze the workflow." })) })] })] })] }));
};
