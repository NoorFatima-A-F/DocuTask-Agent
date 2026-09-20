import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { EsmrReplayApiClient } from '../../services/esmrReplayApiClient';
export const EnterpriseAuditExplorerView = ({ missionId }) => {
    const [auditRecords, setAuditRecords] = useState([]);
    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        Promise.all([
            EsmrReplayApiClient.getAuditTrail(missionId),
            EsmrReplayApiClient.verifyAudit(missionId),
        ])
            .then(([records, rep]) => {
            setAuditRecords(records);
            setReport(rep);
        })
            .catch(console.error)
            .finally(() => setLoading(false));
    }, [missionId]);
    if (loading) {
        return (_jsx("div", { className: "p-6 bg-slate-900 border border-slate-800 rounded-xl text-slate-400 animate-pulse", children: "Verifying Cryptographic Signatures across Enterprise Audit Trail..." }));
    }
    return (_jsxs("div", { className: "bg-slate-950 border border-slate-800 rounded-xl p-6 shadow-2xl space-y-6 text-slate-100", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4", children: [_jsxs("div", { children: [_jsxs("h3", { className: "text-lg font-bold text-white flex items-center gap-2", children: [_jsx("span", { children: "\uD83D\uDEE1\uFE0F" }), " Cryptographically Signed Enterprise Audit Trail"] }), _jsx("p", { className: "text-xs text-slate-400 mt-1", children: "HMAC-SHA256 signed audit records with strict previous-hash chaining and tamper-evident guarantees." })] }), report && (_jsx("div", { className: "flex items-center gap-2", children: _jsx("span", { className: `px-3 py-1 rounded-lg text-xs font-mono font-bold border ${report.is_valid
                                ? 'bg-emerald-950/80 border-emerald-500/40 text-emerald-400'
                                : 'bg-rose-950/80 border-rose-500/40 text-rose-400'}`, children: report.is_valid ? '✓ HMAC-SHA256 AUDIT CHAIN VALID' : '✗ TAMPER DETECTED' }) }))] }), _jsx("div", { className: "overflow-x-auto border border-slate-800 rounded-lg", children: _jsxs("table", { className: "w-full text-left font-mono text-xs border-collapse", children: [_jsx("thead", { className: "bg-slate-900 text-slate-400 border-b border-slate-800", children: _jsxs("tr", { children: [_jsx("th", { className: "py-2.5 px-3", children: "#" }), _jsx("th", { className: "py-2.5 px-3", children: "Category" }), _jsx("th", { className: "py-2.5 px-3", children: "Action Type" }), _jsx("th", { className: "py-2.5 px-3", children: "Actor" }), _jsx("th", { className: "py-2.5 px-3", children: "Audit Hash" }), _jsx("th", { className: "py-2.5 px-3", children: "HMAC Sig" }), _jsx("th", { className: "py-2.5 px-3", children: "Status" })] }) }), _jsx("tbody", { className: "divide-y divide-slate-850", children: auditRecords.map((rec) => (_jsxs("tr", { className: "hover:bg-slate-900/60", children: [_jsx("td", { className: "py-2.5 px-3 text-slate-400", children: rec.sequence_number }), _jsx("td", { className: "py-2.5 px-3 text-cyan-400", children: rec.category }), _jsx("td", { className: "py-2.5 px-3 text-slate-200", children: rec.action_type }), _jsx("td", { className: "py-2.5 px-3 text-slate-400", children: rec.actor }), _jsxs("td", { className: "py-2.5 px-3 text-slate-500 text-[10px]", children: [rec.audit_hash.slice(0, 12), "..."] }), _jsxs("td", { className: "py-2.5 px-3 text-purple-400 text-[10px]", children: [rec.hmac_signature.slice(0, 16), "..."] }), _jsx("td", { className: "py-2.5 px-3", children: _jsx("span", { className: "text-emerald-400 font-bold", children: "\u2713 SIGNED" }) })] }, rec.audit_id))) })] }) })] }));
};
