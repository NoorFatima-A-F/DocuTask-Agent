import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const PolicyEvolutionTimelineView = () => {
    const [policies, setPolicies] = useState([
        {
            id: 'pol_v5_0_cand',
            version: 'v5.0.0-candidate',
            name: 'Bayesian Multi-Objective Prior Optimization',
            stage: 'CANARY_STAGING',
            parameters: {
                weight_accuracy: 0.40,
                weight_latency: 0.20,
                weight_cost: 0.40,
                confidence_threshold: 0.88,
            },
            provenanceHash: '8b4d9e201a4f3312',
            deployedAt: '2 hours ago',
        },
        {
            id: 'pol_v4_2',
            version: 'v4.2.0',
            name: 'Baseline Balanced Pareto Optimization',
            stage: 'PRODUCTION',
            parameters: {
                weight_accuracy: 0.45,
                weight_latency: 0.25,
                weight_cost: 0.30,
                confidence_threshold: 0.85,
            },
            provenanceHash: 'a1f89c44b3e21098',
            deployedAt: '5 days ago',
        },
        {
            id: 'pol_v4_1',
            version: 'v4.1.0',
            name: 'Conservative High-Confidence Router',
            stage: 'RETIRED',
            parameters: {
                weight_accuracy: 0.60,
                weight_latency: 0.20,
                weight_cost: 0.20,
                confidence_threshold: 0.90,
            },
            provenanceHash: '3c19e598fa201b55',
            deployedAt: '2 weeks ago',
        },
    ]);
    const [rollbackLog, setRollbackLog] = useState([]);
    const handleInstantRollback = (policyId) => {
        setPolicies((prev) => prev.map((p) => {
            if (p.id === policyId)
                return { ...p, stage: 'ROLLED_BACK' };
            if (p.id === 'pol_v4_2')
                return { ...p, stage: 'PRODUCTION' };
            return p;
        }));
        setRollbackLog((prev) => [
            `[${new Date().toLocaleTimeString()}] Instant atomic rollback executed: ${policyId} reverted to safe baseline pol_v4_2.`,
            ...prev,
        ]);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsx("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\uD83E\uDDEC" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Policy Self-Evolution & Instant Rollback Timeline" }), _jsx(Badge, { variant: "success", size: "sm", children: "ATOMIC ROLLBACK READY" })] }), _jsx("p", { className: "text-sm font-mono text-[#94A3B8] mt-1", children: "Versioned policy state machine (Draft \u2192 Shadow \u2192 Canary \u2192 Production) with instant rollback governance." })] }) }) }), _jsx("div", { className: "space-y-4", children: policies.map((p) => (_jsxs(Card, { className: "p-6 bg-[#0F172A] border-[#1E293B]", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono text-cyan-400 font-bold", children: p.version }), _jsx("h3", { className: "text-sm font-bold font-mono text-[#F8FAFC]", children: p.name })] }), _jsxs("div", { className: "text-xs font-mono text-[#64748B] mt-1", children: ["SHA256 Provenance: ", p.provenanceHash, " \u2022 Deployed: ", p.deployedAt] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: p.stage === 'PRODUCTION'
                                                ? 'success'
                                                : p.stage === 'CANARY_STAGING'
                                                    ? 'info'
                                                    : p.stage === 'ROLLED_BACK'
                                                        ? 'error'
                                                        : 'default', size: "sm", children: p.stage }), p.stage === 'CANARY_STAGING' && (_jsx("button", { onClick: () => handleInstantRollback(p.id), className: "px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-rose-600/20 border border-rose-500 text-rose-300 hover:bg-rose-600 hover:text-white transition-all shadow-md", children: "\u26A1 INSTANT ROLLBACK" }))] })] }), _jsxs("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-3 mt-4 pt-3 border-t border-[#1E293B]", children: [_jsxs("div", { className: "p-2.5 rounded-lg bg-[#020617] border border-[#1E293B] font-mono text-xs", children: [_jsx("div", { className: "text-[#94A3B8]", children: "Weight Accuracy (w_acc):" }), _jsx("div", { className: "text-cyan-400 font-bold mt-0.5", children: p.parameters.weight_accuracy })] }), _jsxs("div", { className: "p-2.5 rounded-lg bg-[#020617] border border-[#1E293B] font-mono text-xs", children: [_jsx("div", { className: "text-[#94A3B8]", children: "Weight Latency (w_lat):" }), _jsx("div", { className: "text-indigo-400 font-bold mt-0.5", children: p.parameters.weight_latency })] }), _jsxs("div", { className: "p-2.5 rounded-lg bg-[#020617] border border-[#1E293B] font-mono text-xs", children: [_jsx("div", { className: "text-[#94A3B8]", children: "Weight Cost (w_cost):" }), _jsx("div", { className: "text-emerald-400 font-bold mt-0.5", children: p.parameters.weight_cost })] }), _jsxs("div", { className: "p-2.5 rounded-lg bg-[#020617] border border-[#1E293B] font-mono text-xs", children: [_jsx("div", { className: "text-[#94A3B8]", children: "Confidence Threshold:" }), _jsx("div", { className: "text-[#F8FAFC] font-bold mt-0.5", children: p.parameters.confidence_threshold })] })] })] }, p.id))) }), rollbackLog.length > 0 && (_jsxs(Card, { className: "p-4 bg-rose-950/20 border-rose-900/50", children: [_jsx("h4", { className: "text-xs font-bold font-mono text-rose-300 mb-2", children: "\u26A1 Rollback Audit Log" }), _jsx("div", { className: "space-y-1 font-mono text-[11px] text-rose-200", children: rollbackLog.map((log, i) => (_jsx("div", { children: log }, i))) })] }))] }));
};
