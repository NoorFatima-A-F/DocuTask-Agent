import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const ModelRoutingExplorerView = () => {
    const models = [
        {
            id: 'gemini-1.5-flash',
            name: 'Gemini 1.5 Flash',
            expectedAcc: '95.0%',
            expectedCost: '$0.0012',
            expectedLat: '650ms',
            utilityScore: 0.948,
            isWinner: true,
            role: 'Optimal for Current High-Throughput Task',
        },
        {
            id: 'gemini-1.5-pro',
            name: 'Gemini 1.5 Pro',
            expectedAcc: '98.5%',
            expectedCost: '$0.0175',
            expectedLat: '2200ms',
            utilityScore: 0.865,
            isWinner: false,
            role: 'Heavyweight Multimodal & Reasoning',
        },
        {
            id: 'gemini-flash-lite',
            name: 'Gemini Flash Lite',
            expectedAcc: '91.0%',
            expectedCost: '$0.0004',
            expectedLat: '300ms',
            utilityScore: 0.882,
            isWinner: false,
            role: 'Low Cost Pre-Classification',
        },
        {
            id: 'local-ocr-specialist',
            name: 'Local LayoutLM / Tesseract',
            expectedAcc: '88.0%',
            expectedCost: '$0.0000',
            expectedLat: '180ms',
            utilityScore: 0.795,
            isWinner: false,
            role: 'Zero API Cost Local OCR',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\uD83D\uDD00" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Scientific Model Router & Utility Evaluator" }), _jsx(Badge, { variant: "success", size: "sm", children: "UTILITY MAXIMIZING ROUTE" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] mt-1", children: "Model selection is formulated as multi-attribute expected utility maximization under document complexity constraints." })] }), _jsxs("div", { className: "text-right", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Selected Optimal Model" }), _jsx("div", { className: "text-lg font-mono font-bold text-emerald-400", children: "Gemini 1.5 Flash (U=0.948)" })] })] }) }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: models.map((m) => (_jsxs(Card, { className: `p-5 bg-[#0F172A] border transition-all ${m.isWinner
                        ? 'border-emerald-500/70 shadow-[0_0_20px_rgba(16,185,129,0.15)] ring-1 ring-emerald-500/50'
                        : 'border-[#1E293B]'}`, children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono font-bold text-[#F8FAFC]", children: m.name }), m.isWinner && (_jsx(Badge, { variant: "success", size: "sm", children: "WINNER" }))] }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-0.5", children: m.role })] }), _jsxs("div", { className: "text-right", children: [_jsx("div", { className: "text-[10px] text-[#94A3B8]", children: "Expected Utility" }), _jsx("div", { className: "text-base font-mono font-extrabold text-cyan-400", children: m.utilityScore.toFixed(3) })] })] }), _jsxs("div", { className: "grid grid-cols-3 gap-2 mt-4 pt-3 border-t border-[#1E293B] text-center text-xs font-mono", children: [_jsxs("div", { className: "bg-[#131D35]/50 p-2 rounded-lg", children: [_jsx("div", { className: "text-[10px] text-[#64748B]", children: "Exp. Accuracy" }), _jsx("div", { className: "font-bold text-emerald-400", children: m.expectedAcc })] }), _jsxs("div", { className: "bg-[#131D35]/50 p-2 rounded-lg", children: [_jsx("div", { className: "text-[10px] text-[#64748B]", children: "Exp. Cost" }), _jsx("div", { className: "font-bold text-[#F8FAFC]", children: m.expectedCost })] }), _jsxs("div", { className: "bg-[#131D35]/50 p-2 rounded-lg", children: [_jsx("div", { className: "text-[10px] text-[#64748B]", children: "Exp. Latency" }), _jsx("div", { className: "font-bold text-cyan-400", children: m.expectedLat })] })] })] }, m.id))) })] }));
};
