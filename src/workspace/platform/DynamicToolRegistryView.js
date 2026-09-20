import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const DynamicToolRegistryView = () => {
    const tools = [
        {
            id: 'tool.llm.gemini_2_5_flash',
            name: 'Google Gemini 2.5 Flash API',
            category: 'LLM_INTELLIGENCE',
            description: 'High-speed multi-modal reasoning and structured JSON entity extraction.',
            costPerCall: '$0.00018',
            p95Latency: '180 ms',
            rateLimit: '1000 RPM',
            permissions: ['ai:generate'],
            status: 'ONLINE',
        },
        {
            id: 'tool.ocr.tesseract_v5',
            name: 'Tesseract V5 Enhanced OCR Engine',
            category: 'OPTICAL_PERCEPTION',
            description: 'Local OpenCV-accelerated binary segmentation and token bounding-box generator.',
            costPerCall: '$0.00004',
            p95Latency: '120 ms',
            rateLimit: '5000 RPM',
            permissions: ['ocr:read'],
            status: 'ONLINE',
        },
        {
            id: 'tool.storage.gdrive',
            name: 'Google Drive Enterprise Sync',
            category: 'STORAGE',
            description: 'Secure automated cloud document ingestion and PDF export destination.',
            costPerCall: '$0.00001',
            p95Latency: '220 ms',
            rateLimit: '300 RPM',
            permissions: ['drive:rw'],
            status: 'ONLINE',
        },
        {
            id: 'tool.notification.slack',
            name: 'Slack Incident & Handoff Webhook',
            category: 'COMMUNICATION',
            description: 'Broadcasts human-in-the-loop review alerts and executive status summaries.',
            costPerCall: '$0.00000',
            p95Latency: '95 ms',
            rateLimit: '60 RPM',
            permissions: ['slack:write'],
            status: 'ONLINE',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Dynamic Tool Registry" }), _jsx(Badge, { variant: "success", size: "sm", children: "Declarative Integrations" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Pluggable external and local tools. Each tool advertises cost models, permission scopes, rate limits, and latency percentiles." })] }), _jsxs(Badge, { variant: "outline", size: "md", children: [tools.length, " Dynamic Tools Registered"] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: tools.map((t) => (_jsxs(Card, { className: "p-5 space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx(Badge, { variant: "outline", size: "sm", className: "mb-1", children: t.category }), _jsx("div", { className: "font-bold text-sm text-foreground", children: t.name }), _jsx("div", { className: "font-mono text-[11px] text-muted-foreground mt-0.5", children: t.id })] }), _jsx(Badge, { variant: "success", size: "sm", children: t.status })] }), _jsx("p", { className: "text-xs text-muted-foreground", children: t.description }), _jsxs("div", { className: "grid grid-cols-3 gap-2 pt-2 border-t border-border/40 text-xs font-mono", children: [_jsxs("div", { children: [_jsx("span", { className: "text-muted-foreground", children: "Cost: " }), _jsx("span", { className: "text-foreground", children: t.costPerCall })] }), _jsxs("div", { children: [_jsx("span", { className: "text-muted-foreground", children: "P95: " }), _jsx("span", { className: "text-foreground", children: t.p95Latency })] }), _jsxs("div", { children: [_jsx("span", { className: "text-muted-foreground", children: "Limit: " }), _jsx("span", { className: "text-foreground", children: t.rateLimit })] })] }), _jsxs("div", { className: "flex items-center gap-1 text-[11px] font-mono text-muted-foreground", children: [_jsx("span", { children: "Required Scope:" }), t.permissions.map((p) => (_jsx(Badge, { variant: "intelligence", size: "sm", children: p }, p)))] })] }, t.id))) })] }));
};
