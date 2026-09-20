import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { useMissionControl } from '../../context/MissionControlContext';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';
export const MissionGraphSection = () => {
    const { state } = useMissionControl();
    const { dagNodes } = state;
    const [selectedNode, setSelectedNode] = useState(dagNodes[0] || null);
    const getNodeStatusBadge = (status) => {
        switch (status) {
            case 'COMPLETED':
                return _jsx(Badge, { variant: "success", size: "sm", children: "COMPLETED" });
            case 'IN_PROGRESS':
                return _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: true, children: "IN PROGRESS" });
            case 'FAILED':
                return _jsx(Badge, { variant: "error", size: "sm", children: "FAILED" });
            case 'SKIPPED':
                return _jsx(Badge, { variant: "default", size: "sm", children: "SKIPPED" });
            case 'PENDING':
            default:
                return _jsx(Badge, { variant: "default", size: "sm", children: "PENDING" });
        }
    };
    return (_jsx("section", { className: "w-full mt-8", children: _jsxs(Card, { variant: "default", className: "border-[#1E293B] bg-[#0F172A]/80 backdrop-blur-md", children: [_jsx(CardHeader, { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: "STAGE 5 \u2022 DAG TOPOLOGY" }), _jsxs("span", { className: "text-xs text-[#94A3B8] font-mono", children: [dagNodes.length, " Execution Units"] })] }), _jsx(CardTitle, { className: "mt-2 text-lg lg:text-xl font-bold text-[#F8FAFC]", children: "Mission Dependency Graph (DAG)" }), _jsx("p", { className: "mt-1 text-xs text-[#94A3B8]", children: "Topologically sorted execution graph linking goals, adaptive preprocessing, Bayesian search, reflection, SLSA proofs, and publication evolution." })] }) }), _jsx(CardContent, { className: "p-6", children: _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-12 gap-6", children: [_jsx("div", { className: "lg:col-span-7 space-y-3", children: dagNodes.map((node, index) => {
                                    const isSelected = selectedNode?.id === node.id;
                                    const isRunning = node.status === 'IN_PROGRESS';
                                    return (_jsx("div", { className: "relative", children: _jsxs("div", { onClick: () => setSelectedNode(node), className: `p-4 rounded-xl border transition-all cursor-pointer flex items-center justify-between ${isSelected
                                                ? 'bg-[#1E293B] border-[#00D2FF] shadow-[0_0_15px_rgba(0,210,255,0.25)]'
                                                : isRunning
                                                    ? 'bg-[#131D35] border-cyan-400/50 shadow-[0_0_15px_rgba(0,210,255,0.2)]'
                                                    : node.status === 'COMPLETED'
                                                        ? 'bg-[#131D35]/70 border-emerald-500/20 hover:bg-[#1E293B]/50'
                                                        : 'bg-[#0A0F1D]/40 border-[#1E293B] opacity-60 hover:opacity-90'}`, children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: `h-7 w-7 rounded-lg flex items-center justify-center text-xs font-mono font-bold ${node.status === 'COMPLETED'
                                                                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                                                                : isRunning
                                                                    ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 animate-pulse'
                                                                    : 'bg-[#1E293B] text-[#64748B]'}`, children: index + 1 }), _jsxs("div", { children: [_jsx("div", { className: "flex items-center gap-2", children: _jsx("span", { className: "text-xs font-semibold text-[#F8FAFC]", children: node.label }) }), _jsxs("span", { className: "text-[11px] font-mono text-[#64748B] block mt-0.5", children: ["Assigned: ", node.assignedAgent, " \u2022 Type: ", node.nodeType] })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [node.runtimeSeconds !== undefined && (_jsxs("span", { className: "text-[11px] font-mono text-[#94A3B8]", children: [node.runtimeSeconds, "s"] })), getNodeStatusBadge(node.status)] })] }) }, node.id));
                                }) }), _jsx("div", { className: "lg:col-span-5", children: selectedNode ? (_jsxs("div", { className: "p-5 rounded-xl bg-[#131D35] border border-[#334155] h-full flex flex-col justify-between", children: [_jsxs("div", { className: "space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-[#1E293B] pb-3", children: [_jsxs("div", { children: [_jsx("span", { className: "text-[10px] text-[#64748B] uppercase font-mono block", children: "Node Inspector" }), _jsx("h4", { className: "text-sm font-bold text-[#F8FAFC] mt-0.5", children: selectedNode.label })] }), getNodeStatusBadge(selectedNode.status)] }), _jsxs("div", { className: "space-y-2 text-xs", children: [_jsxs("div", { children: [_jsx("span", { className: "text-[#94A3B8] font-medium block", children: "Inputs:" }), _jsx("div", { className: "flex flex-wrap gap-1 mt-1 font-mono text-[11px]", children: selectedNode.inputs.map((inp) => (_jsxs("span", { className: "bg-[#0A0F1D] text-slate-300 px-2 py-0.5 rounded border border-[#1E293B]", children: ["\uD83D\uDCE5 ", inp] }, inp))) })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[#94A3B8] font-medium block", children: "Outputs:" }), _jsx("div", { className: "flex flex-wrap gap-1 mt-1 font-mono text-[11px]", children: selectedNode.outputs.map((out) => (_jsxs("span", { className: "bg-[#0A0F1D] text-emerald-300 px-2 py-0.5 rounded border border-emerald-500/30", children: ["\uD83D\uDCE4 ", out] }, out))) })] }), selectedNode.artifactsProduced.length > 0 && (_jsxs("div", { children: [_jsx("span", { className: "text-[#94A3B8] font-medium block", children: "Produced Artifacts:" }), _jsx("div", { className: "flex flex-wrap gap-1 mt-1 font-mono text-[11px]", children: selectedNode.artifactsProduced.map((art) => (_jsxs("span", { className: "bg-cyan-950/40 text-cyan-300 px-2 py-0.5 rounded border border-cyan-500/30", children: ["\uD83D\uDCC4 ", art] }, art))) })] })), selectedNode.sha256Digest && (_jsxs("div", { className: "pt-2 border-t border-[#1E293B]", children: [_jsx("span", { className: "text-[#64748B] text-[10px] uppercase font-mono block", children: "Cryptographic Digest:" }), _jsx("span", { className: "text-[10px] font-mono text-[#A855F7] block truncate mt-0.5", children: selectedNode.sha256Digest })] }))] })] }), _jsxs("div", { className: "mt-4 pt-3 border-t border-[#1E293B] flex items-center justify-between text-xs font-mono text-[#64748B]", children: [_jsxs("span", { children: ["Retries: ", selectedNode.retryCount] }), _jsxs("span", { children: ["Assigned: ", selectedNode.assignedAgent] })] })] })) : (_jsx("div", { className: "p-8 text-center text-xs text-[#64748B] bg-[#131D35]/30 rounded-xl border border-dashed border-[#334155]", children: "Select a DAG node to inspect execution details" })) })] }) })] }) }));
};
