import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const CapabilityRegistryView = () => {
    const capabilities = [
        {
            name: 'perception.ocr',
            category: 'Perception',
            description: 'Document image binarization, de-skewing, token segmentation, and bounding box coordinates.',
            providers: [
                { name: 'Tesseract V5 Enhanced', plugin: 'plugin.invoice.processing', latency: '120 ms', cost: '$0.00010', quality: '98.0%', status: 'OPTIMAL' },
                { name: 'Cloud Vision API', plugin: 'plugin.cloud_ocr', latency: '450 ms', cost: '$0.00250', quality: '99.5%', status: 'BACKUP' },
            ],
        },
        {
            name: 'extraction.invoice',
            category: 'Extraction',
            description: 'Structured financial extraction including vendor name, tax ID, line items, and totals.',
            providers: [
                { name: 'InvoicePro Structured Extractor', plugin: 'plugin.invoice.processing', latency: '280 ms', cost: '$0.00180', quality: '99.1%', status: 'OPTIMAL' },
            ],
        },
        {
            name: 'validation.reconciliation',
            category: 'Validation',
            description: 'Invariant mathematical proof: subtotal + taxes == invoice total, Mod11 checksum.',
            providers: [
                { name: 'Mod11 Invariant Validator', plugin: 'plugin.invoice.processing', latency: '18 ms', cost: '$0.00000', quality: '100.0%', status: 'OPTIMAL' },
            ],
        },
        {
            name: 'privacy.deidentify',
            category: 'Privacy & Security',
            description: 'Zero-knowledge PHI redaction and HIPAA compliance boundary enforcement.',
            providers: [
                { name: 'HIPAA Shield Enclave', plugin: 'plugin.medical.records', latency: '65 ms', cost: '$0.00020', quality: '99.8%', status: 'OPTIMAL' },
            ],
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Dynamic Capability Registry" }), _jsx(Badge, { variant: "success", size: "sm", children: "Pareto Resolver Active" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Abstract capabilities registered by plugins. The planner dynamically binds to the optimal provider based on real-time cost, latency, and quality." })] }), _jsxs(Badge, { variant: "intelligence", size: "md", children: [capabilities.length, " Abstract Capabilities"] })] }), _jsx("div", { className: "grid grid-cols-1 gap-4", children: capabilities.map((cap) => (_jsxs(Card, { className: "p-5 space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-sm font-bold text-foreground", children: cap.name }), _jsx(Badge, { variant: "outline", size: "sm", children: cap.category })] }), _jsxs("span", { className: "text-xs text-muted-foreground font-mono", children: [cap.providers.length, " Provider(s)"] })] }), _jsx("p", { className: "text-xs text-muted-foreground", children: cap.description }), _jsx("div", { className: "border border-border/40 rounded-lg overflow-hidden mt-2", children: _jsxs("table", { className: "w-full text-left text-xs font-mono", children: [_jsx("thead", { className: "bg-muted/40 text-muted-foreground", children: _jsxs("tr", { children: [_jsx("th", { className: "p-2.5", children: "Provider Implementation" }), _jsx("th", { className: "p-2.5", children: "Plugin Source" }), _jsx("th", { className: "p-2.5", children: "P95 Latency" }), _jsx("th", { className: "p-2.5", children: "Cost / Call" }), _jsx("th", { className: "p-2.5", children: "Quality" }), _jsx("th", { className: "p-2.5", children: "Planner Status" })] }) }), _jsx("tbody", { className: "divide-y divide-border/40", children: cap.providers.map((prov) => (_jsxs("tr", { children: [_jsx("td", { className: "p-2.5 font-bold text-foreground", children: prov.name }), _jsx("td", { className: "p-2.5 text-muted-foreground", children: prov.plugin }), _jsx("td", { className: "p-2.5", children: prov.latency }), _jsx("td", { className: "p-2.5", children: prov.cost }), _jsx("td", { className: "p-2.5 text-emerald-400 font-bold", children: prov.quality }), _jsx("td", { className: "p-2.5", children: _jsx(Badge, { variant: prov.status === 'OPTIMAL' ? 'success' : 'outline', size: "sm", children: prov.status }) })] }, prov.name))) })] }) })] }, cap.name))) })] }));
};
