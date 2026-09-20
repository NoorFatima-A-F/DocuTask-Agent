import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import { TestTube2, CheckCircle2, ShieldCheck, Zap, RefreshCw } from 'lucide-react';
export const TestingCenter = () => {
    const [testResult, setTestResult] = useState(null);
    const [running, setRunning] = useState(false);
    const executeTest = async () => {
        setRunning(true);
        const res = await AILifecycleApiClient.runTests('agt_acme_invoice_reconciler', '1.2.0');
        setTestResult(res);
        setRunning(false);
    };
    useEffect(() => {
        executeTest();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx(TestTube2, { className: "w-7 h-7 text-indigo-400" }), "AI Quality, Grounding & Performance Testing Harness"] }), _jsx("p", { className: "text-sm text-slate-400 mt-1", children: "Automated LLM Judge evaluation for factual grounding, hallucination scoring, and latency assertions." })] }), _jsx(Button, { variant: "intelligence", onClick: executeTest, disabled: running, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${running ? 'animate-spin' : ''}` }), " Run Test Suite"] }) })] }), testResult && (_jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4", children: [_jsx(Card, { className: "bg-slate-900/80 border-slate-800", children: _jsxs(CardContent, { className: "p-4 flex items-center gap-3", children: [_jsx(CheckCircle2, { className: "w-6 h-6 text-emerald-400" }), _jsxs("div", { children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "Grounding Score" }), _jsxs("span", { className: "text-xl font-bold text-white", children: [(testResult.grounding_score * 100).toFixed(1), "%"] })] })] }) }), _jsx(Card, { className: "bg-slate-900/80 border-slate-800", children: _jsxs(CardContent, { className: "p-4 flex items-center gap-3", children: [_jsx(ShieldCheck, { className: "w-6 h-6 text-indigo-400" }), _jsxs("div", { children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "Hallucination Rate" }), _jsxs("span", { className: "text-xl font-bold text-emerald-400", children: [testResult.hallucination_rate_pct, "%"] })] })] }) }), _jsx(Card, { className: "bg-slate-900/80 border-slate-800", children: _jsxs(CardContent, { className: "p-4 flex items-center gap-3", children: [_jsx(Zap, { className: "w-6 h-6 text-amber-400" }), _jsxs("div", { children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "P95 Latency" }), _jsxs("span", { className: "text-xl font-bold text-white", children: [testResult.latency_p95_ms, " ms"] })] })] }) }), _jsx(Card, { className: "bg-slate-900/80 border-slate-800", children: _jsxs(CardContent, { className: "p-4 flex items-center gap-3", children: [_jsx(CheckCircle2, { className: "w-6 h-6 text-cyan-400" }), _jsxs("div", { children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "Overall Status" }), _jsx(Badge, { variant: "success", className: "mt-1", children: testResult.status })] })] }) })] }))] }));
};
