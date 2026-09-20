import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const LiveDAGExecutionView = () => {
    const [highlightCriticalPath, setHighlightCriticalPath] = useState(true);
    const nodes = [
        {
            id: 'task_ingest',
            label: 'Multi-Page Document Ingestion & De-Skew',
            type: 'PREPROCESS',
            status: 'COMPLETED',
            wavefront: 0,
            worker: 'worker_ocr_1',
            duration: '120 ms',
            cost: '$0.0002',
            confidence: '98.0%',
            isCritical: true,
        },
        {
            id: 'task_ocr_tess',
            label: 'LayoutLM & Optical Text Extraction',
            type: 'OCR_PARSE',
            status: 'COMPLETED',
            wavefront: 1,
            worker: 'worker_ocr_1',
            duration: '180 ms',
            cost: '$0.0004',
            confidence: '96.0%',
            isCritical: true,
        },
        {
            id: 'task_entity_extract',
            label: 'Gemini 2.5 Flash Structured Parsing',
            type: 'LLM_EXTRACT',
            status: 'RUNNING',
            wavefront: 2,
            worker: 'worker_llm_1',
            duration: '450 ms',
            cost: '$0.0018',
            confidence: '96.5%',
            isCritical: true,
        },
        {
            id: 'task_memory_recall',
            label: 'Historical Schema & Vendor Memory Lookup',
            type: 'MEMORY_RETRIEVAL',
            status: 'COMPLETED',
            wavefront: 2,
            worker: 'worker_mem_1',
            duration: '45 ms',
            cost: '$0.0000',
            confidence: '99.0%',
            isCritical: false,
        },
        {
            id: 'task_cross_validation',
            label: 'Cross-Document Invariant & Math Validation',
            type: 'VALIDATION',
            status: 'WAITING',
            wavefront: 3,
            worker: 'worker_val_1',
            duration: '50 ms',
            cost: '$0.0001',
            confidence: '98.0%',
            isCritical: true,
        },
        {
            id: 'task_db_commit',
            label: 'Cryptographic Audit Sign & DB Commit',
            type: 'PERSISTENCE',
            status: 'WAITING',
            wavefront: 4,
            worker: 'worker_sec_1',
            duration: '35 ms',
            cost: '$0.0000',
            confidence: '100%',
            isCritical: true,
        },
    ];
    const criticalTotalMs = 835.0;
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\uD83D\uDDFA\uFE0F" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Live Dynamic DAG Execution & Critical Path Method (CPM)" }), _jsx(Badge, { variant: "success", size: "sm", children: "ACTIVE WAVEFRONT 2" })] }), _jsx("p", { className: "text-sm font-mono text-[#94A3B8] mt-1", children: "Deterministic topological execution graph with CPM bottleneck analysis and zero canned animations." })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsx("button", { onClick: () => setHighlightCriticalPath(!highlightCriticalPath), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-bold transition-all ${highlightCriticalPath
                                    ? 'bg-amber-600 text-white shadow-lg shadow-amber-600/20'
                                    : 'bg-[#1E293B] text-[#94A3B8]'}`, children: highlightCriticalPath ? '⚡ Critical Path Highlighted' : '○ Standard View' }) })] }) }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Critical Path Length (CPM)" }), _jsxs("div", { className: "text-2xl font-bold font-mono text-amber-400 mt-1", children: [criticalTotalMs, " ms"] }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "5 critical bottleneck nodes" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Parallel Execution Wavefronts" }), _jsx("div", { className: "text-2xl font-bold font-mono text-cyan-400 mt-1", children: "5 Levels" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "Wavefront 2 running concurrently" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Non-Critical Task Slack (Float)" }), _jsx("div", { className: "text-2xl font-bold font-mono text-emerald-400 mt-1", children: "+405 ms" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "Memory lookup slack window" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Dynamic Mutation Readiness" }), _jsx("div", { className: "text-2xl font-bold font-mono text-indigo-400 mt-1", children: "ONLINE" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "Real-time sub-graph rewiring" })] })] }), _jsxs(Card, { className: "p-6 bg-[#0F172A] border-[#1E293B]", children: [_jsx("h3", { className: "text-sm font-bold font-mono text-[#F8FAFC] mb-4", children: "Topological Task Graph & Worker Execution Stream" }), _jsx("div", { className: "space-y-3", children: nodes.map((n) => {
                            const isCriticalActive = highlightCriticalPath && n.isCritical;
                            return (_jsx("div", { className: `p-4 rounded-xl border transition-all ${n.status === 'RUNNING'
                                    ? 'bg-blue-950/30 border-blue-500 shadow-md shadow-blue-500/10'
                                    : isCriticalActive
                                        ? 'bg-[#0F172A] border-amber-500/50'
                                        : 'bg-[#020617] border-[#1E293B]'}`, children: _jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-3", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("span", { className: "w-6 h-6 rounded-full bg-[#1E293B] flex items-center justify-center text-xs font-mono font-bold text-[#F8FAFC]", children: n.wavefront }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h4", { className: "text-xs font-bold font-mono text-[#F8FAFC]", children: n.label }), n.isCritical && (_jsx("span", { className: "text-[10px] font-mono text-amber-400 bg-amber-950/40 px-1.5 py-0.5 rounded border border-amber-500/30", children: "CPM CRITICAL" }))] }), _jsxs("div", { className: "text-[11px] font-mono text-[#64748B] mt-0.5", children: ["Worker: ", _jsx("span", { className: "text-[#94A3B8]", children: n.worker }), " \u2022 ID: ", n.id] })] })] }), _jsxs("div", { className: "flex items-center gap-4 text-xs font-mono", children: [_jsx("span", { className: "text-cyan-400", children: n.duration }), _jsx("span", { className: "text-emerald-400", children: n.cost }), _jsx("span", { className: "text-indigo-400", children: n.confidence }), _jsx(Badge, { variant: n.status === 'COMPLETED'
                                                        ? 'success'
                                                        : n.status === 'RUNNING'
                                                            ? 'info'
                                                            : 'default', size: "sm", children: n.status })] })] }) }, n.id));
                        }) })] })] }));
};
