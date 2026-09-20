import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Activity, Server, Cpu, RefreshCw, HardDrive, ShieldCheck, Zap } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
export const ResourceHealthCapacityDashboard = ({ missionId = 'mission-current', }) => {
    const [nodes] = useState([
        {
            id: 'node-llm-01',
            name: 'Gemini 1.5 Pro (Global Gateway)',
            category: 'LLM_BACKEND',
            status: 'HEALTHY',
            cpuUtilization: 34,
            memoryUtilization: 42,
            activeConcurrency: 14,
            maxConcurrency: 50,
            errorRate: 0.02,
            p95LatencyMs: 1450,
            failoverTarget: 'Claude 3.5 Sonnet (Direct)',
        },
        {
            id: 'node-llm-02',
            name: 'Gemini 1.5 Flash (Low-Latency)',
            category: 'LLM_BACKEND',
            status: 'HEALTHY',
            cpuUtilization: 28,
            memoryUtilization: 31,
            activeConcurrency: 45,
            maxConcurrency: 150,
            errorRate: 0.00,
            p95LatencyMs: 420,
            failoverTarget: 'Local LLaVA Quantized',
        },
        {
            id: 'node-ocr-01',
            name: 'Azure Computer Vision Engine',
            category: 'OCR_CLUSTER',
            status: 'HEALTHY',
            cpuUtilization: 52,
            memoryUtilization: 60,
            activeConcurrency: 8,
            maxConcurrency: 20,
            errorRate: 0.01,
            p95LatencyMs: 890,
            failoverTarget: 'Tesseract High-DPI Local',
        },
        {
            id: 'node-gpu-01',
            name: 'NVIDIA RTX 4090 Dedicated Inference',
            category: 'GPU_INFERENCE',
            status: 'HEALTHY',
            cpuUtilization: 78,
            memoryUtilization: 85,
            activeConcurrency: 3,
            maxConcurrency: 4,
            errorRate: 0.00,
            p95LatencyMs: 310,
            failoverTarget: 'Gemini 1.5 Flash (Cloud API)',
        },
        {
            id: 'node-wrk-01',
            name: 'Document Segmentation Agent Pool',
            category: 'WORKER_AGENT',
            status: 'HEALTHY',
            cpuUtilization: 45,
            memoryUtilization: 55,
            activeConcurrency: 12,
            maxConcurrency: 24,
            errorRate: 0.00,
            p95LatencyMs: 210,
            failoverTarget: 'Fallback Sync Worker',
        },
    ]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Activity, { className: "w-5 h-5 text-emerald-400" }), "Resource Health, Capacity & Failover Monitor"] }), _jsxs("p", { className: "text-sm text-slate-400", children: ["Real-time health telemetry, cluster concurrency saturation, and zero-downtime failover targets for mission: ", _jsx("code", { className: "text-emerald-300 font-mono text-xs", children: missionId })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: "success", size: "md", children: "Cluster Status: 100% OPERATIONAL" }), _jsxs("button", { className: "flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700", children: [_jsx(RefreshCw, { className: "w-3.5 h-3.5" }), "Poll Health"] })] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 bg-slate-900 border-slate-800", children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx("span", { className: "text-xs font-medium text-slate-400", children: "Total Registered Nodes" }), _jsx(Server, { className: "w-4 h-4 text-indigo-400" })] }), _jsxs("div", { className: "text-2xl font-bold text-slate-100 font-mono", children: [nodes.length, _jsx("span", { className: "text-xs text-emerald-400 font-normal", children: " (5/5 healthy)" })] }), _jsx("span", { className: "text-[11px] text-slate-400 mt-1 block", children: "0 degraded or draining" })] }), _jsxs(Card, { className: "p-4 bg-slate-900 border-slate-800", children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx("span", { className: "text-xs font-medium text-slate-400", children: "Active Concurrency" }), _jsx(Zap, { className: "w-4 h-4 text-amber-400" })] }), _jsx("div", { className: "text-2xl font-bold text-amber-400 font-mono", children: "82 / 248" }), _jsx("span", { className: "text-[11px] text-slate-400 mt-1 block", children: "33.1% Total Pool Saturation" })] }), _jsxs(Card, { className: "p-4 bg-slate-900 border-slate-800", children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx("span", { className: "text-xs font-medium text-slate-400", children: "Mean P95 Latency" }), _jsx(Activity, { className: "w-4 h-4 text-purple-400" })] }), _jsx("div", { className: "text-2xl font-bold text-purple-400 font-mono", children: "656 ms" }), _jsx("span", { className: "text-[11px] text-slate-400 mt-1 block", children: "Sub-second execution SLA met" })] }), _jsxs(Card, { className: "p-4 bg-slate-900 border-slate-800", children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx("span", { className: "text-xs font-medium text-slate-400", children: "Failover Readiness" }), _jsx(ShieldCheck, { className: "w-4 h-4 text-emerald-400" })] }), _jsx("div", { className: "text-2xl font-bold text-emerald-400 font-mono", children: "100%" }), _jsx("span", { className: "text-[11px] text-slate-400 mt-1 block", children: "All nodes paired with warm backups" })] })] }), _jsxs(Card, { className: "p-5 bg-slate-900 border-slate-800", children: [_jsxs("h3", { className: "text-sm font-semibold text-slate-200 mb-4 flex items-center gap-2", children: [_jsx(Server, { className: "w-4 h-4 text-indigo-400" }), "Active Execution Nodes & Concurrency Breakdown"] }), _jsx("div", { className: "space-y-3", children: nodes.map(node => {
                            const saturation = (node.activeConcurrency / node.maxConcurrency) * 100;
                            return (_jsxs("div", { className: "p-4 rounded-xl bg-slate-950 border border-slate-800 hover:border-slate-700 transition-all", children: [_jsxs("div", { className: "flex items-center justify-between mb-3", children: [_jsxs("div", { className: "flex items-center gap-2.5", children: [_jsx("div", { className: "w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" }), _jsxs("div", { children: [_jsx("span", { className: "text-xs font-bold text-slate-200 block", children: node.name }), _jsxs("span", { className: "text-[10px] text-slate-400 font-mono", children: [node.id, " \u2022 ", node.category] })] })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "success", size: "sm", children: node.status }), _jsxs("span", { className: "text-xs font-mono text-slate-300", children: ["Concurrency: ", _jsx("strong", { className: "text-amber-400", children: node.activeConcurrency }), " / ", node.maxConcurrency] })] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-3 pt-2 border-t border-slate-800/80 text-xs", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex justify-between text-slate-400 mb-1", children: [_jsxs("span", { className: "flex items-center gap-1", children: [_jsx(Cpu, { className: "w-3 h-3" }), " CPU Load"] }), _jsxs("span", { className: "font-mono text-slate-200", children: [node.cpuUtilization, "%"] })] }), _jsx("div", { className: "w-full bg-slate-800 h-1.5 rounded-full overflow-hidden", children: _jsx("div", { className: "bg-indigo-500 h-full rounded-full", style: { width: `${node.cpuUtilization}%` } }) })] }), _jsxs("div", { children: [_jsxs("div", { className: "flex justify-between text-slate-400 mb-1", children: [_jsxs("span", { className: "flex items-center gap-1", children: [_jsx(HardDrive, { className: "w-3 h-3" }), " Memory / VRAM"] }), _jsxs("span", { className: "font-mono text-slate-200", children: [node.memoryUtilization, "%"] })] }), _jsx("div", { className: "w-full bg-slate-800 h-1.5 rounded-full overflow-hidden", children: _jsx("div", { className: "bg-purple-500 h-full rounded-full", style: { width: `${node.memoryUtilization}%` } }) })] }), _jsxs("div", { children: [_jsxs("div", { className: "flex justify-between text-slate-400 mb-1", children: [_jsxs("span", { className: "flex items-center gap-1", children: [_jsx(Zap, { className: "w-3 h-3" }), " Pool Saturation"] }), _jsxs("span", { className: "font-mono text-slate-200", children: [saturation.toFixed(0), "%"] })] }), _jsx("div", { className: "w-full bg-slate-800 h-1.5 rounded-full overflow-hidden", children: _jsx("div", { className: "bg-amber-500 h-full rounded-full", style: { width: `${saturation}%` } }) })] })] }), _jsxs("div", { className: "mt-3 flex items-center justify-between text-[11px] text-slate-400 bg-slate-900/60 p-2 rounded border border-slate-800", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-slate-500 font-mono", children: "Warm Failover Target:" }), _jsx("span", { className: "text-indigo-300 font-semibold", children: node.failoverTarget })] }), _jsxs("div", { className: "flex items-center gap-3 font-mono text-[10px]", children: [_jsxs("span", { children: ["P95 Latency: ", _jsxs("strong", { className: "text-amber-300", children: [node.p95LatencyMs, "ms"] })] }), _jsxs("span", { children: ["Error Rate: ", _jsxs("strong", { className: "text-emerald-400", children: [(node.errorRate * 100).toFixed(1), "%"] })] })] })] })] }, node.id));
                        }) })] })] }));
};
