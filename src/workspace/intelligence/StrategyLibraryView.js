import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const StrategyLibraryView = () => {
    const [promotedOnly, setPromotedOnly] = useState(false);
    const strategies = [
        {
            id: 'strat_inv_01',
            name: 'Optimized Invoice Parallel Fan-Out Strategy',
            domain: 'Invoice',
            version: '2.1.0',
            isPromoted: true,
            successRate: 0.994,
            meanLatency: 910.4,
            meanCost: 0.0078,
            sampleSize: 420,
            tools: ['tesseract_v2', 'schema_validator', 'gemini-1.5-flash'],
            failureModes: ['Low-resolution skew on line item headers'],
        },
        {
            id: 'strat_con_01',
            name: 'High-Fidelity Legal Contract Multi-Pass Strategy',
            domain: 'Contract',
            version: '1.4.0',
            isPromoted: true,
            successRate: 0.982,
            meanLatency: 2150.0,
            meanCost: 0.0320,
            sampleSize: 180,
            tools: ['pdfplumber_advanced', 'clause_extractor', 'gemini-1.5-pro'],
            failureModes: ['Unstandardized indemnification phrasing'],
        },
        {
            id: 'strat_med_01',
            name: 'Clinical Record & HIPAA Redaction Fast-Track',
            domain: 'Medical',
            version: '1.2.0',
            isPromoted: false,
            successRate: 0.965,
            meanLatency: 1750.0,
            meanCost: 0.0240,
            sampleSize: 95,
            tools: ['vision_multimodal_ocr', 'hipaa_guard', 'gemini-1.5-pro'],
            failureModes: ['Handwritten doctor signatures'],
        },
    ];
    const displayed = promotedOnly ? strategies.filter((s) => s.isPromoted) : strategies;
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Strategy Mining Library" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Pillar 2" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Empirically mined and validated execution strategies with statistical performance profiles and failure mode catalog." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx("button", { onClick: () => setPromotedOnly(!promotedOnly), className: `text-xs px-3 py-1.5 rounded transition-colors font-medium ${promotedOnly ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground'}`, children: promotedOnly ? 'Showing Promoted Only' : 'Show All Strategies' }) })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: displayed.map((strat) => (_jsxs(Card, { className: "p-5 flex flex-col justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between gap-2 mb-2", children: [_jsx("span", { className: "font-mono text-xs text-primary font-semibold", children: strat.id }), _jsxs("div", { className: "flex items-center gap-1.5", children: [_jsx(Badge, { variant: "outline", size: "sm", className: "font-mono", children: strat.version }), strat.isPromoted && _jsx(Badge, { variant: "success", size: "sm", children: "PROMOTED" })] })] }), _jsx("h3", { className: "text-sm font-semibold text-foreground mb-2", children: strat.name }), _jsxs("p", { className: "text-xs text-muted-foreground mb-4", children: ["Domain: ", _jsx("strong", { className: "text-foreground", children: strat.domain })] }), _jsxs("div", { className: "grid grid-cols-3 gap-2 p-2.5 rounded bg-muted/20 border border-border/40 mb-4 text-center", children: [_jsxs("div", { children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Success Rate" }), _jsxs("div", { className: "text-xs font-mono font-bold text-emerald-400", children: [(strat.successRate * 100).toFixed(1), "%"] })] }), _jsxs("div", { children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Mean Latency" }), _jsxs("div", { className: "text-xs font-mono font-bold text-foreground", children: [strat.meanLatency.toFixed(0), " ms"] })] }), _jsxs("div", { children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Mean Cost" }), _jsxs("div", { className: "text-xs font-mono font-bold text-foreground", children: ["$", strat.meanCost.toFixed(4)] })] })] }), _jsxs("div", { className: "mb-4", children: [_jsx("div", { className: "text-[11px] font-semibold text-muted-foreground mb-1", children: "Recommended Tools" }), _jsx("div", { className: "flex flex-wrap gap-1", children: strat.tools.map((t) => (_jsx("span", { className: "text-[10px] px-2 py-0.5 rounded bg-muted font-mono text-muted-foreground", children: t }, t))) })] })] }), _jsxs("div", { className: "border-t border-border/40 pt-3 flex items-center justify-between text-xs text-muted-foreground", children: [_jsxs("span", { children: ["Samples: ", strat.sampleSize, " runs"] }), _jsx("button", { className: "text-primary hover:underline font-medium", children: "Inspect Lineage \u2192" })] })] }, strat.id))) })] }));
};
