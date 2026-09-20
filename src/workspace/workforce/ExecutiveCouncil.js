import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { workforceApiClient } from '../../services/workforceApiClient';
import { Check, X } from 'lucide-react';
export const ExecutiveCouncil = () => {
    const [props, setProps] = useState([]);
    useEffect(() => {
        workforceApiClient.getCouncilPropositions().then(setProps);
    }, []);
    const handleVote = async (id, role, vote) => {
        const updated = await workforceApiClient.voteCouncilProposition(id, role, vote);
        setProps(props.map(p => p.id === id ? updated : p));
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "bg-slate-900/60 p-5 rounded-2xl border border-slate-800", children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx("span", { className: "p-2 bg-indigo-500/20 text-indigo-400 rounded-xl", children: "\uD83C\uDFDB\uFE0F" }), "Executive AI Council Chamber"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Highest C-Suite Autonomous Decision Quorum & Constitutional Policies" })] }), _jsx("div", { className: "space-y-6", children: props.map((p) => (_jsxs(Card, { className: "p-6 bg-slate-900/50 border-slate-800", children: [_jsxs("div", { className: "flex justify-between items-start mb-3", children: [_jsxs("div", { children: [_jsx("div", { className: "text-lg font-bold text-white", children: p.title }), _jsxs("div", { className: "text-xs text-indigo-400 font-medium mt-0.5", children: ["Category: ", p.category] })] }), _jsx(Badge, { variant: p.enacted ? "default" : "outline", children: p.enacted ? "CONSTITUTIONALLY ENACTED" : "AWAITING QUORUM" })] }), _jsx("p", { className: "text-sm text-slate-300 my-4 bg-slate-950/60 p-4 rounded-xl border border-slate-800/80", children: p.summary }), _jsx("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-3 my-4", children: ['CEO', 'VP_ENG', 'SECURITY_DIR', 'FINANCE_DIR'].map((role) => {
                                const currentVote = p.council_votes[role];
                                return (_jsxs("div", { className: "p-3 bg-slate-950 rounded-xl border border-slate-800 text-xs", children: [_jsx("div", { className: "font-semibold text-slate-400 mb-1", children: role }), _jsxs("div", { className: "flex justify-between items-center", children: [_jsx("span", { className: "text-emerald-400 font-bold", children: currentVote || 'PENDING' }), _jsxs("div", { className: "flex gap-1", children: [_jsx("button", { onClick: () => handleVote(p.id, role, 'APPROVE'), className: "p-1 hover:bg-emerald-500/20 text-emerald-400 rounded", title: "Approve", children: _jsx(Check, { className: "w-3.5 h-3.5" }) }), _jsx("button", { onClick: () => handleVote(p.id, role, 'REJECT'), className: "p-1 hover:bg-rose-500/20 text-rose-400 rounded", title: "Reject", children: _jsx(X, { className: "w-3.5 h-3.5" }) })] })] })] }, role));
                            }) })] }, p.id))) })] }));
};
