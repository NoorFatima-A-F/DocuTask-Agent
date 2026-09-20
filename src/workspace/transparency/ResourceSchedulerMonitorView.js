import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const ResourceSchedulerMonitorView = () => {
    const workerPools = [
        {
            poolName: 'OCR Processing Pool',
            type: 'OCR_POOL',
            workers: '2 active instances',
            capacity: '4 concurrent slots',
            activeJobs: 1,
            utilization: '25.0%',
            latency: '180 ms',
            status: 'HEALTHY',
        },
        {
            poolName: 'LLM Reasoning & Inference Pool',
            type: 'LLM_POOL',
            workers: '2 active instances',
            capacity: '8 concurrent slots',
            activeJobs: 3,
            utilization: '37.5%',
            latency: '450 ms',
            status: 'HEALTHY',
        },
        {
            poolName: 'Schema & Invariant Validation Pool',
            type: 'VALIDATION_POOL',
            workers: '1 active instance',
            capacity: '8 concurrent slots',
            activeJobs: 0,
            utilization: '0.0%',
            latency: '45 ms',
            status: 'IDLE',
        },
        {
            poolName: 'Memory & Knowledge Retrieval Pool',
            type: 'MEMORY_POOL',
            workers: '1 active instance',
            capacity: '4 concurrent slots',
            activeJobs: 0,
            utilization: '0.0%',
            latency: '60 ms',
            status: 'IDLE',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsx("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\u2699\uFE0F" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Resource Scheduler & Priority Queue Orchestrator" }), _jsx(Badge, { variant: "success", size: "sm", children: "CLUSTER OPTIMAL" })] }), _jsx("p", { className: "text-sm font-mono text-[#94A3B8] mt-1", children: "Heterogeneous worker pools, priority fair queuing (CRITICAL > HIGH > NORMAL), and backpressure management." })] }) }) }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Total Cluster Workers" }), _jsx("div", { className: "text-2xl font-bold font-mono text-cyan-400 mt-1", children: "6 Instances" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "4 dedicated pools" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Active Task Queue Depth" }), _jsx("div", { className: "text-2xl font-bold font-mono text-emerald-400 mt-1", children: "2 queued" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "Max capacity 1,000 tasks" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Backpressure Status" }), _jsx("div", { className: "text-2xl font-bold font-mono text-emerald-400 mt-1", children: "NOMINAL (0%)" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "Zero dropped requests" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Average Cluster Utilization" }), _jsx("div", { className: "text-2xl font-bold font-mono text-indigo-400 mt-1", children: "31.2%" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "Balanced load across TPUs" })] })] }), _jsxs(Card, { className: "p-6 bg-[#0F172A] border-[#1E293B]", children: [_jsx("h3", { className: "text-sm font-bold font-mono text-[#F8FAFC] mb-4", children: "Dedicated Subsystem Worker Pools" }), _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left font-mono text-xs", children: [_jsx("thead", { children: _jsxs("tr", { className: "border-b border-[#1E293B] text-[#94A3B8]", children: [_jsx("th", { className: "pb-3", children: "Worker Pool" }), _jsx("th", { className: "pb-3", children: "Pool Type" }), _jsx("th", { className: "pb-3", children: "Active Instances" }), _jsx("th", { className: "pb-3", children: "Concurrency Capacity" }), _jsx("th", { className: "pb-3", children: "Utilization" }), _jsx("th", { className: "pb-3", children: "Average Latency" }), _jsx("th", { className: "pb-3", children: "Health Status" })] }) }), _jsx("tbody", { className: "divide-y divide-[#1E293B]", children: workerPools.map((p, idx) => (_jsxs("tr", { className: "hover:bg-[#1E293B]/40 transition-colors", children: [_jsx("td", { className: "py-3 font-bold text-[#F8FAFC]", children: p.poolName }), _jsx("td", { className: "py-3 text-cyan-400", children: p.type }), _jsx("td", { className: "py-3 text-[#E2E8F0]", children: p.workers }), _jsx("td", { className: "py-3 text-[#94A3B8]", children: p.capacity }), _jsx("td", { className: "py-3 text-indigo-400 font-bold", children: p.utilization }), _jsx("td", { className: "py-3 text-emerald-400", children: p.latency }), _jsx("td", { className: "py-3", children: _jsx(Badge, { variant: p.status === 'HEALTHY' ? 'success' : 'default', size: "sm", children: p.status }) })] }, idx))) })] }) })] })] }));
};
