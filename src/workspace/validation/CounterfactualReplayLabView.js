import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const CounterfactualReplayLabView = () => {
    const [selectedScenario, setSelectedScenario] = useState('sc_nominal');
    const scenarios = [
        {
            id: 'sc_nominal',
            name: 'Nominal Production',
            desc: 'Standard operational conditions with stable low-latency responses.',
            latMultiplier: 1.0,
            costMultiplier: 1.0,
        },
        {
            id: 'sc_peak_load',
            name: 'Extreme Peak Queue Congestion',
            desc: 'Heavy queue backpressure causing 2.5x latency inflation on external LLM calls.',
            latMultiplier: 2.5,
            costMultiplier: 1.0,
        },
        {
            id: 'sc_degraded_scan',
            name: 'Degraded Physical Scan Quality',
            desc: 'Severe visual noise and skew lowering OCR recognition by 15%.',
            latMultiplier: 1.2,
            costMultiplier: 1.0,
        },
        {
            id: 'sc_cloud_rate_limit',
            name: 'Cloud API Rate-Limit Throttling',
            desc: 'Transient HTTP 429 throttling causing exponential backoff retries.',
            latMultiplier: 3.0,
            costMultiplier: 1.1,
        },
    ];
    const candidateBranches = [
        {
            branchId: 'FACTUAL-RUN',
            label: 'Factual Production Choice (Gemini 2.5 Flash)',
            accuracy: '96.2%',
            latency: '480 ms',
            cost: '$0.0018',
            utility: '0.884',
            regret: '0.000',
            isFactual: true,
            isOptimal: true,
        },
        {
            branchId: 'CF-PRO-001',
            label: 'What if Gemini 1.5 Pro was selected?',
            accuracy: '97.7%',
            latency: '1344 ms',
            cost: '$0.0153',
            utility: '0.812',
            regret: '+0.072',
            isFactual: false,
            isOptimal: false,
        },
        {
            branchId: 'CF-LITE-002',
            label: 'What if Gemini Flash-Lite was selected?',
            accuracy: '91.7%',
            latency: '216 ms',
            cost: '$0.0004',
            utility: '0.865',
            regret: '+0.019',
            isFactual: false,
            isOptimal: false,
        },
        {
            branchId: 'CF-NORETRY-003',
            label: 'What if Zero-Retry Fast-Fail policy was applied?',
            accuracy: '88.2%',
            latency: '336 ms',
            cost: '$0.0014',
            utility: '0.835',
            regret: '+0.049',
            isFactual: false,
            isOptimal: false,
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsx("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\uD83D\uDD00" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Counterfactual Simulator & Opportunity Cost Lab" }), _jsx(Badge, { variant: "success", size: "sm", children: "REPLAY READY" })] }), _jsx("p", { className: "text-sm font-mono text-[#94A3B8] mt-1", children: "Simulate alternative decisions (\"What if Pro?\", \"What if No Retry?\") on historical missions to prove decision optimality." })] }) }) }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4", children: scenarios.map((sc) => (_jsxs("div", { onClick: () => setSelectedScenario(sc.id), className: `p-4 rounded-xl cursor-pointer border transition-all ${selectedScenario === sc.id
                        ? 'bg-blue-950/40 border-blue-500 shadow-lg shadow-blue-500/10'
                        : 'bg-[#0F172A] border-[#1E293B] hover:border-[#334155]'}`, children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-mono text-xs font-bold text-[#F8FAFC]", children: sc.name }), selectedScenario === sc.id && (_jsx(Badge, { variant: "info", size: "sm", children: "ACTIVE" }))] }), _jsx("p", { className: "text-[11px] font-mono text-[#94A3B8] mt-2", children: sc.desc })] }, sc.id))) }), _jsxs(Card, { className: "p-6 bg-[#0F172A] border-[#1E293B]", children: [_jsx("h3", { className: "text-sm font-bold font-mono text-[#F8FAFC] mb-4", children: "Factual vs Counterfactual Decision Differential" }), _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left font-mono text-xs", children: [_jsx("thead", { children: _jsxs("tr", { className: "border-b border-[#1E293B] text-[#94A3B8]", children: [_jsx("th", { className: "pb-3", children: "Candidate Branch" }), _jsx("th", { className: "pb-3", children: "Simulated Acc" }), _jsx("th", { className: "pb-3", children: "Simulated Latency" }), _jsx("th", { className: "pb-3", children: "Simulated Cost" }), _jsx("th", { className: "pb-3", children: "Utility U(x)" }), _jsx("th", { className: "pb-3", children: "Planner Regret" }), _jsx("th", { className: "pb-3", children: "Verdict" })] }) }), _jsx("tbody", { className: "divide-y divide-[#1E293B]", children: candidateBranches.map((b) => (_jsxs("tr", { className: `hover:bg-[#1E293B]/40 transition-colors ${b.isFactual ? 'bg-emerald-950/20' : ''}`, children: [_jsxs("td", { className: "py-3", children: [_jsx("div", { className: "font-bold text-[#F8FAFC]", children: b.label }), _jsx("div", { className: "text-[#64748B] text-[11px]", children: b.branchId })] }), _jsx("td", { className: "py-3 text-cyan-400", children: b.accuracy }), _jsx("td", { className: "py-3 text-[#E2E8F0]", children: b.latency }), _jsx("td", { className: "py-3 text-[#E2E8F0]", children: b.cost }), _jsx("td", { className: "py-3 text-indigo-400 font-bold", children: b.utility }), _jsx("td", { className: "py-3", children: _jsx("span", { className: b.isOptimal ? 'text-emerald-400 font-bold' : 'text-amber-400', children: b.regret }) }), _jsx("td", { className: "py-3", children: _jsx(Badge, { variant: b.isOptimal ? 'success' : 'default', size: "sm", children: b.isOptimal ? 'OPTIMAL FACTUAL' : 'SUB-OPTIMAL' }) })] }, b.branchId))) })] }) })] })] }));
};
