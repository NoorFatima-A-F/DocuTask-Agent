import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import { CheckSquare, UserCheck, RefreshCw } from 'lucide-react';
export const ApprovalWorkflowCenter = () => {
    const [approvals, setApprovals] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        const load = async () => {
            setLoading(true);
            const list = await AILifecycleApiClient.listApprovals('agt_acme_invoice_reconciler');
            setApprovals(list);
            setLoading(false);
        };
        load();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx(CheckSquare, { className: "w-7 h-7 text-indigo-400" }), "Enterprise Approval Workflow Engine"] }), _jsx("p", { className: "text-sm text-slate-400 mt-1", children: "Multi-stage review gates: Developer Submission \u2192 Security Gate \u2192 Business Signoff \u2192 Compliance Release." })] }) }), _jsxs(Card, { className: "bg-slate-900/80 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base text-white flex items-center gap-2", children: [_jsx(UserCheck, { className: "w-5 h-5 text-emerald-400" }), " Governance Signoff History"] }) }), _jsx(CardContent, { className: "space-y-3", children: loading ? (_jsxs("div", { className: "p-8 text-center text-slate-400", children: [_jsx(RefreshCw, { className: "w-6 h-6 animate-spin mx-auto mb-2" }), " Loading Approvals..."] })) : (approvals.map((appr) => (_jsxs("div", { className: "p-4 bg-slate-800/40 rounded border border-slate-700/50 space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-sm font-semibold text-white", children: appr.stage }), _jsx(Badge, { variant: appr.decision === 'APPROVED' ? 'success' : 'warning', children: appr.decision })] }), _jsx("p", { className: "text-xs text-slate-300", children: appr.comments }), _jsxs("div", { className: "text-[10px] text-slate-400 flex justify-between pt-2 border-t border-slate-700/40 font-mono", children: [_jsxs("span", { children: ["Approver: ", appr.approver_email || 'System Governor'] }), _jsx("span", { children: new Date(appr.timestamp).toLocaleString() })] })] }, appr.approval_id)))) })] })] }));
};
