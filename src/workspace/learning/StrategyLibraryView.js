import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Layers, CheckCircle2, ShieldCheck } from 'lucide-react';
export const StrategyLibraryView = () => {
    const strategies = [
        {
            id: 'strat-001',
            name: 'Dynamic High-Throughput Wavefront Strategy',
            goalType: 'DYNAMIC_EXTRACTION',
            gain: '+26.4%',
            version: '1.2.0',
            status: 'ACTIVE_IN_PRODUCTION',
            tactics: [
                'Concurrent OCR Sharding (4 workers)',
                'Pre-verification Schema Invariance Checks',
                'Exponential Retry with 250ms Base Backoff',
            ],
            applicableGoals: ['EXTRACTION', 'OCR', 'SCHEMA_MAPPING'],
        },
        {
            id: 'strat-002',
            name: 'SMT-Gated High-Assurance Reasoning Strategy',
            goalType: 'VERIFICATION_AND_REASONING',
            gain: '100% Invariance',
            version: '1.0.0',
            status: 'ACTIVE_IN_PRODUCTION',
            tactics: [
                'Multi-agent cross validation referee',
                'Z3 Symbolic SMT constraint proving',
                'Cryptographic truth ledger anchor before output',
            ],
            applicableGoals: ['REASONING', 'VALIDATION', 'LEGAL_AUDIT'],
        },
        {
            id: 'strat-003',
            name: 'Low-Latency Jittered Throttle Recovery Strategy',
            goalType: 'RESILIENCE_AND_RECOVERY',
            gain: '0% Task Loss',
            version: '1.1.0',
            status: 'ACTIVE_IN_PRODUCTION',
            tactics: [
                'Adaptive sliding rate-limit throttle monitoring',
                'Automatic task rerouting to secondary worker pool',
                'Circuit breaker tripped after 3 consecutive failures',
            ],
            applicableGoals: ['WORKER_EXECUTION', 'API_DISPATCH', 'RETRY'],
        },
    ];
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-amber-500/20 to-orange-500/20 border border-amber-500/30 rounded-xl text-amber-400", children: _jsx(Layers, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Autonomous Execution Strategy Library", _jsx(Badge, { variant: "intelligence", size: "sm", children: "Phase 13.5" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] font-mono", children: "Reusable, high-utility execution templates synthesized from empirical reflections and validated by governance" })] })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx(Badge, { variant: "success", size: "md", children: "3 Active Strategies" }) })] }), _jsx("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6 font-mono", children: strategies.map((strat) => (_jsxs(Card, { className: "p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] space-y-4 flex flex-col justify-between", children: [_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between gap-2", children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: strat.goalType }), _jsxs(Badge, { variant: "outline", size: "sm", children: ["v", strat.version] })] }), _jsxs("div", { children: [_jsx("h3", { className: "text-sm font-bold text-white", children: strat.name }), _jsxs("span", { className: "text-emerald-400 text-xs font-bold block mt-1", children: ["Expected Gain: ", strat.gain] })] }), _jsxs("div", { className: "p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl space-y-2 text-xs", children: [_jsx("span", { className: "text-[10px] text-[#64748B] block font-bold", children: "PRESCRIBED TACTICS:" }), strat.tactics.map((tactic, idx) => (_jsxs("div", { className: "flex items-start gap-2 text-[#94A3B8]", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5 text-indigo-400 shrink-0 mt-0.5" }), _jsx("span", { children: tactic })] }, idx)))] }), _jsx("div", { className: "flex flex-wrap gap-1.5 pt-1", children: strat.applicableGoals.map((g, idx) => (_jsx("span", { className: "px-2 py-0.5 bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 rounded text-[10px]", children: g }, idx))) })] }), _jsxs("div", { className: "pt-3 border-t border-[#1E293B] flex items-center justify-between text-xs", children: [_jsxs("span", { className: "text-emerald-400 font-bold flex items-center gap-1", children: [_jsx(ShieldCheck, { className: "w-3.5 h-3.5" }), strat.status] }), _jsxs("span", { className: "text-[11px] text-[#64748B]", children: ["ID: ", strat.id] })] })] }, strat.id))) })] }));
};
