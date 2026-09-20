import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { AlertTriangle, Bug, Wrench, RefreshCw, Clock, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';
export const FailureAnalysisStudio = () => {
    const [failures, setFailures] = useState([]);
    const [selectedFailure, setSelectedFailure] = useState(null);
    const [loading, setLoading] = useState(true);
    const loadFailures = async () => {
        try {
            setLoading(true);
            const data = await AIOperationsApiClient.getFailureDiagnoses(50);
            setFailures(data);
            if (data.length > 0 && !selectedFailure) {
                setSelectedFailure(data[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load failure diagnoses:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadFailures();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-rose-500/10 rounded-xl border border-rose-500/20", children: _jsx(Bug, { className: "w-6 h-6 text-rose-400" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-xl font-bold text-white", children: "Failure Analysis & Root-Cause Studio" }), _jsx("p", { className: "text-xs text-slate-400", children: "Automated failure categorization, critical path bottlenecks, and AI remediation plans" })] })] }), _jsx(Button, { variant: "outline", onClick: loadFailures, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-12 gap-6", children: [_jsxs("div", { className: "lg:col-span-4 space-y-3", children: [_jsx("h2", { className: "text-xs font-semibold text-slate-400 uppercase tracking-wider px-1", children: "Diagnosed Failure Incidents" }), _jsx("div", { className: "space-y-2 max-h-[600px] overflow-y-auto pr-1", children: failures.map((f) => (_jsxs(Card, { className: `p-3.5 cursor-pointer transition-all border ${selectedFailure?.analysis_id === f.analysis_id
                                        ? 'bg-rose-950/30 border-rose-500/50 shadow-md shadow-rose-950/20'
                                        : 'bg-slate-900/40 border-slate-800/80 hover:bg-slate-800/40'}`, onClick: () => setSelectedFailure(f), children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-semibold text-white text-xs", children: f.agent_id }), _jsx(Badge, { variant: "error", children: f.category })] }), _jsx("p", { className: "text-xs text-slate-400 mt-1 line-clamp-2", children: f.root_cause_summary }), _jsxs("div", { className: "flex items-center justify-between mt-2.5 text-[11px] text-slate-500 border-t border-slate-800/60 pt-2", children: [_jsxs("span", { children: ["Confidence: ", (f.confidence * 100).toFixed(0), "%"] }), _jsx("span", { children: new Date(f.timestamp).toLocaleTimeString() })] })] }, f.analysis_id))) })] }), _jsx("div", { className: "lg:col-span-8 space-y-4", children: selectedFailure ? (_jsxs(Card, { className: "p-6 bg-slate-900/50 border-slate-800 space-y-5", children: [_jsxs("div", { className: "flex items-start justify-between border-b border-slate-800 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "error", children: selectedFailure.category }), _jsx("h2", { className: "text-base font-bold text-white", children: selectedFailure.agent_id })] }), _jsxs("p", { className: "text-xs text-slate-400 font-mono mt-0.5", children: ["Analysis ID: ", selectedFailure.analysis_id, " \u2022 Trace: ", selectedFailure.trace_id] })] }), _jsxs(Badge, { variant: "intelligence", children: [(selectedFailure.confidence * 100).toFixed(0), "% Diagnostic Match"] })] }), _jsxs("div", { className: "p-4 bg-slate-950/80 rounded-xl border border-slate-800", children: [_jsxs("h4", { className: "text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1 flex items-center gap-1.5", children: [_jsx(AlertTriangle, { className: "w-3.5 h-3.5 text-rose-400" }), " Root Cause Diagnosis"] }), _jsx("p", { className: "text-sm text-slate-200 leading-relaxed", children: selectedFailure.root_cause_summary })] }), _jsxs("div", { children: [_jsxs("h4", { className: "text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5", children: [_jsx(Clock, { className: "w-3.5 h-3.5 text-cyan-400" }), " Critical Path Execution Tree"] }), _jsx("div", { className: "space-y-1.5", children: selectedFailure.critical_path.map((step, idx) => (_jsxs("div", { className: "p-2.5 bg-slate-950/60 rounded-lg border border-slate-800/80 text-xs text-slate-300 font-mono flex items-center gap-2", children: [_jsxs("span", { className: "text-slate-500 font-semibold", children: [idx + 1, "."] }), _jsx("span", { children: step })] }, idx))) })] }), _jsxs("div", { className: "p-4 bg-emerald-950/20 border border-emerald-500/20 rounded-xl", children: [_jsxs("h4", { className: "text-xs font-semibold text-emerald-300 mb-1 flex items-center gap-1.5", children: [_jsx(Wrench, { className: "w-3.5 h-3.5 text-emerald-400" }), " Recommended AI Remediation"] }), _jsx("p", { className: "text-xs text-slate-200 leading-relaxed", children: selectedFailure.suggested_remediation })] })] })) : (_jsxs(Card, { className: "p-8 text-center text-slate-400 bg-slate-900/40 border-slate-800", children: [_jsx(Bug, { className: "w-8 h-8 text-slate-600 mx-auto mb-2" }), _jsx("p", { children: "Select a failure diagnosis to inspect root causes and remediation recommendations." })] })) })] })] }));
};
