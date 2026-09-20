import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Cpu, Sparkles, Code } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { knowledgeApiClient } from '../../services/knowledgeApiClient';
export const ContextDebugger = () => {
    const [goal, setGoal] = useState('Reconcile invoice #INV-99014 exceeding $50k purchase order threshold');
    const [contextData, setContextData] = useState(null);
    const [loading, setLoading] = useState(false);
    const handleRetrieveContext = async () => {
        setLoading(true);
        try {
            const res = await knowledgeApiClient.retrieveContext(goal);
            setContextData(res);
        }
        finally {
            setLoading(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Cpu, { className: "w-7 h-7 text-indigo-400" }), "Agent Context Engineering & Budget Debugger"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Inspect the complete retrieval \u2192 rerank \u2192 compression \u2192 prompt injection pipeline." })] }), _jsx(Card, { className: "p-5 bg-slate-900/60 border-slate-800 space-y-4", children: _jsxs("div", { className: "flex gap-3", children: [_jsx("input", { value: goal, onChange: (e) => setGoal(e.target.value), placeholder: "Agent goal or execution prompt...", className: "flex-1 px-3 py-2 bg-slate-800/80 border border-slate-700 rounded-lg text-slate-200 text-sm focus:outline-none focus:border-indigo-500" }), _jsx(Button, { variant: "intelligence", onClick: handleRetrieveContext, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4" }), loading ? 'Assembling...' : 'Assemble Context'] }) })] }) }), contextData && (_jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-2 gap-6", children: [_jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 space-y-4", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsx("h2", { className: "text-base font-semibold text-slate-200", children: "Assembled Context Metrics" }), _jsxs(Badge, { variant: "success", children: ["Compression: ", contextData.compression_ratio, "x"] })] }), _jsxs("div", { className: "space-y-2 text-xs text-slate-300", children: [_jsxs("div", { className: "p-3 bg-slate-800/40 rounded border border-slate-700 flex justify-between", children: [_jsx("span", { children: "Estimated Prompt Tokens:" }), _jsxs("span", { className: "font-mono text-cyan-400", children: [contextData.total_tokens_estimated, " tokens"] })] }), _jsxs("div", { className: "p-3 bg-slate-800/40 rounded border border-slate-700 flex justify-between", children: [_jsx("span", { children: "Retrieval Latency:" }), _jsxs("span", { className: "font-mono text-emerald-400", children: [contextData.retrieval_latency_ms, " ms"] })] })] }), _jsxs("div", { children: [_jsx("h3", { className: "text-sm font-semibold text-slate-300 mb-2", children: "Graph Ontology Injected" }), contextData.graph_context.map((g, i) => (_jsx("p", { className: "text-xs bg-slate-800/60 p-2 rounded text-cyan-300 font-mono mb-1", children: g }, i)))] }), _jsxs("div", { children: [_jsx("h3", { className: "text-sm font-semibold text-slate-300 mb-2", children: "Procedural Memories Injected" }), contextData.memory_context.map((m, i) => (_jsx("p", { className: "text-xs bg-slate-800/60 p-2 rounded text-indigo-300 font-mono mb-1", children: m }, i)))] })] }), _jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 space-y-3", children: [_jsxs("h2", { className: "text-base font-semibold text-slate-200 flex items-center gap-2", children: [_jsx(Code, { className: "w-4 h-4 text-emerald-400" }), "Final Prompt Injected into Autonomous Agent"] }), _jsx("pre", { className: "text-xs font-mono text-slate-300 bg-slate-950 p-4 rounded-lg border border-slate-800 overflow-x-auto whitespace-pre-wrap max-h-[460px]", children: contextData.optimized_context_prompt })] })] }))] }));
};
