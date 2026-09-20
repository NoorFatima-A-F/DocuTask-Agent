import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const PredictionAnalyticsView = () => {
    const predictions = [
        {
            missionId: 'msn_1001',
            domain: 'Invoice',
            predLatency: 920.0,
            actLatency: 940.5,
            latencyError: 20.5,
            predCost: 0.0080,
            actCost: 0.0084,
            costError: 0.0004,
            accuracy: 0.965,
        },
        {
            missionId: 'msn_1002',
            domain: 'Contract',
            predLatency: 2100.0,
            actLatency: 2150.0,
            latencyError: 50.0,
            predCost: 0.0320,
            actCost: 0.0342,
            costError: 0.0022,
            accuracy: 0.941,
        },
        {
            missionId: 'msn_1003',
            domain: 'Medical',
            predLatency: 1750.0,
            actLatency: 1820.0,
            latencyError: 70.0,
            predCost: 0.0240,
            actCost: 0.0265,
            costError: 0.0025,
            accuracy: 0.928,
        },
        {
            missionId: 'msn_1004',
            domain: 'Invoice',
            predLatency: 900.0,
            actLatency: 915.0,
            latencyError: 15.0,
            predCost: 0.0080,
            actCost: 0.0082,
            costError: 0.0002,
            accuracy: 0.982,
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Predictive Mission Analytics" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Pillar 9" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Pre-flight forecast comparison vs post-execution empirical telemetry measuring loss function convergence." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "success", size: "md", children: "Mean MAE: 38.9 ms" }), _jsx(Badge, { variant: "outline", size: "md", children: "Loss Convergence: 94.6%" })] })] }), _jsx(Card, { className: "p-0 overflow-hidden", children: _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left text-xs border-collapse", children: [_jsx("thead", { children: _jsxs("tr", { className: "border-b border-border/40 bg-muted/20 font-semibold text-muted-foreground", children: [_jsx("th", { className: "p-3", children: "Mission ID" }), _jsx("th", { className: "p-3", children: "Domain" }), _jsx("th", { className: "p-3", children: "Predicted Latency" }), _jsx("th", { className: "p-3", children: "Observed Latency" }), _jsx("th", { className: "p-3", children: "Latency Delta" }), _jsx("th", { className: "p-3", children: "Predicted Cost" }), _jsx("th", { className: "p-3", children: "Observed Cost" }), _jsx("th", { className: "p-3", children: "Prediction Accuracy" })] }) }), _jsx("tbody", { className: "divide-y divide-border/20", children: predictions.map((p) => (_jsxs("tr", { className: "hover:bg-muted/10 transition-colors", children: [_jsx("td", { className: "p-3 font-mono text-primary font-semibold", children: p.missionId }), _jsx("td", { className: "p-3 font-medium text-foreground", children: p.domain }), _jsxs("td", { className: "p-3 font-mono text-muted-foreground", children: [p.predLatency.toFixed(1), " ms"] }), _jsxs("td", { className: "p-3 font-mono text-foreground font-semibold", children: [p.actLatency.toFixed(1), " ms"] }), _jsxs("td", { className: "p-3 font-mono text-emerald-400", children: ["+", p.latencyError.toFixed(1), " ms"] }), _jsxs("td", { className: "p-3 font-mono text-muted-foreground", children: ["$", p.predCost.toFixed(4)] }), _jsxs("td", { className: "p-3 font-mono text-foreground", children: ["$", p.actCost.toFixed(4)] }), _jsx("td", { className: "p-3", children: _jsxs(Badge, { variant: p.accuracy > 0.95 ? 'success' : 'intelligence', size: "sm", children: [(p.accuracy * 100).toFixed(1), "%"] }) })] }, p.missionId))) })] }) }) })] }));
};
