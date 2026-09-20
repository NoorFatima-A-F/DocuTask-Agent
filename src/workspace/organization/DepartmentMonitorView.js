import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const DepartmentMonitorView = () => {
    const [selectedDeptId, setSelectedDeptId] = useState('dept_extraction');
    const deptData = {
        dept_ocr: {
            name: 'Optical Perception & Ingestion',
            head: 'Lead Vision Agent',
            workers: [
                { id: 'w_ocr_1', type: 'LayoutLM GPU Worker', status: 'BUSY', load: '78%', latency: '180 ms', tasks: 420 },
                { id: 'w_ocr_2', type: 'Tesseract Fallback Worker', status: 'IDLE', load: '12%', latency: '140 ms', tasks: 210 },
            ],
            queue: [
                { id: 'q_01', doc: 'DOC-INV-2026-EU', priority: 'HIGH', pages: 4, waitingMs: '120 ms' },
                { id: 'q_02', doc: 'DOC-RECEIPT-8812', priority: 'NORMAL', pages: 1, waitingMs: '45 ms' },
            ],
            kpis: { throughput: '180 items/min', accuracy: '98.5%', errorRate: '0.8%', sla: '99.1%' },
        },
        dept_extraction: {
            name: 'Structured Intelligence & Extraction',
            head: 'Lead Extraction Specialist',
            workers: [
                { id: 'w_llm_1', type: 'Gemini 2.5 Flash Primary', status: 'BUSY', load: '85%', latency: '420 ms', tasks: 1250 },
                { id: 'w_llm_2', type: 'Gemini Flash Lite Secondary', status: 'BUSY', load: '65%', latency: '210 ms', tasks: 890 },
            ],
            queue: [
                { id: 'q_10', doc: 'DOC-HEALTH-REC-01', priority: 'CRITICAL', pages: 6, waitingMs: '210 ms' },
                { id: 'q_11', doc: 'DOC-TAX-1099-2026', priority: 'HIGH', pages: 2, waitingMs: '80 ms' },
                { id: 'q_12', doc: 'DOC-INV-VENDOR-44', priority: 'NORMAL', pages: 3, waitingMs: '40 ms' },
            ],
            kpis: { throughput: '240 items/min', accuracy: '99.1%', errorRate: '0.5%', sla: '98.9%' },
        },
        dept_validation: {
            name: 'Mathematical & Invariant Validation',
            head: 'Lead Verification Auditor',
            workers: [
                { id: 'w_val_1', type: 'Z3 Theorem Prover Engine', status: 'IDLE', load: '24%', latency: '45 ms', tasks: 1600 },
                { id: 'w_val_2', type: 'Zero-Fabrication Sentinel', status: 'BUSY', load: '32%', latency: '50 ms', tasks: 1580 },
            ],
            queue: [
                { id: 'q_20', doc: 'DOC-INV-TOTALS-CHECK', priority: 'HIGH', pages: 2, waitingMs: '30 ms' },
            ],
            kpis: { throughput: '320 items/min', accuracy: '100.0%', errorRate: '0.0%', sla: '100.0%' },
        },
    };
    const current = deptData[selectedDeptId] || deptData['dept_extraction'];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-2xl", children: "\u2699\uFE0F" }), _jsx("h2", { className: "text-xl font-bold text-[#F8FAFC]", children: "Department Operations & Workload Monitor" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Live Telemetry" })] }), _jsx("p", { className: "text-sm text-[#94A3B8] mt-1", children: "Real-time worker pool allocation, task queue pressure, throughput velocity, and SLA telemetry per department." })] }), _jsx("div", { className: "flex gap-2", children: Object.keys(deptData).map((dId) => (_jsx("button", { onClick: () => setSelectedDeptId(dId), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${selectedDeptId === dId ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'}`, children: deptData[dId].name.split(' ')[0] }, dId))) })] }), _jsx(Card, { className: "p-5 bg-[#0F172A] border-[#1E293B]", children: _jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-lg font-bold text-[#F8FAFC]", children: current.name }), _jsx(Badge, { variant: "success", size: "sm", children: "OPERATIONAL" })] }), _jsxs("div", { className: "text-xs text-[#94A3B8] font-mono mt-1", children: ["Lead Officer: ", _jsx("span", { className: "text-[#38BDF8]", children: current.head })] })] }), _jsxs("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-4 text-xs font-mono", children: [_jsxs("div", { children: [_jsx("span", { className: "text-[#64748B] block", children: "THROUGHPUT" }), _jsx("span", { className: "text-[#10B981] font-bold", children: current.kpis.throughput })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[#64748B] block", children: "ACCURACY" }), _jsx("span", { className: "text-[#00D2FF] font-bold", children: current.kpis.accuracy })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[#64748B] block", children: "ERROR RATE" }), _jsx("span", { className: "text-[#F59E0B] font-bold", children: current.kpis.errorRate })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[#64748B] block", children: "SLA COMPLIANCE" }), _jsx("span", { className: "text-[#A855F7] font-bold", children: current.kpis.sla })] })] })] }) }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6", children: [_jsxs(Card, { className: "p-5 bg-[#0F172A] border-[#1E293B] space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-sm font-bold font-mono uppercase text-[#94A3B8]", children: "Dedicated Worker Nodes" }), _jsxs(Badge, { variant: "intelligence", size: "sm", children: [current.workers.length, " Active"] })] }), _jsx("div", { className: "space-y-3", children: current.workers.map((w) => (_jsxs("div", { className: "p-3 rounded-xl bg-[#020617] border border-[#1E293B] flex items-center justify-between", children: [_jsxs("div", { children: [_jsx("div", { className: "text-xs font-bold text-[#F8FAFC] font-mono", children: w.id }), _jsx("div", { className: "text-[11px] text-[#94A3B8]", children: w.type }), _jsxs("div", { className: "text-[10px] text-[#64748B] font-mono mt-1", children: ["Latency: ", w.latency, " | Total: ", w.tasks, " ops"] })] }), _jsxs("div", { className: "text-right", children: [_jsx(Badge, { variant: w.status === 'BUSY' ? 'warning' : 'success', size: "sm", children: w.status }), _jsxs("div", { className: "text-xs font-bold font-mono text-[#00D2FF] mt-1", children: [w.load, " Load"] })] })] }, w.id))) })] }), _jsxs(Card, { className: "p-5 bg-[#0F172A] border-[#1E293B] space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-sm font-bold font-mono uppercase text-[#94A3B8]", children: "Incoming Task Queue" }), _jsxs(Badge, { variant: "warning", size: "sm", children: [current.queue.length, " Queued"] })] }), _jsx("div", { className: "space-y-3", children: current.queue.map((q) => (_jsxs("div", { className: "p-3 rounded-xl bg-[#020617] border border-[#1E293B] flex items-center justify-between", children: [_jsxs("div", { children: [_jsx("div", { className: "text-xs font-bold text-[#F8FAFC] font-mono", children: q.doc }), _jsxs("div", { className: "text-[11px] text-[#94A3B8]", children: [q.pages, " Pages | Task ID: ", q.id] })] }), _jsxs("div", { className: "text-right", children: [_jsx(Badge, { variant: q.priority === 'CRITICAL' ? 'error' : 'default', size: "sm", children: q.priority }), _jsxs("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: ["Wait: ", q.waitingMs] })] })] }, q.id))) })] })] })] }));
};
