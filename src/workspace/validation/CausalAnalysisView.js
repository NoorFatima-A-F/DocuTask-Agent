import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const CausalAnalysisView = () => {
    const [selectedTreatment, setSelectedTreatment] = useState('gemini-1.5-pro');
    const scmNodes = [
        { id: 'complexity', name: 'Document Complexity (Z)', type: 'EXOGENOUS', desc: 'Layout density, table count, visual noise' },
        { id: 'ocr_noise', name: 'OCR Quality Noise (W)', type: 'EXOGENOUS', desc: 'Base optical character recognition confidence score' },
        { id: 'model_choice', name: 'Planner Model Choice (X)', type: 'INTERVENTION', desc: 'Routing decision: Flash vs Pro vs Flash-Lite' },
        { id: 'retry_count', name: 'Retry Loop Count (R)', type: 'MEDIATOR', desc: 'Validation failures & exponential backoff retries' },
        { id: 'accuracy', name: 'Extraction Accuracy (Y_A)', type: 'OUTCOME', desc: 'Ground truth field-level exact-match score' },
        { id: 'latency_ms', name: 'End-to-End Latency (Y_L)', type: 'OUTCOME', desc: 'Total mission execution duration (ms)' },
        { id: 'cost_usd', name: 'Execution Cost USD (Y_C)', type: 'OUTCOME', desc: 'Total LLM API token monetary expenditure' },
    ];
    const rootCauseAttributions = [
        {
            node: 'OCR Quality Noise (W)',
            share: '35.0%',
            isRoot: true,
            explanation: 'Low OCR confidence (0.68) triggered extensive re-OCR and heuristic repair passes.',
        },
        {
            node: 'Retry Loop Count (R)',
            share: '40.0%',
            isRoot: false,
            explanation: '3 exponential backoff retries amplified cumulative mission latency by +1200ms.',
        },
        {
            node: 'Planner Model Choice (X)',
            share: '25.0%',
            isRoot: false,
            explanation: 'Heavyweight reasoning model choice incurred higher base token processing time.',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsx("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\uD83D\uDD78\uFE0F" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Pearl's Structural Causal Models (SCM) & do()-Calculus" }), _jsx(Badge, { variant: "success", size: "sm", children: "BACKDOOR ADJUSTED" })] }), _jsx("p", { className: "text-sm font-mono text-[#94A3B8] mt-1", children: "Causal DAG structural equation modeling, interventional Average Treatment Effect (ATE), and root-cause attribution." })] }) }) }), _jsxs(Card, { className: "p-6 bg-[#0F172A] border-[#1E293B]", children: [_jsx("h3", { className: "text-sm font-bold font-mono text-[#F8FAFC] mb-4", children: "Structural Causal Model DAG Architecture" }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-3", children: scmNodes.map((n) => (_jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B]", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-bold font-mono text-[#F8FAFC]", children: n.name }), _jsx(Badge, { variant: n.type === 'INTERVENTION'
                                                ? 'info'
                                                : n.type === 'OUTCOME'
                                                    ? 'success'
                                                    : n.type === 'MEDIATOR'
                                                        ? 'warning'
                                                        : 'default', size: "sm", children: n.type })] }), _jsx("p", { className: "text-[11px] font-mono text-[#94A3B8] mt-2", children: n.desc })] }, n.id))) })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6", children: [_jsxs(Card, { className: "p-6 bg-[#0F172A] border-[#1E293B]", children: [_jsx("h3", { className: "text-sm font-bold font-mono text-[#F8FAFC] mb-2", children: "Interventional do(X = x) Average Treatment Effect" }), _jsx("p", { className: "text-xs font-mono text-[#94A3B8] mb-4", children: "Formula: P(Y | do(X=x)) = \u2211_z P(Y | X=x, Z=z) \u00B7 P(Z=z)" }), _jsxs("div", { className: "flex items-center gap-2 mb-4", children: [_jsx("button", { onClick: () => setSelectedTreatment('gemini-1.5-pro'), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${selectedTreatment === 'gemini-1.5-pro'
                                            ? 'bg-blue-600 text-white'
                                            : 'bg-[#1E293B] text-[#94A3B8]'}`, children: "do(Model = Gemini 1.5 Pro)" }), _jsx("button", { onClick: () => setSelectedTreatment('gemini-flash-lite'), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${selectedTreatment === 'gemini-flash-lite'
                                            ? 'bg-blue-600 text-white'
                                            : 'bg-[#1E293B] text-[#94A3B8]'}`, children: "do(Model = Flash-Lite)" })] }), _jsxs("div", { className: "p-4 rounded-xl bg-[#020617] border border-[#1E293B] space-y-2 font-mono text-xs", children: [_jsxs("div", { className: "flex justify-between", children: [_jsx("span", { className: "text-[#94A3B8]", children: "Observational Expectation E[Y|X]:" }), _jsx("span", { className: "text-[#F8FAFC]", children: "0.9700" })] }), _jsxs("div", { className: "flex justify-between", children: [_jsx("span", { className: "text-[#94A3B8]", children: "Interventional Expectation E[Y|do(X)]:" }), _jsx("span", { className: "text-cyan-400 font-bold", children: "0.9855" })] }), _jsxs("div", { className: "flex justify-between", children: [_jsx("span", { className: "text-[#94A3B8]", children: "Confounding Bias (Selection Effect):" }), _jsx("span", { className: "text-amber-400", children: "-0.0155" })] }), _jsxs("div", { className: "flex justify-between pt-2 border-t border-[#1E293B]", children: [_jsx("span", { className: "text-[#94A3B8]", children: "Average Treatment Effect (ATE):" }), _jsx("span", { className: "text-emerald-400 font-bold", children: "+0.0355 (+3.55% Acc)" })] })] })] }), _jsxs(Card, { className: "p-6 bg-[#0F172A] border-[#1E293B]", children: [_jsx("h3", { className: "text-sm font-bold font-mono text-[#F8FAFC] mb-2", children: "Causal Root-Cause Attribution Waterfall" }), _jsx("p", { className: "text-xs font-mono text-[#94A3B8] mb-4", children: "Decomposition of +1970ms Latency Spike on Mission MIS-SCAN-1099." }), _jsx("div", { className: "space-y-3 font-mono text-xs", children: rootCauseAttributions.map((att, idx) => (_jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B]", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-bold text-[#F8FAFC]", children: att.node }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-cyan-400 font-bold", children: att.share }), att.isRoot && (_jsx(Badge, { variant: "error", size: "sm", children: "ROOT CAUSE" }))] })] }), _jsx("p", { className: "text-[11px] text-[#94A3B8] mt-1", children: att.explanation })] }, idx))) })] })] })] }));
};
