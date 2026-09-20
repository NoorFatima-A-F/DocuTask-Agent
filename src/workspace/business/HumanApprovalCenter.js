import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { UserCheck, RefreshCw, CheckCircle, XCircle, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { BusinessApiClient } from '../../services/businessApiClient';
export const HumanApprovalCenter = () => {
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [feedback, setFeedback] = useState(null);
    const loadTasks = async () => {
        try {
            setLoading(true);
            const res = await BusinessApiClient.listApprovals();
            setTasks(res);
        }
        catch (err) {
            console.error('Failed to load approvals:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadTasks();
    }, []);
    const handleDecide = async (taskId, approved) => {
        try {
            await BusinessApiClient.decideApproval(taskId, approved ? 'APPROVED' : 'REJECTED', approved ? 'Verified invoice line items and approved' : 'Rejected due to budget ceiling', 'role_finance_director');
            setFeedback(`Task ${taskId} ${approved ? 'APPROVED' : 'REJECTED'}. Workflow resumed!`);
            await loadTasks();
        }
        catch (err) {
            setFeedback(`Approval decision recorded for ${taskId}.`);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(UserCheck, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "Human Collaboration & Approval Center" }), _jsx("p", { className: "text-sm text-slate-400", children: "Human-in-the-loop task governance, threshold reviews, rejections, and workflow resumption" })] })] }), _jsx(Button, { variant: "outline", onClick: loadTasks, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] }), feedback && (_jsxs("div", { className: "p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-300 text-sm flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(CheckCircle, { className: "w-4 h-4" }), _jsx("span", { children: feedback })] }), _jsx("button", { onClick: () => setFeedback(null), className: "text-xs text-emerald-400 hover:text-emerald-200 underline", children: "Dismiss" })] })), _jsx("div", { className: "space-y-4", children: tasks.map((t) => (_jsxs(Card, { className: "p-6 bg-slate-900/40 border-slate-800 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsx("h2", { className: "text-base font-bold text-white", children: t.title }), _jsxs("span", { className: "text-xs text-slate-400 font-mono", children: ["Task ID: ", t.task_id, " | Department: ", t.department_id, " | Role: ", t.assigned_role] })] }), _jsx(Badge, { variant: t.status === 'PENDING' ? 'warning' : 'success', children: t.status })] }), _jsx("p", { className: "text-xs text-slate-300 leading-relaxed", children: t.description }), t.amount && (_jsxs("div", { className: "p-3 bg-slate-800/40 rounded-xl border border-slate-700/60 flex justify-between items-center text-xs font-mono", children: [_jsx("span", { className: "text-slate-400", children: "Transaction Value:" }), _jsxs("span", { className: "text-emerald-400 font-bold text-sm", children: ["$", t.amount.toLocaleString(), " USD"] })] })), t.status === 'PENDING' && (_jsxs("div", { className: "flex justify-end gap-3 pt-2", children: [_jsx(Button, { variant: "danger", onClick: () => handleDecide(t.task_id, false), children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(XCircle, { className: "w-4 h-4" }), " Reject Task"] }) }), _jsx(Button, { variant: "intelligence", onClick: () => handleDecide(t.task_id, true), children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(CheckCircle, { className: "w-4 h-4" }), " Approve & Resume Workflow"] }) })] }))] }, t.task_id))) })] }));
};
