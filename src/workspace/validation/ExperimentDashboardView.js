import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const ExperimentDashboardView = () => {
    const [activeAnalysisMode, setActiveAnalysisMode] = useState('BAYESIAN');
    const experiments = [
        {
            id: 'EXP-2026-001',
            name: 'Pareto Cost Preference Weight Shift',
            controlPolicy: 'v4.2-pareto (w_cost=0.30)',
            treatmentPolicy: 'v5.0-candidate (w_cost=0.40)',
            sampleSize: '235 / 500 trials',
            tStat: 't = 2.84',
            pValue: 'p = 0.0048',
            cohensD: 'd = +0.42 (Medium)',
            probSuperior: '98.4%',
            expectedLoss: '0.0008',
            sprtDecision: 'ACCEPT_H1_TREATMENT',
            status: 'CONVERGED_SUCCESS',
        },
        {
            id: 'EXP-2026-002',
            name: 'Adaptive Fast-Fail Speculative Execution',
            controlPolicy: 'Serial Fallback Chain',
            treatmentPolicy: 'Speculative Parallel Flash-Lite',
            sampleSize: '410 / 500 trials',
            tStat: 't = 4.12',
            pValue: 'p < 0.0001',
            cohensD: 'd = +0.78 (Large)',
            probSuperior: '99.9%',
            expectedLoss: '0.0002',
            sprtDecision: 'ACCEPT_H1_TREATMENT',
            status: 'READY_FOR_PROMOTION',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\uD83E\uDDEA" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Scientific Experimentation & A/B Hypothesis Lab" }), _jsx(Badge, { variant: "success", size: "sm", children: "SPRT & BAYESIAN READY" })] }), _jsx("p", { className: "text-sm font-mono text-[#94A3B8] mt-1", children: "Rigorous A/B hypothesis testing, Welch's t-test, Cohen's d effect sizes, Bayesian posterior updates, and Wald's SPRT early stopping." })] }), _jsx("div", { className: "flex items-center gap-2", children: ['BAYESIAN', 'FREQUENTIST', 'SPRT'].map((mode) => (_jsx("button", { onClick: () => setActiveAnalysisMode(mode), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${activeAnalysisMode === mode
                                    ? 'bg-blue-600 text-white'
                                    : 'bg-[#1E293B] text-[#94A3B8] hover:bg-[#334155]'}`, children: mode }, mode))) })] }) }), _jsx("div", { className: "grid grid-cols-1 gap-4", children: experiments.map((exp) => (_jsxs(Card, { className: "p-6 bg-[#0F172A] border-[#1E293B]", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono text-cyan-400 font-bold", children: exp.id }), _jsx("h3", { className: "text-sm font-bold font-mono text-[#F8FAFC]", children: exp.name })] }), _jsxs("div", { className: "text-xs font-mono text-[#94A3B8] mt-1", children: ["Control: ", _jsx("span", { className: "text-[#E2E8F0]", children: exp.controlPolicy }), " vs Treatment:", ' ', _jsx("span", { className: "text-indigo-400 font-bold", children: exp.treatmentPolicy })] })] }), _jsx(Badge, { variant: "success", size: "sm", children: exp.status })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4 mt-6 pt-4 border-t border-[#1E293B]", children: [activeAnalysisMode === 'BAYESIAN' && (_jsxs(_Fragment, { children: [_jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B]", children: [_jsx("div", { className: "text-[11px] font-mono text-[#94A3B8]", children: "P(Treatment > Control)" }), _jsx("div", { className: "text-xl font-bold font-mono text-emerald-400 mt-1", children: exp.probSuperior })] }), _jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B]", children: [_jsx("div", { className: "text-[11px] font-mono text-[#94A3B8]", children: "Expected Loss E[L]" }), _jsx("div", { className: "text-xl font-bold font-mono text-cyan-400 mt-1", children: exp.expectedLoss })] }), _jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B]", children: [_jsx("div", { className: "text-[11px] font-mono text-[#94A3B8]", children: "Sample Progress" }), _jsx("div", { className: "text-xl font-bold font-mono text-[#F8FAFC] mt-1", children: exp.sampleSize })] }), _jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B]", children: [_jsx("div", { className: "text-[11px] font-mono text-[#94A3B8]", children: "Bayesian Recommendation" }), _jsx("div", { className: "text-sm font-bold font-mono text-emerald-400 mt-1", children: "ADOPT_TREATMENT" })] })] })), activeAnalysisMode === 'FREQUENTIST' && (_jsxs(_Fragment, { children: [_jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B]", children: [_jsx("div", { className: "text-[11px] font-mono text-[#94A3B8]", children: "Welch's t-Statistic" }), _jsx("div", { className: "text-xl font-bold font-mono text-indigo-400 mt-1", children: exp.tStat })] }), _jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B]", children: [_jsx("div", { className: "text-[11px] font-mono text-[#94A3B8]", children: "p-Value (Alpha=0.05)" }), _jsx("div", { className: "text-xl font-bold font-mono text-emerald-400 mt-1", children: exp.pValue })] }), _jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B]", children: [_jsx("div", { className: "text-[11px] font-mono text-[#94A3B8]", children: "Cohen's d Effect Size" }), _jsx("div", { className: "text-xl font-bold font-mono text-cyan-400 mt-1", children: exp.cohensD })] }), _jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B]", children: [_jsx("div", { className: "text-[11px] font-mono text-[#94A3B8]", children: "Null Hypothesis H0" }), _jsx("div", { className: "text-sm font-bold font-mono text-emerald-400 mt-1", children: "REJECTED (p < 0.05)" })] })] })), activeAnalysisMode === 'SPRT' && (_jsxs(_Fragment, { children: [_jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B]", children: [_jsx("div", { className: "text-[11px] font-mono text-[#94A3B8]", children: "Wald's LLR Boundary" }), _jsx("div", { className: "text-xl font-bold font-mono text-emerald-400 mt-1", children: "ln(A) > +2.89" })] }), _jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B]", children: [_jsx("div", { className: "text-[11px] font-mono text-[#94A3B8]", children: "Sequential Decision" }), _jsx("div", { className: "text-sm font-bold font-mono text-emerald-400 mt-1", children: exp.sprtDecision })] }), _jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B]", children: [_jsx("div", { className: "text-[11px] font-mono text-[#94A3B8]", children: "Trials to Stop" }), _jsx("div", { className: "text-xl font-bold font-mono text-[#F8FAFC] mt-1", children: exp.sampleSize })] }), _jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B]", children: [_jsx("div", { className: "text-[11px] font-mono text-[#94A3B8]", children: "Type I / II Error Bounds" }), _jsx("div", { className: "text-sm font-bold font-mono text-cyan-400 mt-1", children: "\u03B1 = 0.05, \u03B2 = 0.10" })] })] }))] })] }, exp.id))) })] }));
};
