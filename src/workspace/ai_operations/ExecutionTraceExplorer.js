import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { ListTree, Clock, Zap, CheckCircle, XCircle, Code, Search, RefreshCw, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';
export const ExecutionTraceExplorer = () => {
    const [traces, setTraces] = useState([]);
    const [selectedTrace, setSelectedTrace] = useState(null);
    const [selectedSpan, setSelectedSpan] = useState(null);
    const [loading, setLoading] = useState(true);
    const [filterQuery, setFilterQuery] = useState('');
    const loadTraces = async () => {
        try {
            setLoading(true);
            const data = await AIOperationsApiClient.getTraces(50);
            setTraces(data);
            const first = data[0];
            if (first && !selectedTrace) {
                setSelectedTrace(first);
                if (first.spans && first.spans.length > 0) {
                    setSelectedSpan(first.spans[0] || null);
                }
            }
        }
        catch (err) {
            console.error('Failed to load traces:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadTraces();
    }, []);
    const handleSelectTrace = (trace) => {
        setSelectedTrace(trace);
        if (trace.spans && trace.spans.length > 0) {
            setSelectedSpan(trace.spans[0] || null);
        }
        else {
            setSelectedSpan(null);
        }
    };
    const filteredTraces = traces.filter((t) => t.root_span_name.toLowerCase().includes(filterQuery.toLowerCase()) ||
        t.agent_id.toLowerCase().includes(filterQuery.toLowerCase()) ||
        t.trace_id.toLowerCase().includes(filterQuery.toLowerCase()));
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-indigo-500/10 rounded-xl border border-indigo-500/20", children: _jsx(ListTree, { className: "w-6 h-6 text-indigo-400" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-xl font-bold text-white", children: "Execution Trace Explorer" }), _jsx("p", { className: "text-xs text-slate-400", children: "OpenTelemetry span waterfall, reasoning latency, and token breakdowns" })] })] }), _jsx(Button, { variant: "outline", onClick: loadTraces, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-12 gap-6", children: [_jsxs("div", { className: "lg:col-span-4 space-y-3", children: [_jsxs("div", { className: "relative", children: [_jsx(Search, { className: "w-4 h-4 absolute left-3 top-3 text-slate-500" }), _jsx("input", { type: "text", placeholder: "Filter by agent, trace ID, or name...", className: "w-full bg-slate-900/60 border border-slate-800 rounded-xl pl-9 pr-4 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500", value: filterQuery, onChange: (e) => setFilterQuery(e.target.value) })] }), _jsx("div", { className: "space-y-2 max-h-[600px] overflow-y-auto pr-1", children: filteredTraces.map((trace) => (_jsxs(Card, { className: `p-3.5 cursor-pointer transition-all border ${selectedTrace?.trace_id === trace.trace_id
                                        ? 'bg-indigo-950/30 border-indigo-500/50 shadow-md shadow-indigo-950/20'
                                        : 'bg-slate-900/40 border-slate-800/80 hover:bg-slate-800/40'}`, onClick: () => handleSelectTrace(trace), children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [trace.status === 'OK' ? (_jsx(CheckCircle, { className: "w-4 h-4 text-emerald-400 flex-shrink-0" })) : (_jsx(XCircle, { className: "w-4 h-4 text-rose-400 flex-shrink-0" })), _jsx("h3", { className: "font-semibold text-white text-xs line-clamp-1", children: trace.root_span_name })] }), _jsx(Badge, { variant: trace.status === 'OK' ? 'success' : 'error', children: trace.status })] }), _jsxs("div", { className: "flex items-center justify-between mt-2.5 text-[11px] text-slate-400", children: [_jsx("span", { className: "font-mono", children: trace.agent_id }), _jsxs("span", { className: "flex items-center gap-1 font-semibold text-slate-300", children: [_jsx(Clock, { className: "w-3 h-3 text-cyan-400" }), trace.total_duration_ms.toFixed(1), " ms"] })] })] }, trace.trace_id))) })] }), _jsx("div", { className: "lg:col-span-8 space-y-4", children: selectedTrace ? (_jsx(_Fragment, { children: _jsxs(Card, { className: "p-5 bg-slate-900/50 border-slate-800", children: [_jsxs("div", { className: "flex items-start justify-between border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsx("h2", { className: "text-base font-bold text-white", children: selectedTrace.root_span_name }), _jsxs("p", { className: "text-xs text-slate-400 font-mono mt-0.5", children: ["Trace ID: ", selectedTrace.trace_id, " \u2022 Session: ", selectedTrace.session_id] })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Badge, { variant: "intelligence", children: [_jsx(Zap, { className: "w-3 h-3 inline mr-1 text-amber-400" }), selectedTrace.total_prompt_tokens + selectedTrace.total_completion_tokens, " Tokens"] }), _jsxs(Badge, { variant: "default", children: ["$", selectedTrace.total_cost_usd.toFixed(4)] })] })] }), _jsxs("div", { className: "mt-4 space-y-2", children: [_jsx("h4", { className: "text-xs font-semibold text-slate-400 uppercase tracking-wider", children: "Span Waterfall" }), _jsx("div", { className: "space-y-1.5", children: selectedTrace.spans.map((span) => {
                                                    const pct = Math.max(8, Math.min(100, (span.duration_ms / Math.max(1, selectedTrace.total_duration_ms)) * 100));
                                                    const isSelected = selectedSpan?.span_id === span.span_id;
                                                    return (_jsxs("div", { className: `p-2.5 rounded-xl border cursor-pointer transition-all ${isSelected
                                                            ? 'bg-slate-800/80 border-indigo-500'
                                                            : 'bg-slate-950/40 border-slate-800/60 hover:bg-slate-800/40'}`, onClick: () => setSelectedSpan(span), children: [_jsxs("div", { className: "flex items-center justify-between text-xs mb-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: span.span_type === 'LLM_CALL' ? 'intelligence' : 'outline', children: span.span_type }), _jsx("span", { className: "font-medium text-white", children: span.name })] }), _jsxs("span", { className: "text-slate-300 font-mono", children: [span.duration_ms.toFixed(1), " ms"] })] }), _jsx("div", { className: "w-full bg-slate-900 h-1.5 rounded-full overflow-hidden", children: _jsx("div", { className: `h-full rounded-full ${span.status === 'ERROR'
                                                                        ? 'bg-rose-500'
                                                                        : span.span_type === 'LLM_CALL'
                                                                            ? 'bg-indigo-500'
                                                                            : 'bg-cyan-500'}`, style: { width: `${pct}%` } }) })] }, span.span_id));
                                                }) })] }), selectedSpan && (_jsxs("div", { className: "mt-5 border-t border-slate-800 pt-4 space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("h4", { className: "text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5", children: [_jsx(Code, { className: "w-3.5 h-3.5 text-indigo-400" }), " Span Inspector (", selectedSpan.name, ")"] }), _jsx(Badge, { variant: selectedSpan.status === 'OK' ? 'success' : 'error', children: selectedSpan.status })] }), _jsxs("div", { className: "grid grid-cols-2 gap-3 text-xs bg-slate-950/60 p-3 rounded-xl border border-slate-800/80", children: [_jsxs("div", { children: [_jsx("span", { className: "text-slate-500", children: "Span ID:" }), ' ', _jsx("span", { className: "font-mono text-slate-300", children: selectedSpan.span_id })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500", children: "Duration:" }), ' ', _jsxs("span", { className: "font-mono text-slate-300", children: [selectedSpan.duration_ms.toFixed(1), " ms"] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500", children: "Token Usage:" }), ' ', _jsxs("span", { className: "font-mono text-slate-300", children: [selectedSpan.token_usage?.total_tokens ?? 0, " (", selectedSpan.token_usage?.prompt_tokens ?? 0, " prompt / ", selectedSpan.token_usage?.completion_tokens ?? 0, " comp)"] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500", children: "Cost:" }), ' ', _jsxs("span", { className: "font-mono text-slate-300", children: ["$", selectedSpan.cost_usd.toFixed(5)] })] })] }), selectedSpan.error_message && (_jsxs("div", { className: "p-3 bg-rose-950/30 border border-rose-500/30 rounded-xl text-xs text-rose-300", children: [_jsx("strong", { children: "Error:" }), " ", selectedSpan.error_message] }))] }))] }) })) : (_jsxs(Card, { className: "p-8 text-center text-slate-400 bg-slate-900/40 border-slate-800", children: [_jsx(ListTree, { className: "w-8 h-8 text-slate-600 mx-auto mb-2" }), _jsx("p", { children: "Select an execution trace to inspect the distributed span call tree." })] })) })] })] }));
};
