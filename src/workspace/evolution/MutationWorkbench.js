import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { GitPullRequest, FileCode, ShieldCheck, PlusCircle, RefreshCw, Copy, Check, Lock, } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
export const MutationWorkbench = () => {
    const [proposals, setProposals] = useState([]);
    const [selectedProposal, setSelectedProposal] = useState(null);
    const [loading, setLoading] = useState(true);
    const [copied, setCopied] = useState(false);
    const [showModal, setShowModal] = useState(false);
    // Form
    const [title, setTitle] = useState('');
    const [mutationType, setMutationType] = useState('PLANNER_REDESIGN');
    const [targetComponent, setTargetComponent] = useState('swarm_planner');
    const [diffSpec, setDiffSpec] = useState('--- a/module.py\n+++ b/module.py\n-serial_call()\n+await parallel_task_group()');
    const [rationale, setRationale] = useState('');
    useEffect(() => {
        loadProposals();
    }, []);
    const loadProposals = async () => {
        setLoading(true);
        try {
            const data = await EvolutionPlatformApiClient.listMutations();
            setProposals(data);
            if (data.length > 0 && data[0]) {
                setSelectedProposal(data[0]);
            }
        }
        catch (err) {
            console.error('Failed to load mutations:', err);
        }
        finally {
            setLoading(false);
        }
    };
    const handlePropose = async (e) => {
        e.preventDefault();
        if (!title.trim())
            return;
        try {
            const mut = await EvolutionPlatformApiClient.proposeMutation({
                title,
                mutation_type: mutationType,
                target_components: [targetComponent],
                code_diff_spec: diffSpec,
                rationale: rationale || 'Automated performance refactoring.',
            });
            setProposals((prev) => [mut, ...prev]);
            setSelectedProposal(mut);
            setShowModal(false);
            setTitle('');
            setRationale('');
        }
        catch (err) {
            console.error('Failed to propose mutation:', err);
        }
    };
    const copyHash = (hash) => {
        navigator.clipboard.writeText(hash);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-indigo-500/10 border border-indigo-500/20 rounded-xl", children: _jsx(GitPullRequest, { className: "w-6 h-6 text-indigo-400" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-xl font-bold text-slate-100", children: "Self-Modification & Mutation Workbench" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "AST Invariant Synthesis" })] }), _jsx("p", { className: "text-sm text-slate-400 mt-0.5", children: "Inspect and synthesize non-destructive code mutations, AST rewrites, and cryptographic diff seals." })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: loadProposals, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: () => setShowModal(true), children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(PlusCircle, { className: "w-4 h-4" }), "Propose Mutation"] }) })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-sm font-semibold text-slate-200", children: "Active Mutation Proposals" }), _jsxs(Badge, { variant: "outline", size: "sm", children: [proposals.length, " Total"] })] }), _jsx("div", { className: "space-y-3", children: proposals.map((m) => (_jsxs("div", { onClick: () => setSelectedProposal(m), className: `p-4 rounded-xl border cursor-pointer transition-all ${selectedProposal?.mutation_id === m.mutation_id
                                        ? 'bg-indigo-950/40 border-indigo-500/50 shadow-md'
                                        : 'bg-slate-950/60 border-slate-800/80 hover:border-slate-700'}`, children: [_jsxs("div", { className: "flex items-center justify-between gap-2 mb-1.5", children: [_jsx("span", { className: "font-mono text-xs text-indigo-400 font-bold", children: m.mutation_id }), _jsx(Badge, { variant: m.status === 'APPROVED' ? 'success' : 'outline', size: "sm", children: m.status })] }), _jsx("h3", { className: "text-sm font-medium text-slate-200 leading-snug", children: m.title }), _jsxs("div", { className: "text-xs text-slate-400 mt-2 flex justify-between font-mono", children: [_jsx("span", { children: m.mutation_type }), _jsxs("span", { className: "text-emerald-400 font-bold", children: [(m.confidence_score * 100).toFixed(0), "% Conf"] })] })] }, m.mutation_id))) })] }), selectedProposal && (_jsx("div", { className: "lg:col-span-2 space-y-4", children: _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-3 pb-4 border-b border-slate-800", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h2", { className: "text-lg font-bold text-slate-100", children: selectedProposal.title }), _jsx(Badge, { variant: "info", size: "sm", children: selectedProposal.mutation_type })] }), _jsx("p", { className: "text-xs text-slate-400 mt-1", children: selectedProposal.rationale })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs("button", { onClick: () => copyHash(selectedProposal.sha256_hash), className: "flex items-center gap-1.5 text-xs font-mono text-slate-400 hover:text-slate-200 bg-slate-950 border border-slate-800 px-3 py-1.5 rounded-lg", children: [_jsx(Lock, { className: "w-3.5 h-3.5 text-purple-400" }), _jsxs("span", { className: "truncate max-w-[120px]", children: [selectedProposal.sha256_hash.substring(0, 16), "..."] }), copied ? _jsx(Check, { className: "w-3.5 h-3.5 text-emerald-400" }) : _jsx(Copy, { className: "w-3.5 h-3.5" })] }) })] }), _jsxs("div", { className: "p-4 bg-purple-950/30 border border-purple-500/20 rounded-xl space-y-1.5", children: [_jsxs("div", { className: "flex items-center gap-2 text-xs font-bold text-purple-300", children: [_jsx(ShieldCheck, { className: "w-4 h-4 text-purple-400" }), _jsx("span", { children: "Automated AST Safety & Invariant Verification" })] }), _jsx("p", { className: "text-xs text-slate-300 font-mono", children: selectedProposal.safety_analysis })] }), _jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex items-center gap-2 text-xs font-mono text-slate-400", children: [_jsx(FileCode, { className: "w-4 h-4 text-slate-400" }), _jsx("span", { children: "Synthesized Unified Code Diff" })] }), _jsx("pre", { className: "bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs font-mono text-slate-300 overflow-x-auto leading-relaxed", children: selectedProposal.code_diff_spec.split('\n').map((line, idx) => {
                                                const isAdd = line.startsWith('+');
                                                const isDel = line.startsWith('-');
                                                const isHeader = line.startsWith('@@') || line.startsWith('---') || line.startsWith('+++');
                                                return (_jsx("div", { className: isAdd
                                                        ? 'text-emerald-400 bg-emerald-950/30 px-1 rounded'
                                                        : isDel
                                                            ? 'text-rose-400 bg-rose-950/30 px-1 rounded'
                                                            : isHeader
                                                                ? 'text-indigo-400 font-bold'
                                                                : 'text-slate-400', children: line }, idx));
                                            }) })] })] }) }))] }), showModal && (_jsx("div", { className: "fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4", children: _jsxs("div", { className: "bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-lg w-full space-y-4 shadow-2xl", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("h3", { className: "text-lg font-bold text-slate-100", children: "Propose Architecture Mutation" }), _jsx("button", { onClick: () => setShowModal(false), className: "text-slate-400 hover:text-slate-200 text-sm font-semibold", children: "\u2715" })] }), _jsxs("form", { onSubmit: handlePropose, className: "space-y-4", children: [_jsxs("div", { children: [_jsx("label", { className: "text-xs font-medium text-slate-300 block mb-1", children: "Proposal Title" }), _jsx("input", { type: "text", value: title, onChange: (e) => setTitle(e.target.value), placeholder: "e.g. Async Concurrent Validator", className: "w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500", required: true })] }), _jsxs("div", { className: "grid grid-cols-2 gap-4", children: [_jsxs("div", { children: [_jsx("label", { className: "text-xs font-medium text-slate-300 block mb-1", children: "Mutation Type" }), _jsxs("select", { value: mutationType, onChange: (e) => setMutationType(e.target.value), className: "w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500", children: [_jsx("option", { value: "PLANNER_REDESIGN", children: "PLANNER_REDESIGN" }), _jsx("option", { value: "ROUTING_REFACTOR", children: "ROUTING_REFACTOR" }), _jsx("option", { value: "MODULE_REFACTORING", children: "MODULE_REFACTORING" }), _jsx("option", { value: "CACHE_REDESIGN", children: "CACHE_REDESIGN" })] })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs font-medium text-slate-300 block mb-1", children: "Target Component" }), _jsx("input", { type: "text", value: targetComponent, onChange: (e) => setTargetComponent(e.target.value), className: "w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500 font-mono" })] })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs font-medium text-slate-300 block mb-1", children: "Unified Diff Spec" }), _jsx("textarea", { value: diffSpec, onChange: (e) => setDiffSpec(e.target.value), rows: 4, className: "w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-slate-100 font-mono focus:outline-none focus:border-indigo-500" })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs font-medium text-slate-300 block mb-1", children: "Rationale" }), _jsx("input", { type: "text", value: rationale, onChange: (e) => setRationale(e.target.value), placeholder: "Why this refactor improves performance or safety...", className: "w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500" })] }), _jsxs("div", { className: "flex justify-end gap-3 pt-2", children: [_jsx(Button, { variant: "ghost", onClick: () => setShowModal(false), children: "Cancel" }), _jsx(Button, { variant: "intelligence", type: "submit", children: "Submit Mutation" })] })] })] }) }))] }));
};
