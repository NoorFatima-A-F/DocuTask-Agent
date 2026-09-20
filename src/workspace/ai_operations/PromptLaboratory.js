import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { FlaskConical, Sparkles, RefreshCw, FileCode, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';
export const PromptLaboratory = () => {
    const [prompts, setPrompts] = useState([]);
    const [selectedPrompt, setSelectedPrompt] = useState(null);
    const [loading, setLoading] = useState(true);
    const loadPrompts = async () => {
        try {
            setLoading(true);
            const data = await AIOperationsApiClient.getPrompts();
            setPrompts(data);
            if (data.length > 0 && !selectedPrompt) {
                setSelectedPrompt(data[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load prompts:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadPrompts();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-purple-500/10 rounded-xl border border-purple-500/20", children: _jsx(FlaskConical, { className: "w-6 h-6 text-purple-400" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-xl font-bold text-white", children: "Prompt Laboratory & Evolution" }), _jsx("p", { className: "text-xs text-slate-400", children: "Version control, automated mutations, few-shot tuning, and evaluation benchmarks" })] })] }), _jsx(Button, { variant: "outline", onClick: loadPrompts, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-12 gap-6", children: [_jsxs("div", { className: "lg:col-span-4 space-y-3", children: [_jsx("h2", { className: "text-xs font-semibold text-slate-400 uppercase tracking-wider px-1", children: "Prompt Versions" }), _jsx("div", { className: "space-y-2 max-h-[600px] overflow-y-auto pr-1", children: prompts.map((p) => (_jsxs(Card, { className: `p-3.5 cursor-pointer transition-all border ${selectedPrompt?.prompt_id === p.prompt_id
                                        ? 'bg-purple-950/30 border-purple-500/50 shadow-md shadow-purple-950/20'
                                        : 'bg-slate-900/40 border-slate-800/80 hover:bg-slate-800/40'}`, onClick: () => setSelectedPrompt(p), children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-semibold text-white text-xs", children: p.version }), _jsx(Badge, { variant: p.active ? 'success' : 'outline', children: p.active ? 'Active' : 'Candidate' })] }), _jsx("p", { className: "text-xs text-slate-400 mt-1 font-mono", children: p.agent_id }), _jsxs("div", { className: "flex items-center justify-between mt-2.5 text-[11px] text-slate-400 border-t border-slate-800/60 pt-2", children: [_jsxs("span", { children: ["Score: ", (p.average_score * 100).toFixed(0), "%"] }), _jsx("span", { className: "text-slate-500", children: new Date(p.created_at).toLocaleDateString() })] })] }, p.prompt_id))) })] }), _jsx("div", { className: "lg:col-span-8 space-y-4", children: selectedPrompt ? (_jsxs(Card, { className: "p-6 bg-slate-900/50 border-slate-800 space-y-5", children: [_jsxs("div", { className: "flex items-start justify-between border-b border-slate-800 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h2", { className: "text-lg font-bold text-white", children: selectedPrompt.version }), _jsx(Badge, { variant: selectedPrompt.active ? 'success' : 'outline', children: selectedPrompt.active ? 'Production Active' : 'Offline Version' })] }), _jsxs("p", { className: "text-xs text-slate-400 font-mono mt-0.5", children: ["Target: ", selectedPrompt.agent_id, " \u2022 ID: ", selectedPrompt.prompt_id] })] }), _jsxs("div", { className: "text-right", children: [_jsxs("span", { className: "text-2xl font-bold text-purple-400", children: [(selectedPrompt.average_score * 100).toFixed(1), "%"] }), _jsx("p", { className: "text-[11px] text-slate-400", children: "Benchmark Rating" })] })] }), _jsxs("div", { children: [_jsxs("h4", { className: "text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5", children: [_jsx(FileCode, { className: "w-3.5 h-3.5 text-purple-400" }), " System Instruction"] }), _jsx("div", { className: "p-4 bg-slate-950/80 rounded-xl border border-slate-800 font-mono text-xs text-slate-300 whitespace-pre-wrap leading-relaxed", children: selectedPrompt.system_instruction })] }), selectedPrompt.mutation_notes && (_jsxs("div", { className: "p-4 bg-purple-950/20 border border-purple-500/20 rounded-xl", children: [_jsxs("h4", { className: "text-xs font-semibold text-purple-300 mb-1 flex items-center gap-1.5", children: [_jsx(Sparkles, { className: "w-3.5 h-3.5 text-purple-400" }), " Optimization & Mutation Rationale"] }), _jsx("p", { className: "text-xs text-slate-300", children: selectedPrompt.mutation_notes })] }))] })) : (_jsxs(Card, { className: "p-8 text-center text-slate-400 bg-slate-900/40 border-slate-800", children: [_jsx(FlaskConical, { className: "w-8 h-8 text-slate-600 mx-auto mb-2" }), _jsx("p", { children: "Select a prompt version to inspect and refine system instructions." })] })) })] })] }));
};
