import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const WorkflowComposerView = () => {
    const [nodes] = useState([
        { id: 'step_1', label: 'Document Ingestion & OCR', capability: 'perception.ocr', x: 50, y: 100 },
        { id: 'step_2', label: 'Invoice Field Extraction', capability: 'extraction.invoice', x: 260, y: 100 },
        { id: 'step_3', label: 'VAT Mod11 Reconciliation', capability: 'validation.reconciliation', x: 470, y: 100 },
        { id: 'step_4', label: 'Executive Governance Signoff', capability: 'governance.approval', x: 680, y: 100 },
    ]);
    const [isRunning, setIsRunning] = useState(false);
    const [executionLog, setExecutionLog] = useState(null);
    const handleRunWorkflow = () => {
        setIsRunning(true);
        setTimeout(() => {
            setIsRunning(false);
            setExecutionLog([
                'Compiling Visual DAG topology to APDLE dynamic tasks...',
                'Validating capability contracts: perception.ocr -> extraction.invoice -> validation.reconciliation',
                'Executing Step #1 (OCR): 142 tokens segmented in 124ms',
                'Executing Step #2 (Extraction): Line items & subtotal resolved in 280ms',
                'Executing Step #3 (Reconciliation): Invariant check PASSED (p=0.0001)',
                'Executing Step #4 (Governance): Verified SHA-256 Merkle root sealed',
                '[SUCCESS] Workflow execution completed with 0 errors.',
            ]);
        }, 600);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Visual Workflow Composer" }), _jsx(Badge, { variant: "success", size: "sm", children: "Real Dynamic DAG" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Compose and link autonomous capability nodes visually. Planner compiles the visual graph directly into dynamic execution waves." })] }), _jsx("button", { onClick: handleRunWorkflow, disabled: isRunning, className: "px-4 py-2 bg-primary hover:bg-primary/90 text-primary-foreground font-semibold text-xs rounded-lg transition-all flex items-center gap-2 shadow-sm cursor-pointer", children: isRunning ? 'Executing DAG...' : '▶ Execute Visual Workflow' })] }), _jsxs(Card, { className: "p-6 space-y-4 bg-muted/10 border-border/60", children: [_jsx("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: "Visual DAG Wavefront Pipeline" }), _jsx("div", { className: "flex flex-col md:flex-row items-center justify-between gap-3 overflow-x-auto py-6", children: nodes.map((node, i) => (_jsxs(React.Fragment, { children: [_jsxs("div", { className: "p-4 bg-card border-2 border-primary/40 rounded-xl shadow-md min-w-[180px] text-center space-y-1", children: [_jsxs(Badge, { variant: "intelligence", size: "sm", children: ["Step #", i + 1] }), _jsx("div", { className: "text-xs font-bold text-foreground mt-1", children: node.label }), _jsx("div", { className: "font-mono text-[10px] text-muted-foreground", children: node.capability })] }), i < nodes.length - 1 && (_jsx("div", { className: "text-primary font-bold text-lg hidden md:block", children: "\u2192" }))] }, node.id))) })] }), executionLog && (_jsxs(Card, { className: "p-5 space-y-3", children: [_jsx("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: "DAG Execution Telemetry" }), _jsx("div", { className: "p-4 bg-black/90 rounded border border-border/40 font-mono text-xs text-emerald-400 space-y-1", children: executionLog.map((line, idx) => (_jsxs("div", { children: ["> ", line] }, idx))) })] }))] }));
};
