import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const FailureChaosRecoveryLabView = () => {
    const [injectedHistory, setInjectedHistory] = useState([
        {
            faultId: 'fault_ocr_crash',
            target: 'OCR_INGEST',
            type: 'PROCESS_CRASH',
            actionTaken: 'ALTERNATE_OCR_FALLBACK',
            replannedNodes: ['task_ocr_tesseract_fallback', 'task_dewarp_repair'],
            recoveryMs: 38.2,
            status: 'AUTONOMOUSLY_RECOVERED',
            timestamp: '5 mins ago',
        },
        {
            faultId: 'fault_gemini_429',
            target: 'LLM_EXTRACT',
            type: 'HTTP_429_RATE_LIMIT',
            actionTaken: 'EXPONENTIAL_BACKOFF_RETRY',
            replannedNodes: ['task_llm_backoff_jitter', 'task_flash_lite_route'],
            recoveryMs: 42.5,
            status: 'AUTONOMOUSLY_RECOVERED',
            timestamp: '12 mins ago',
        },
    ]);
    const handleInjectFault = (faultType) => {
        const newEvent = {
            faultId: `fault_${Date.now()}`,
            target: 'LLM_EXTRACT',
            type: faultType,
            actionTaken: 'DYNAMIC_REPLAN_FALLBACK',
            replannedNodes: ['task_speculative_fallback', 'task_schema_patch'],
            recoveryMs: 35.0,
            status: 'AUTONOMOUSLY_RECOVERED',
            timestamp: 'Just now',
        };
        setInjectedHistory([newEvent, ...injectedHistory]);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\u26A1" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Failure Recovery & Chaos Fault Injection Lab" }), _jsx(Badge, { variant: "success", size: "sm", children: "SELF-HEALING ACTIVE" })] }), _jsx("p", { className: "text-sm font-mono text-[#94A3B8] mt-1", children: "Test autonomous resilience by injecting simulated worker crashes, API rate-limits, and schema drift." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx("button", { onClick: () => handleInjectFault('PROCESS_CRASH'), className: "px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-rose-600/20 border border-rose-500 text-rose-300 hover:bg-rose-600 hover:text-white transition-all", children: "\uD83D\uDCA5 Inject OCR Crash" }), _jsx("button", { onClick: () => handleInjectFault('HTTP_429_RATE_LIMIT'), className: "px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-amber-600/20 border border-amber-500 text-amber-300 hover:bg-amber-600 hover:text-white transition-all", children: "\u26A0\uFE0F Inject HTTP 429 Quota" })] })] }) }), _jsxs(Card, { className: "p-6 bg-[#0F172A] border-[#1E293B]", children: [_jsx("h3", { className: "text-sm font-bold font-mono text-[#F8FAFC] mb-4", children: "Autonomous Replanning & Fault Mitigation Stream" }), _jsx("div", { className: "space-y-3", children: injectedHistory.map((item, idx) => (_jsx("div", { className: "p-4 rounded-xl bg-[#020617] border border-[#1E293B]", children: _jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-2", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono text-rose-400 font-bold", children: item.type }), _jsxs("span", { className: "text-xs font-mono text-[#94A3B8]", children: ["on ", item.target] })] }), _jsxs("div", { className: "text-xs font-mono text-[#F8FAFC] mt-1", children: ["Mitigation: ", _jsx("span", { className: "text-cyan-400 font-bold", children: item.actionTaken })] }), _jsxs("div", { className: "text-[11px] font-mono text-[#64748B] mt-0.5", children: ["Synthesized Subgraph: ", item.replannedNodes.join(' → '), " \u2022 Recovery Time: ", item.recoveryMs, " ms"] })] }), _jsx(Badge, { variant: "success", size: "sm", children: item.status })] }) }, idx))) })] })] }));
};
