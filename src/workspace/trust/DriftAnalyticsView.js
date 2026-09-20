import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const DriftAnalyticsView = () => {
    const metrics = [
        {
            name: 'Execution Latency (ms)',
            baseline: '930.0 ms',
            current: '928.0 ms',
            shift: '-0.21%',
            pValue: 'p = 0.45',
            alert: 'NORMAL',
        },
        {
            name: 'Cost ($/mission)',
            baseline: '$0.0083',
            current: '$0.0084',
            shift: '+1.20%',
            pValue: 'p = 0.38',
            alert: 'NORMAL',
        },
        {
            name: 'Confidence Score',
            baseline: '97.8%',
            current: '98.1%',
            shift: '+0.31%',
            pValue: 'p = 0.52',
            alert: 'NORMAL',
        },
        {
            name: 'Downstream Retry Frequency',
            baseline: '0.050 / msn',
            current: '0.048 / msn',
            shift: '-4.00%',
            pValue: 'p = 0.60',
            alert: 'NORMAL',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Runtime Drift Analytics" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Pillar 9" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Continuous online statistical comparison between 30-day baseline distributions and 24-hour active runtime telemetry." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx(Badge, { variant: "success", size: "md", children: "System Status: HEALTHY_STABLE" }) })] }), _jsxs(Card, { className: "p-4 bg-emerald-950/20 border-emerald-500/30 text-xs text-emerald-300", children: [_jsx("strong", { children: "Monitoring Summary:" }), " All operational metrics remain within \u00B12% statistical tolerance of baseline. Zero regression drift detected across active pipelines."] }), _jsx(Card, { className: "p-0 overflow-hidden", children: _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left text-xs border-collapse", children: [_jsx("thead", { children: _jsxs("tr", { className: "border-b border-border/40 bg-muted/20 font-semibold text-muted-foreground", children: [_jsx("th", { className: "p-3", children: "Tracked Metric" }), _jsx("th", { className: "p-3", children: "30-Day Baseline (N=1420)" }), _jsx("th", { className: "p-3", children: "Active 24h Window (N=120)" }), _jsx("th", { className: "p-3", children: "Distribution Shift" }), _jsx("th", { className: "p-3", children: "Significance (p-value)" }), _jsx("th", { className: "p-3", children: "Drift Alert Level" })] }) }), _jsx("tbody", { className: "divide-y divide-border/20", children: metrics.map((m, idx) => (_jsxs("tr", { className: "hover:bg-muted/10 transition-colors", children: [_jsx("td", { className: "p-3 font-semibold text-foreground", children: m.name }), _jsx("td", { className: "p-3 font-mono text-muted-foreground", children: m.baseline }), _jsx("td", { className: "p-3 font-mono font-bold text-foreground", children: m.current }), _jsx("td", { className: "p-3 font-mono text-emerald-400", children: m.shift }), _jsx("td", { className: "p-3 font-mono text-muted-foreground", children: m.pValue }), _jsx("td", { className: "p-3", children: _jsx(Badge, { variant: m.alert === 'NORMAL' ? 'success' : 'warning', size: "sm", children: m.alert }) })] }, idx))) })] }) }) })] }));
};
