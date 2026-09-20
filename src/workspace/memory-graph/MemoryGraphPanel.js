import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useWorkspace } from '../context/WorkspaceContext';
import { CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
export const MemoryGraphPanel = () => {
    const { memoryNodes, selectedMemoryNodeId, selectMemoryNode } = useWorkspace();
    const activeNode = memoryNodes.find((n) => n.id === selectedMemoryNodeId) || memoryNodes[0];
    const getNodeColor = (type) => {
        switch (type) {
            case 'DOCUMENT':
                return 'border-blue-500/50 text-blue-300 bg-blue-950/30';
            case 'FAILURE_MODE':
                return 'border-red-500/50 text-red-300 bg-red-950/30';
            case 'REFLECTION':
                return 'border-amber-500/50 text-amber-300 bg-amber-950/30';
            case 'LESSON_LEARNED':
                return 'border-cyan-500/50 text-cyan-300 bg-cyan-950/30';
            case 'INVARIANT_APPLIED':
                return 'border-emerald-500/50 text-emerald-300 bg-emerald-950/30';
            default:
                return 'border-slate-500/50 text-slate-300 bg-slate-950/30';
        }
    };
    return (_jsxs("div", { className: "w-full flex flex-col h-[700px] rounded-2xl bg-[#0F172A]/90 border border-[#1E293B] shadow-2xl overflow-hidden", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between py-4 px-6 border-b border-[#1E293B] bg-[#131D35]/50", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: "CAUSAL REASONING GRAPH" }), _jsxs("span", { className: "text-xs text-[#94A3B8] font-mono", children: [memoryNodes.length, " Invariant Nodes"] })] }), _jsx(CardTitle, { className: "mt-1 text-base font-bold text-[#F8FAFC]", children: "Causal Memory & Experience Graph" })] }), _jsx("div", { className: "text-xs font-mono text-[#10B981] bg-[#0A0F1D] px-3 py-1.5 rounded-lg border border-emerald-500/30", children: "Decay Half-Life: Active (R \u2265 0.90)" })] }), _jsxs(CardContent, { className: "flex-1 overflow-y-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6", children: [_jsxs("div", { className: "lg:col-span-7 space-y-4", children: [_jsx("span", { className: "text-[11px] font-bold font-mono text-[#64748B] uppercase block", children: "Causal Progression Chain:" }), memoryNodes.map((node, i) => {
                                const isSelected = selectedMemoryNodeId === node.id;
                                const isLast = i === memoryNodes.length - 1;
                                return (_jsxs("div", { className: "relative", children: [_jsxs("div", { onClick: () => selectMemoryNode(node.id), className: `p-4 rounded-xl border transition-all cursor-pointer ${isSelected
                                                ? 'bg-[#1E293B] border-cyan-400 shadow-[0_0_20px_rgba(0,210,255,0.25)] ring-1 ring-cyan-400'
                                                : 'bg-[#131D35] hover:border-[#334155]'}`, children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: `text-[10px] font-mono uppercase px-2 py-0.5 rounded border ${getNodeColor(node.nodeType)}`, children: node.nodeType }), _jsx("h4", { className: "text-xs font-bold text-[#F8FAFC]", children: node.label })] }), _jsxs("span", { className: "text-[11px] font-mono text-[#00D2FF]", children: ["R=", (node.retentionScore * 100).toFixed(0), "%"] })] }), _jsx("p", { className: "mt-1.5 text-xs text-[#94A3B8] leading-relaxed", children: node.description }), node.metricImpact && (_jsxs("div", { className: "mt-2 text-[11px] font-mono text-[#10B981]", children: ["\u2605 Impact: ", node.metricImpact] }))] }), !isLast && (_jsx("div", { className: "flex justify-center my-1 text-[#00D2FF] font-mono text-xs animate-pulse", children: "\u2193" }))] }, node.id));
                            })] }), _jsx("div", { className: "lg:col-span-5", children: activeNode ? (_jsxs("div", { className: "p-6 rounded-2xl bg-[#131D35] border border-[#334155] space-y-4 h-full flex flex-col justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "border-b border-[#1E293B] pb-3", children: [_jsx("span", { className: "text-[10px] text-[#64748B] uppercase font-mono block", children: "Causal Memory Inspector" }), _jsx("h3", { className: "text-sm font-bold text-[#F8FAFC] mt-0.5", children: activeNode.label })] }), _jsxs("div", { className: "mt-4 space-y-3 text-xs", children: [_jsxs("div", { children: [_jsx("span", { className: "text-[#64748B] uppercase font-mono text-[10px] block", children: "Node Type:" }), _jsx("span", { className: "text-[#38BDF8] font-mono font-medium block mt-0.5", children: activeNode.nodeType })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[#64748B] uppercase font-mono text-[10px] block", children: "Causal Description:" }), _jsx("p", { className: "text-[#F8FAFC] leading-relaxed mt-0.5", children: activeNode.description })] }), activeNode.metricImpact && (_jsxs("div", { children: [_jsx("span", { className: "text-[#64748B] uppercase font-mono text-[10px] block", children: "Observed Metric Shift:" }), _jsx("span", { className: "text-[#10B981] font-mono font-bold block mt-0.5", children: activeNode.metricImpact })] }))] })] }), _jsxs("div", { className: "pt-4 border-t border-[#1E293B] flex items-center justify-between text-xs font-mono text-[#64748B]", children: [_jsxs("span", { children: ["Retention Weight: ", (activeNode.retentionScore * 100).toFixed(0), "%"] }), _jsx("span", { className: "text-[#10B981]", children: "\u2713 Verified Link" })] })] })) : (_jsx("div", { className: "p-8 text-center text-xs text-[#64748B]", children: "Select a node to inspect" })) })] })] }));
};
