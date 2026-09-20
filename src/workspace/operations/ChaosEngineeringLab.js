import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Flame, CheckCircle2, RefreshCw, Play, Layers, StopCircle } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
export const ChaosEngineeringLab = ({ missionId = 'cluster-primary-master', }) => {
    const [experiments] = useState([
        {
            experimentId: 'exp-wrk-01',
            name: 'Worker Crash & Auto-Heal Resilience',
            target: 'WORKERS',
            fault: 'WORKER_CRASH',
            status: 'COMPLETED',
            mttrMs: 185.0,
            resilienceScore: 98.2,
            invariantsPreserved: true,
            timestamp: '10:14 UTC',
        },
        {
            experimentId: 'exp-net-02',
            name: 'Simulated LLM Rate Limit Injection',
            target: 'API',
            fault: 'LLM_RATE_LIMIT',
            status: 'COMPLETED',
            mttrMs: 82.0,
            resilienceScore: 99.4,
            invariantsPreserved: true,
            timestamp: '09:42 UTC',
        },
        {
            experimentId: 'exp-gpu-03',
            name: 'OCR Latency Spike Injection',
            target: 'WORKERS',
            fault: 'OCR_FAILURE',
            status: 'COMPLETED',
            mttrMs: 210.0,
            resilienceScore: 97.5,
            invariantsPreserved: true,
            timestamp: '08:30 UTC',
        },
    ]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Flame, { className: "w-5 h-5 text-rose-400" }), "Controlled Chaos Engineering & Resilience Lab"] }), _jsxs("p", { className: "text-sm text-slate-400", children: ["Automated fault injection, recovery evaluation, zero data-loss invariant validation, and resilience benchmarking for: ", _jsx("code", { className: "text-rose-300 font-mono text-xs", children: missionId })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: "success", size: "md", children: "Invariant Preservation: 100%" }), _jsxs("button", { className: "flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700", children: [_jsx(RefreshCw, { className: "w-3.5 h-3.5" }), "Scan Resilience"] })] })] }), _jsxs(Card, { className: "p-5 bg-slate-900 border-slate-800 space-y-4 font-mono", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-slate-800 pb-3", children: [_jsxs("h3", { className: "text-sm font-semibold text-slate-200 flex items-center gap-2", children: [_jsx(Play, { className: "w-4 h-4 text-emerald-400" }), "Fault Injection Control Panel"] }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Blast Radius: ISOLATED_CONTAINER" })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-3 gap-3", children: [_jsxs("button", { className: "p-3.5 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-xl text-left space-y-1 transition-all", children: [_jsxs("span", { className: "text-xs font-bold text-slate-200 block flex items-center gap-1.5", children: [_jsx(Flame, { className: "w-3.5 h-3.5 text-rose-400" }), " Inject Worker Crash"] }), _jsx("span", { className: "text-[11px] text-slate-400 block", children: "Simulates worker segfault" })] }), _jsxs("button", { className: "p-3.5 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-xl text-left space-y-1 transition-all", children: [_jsxs("span", { className: "text-xs font-bold text-slate-200 block flex items-center gap-1.5", children: [_jsx(Flame, { className: "w-3.5 h-3.5 text-amber-400" }), " Inject 429 Rate Limit"] }), _jsx("span", { className: "text-[11px] text-slate-400 block", children: "Tests fallback model engagement" })] }), _jsxs("button", { className: "p-3.5 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-xl text-left space-y-1 transition-all", children: [_jsxs("span", { className: "text-xs font-bold text-slate-200 block flex items-center gap-1.5", children: [_jsx(StopCircle, { className: "w-3.5 h-3.5 text-indigo-400" }), " Inject 3s Latency Delay"] }), _jsx("span", { className: "text-[11px] text-slate-400 block", children: "Validates circuit breaker triggers" })] })] })] }), _jsxs("div", { className: "space-y-3 font-mono", children: [_jsxs("h3", { className: "text-sm font-semibold text-slate-200 flex items-center gap-2", children: [_jsx(Layers, { className: "w-4 h-4 text-cyan-400" }), "Completed Chaos Experiment Reports"] }), experiments.map((exp) => (_jsxs(Card, { className: "p-4 bg-slate-900 border-slate-800 space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-bold text-indigo-400", children: exp.experimentId }), _jsx("span", { className: "text-xs font-bold text-slate-200", children: exp.name }), _jsx(Badge, { variant: "intelligence", size: "sm", children: exp.target })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Badge, { variant: "success", size: "sm", children: [_jsx(CheckCircle2, { className: "w-3 h-3 mr-1" }), "Score: ", exp.resilienceScore, "%"] }), _jsxs("span", { className: "text-xs text-slate-400", children: [exp.mttrMs, "ms MTTR"] })] })] }), _jsxs("div", { className: "flex items-center justify-between text-[11px] bg-slate-950 p-2.5 rounded border border-slate-800 text-slate-400", children: [_jsxs("span", { children: ["Fault: ", _jsx("strong", { className: "text-amber-400", children: exp.fault })] }), _jsxs("span", { children: ["Invariants Preserved: ", _jsx("strong", { className: "text-emerald-400", children: "TRUE (0 LEAKS)" })] }), _jsxs("span", { children: ["Run Time: ", _jsx("strong", { className: "text-slate-300", children: exp.timestamp })] })] })] }, exp.experimentId)))] })] }));
};
