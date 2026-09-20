import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Sparkles, CheckCircle, XCircle, ShieldAlert, GitPullRequest, RefreshCw, TrendingUp, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';
export const ImprovementStudio = () => {
    const [proposals, setProposals] = useState([]);
    const [selectedProposal, setSelectedProposal] = useState(null);
    const [loading, setLoading] = useState(true);
    const [actionInProgress, setActionInProgress] = useState(false);
    const loadProposals = async () => {
        try {
            setLoading(true);
            const data = await AIOperationsApiClient.getProposals();
            setProposals(data);
            if (data.length > 0 && !selectedProposal) {
                setSelectedProposal(data[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load improvement proposals:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadProposals();
    }, []);
    const handleApprove = async (propId) => {
        try {
            setActionInProgress(true);
            const updated = await AIOperationsApiClient.approveProposal(propId);
            setSelectedProposal(updated);
            await loadProposals();
        }
        catch (err) {
            console.error('Failed to approve proposal:', err);
        }
        finally {
            setActionInProgress(false);
        }
    };
    const handleReject = async (propId) => {
        try {
            setActionInProgress(true);
            const updated = await AIOperationsApiClient.rejectProposal(propId);
            setSelectedProposal(updated);
            await loadProposals();
        }
        catch (err) {
            console.error('Failed to reject proposal:', err);
        }
        finally {
            setActionInProgress(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-indigo-500/10 rounded-xl border border-indigo-500/20", children: _jsx(Sparkles, { className: "w-6 h-6 text-indigo-400" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-xl font-bold text-white", children: "Controlled Self-Improvement Studio" }), _jsx("p", { className: "text-xs text-slate-400", children: "AI proposes optimizations \u2022 Canary validates \u2022 Human approval gates production deployment" })] })] }), _jsx(Button, { variant: "outline", onClick: loadProposals, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-12 gap-6", children: [_jsxs("div", { className: "lg:col-span-4 space-y-3", children: [_jsx("h2", { className: "text-xs font-semibold text-slate-400 uppercase tracking-wider px-1", children: "Improvement Proposals" }), _jsx("div", { className: "space-y-2 max-h-[600px] overflow-y-auto pr-1", children: proposals.map((p) => (_jsxs(Card, { className: `p-3.5 cursor-pointer transition-all border ${selectedProposal?.proposal_id === p.proposal_id
                                        ? 'bg-indigo-950/30 border-indigo-500/50 shadow-md shadow-indigo-950/20'
                                        : 'bg-slate-900/40 border-slate-800/80 hover:bg-slate-800/40'}`, onClick: () => setSelectedProposal(p), children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-semibold text-white text-xs", children: p.target_agent_id }), _jsx(Badge, { variant: p.status === 'APPROVED' || p.status === 'DEPLOYED'
                                                        ? 'success'
                                                        : p.status === 'REJECTED'
                                                            ? 'error'
                                                            : 'warning', children: p.status })] }), _jsx("h3", { className: "font-medium text-slate-200 text-xs mt-1.5 line-clamp-2", children: p.title }), _jsxs("div", { className: "flex items-center justify-between mt-2.5 text-[11px] text-slate-400 border-t border-slate-800/60 pt-2", children: [_jsxs("span", { className: "text-emerald-400 font-semibold", children: ["+", (p.expected_quality_delta * 100).toFixed(0), "% Quality"] }), _jsx("span", { className: "text-slate-500", children: new Date(p.created_at).toLocaleDateString() })] })] }, p.proposal_id))) })] }), _jsx("div", { className: "lg:col-span-8 space-y-4", children: selectedProposal ? (_jsxs(Card, { className: "p-6 bg-slate-900/50 border-slate-800 space-y-5", children: [_jsxs("div", { className: "flex items-start justify-between border-b border-slate-800 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "intelligence", children: selectedProposal.proposal_type }), _jsx("h2", { className: "text-lg font-bold text-white", children: selectedProposal.title })] }), _jsxs("p", { className: "text-xs text-slate-400 font-mono mt-0.5", children: ["Target: ", selectedProposal.target_agent_id, " \u2022 Proposal ID: ", selectedProposal.proposal_id] })] }), _jsx(Badge, { variant: selectedProposal.status === 'APPROVED' || selectedProposal.status === 'DEPLOYED'
                                                ? 'success'
                                                : selectedProposal.status === 'REJECTED'
                                                    ? 'error'
                                                    : 'warning', children: selectedProposal.status })] }), _jsx("p", { className: "text-sm text-slate-300 leading-relaxed", children: selectedProposal.description }), _jsxs("div", { className: "grid grid-cols-3 gap-3", children: [_jsxs("div", { className: "p-3 bg-slate-950/60 rounded-xl border border-slate-800/60", children: [_jsxs("span", { className: "text-xs text-slate-400 flex items-center gap-1", children: [_jsx(TrendingUp, { className: "w-3.5 h-3.5 text-emerald-400" }), " Quality Delta"] }), _jsxs("p", { className: "text-lg font-bold text-emerald-400 mt-1", children: ["+", (selectedProposal.expected_quality_delta * 100).toFixed(1), "%"] })] }), _jsxs("div", { className: "p-3 bg-slate-950/60 rounded-xl border border-slate-800/60", children: [_jsxs("span", { className: "text-xs text-slate-400 flex items-center gap-1", children: [_jsx(TrendingUp, { className: "w-3.5 h-3.5 text-cyan-400" }), " Latency Delta"] }), _jsxs("p", { className: "text-lg font-bold text-cyan-300 mt-1", children: [selectedProposal.expected_latency_delta_ms, " ms"] })] }), _jsxs("div", { className: "p-3 bg-slate-950/60 rounded-xl border border-slate-800/60", children: [_jsxs("span", { className: "text-xs text-slate-400 flex items-center gap-1", children: [_jsx(TrendingUp, { className: "w-3.5 h-3.5 text-indigo-400" }), " Cost Delta"] }), _jsxs("p", { className: "text-lg font-bold text-indigo-300 mt-1", children: [selectedProposal.expected_cost_delta_pct, "%"] })] })] }), _jsxs("div", { children: [_jsxs("h4", { className: "text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5", children: [_jsx(GitPullRequest, { className: "w-3.5 h-3.5 text-indigo-400" }), " Change Diff Summary"] }), _jsx("div", { className: "p-4 bg-slate-950/80 rounded-xl border border-slate-800 font-mono text-xs text-emerald-400 whitespace-pre-wrap leading-relaxed", children: selectedProposal.diff_summary })] }), selectedProposal.status === 'PENDING_HITL_APPROVAL' && (_jsxs("div", { className: "p-4 bg-amber-950/20 border border-amber-500/30 rounded-xl space-y-3", children: [_jsxs("div", { className: "flex items-center gap-2 text-amber-300 text-xs font-semibold", children: [_jsx(ShieldAlert, { className: "w-4 h-4" }), " Human-in-the-Loop Governance Gate Required"] }), _jsx("p", { className: "text-xs text-slate-300", children: "This modification has passed canary validation ($p < 0.05$). Confirm deployment to production fleet." }), _jsxs("div", { className: "flex items-center gap-3 pt-1", children: [_jsx(Button, { variant: "intelligence", onClick: () => handleApprove(selectedProposal.proposal_id), disabled: actionInProgress, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(CheckCircle, { className: "w-4 h-4" }), "Approve & Deploy"] }) }), _jsx(Button, { variant: "danger", onClick: () => handleReject(selectedProposal.proposal_id), disabled: actionInProgress, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(XCircle, { className: "w-4 h-4" }), "Reject Proposal"] }) })] })] }))] })) : (_jsxs(Card, { className: "p-8 text-center text-slate-400 bg-slate-900/40 border-slate-800", children: [_jsx(Sparkles, { className: "w-8 h-8 text-slate-600 mx-auto mb-2" }), _jsx("p", { children: "Select an improvement proposal to review diffs and execute human approval decisions." })] })) })] })] }));
};
