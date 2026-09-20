import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { ShieldAlert, RotateCw, CheckCircle, XCircle, AlertTriangle, Lock, } from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
export const PolicyGovernanceCenter = () => {
    const [rules, setRules] = useState([]);
    const [approvals, setApprovals] = useState([]);
    const [loading, setLoading] = useState(true);
    const loadData = async () => {
        try {
            setLoading(true);
            const [rList, aList] = await Promise.all([
                executionPlatformApiClient.listPolicyRules(),
                executionPlatformApiClient.listApprovals(),
            ]);
            setRules(rList.rules || []);
            setApprovals(aList.approvals || []);
        }
        catch (err) {
            console.error('Failed to load governance rules:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadData();
    }, []);
    const handleResolveApproval = async (approvalId, approved) => {
        try {
            await executionPlatformApiClient.resolveApproval(approvalId, approved, 'Executive Governance Officer');
            await loadData();
        }
        catch (err) {
            console.error('Error resolving approval:', err);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold text-white flex items-center gap-2", children: [_jsx(ShieldAlert, { className: "w-5 h-5 text-amber-400" }), "Execution Policy, Governance & HITL Sign-off Gates"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "RBAC/ABAC rule evaluation, spending cap thresholds, destructive mutation guards & human escalation" })] }), _jsx(Button, { variant: "outline", onClick: loadData, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: "w-4 h-4" }), "Refresh"] }) })] }), loading && rules.length === 0 && (_jsx("p", { className: "text-xs text-slate-500 py-4 text-center", children: "Loading governance rules..." })), _jsxs(Card, { className: "bg-slate-900/80 border-amber-800/40", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base text-white flex items-center gap-2", children: [_jsx(AlertTriangle, { className: "w-5 h-5 text-amber-400" }), "Human-In-The-Loop Approval Requests (", approvals.filter((a) => a.status === 'pending').length, " Pending)"] }) }), _jsx(CardContent, { children: approvals.filter((a) => a.status === 'pending').length === 0 ? (_jsx("div", { className: "py-6 text-center text-xs text-slate-500", children: "No pending execution escalations. All operational thresholds clear." })) : (_jsx("div", { className: "space-y-3", children: approvals
                                .filter((a) => a.status === 'pending')
                                .map((req) => (_jsxs("div", { className: "p-4 bg-slate-950 border border-amber-800/60 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-sm font-semibold text-white", children: req.reason }), _jsxs(Badge, { variant: "error", children: [req.risk_level, " risk"] })] }), _jsxs("p", { className: "text-xs text-slate-400 mt-1 font-mono", children: ["Tool: ", req.tool_id, " \u2022 Mission: ", req.mission_id, " \u2022 Requester: ", req.requester] })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Button, { variant: "secondary", onClick: () => handleResolveApproval(req.approval_id, true), children: _jsxs("span", { className: "flex items-center gap-1.5 text-xs text-emerald-400", children: [_jsx(CheckCircle, { className: "w-4 h-4" }), " Approve"] }) }), _jsx(Button, { variant: "outline", onClick: () => handleResolveApproval(req.approval_id, false), children: _jsxs("span", { className: "flex items-center gap-1.5 text-xs text-rose-400", children: [_jsx(XCircle, { className: "w-4 h-4" }), " Deny"] }) })] })] }, req.approval_id))) })) })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base text-white flex items-center gap-2", children: [_jsx(Lock, { className: "w-4 h-4 text-purple-400" }), "Active Governance Policy Rules (", rules.length, ")"] }) }), _jsx(CardContent, { children: _jsx("div", { className: "border border-slate-800 rounded-xl overflow-hidden", children: _jsxs("table", { className: "w-full text-left text-xs", children: [_jsx("thead", { className: "bg-slate-950 text-slate-400 font-mono", children: _jsxs("tr", { children: [_jsx("th", { className: "p-3", children: "Rule Name" }), _jsx("th", { className: "p-3", children: "Target Scope" }), _jsx("th", { className: "p-3", children: "Policy Decision" }), _jsx("th", { className: "p-3", children: "Condition Expression" }), _jsx("th", { className: "p-3", children: "Simulation Mandatory" })] }) }), _jsx("tbody", { className: "divide-y divide-slate-800 text-slate-300", children: rules.map((r) => (_jsxs("tr", { className: "hover:bg-slate-800/30", children: [_jsxs("td", { className: "p-3 font-semibold text-white", children: [r.name, _jsx("p", { className: "text-[11px] text-slate-400 font-normal mt-0.5", children: r.description })] }), _jsx("td", { className: "p-3 font-mono text-purple-300", children: r.target_tools.join(', ') }), _jsx("td", { className: "p-3", children: _jsx(Badge, { variant: r.decision === 'allow'
                                                            ? 'success'
                                                            : r.decision === 'deny'
                                                                ? 'error'
                                                                : 'warning', children: r.decision }) }), _jsx("td", { className: "p-3 font-mono text-slate-400", children: r.condition_expression }), _jsx("td", { className: "p-3", children: r.requires_simulation ? (_jsx(Badge, { variant: "intelligence", children: "Required" })) : (_jsx("span", { className: "text-slate-500", children: "Optional" })) })] }, r.rule_id))) })] }) }) })] })] }));
};
