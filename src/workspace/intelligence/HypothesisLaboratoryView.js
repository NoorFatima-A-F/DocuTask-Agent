import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const HypothesisLaboratoryView = () => {
    const [activeTab, setActiveTab] = useState('ALL');
    const hypotheses = [
        {
            id: 'hyp_inv_parallel',
            title: 'Parallel Sub-DAG Fan-Out for Invoices',
            category: 'LATENCY_REDUCTION',
            domain: 'Invoice',
            premise: 'Sequential OCR and table extraction accounts for 940ms latency.',
            action: 'Execute table parsing and metadata extraction concurrently in parallel DAG workers.',
            baseline: '940.0 ms',
            expected: '720.0 ms',
            delta: '-23.4%',
            status: 'VALIDATED',
            pValue: 'p = 0.0004',
        },
        {
            id: 'hyp_con_preval',
            title: 'Pre-validation Invariant Guard for Contracts',
            category: 'RETRY_MINIMIZATION',
            domain: 'Contract',
            premise: 'Contract missions exhibit 0.18 retry rate due to missing liability clauses.',
            action: 'Inject pre-extraction schema invariant validation node in DAG pipeline.',
            baseline: '0.18 retries',
            expected: '0.02 retries',
            delta: '-88.9%',
            status: 'VALIDATED',
            pValue: 'p = 0.0012',
        },
        {
            id: 'hyp_med_flash',
            title: 'Vision-Multimodal Direct Tiering for Medical Docs',
            category: 'COST_OPTIMIZATION',
            domain: 'Medical',
            premise: 'High-clarity medical PDFs can be reliably extracted via multimodal vision directly.',
            action: 'Route clear medical scans directly to vision multimodal pipeline.',
            baseline: '$0.028',
            expected: '$0.016',
            delta: '-42.8%',
            status: 'IN_EXPERIMENT',
            pValue: 'Pending A/B',
        },
        {
            id: 'hyp_receipt_ocr',
            title: 'Heuristic Bounding Box Pre-filter for Receipts',
            category: 'LATENCY_REDUCTION',
            domain: 'Receipt',
            premise: 'Full-page OCR on thermal receipts processes excessive background noise.',
            action: 'Crop active receipt bounding box prior to OCR parse.',
            baseline: '850.0 ms',
            expected: '550.0 ms',
            delta: '-35.3%',
            status: 'PROPOSED',
            pValue: 'Unscheduled',
        },
    ];
    const filtered = activeTab === 'ALL' ? hypotheses : hypotheses.filter((h) => h.status === activeTab);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Hypothesis Formulation Laboratory" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Pillar 4" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Automated discovery of optimization hypotheses from empirical failure patterns and prediction error bottlenecks." })] }), _jsx("div", { className: "flex items-center gap-2", children: ['ALL', 'VALIDATED', 'IN_EXPERIMENT', 'PROPOSED'].map((tab) => (_jsx("button", { onClick: () => setActiveTab(tab), className: `text-xs px-2.5 py-1 rounded transition-colors font-medium ${activeTab === tab ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground'}`, children: tab }, tab))) })] }), _jsx("div", { className: "space-y-3", children: filtered.map((hyp) => (_jsxs(Card, { className: "p-4 border-border/60", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 mb-2", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-xs text-primary font-semibold", children: hyp.id }), _jsx(Badge, { variant: hyp.status === 'VALIDATED' ? 'success' : hyp.status === 'IN_EXPERIMENT' ? 'warning' : 'outline', size: "sm", children: hyp.status }), _jsxs("span", { className: "text-[11px] text-muted-foreground font-mono", children: ["[", hyp.domain, "]"] })] }), _jsx("h3", { className: "text-sm font-semibold text-foreground mt-1", children: hyp.title })] }), _jsxs("div", { className: "text-right", children: [_jsx("div", { className: "text-xs font-semibold text-emerald-400", children: hyp.pValue }), _jsxs("div", { className: "text-[10px] text-muted-foreground", children: ["Category: ", hyp.category] })] })] }), _jsx("p", { className: "text-xs text-muted-foreground mb-3", children: hyp.premise }), _jsxs("div", { className: "p-2.5 rounded bg-muted/20 border border-border/40 text-xs flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2", children: [_jsxs("div", { children: [_jsx("strong", { className: "text-foreground", children: "Proposed Action:" }), " ", _jsx("span", { className: "text-muted-foreground", children: hyp.action })] }), _jsxs("div", { className: "flex items-center gap-3 shrink-0", children: [_jsxs("span", { className: "text-muted-foreground", children: ["Baseline: ", _jsx("strong", { className: "text-foreground", children: hyp.baseline })] }), _jsxs("span", { className: "text-muted-foreground", children: ["\u2192 Expected: ", _jsx("strong", { className: "text-emerald-400", children: hyp.expected }), " (", hyp.delta, ")"] })] })] })] }, hyp.id))) })] }));
};
