import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { ShieldCheck, CheckCircle, XCircle, Lock, RefreshCw, Database, FileCheck, } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
export const GovernanceApprovalCenter = () => {
    const [reviews, setReviews] = useState([]);
    const [snapshots, setSnapshots] = useState([]);
    const [loading, setLoading] = useState(true);
    const [actionLoading, setActionLoading] = useState(null);
    useEffect(() => {
        loadData();
    }, []);
    const loadData = async () => {
        setLoading(true);
        try {
            const [revData, snapData] = await Promise.all([
                EvolutionPlatformApiClient.listGovernanceReviews(),
                EvolutionPlatformApiClient.listRollbackSnapshots(),
            ]);
            setReviews(revData);
            setSnapshots(snapData);
        }
        catch (err) {
            console.error('Failed to load governance data:', err);
        }
        finally {
            setLoading(false);
        }
    };
    const handleApprove = async (reviewId) => {
        setActionLoading(reviewId);
        try {
            const updated = await EvolutionPlatformApiClient.approveReview(reviewId);
            setReviews((prev) => prev.map((r) => (r.review_id === reviewId ? updated : r)));
        }
        catch (err) {
            console.error('Approval failed:', err);
        }
        finally {
            setActionLoading(null);
        }
    };
    const handleReject = async (reviewId) => {
        setActionLoading(reviewId);
        try {
            const updated = await EvolutionPlatformApiClient.rejectReview(reviewId, 'Rejected by operator');
            setReviews((prev) => prev.map((r) => (r.review_id === reviewId ? updated : r)));
        }
        catch (err) {
            console.error('Rejection failed:', err);
        }
        finally {
            setActionLoading(null);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-purple-500/10 border border-purple-500/20 rounded-xl", children: _jsx(ShieldCheck, { className: "w-6 h-6 text-purple-400" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-xl font-bold text-slate-100", children: "Cryptographic Governance & Rollback Center" }), _jsx(Badge, { variant: "sentinel", size: "sm", children: "Zero-Risk Gatekeeper" })] }), _jsx("p", { className: "text-sm text-slate-400 mt-0.5", children: "Enforces multi-stage verification gates, cryptographic SHA-256 rollback snapshots, and policy compliance." })] })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsx(Button, { variant: "outline", onClick: loadData, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "lg:col-span-2 bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(FileCheck, { className: "w-5 h-5 text-purple-400" }), _jsx("h2", { className: "text-base font-semibold text-slate-100", children: "Governance Review Gates" })] }), _jsxs(Badge, { variant: "outline", size: "sm", children: [reviews.length, " Active Reviews"] })] }), _jsx("div", { className: "space-y-4", children: reviews.map((r) => (_jsxs("div", { className: "bg-slate-950/60 border border-slate-800/80 rounded-xl p-5 space-y-4 hover:border-slate-700 transition-all", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-2 pb-3 border-b border-slate-800/80", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-sm font-bold text-purple-400", children: r.review_id }), _jsx(Badge, { variant: r.approval_status === 'APPROVED'
                                                                        ? 'success'
                                                                        : r.approval_status === 'REJECTED'
                                                                            ? 'error'
                                                                            : 'warning', size: "sm", children: r.approval_status })] }), _jsxs("span", { className: "text-xs text-slate-400 font-mono mt-0.5 block", children: ["Target Mutation: ", _jsx("span", { className: "text-slate-200", children: r.mutation_id }), " \u2022 Reviewer: ", r.reviewer_agent_id] })] }), r.approval_status === 'PENDING' && (_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Button, { variant: "danger", size: "sm", onClick: () => handleReject(r.review_id), disabled: actionLoading === r.review_id, children: _jsxs("span", { className: "flex items-center gap-1.5", children: [_jsx(XCircle, { className: "w-3.5 h-3.5" }), "Reject"] }) }), _jsx(Button, { variant: "intelligence", size: "sm", onClick: () => handleApprove(r.review_id), disabled: actionLoading === r.review_id, children: _jsxs("span", { className: "flex items-center gap-1.5", children: [_jsx(CheckCircle, { className: "w-3.5 h-3.5" }), "Approve & Seal"] }) })] }))] }), _jsxs("div", { className: "grid grid-cols-3 gap-3 text-xs font-mono", children: [_jsxs("div", { className: "p-2.5 bg-slate-900 border border-slate-800 rounded-lg flex items-center gap-2", children: [_jsx(CheckCircle, { className: "w-4 h-4 text-emerald-400 flex-shrink-0" }), _jsxs("div", { children: [_jsx("div", { className: "text-slate-400 text-[10px]", children: "FORMAL VERIFICATION" }), _jsx("div", { className: "text-slate-200 font-semibold", children: r.formal_verification_passed ? 'PASSED' : 'FAILED' })] })] }), _jsxs("div", { className: "p-2.5 bg-slate-900 border border-slate-800 rounded-lg flex items-center gap-2", children: [_jsx(CheckCircle, { className: "w-4 h-4 text-emerald-400 flex-shrink-0" }), _jsxs("div", { children: [_jsx("div", { className: "text-slate-400 text-[10px]", children: "SHADOW SIMULATION" }), _jsx("div", { className: "text-slate-200 font-semibold", children: r.simulation_verified ? 'VERIFIED' : 'PENDING' })] })] }), _jsxs("div", { className: "p-2.5 bg-slate-900 border border-slate-800 rounded-lg flex items-center gap-2", children: [_jsx(CheckCircle, { className: "w-4 h-4 text-emerald-400 flex-shrink-0" }), _jsxs("div", { children: [_jsx("div", { className: "text-slate-400 text-[10px]", children: "BENCHMARK PROOF" }), _jsx("div", { className: "text-slate-200 font-semibold", children: r.benchmark_verified ? 'SUPERIOR' : 'PENDING' })] })] })] }), r.cryptographic_signature && (_jsxs("div", { className: "p-2.5 bg-slate-900/90 border border-purple-500/20 rounded-lg text-xs font-mono text-slate-400 flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Lock, { className: "w-3.5 h-3.5 text-purple-400" }), _jsx("span", { children: "Signature:" })] }), _jsx("span", { className: "text-purple-300 font-semibold truncate max-w-[320px]", children: r.cryptographic_signature })] }))] }, r.review_id))) })] }), _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Database, { className: "w-5 h-5 text-indigo-400" }), _jsx("h2", { className: "text-base font-semibold text-slate-100", children: "Rollback Snapshots" })] }), _jsx(Badge, { variant: "sentinel", size: "sm", children: "Immutable" })] }), _jsx("div", { className: "space-y-3", children: snapshots.map((s) => (_jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-xl p-4 space-y-2 text-xs font-mono", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-bold text-slate-200", children: s.snapshot_id }), _jsx(Badge, { variant: "outline", size: "sm", children: s.platform_version })] }), _jsxs("div", { className: "text-slate-400 text-[11px] truncate", children: [_jsx("span", { className: "text-purple-400 font-semibold", children: "SHA256: " }), s.sha256_seal] })] }, s.snapshot_id))) })] })] })] }));
};
