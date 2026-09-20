import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Server, Activity } from 'lucide-react';
export const ResourceIntelligenceDashboard = () => {
    const resources = [
        {
            id: 'res-pool-worker-01',
            name: 'General Async Worker Pool',
            type: 'WORKER_POOL',
            capacity: 16,
            allocated: 6,
            available: 10,
            utilization: 37.5,
            status: 'HEALTHY',
        },
        {
            id: 'res-llm-gemini-flash',
            name: 'Gemini 1.5 Flash Quota (RPM)',
            type: 'LLM_QUOTA',
            capacity: 1000,
            allocated: 150,
            available: 850,
            utilization: 15.0,
            status: 'HEALTHY',
        },
        {
            id: 'res-ocr-tesseract',
            name: 'Local Tesseract OCR Cluster',
            type: 'OCR_ENGINE',
            capacity: 8,
            allocated: 3,
            available: 5,
            utilization: 37.5,
            status: 'HEALTHY',
        },
        {
            id: 'res-gpu-v100',
            name: 'NVIDIA V100 Acceleration Node',
            type: 'GPU_NODE',
            capacity: 4,
            allocated: 1,
            available: 3,
            utilization: 25.0,
            status: 'HEALTHY',
        },
    ];
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 rounded-xl text-cyan-400", children: _jsx(Server, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Autonomous Resource Intelligence Dashboard", _jsx(Badge, { variant: "intelligence", size: "sm", children: "Phase 13.6 ARIA-EOP" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] font-mono", children: "Live capacity inventory, worker thread pools, LLM quotas, and GPU node utilization tracking" })] })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx(Badge, { variant: "success", size: "md", children: "System Capacity: 62.5% Available" }) })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6 font-mono", children: resources.map((res) => (_jsxs(Card, { className: "p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] space-y-4", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: res.type }), _jsx("h3", { className: "text-sm font-bold text-white mt-1.5", children: res.name }), _jsxs("span", { className: "text-[11px] text-[#64748B]", children: ["ID: ", res.id] })] }), _jsx(Badge, { variant: "success", size: "sm", children: res.status })] }), _jsxs("div", { className: "space-y-1.5 text-xs", children: [_jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsxs("span", { children: ["Allocated: ", res.allocated, " / ", res.capacity, " units"] }), _jsxs("span", { className: "text-cyan-400 font-bold", children: [res.utilization, "%"] })] }), _jsx("div", { className: "w-full bg-[#1E293B] rounded-full h-2 overflow-hidden", children: _jsx("div", { className: "bg-gradient-to-r from-cyan-500 to-indigo-500 h-2 rounded-full", style: { width: `${res.utilization}%` } }) })] }), _jsxs("div", { className: "pt-2 border-t border-[#1E293B] flex items-center justify-between text-xs text-[#94A3B8]", children: [_jsxs("span", { children: ["Available Capacity: ", _jsxs("strong", { className: "text-emerald-400", children: [res.available, " units"] })] }), _jsxs("span", { className: "flex items-center gap-1 text-cyan-300", children: [_jsx(Activity, { className: "w-3.5 h-3.5" }), " Live Monitored"] })] })] }, res.id))) })] }));
};
