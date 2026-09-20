import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const ReplayCertificationView = () => {
    const reports = [
        {
            certId: 'cert_rep_001',
            missionId: 'msn_1001',
            domain: 'Invoice',
            origLat: 940.5,
            repLat: 942.0,
            latDelta: '+0.16%',
            origCost: 0.0084,
            repCost: 0.0084,
            costDelta: '0.00%',
            stateMatch: '99.98%',
            outputSimilarity: '99.95%',
            tier: 'SCIENTIFIC_REPRODUCIBLE',
            certified: true,
            signature: '0x3c7e...b44a',
        },
        {
            certId: 'cert_rep_002',
            missionId: 'msn_1002',
            domain: 'Contract',
            origLat: 2150.0,
            repLat: 2162.0,
            latDelta: '+0.56%',
            origCost: 0.0342,
            repCost: 0.0342,
            costDelta: '0.00%',
            stateMatch: '99.96%',
            outputSimilarity: '99.92%',
            tier: 'SCIENTIFIC_REPRODUCIBLE',
            certified: true,
            signature: '0x991a...fe82',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Runtime Replay Certification" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Pillar 3" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Scientific replay verification comparing original execution traces against deterministic replayed runs." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx(Badge, { variant: "success", size: "md", children: "Parity Pass Rate: 100.0%" }) })] }), _jsx("div", { className: "space-y-4", children: reports.map((r) => (_jsxs(Card, { className: "p-5 border-border/60", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 border-b border-border/40 pb-3 mb-4", children: [_jsxs("div", { children: [_jsx("span", { className: "font-mono text-xs text-primary font-semibold", children: r.certId }), _jsxs("h3", { className: "text-sm font-semibold text-foreground mt-0.5", children: ["Deterministic Replay Certificate for Mission ", _jsx("strong", { className: "font-mono text-primary", children: r.missionId })] })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx(Badge, { variant: "success", size: "sm", children: r.tier }) })] }), _jsxs("div", { className: "grid grid-cols-2 sm:grid-cols-4 gap-3 text-center text-xs mb-4", children: [_jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Bitwise State Match" }), _jsx("div", { className: "font-mono font-bold text-emerald-400 text-sm mt-0.5", children: r.stateMatch }), _jsx("div", { className: "text-[10px] text-muted-foreground mt-0.5", children: "\u2265 99.0% Floor" })] }), _jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Output JSON Similarity" }), _jsx("div", { className: "font-mono font-bold text-emerald-400 text-sm mt-0.5", children: r.outputSimilarity }), _jsx("div", { className: "text-[10px] text-muted-foreground mt-0.5", children: "Cosine / AST Match" })] }), _jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Latency Parity" }), _jsxs("div", { className: "font-mono font-bold text-foreground text-sm mt-0.5", children: [r.origLat, " \u2192 ", r.repLat, " ms"] }), _jsxs("div", { className: "text-[10px] text-emerald-400 mt-0.5", children: [r.latDelta, " Delta"] })] }), _jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Cost Parity" }), _jsxs("div", { className: "font-mono font-bold text-foreground text-sm mt-0.5", children: ["$", r.origCost.toFixed(4)] }), _jsxs("div", { className: "text-[10px] text-emerald-400 mt-0.5", children: [r.costDelta, " Delta"] })] })] }), _jsxs("div", { className: "text-xs text-muted-foreground flex items-center justify-between border-t border-border/40 pt-3 font-mono", children: [_jsxs("span", { children: ["Verifier Authority Signature: ", _jsx("strong", { className: "text-foreground", children: r.signature })] }), _jsx("button", { className: "text-primary hover:underline font-medium font-sans", children: "View Replay Bitstream \u2192" })] })] }, r.certId))) })] }));
};
