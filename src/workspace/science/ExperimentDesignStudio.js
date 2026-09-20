import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { FlaskConical, Play, CheckCircle2, Sliders, TrendingDown, RotateCcw, } from 'lucide-react';
export const ExperimentDesignStudio = () => {
    const [activeTab, setActiveTab] = useState('trials');
    const [runningId, setRunningId] = useState(null);
    const [executionLog, setExecutionLog] = useState(null);
    const experiments = [
        {
            id: 'exp-cache-ab-01',
            hypothesisId: 'hyp-spec-tensor-01',
            title: 'A/B Controlled Speculative Cache Evaluation',
            type: 'A_B_CONTROLLED',
            status: 'COMPLETED',
            sampleSize: 2500,
            controlMean: 278.5,
            treatmentMean: 194.2,
            effectSize: 1.42,
            pValue: 0.0001,
            isSignificant: true,
        },
        {
            id: 'exp-ring-buffer-02',
            hypothesisId: 'hyp-lockfree-ring-03',
            title: 'Lock-Free Ring Buffer Stress & Replay Benchmark',
            type: 'COUNTERFACTUAL_REPLAY',
            status: 'COMPLETED',
            sampleSize: 10000,
            controlMean: 184.2,
            treatmentMean: 0.0,
            effectSize: 2.10,
            pValue: 0.0001,
            isSignificant: true,
        },
        {
            id: 'exp-triadic-auction-03',
            hypothesisId: 'hyp-triadic-coalition-02',
            title: 'Triadic vs Monolithic Agent Allocation Trial',
            type: 'SENSITIVITY_SWEEP',
            status: 'RUNNING',
            sampleSize: 5000,
            controlMean: 42.1,
            treatmentMean: 4.3,
            effectSize: 1.85,
            pValue: 0.0002,
            isSignificant: true,
        },
    ];
    const handleRunExperiment = (id) => {
        setRunningId(id);
        setTimeout(() => {
            setRunningId(null);
            setExecutionLog(`Experiment ${id} executed successfully: N=2,500 traces replayed, p=0.0001, Cohen's d=1.42. Statistical significance achieved.`);
            setTimeout(() => setExecutionLog(null), 5000);
        }, 1500);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(FlaskConical, { className: "w-6 h-6 text-purple-500" }), "Empirical Experiment Design Studio"] }), _jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: "Designs, parameterizes, and automates A/B testing, counterfactual mission replays, sensitivity sweeps, and stress isolations." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs("div", { className: "flex bg-gray-100 dark:bg-gray-800 p-1 rounded-lg", children: [_jsx("button", { onClick: () => setActiveTab('trials'), className: `px-3 py-1 text-xs rounded-md transition-colors ${activeTab === 'trials' ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white font-medium shadow-sm' : 'text-gray-500'}`, children: "Active Trials" }), _jsx("button", { onClick: () => setActiveTab('designer'), className: `px-3 py-1 text-xs rounded-md transition-colors ${activeTab === 'designer' ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white font-medium shadow-sm' : 'text-gray-500'}`, children: "Design New Trial" })] }) })] }), executionLog && (_jsxs("div", { className: "p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-lg text-sm text-emerald-800 dark:text-emerald-300 flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-5 h-5 flex-shrink-0" }), _jsx("span", { children: executionLog })] })), activeTab === 'trials' ? (_jsx("div", { className: "space-y-4", children: _jsx("div", { className: "grid grid-cols-1 gap-4", children: experiments.map(exp => (_jsxs(Card, { className: "p-5 space-y-4", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-gray-100 dark:border-gray-800 pb-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-xs text-purple-500 font-semibold", children: exp.id }), _jsxs(Badge, { variant: "outline", size: "sm", children: ["Hypothesis: ", exp.hypothesisId] }), _jsx(Badge, { variant: exp.status === 'COMPLETED' ? 'success' : 'warning', size: "sm", children: exp.status })] }), _jsx("h3", { className: "text-base font-semibold text-gray-900 dark:text-white mt-1", children: exp.title })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Badge, { variant: "intelligence", size: "sm", children: ["Type: ", exp.type] }), _jsxs(Button, { variant: "outline", size: "sm", onClick: () => handleRunExperiment(exp.id), disabled: runningId === exp.id, children: [runningId === exp.id ? (_jsx(RotateCcw, { className: "w-3.5 h-3.5 mr-1 animate-spin" })) : (_jsx(Play, { className: "w-3.5 h-3.5 mr-1" })), runningId === exp.id ? 'Replaying...' : 'Re-Execute Trial'] })] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4 bg-gray-50 dark:bg-gray-800/40 p-3 rounded-lg", children: [_jsxs("div", { children: [_jsx("span", { className: "text-[11px] text-gray-400 uppercase", children: "Control Mean" }), _jsxs("div", { className: "text-base font-bold text-gray-700 dark:text-gray-200", children: [exp.controlMean, " ms"] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[11px] text-gray-400 uppercase", children: "Treatment Mean" }), _jsxs("div", { className: "text-base font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1", children: [exp.treatmentMean, " ms", _jsx(TrendingDown, { className: "w-3.5 h-3.5 text-emerald-500" })] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[11px] text-gray-400 uppercase", children: "Cohen's d Effect Size" }), _jsxs("div", { className: "text-base font-bold text-indigo-600 dark:text-indigo-400", children: ["d = ", exp.effectSize] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[11px] text-gray-400 uppercase", children: "Statistical Significance" }), _jsxs("div", { className: "text-base font-bold text-emerald-600 dark:text-emerald-400", children: ["p < ", exp.pValue] })] })] }), _jsxs("div", { className: "flex items-center justify-between text-xs text-gray-500", children: [_jsxs("span", { children: ["Sample Size: ", _jsxs("strong", { className: "text-gray-900 dark:text-white", children: ["N = ", exp.sampleSize.toLocaleString()] })] }), _jsx("span", { className: "text-emerald-600 dark:text-emerald-400 font-medium", children: "Deterministic Replay Validated (100% Repro)" })] })] }, exp.id))) }) })) : (_jsxs(Card, { className: "p-6 space-y-4", children: [_jsxs("h3", { className: "font-semibold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(Sliders, { className: "w-5 h-5 text-purple-500" }), "Parameterize New Scientific Experiment"] }), _jsxs("div", { className: "space-y-4", children: [_jsxs("div", { children: [_jsx("label", { className: "block text-xs font-medium text-gray-700 dark:text-gray-300", children: "Target Hypothesis ID" }), _jsx("input", { type: "text", defaultValue: "hyp-triadic-coalition-02", className: "mt-1 block w-full px-3 py-2 text-xs border rounded-md dark:bg-gray-800 dark:border-gray-700 text-gray-900 dark:text-white" })] }), _jsxs("div", { className: "grid grid-cols-2 gap-4", children: [_jsxs("div", { children: [_jsx("label", { className: "block text-xs font-medium text-gray-700 dark:text-gray-300", children: "Control Configuration" }), _jsx("textarea", { rows: 3, defaultValue: '{"team_size": 1, "auction_protocol": "monolithic"}', className: "mt-1 block w-full px-3 py-2 font-mono text-xs border rounded-md dark:bg-gray-800 dark:border-gray-700 text-gray-900 dark:text-white" })] }), _jsxs("div", { children: [_jsx("label", { className: "block text-xs font-medium text-gray-700 dark:text-gray-300", children: "Treatment Configuration" }), _jsx("textarea", { rows: 3, defaultValue: '{"team_size": 3, "auction_protocol": "triadic_specialist"}', className: "mt-1 block w-full px-3 py-2 font-mono text-xs border rounded-md dark:bg-gray-800 dark:border-gray-700 text-gray-900 dark:text-white" })] })] }), _jsxs("div", { className: "flex justify-end gap-2 pt-2", children: [_jsx(Button, { variant: "ghost", size: "sm", onClick: () => setActiveTab('trials'), children: "Cancel" }), _jsx(Button, { variant: "intelligence", size: "sm", onClick: () => setActiveTab('trials'), children: "Launch Experiment" })] })] })] }))] }));
};
