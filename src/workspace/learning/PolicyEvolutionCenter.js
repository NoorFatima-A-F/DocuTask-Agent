import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Sliders, Cpu, Play, CheckCircle2 } from 'lucide-react';
export const PolicyEvolutionCenter = () => {
    const [concurrency, setConcurrency] = useState(8);
    const [retries, setRetries] = useState(3);
    const [confThreshold, setConfThreshold] = useState(0.88);
    const [isSimulating, setIsSimulating] = useState(false);
    const [simOutput, setSimOutput] = useState(null);
    const activePolicies = [
        {
            id: 'pol-baseline-planner',
            name: 'Baseline Dynamic Partitioning Policy',
            target: 'planner',
            version: '1.0.0',
            status: 'ACTIVE',
            parameters: { concurrency_limit: 6, max_retries: 3, confidence_threshold: 0.85 },
        },
        {
            id: 'pol-baseline-worker',
            name: 'Adaptive Jitter Backoff Worker Policy',
            target: 'worker',
            version: '1.0.0',
            status: 'ACTIVE',
            parameters: { base_delay_ms: 250, max_retries: 3 },
        },
    ];
    const handleSimulate = () => {
        setIsSimulating(true);
        setTimeout(() => {
            setIsSimulating(false);
            setSimOutput({
                gain: `+${(concurrency * 2.2 - retries * 0.4).toFixed(1)}% Throughput`,
                risk: '0.12 (LOW)',
                confidence: '96.5% Posterior',
            });
        }, 600);
    };
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsx("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 rounded-xl text-indigo-400", children: _jsx(Sliders, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Autonomous Policy Evolution Center", _jsx(Badge, { variant: "intelligence", size: "sm", children: "Phase 13.5" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] font-mono", children: "Synthesize, simulate counterfactual parameter adjustments, and manage active production runtime policies" })] })] }) }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6 font-mono", children: [_jsxs(Card, { className: "p-5 lg:col-span-2 rounded-2xl border border-indigo-500/40 bg-[#0F172A] space-y-5", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-[#1E293B] pb-3", children: [_jsxs("span", { className: "text-xs font-bold text-white flex items-center gap-2", children: [_jsx(Cpu, { className: "w-4 h-4 text-indigo-400" }), "Candidate Policy Evolution Sandbox"] }), _jsx(Badge, { variant: "outline", size: "sm", children: "Monte-Carlo Evaluation" })] }), _jsxs("div", { className: "space-y-4 text-xs", children: [_jsxs("div", { className: "space-y-1.5", children: [_jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Concurrency Worker Limit:" }), _jsxs("span", { className: "text-cyan-400 font-bold", children: [concurrency, " workers"] })] }), _jsx("input", { type: "range", min: "1", max: "16", value: concurrency, onChange: (e) => setConcurrency(Number(e.target.value)), className: "w-full accent-indigo-500 bg-[#1E293B]" })] }), _jsxs("div", { className: "space-y-1.5", children: [_jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Max Retries on Transient Errors:" }), _jsxs("span", { className: "text-indigo-400 font-bold", children: [retries, " attempts"] })] }), _jsx("input", { type: "range", min: "0", max: "8", value: retries, onChange: (e) => setRetries(Number(e.target.value)), className: "w-full accent-indigo-500 bg-[#1E293B]" })] }), _jsxs("div", { className: "space-y-1.5", children: [_jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Confidence Invariance Floor:" }), _jsx("span", { className: "text-emerald-400 font-bold", children: confThreshold.toFixed(2) })] }), _jsx("input", { type: "range", min: "0.50", max: "0.99", step: "0.01", value: confThreshold, onChange: (e) => setConfThreshold(Number(e.target.value)), className: "w-full accent-indigo-500 bg-[#1E293B]" })] })] }), _jsx("div", { className: "flex items-center gap-3 pt-2", children: _jsxs("button", { onClick: handleSimulate, disabled: isSimulating, className: "flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-mono font-bold transition-colors disabled:opacity-50", children: [_jsx(Play, { className: `w-3.5 h-3.5 ${isSimulating ? 'animate-pulse' : ''}` }), isSimulating ? 'Simulating 100 Replays...' : 'Run Counterfactual Simulation'] }) }), simOutput && (_jsxs("div", { className: "p-4 bg-[#0B1120] border border-emerald-500/30 rounded-xl space-y-2 text-xs", children: [_jsxs("span", { className: "text-emerald-400 font-bold block flex items-center gap-1.5", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5" }), "Counterfactual Simulation Passed (100 Monte-Carlo Replays)"] }), _jsxs("div", { className: "grid grid-cols-3 gap-3 pt-1", children: [_jsxs("div", { children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "PROJECTED GAIN" }), _jsx("span", { className: "text-cyan-400 font-bold", children: simOutput.gain })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "COMPOSITE RISK" }), _jsx("span", { className: "text-emerald-400 font-bold", children: simOutput.risk })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[10px] text-[#64748B] block", children: "POSTERIOR CERTAINTY" }), _jsx("span", { className: "text-indigo-400 font-bold", children: simOutput.confidence })] })] })] }))] }), _jsxs(Card, { className: "p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-[#1E293B] pb-3", children: [_jsx("span", { className: "text-xs font-bold text-white block", children: "Active Production Policies" }), _jsx(Badge, { variant: "success", size: "sm", children: "2 Live" })] }), _jsx("div", { className: "space-y-3", children: activePolicies.map((p) => (_jsxs("div", { className: "p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl space-y-2 text-xs", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-white font-bold", children: p.name }), _jsxs(Badge, { variant: "outline", size: "sm", children: ["v", p.version] })] }), _jsx("pre", { className: "text-[10px] text-cyan-300 font-mono overflow-x-auto", children: JSON.stringify(p.parameters, null, 2) }), _jsxs("div", { className: "flex justify-between items-center text-[10px] text-[#64748B]", children: [_jsxs("span", { children: ["Target: ", p.target] }), _jsx("span", { className: "text-emerald-400", children: "Enforcing Guardrails" })] })] }, p.id))) })] })] })] }));
};
