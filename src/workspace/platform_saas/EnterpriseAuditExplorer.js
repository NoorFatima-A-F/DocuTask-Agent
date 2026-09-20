import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import { ShieldAlert, CheckCircle2, RefreshCw, FileCheck } from 'lucide-react';
export const EnterpriseAuditExplorer = () => {
    const [events, setEvents] = useState([]);
    const [integrity, setIntegrity] = useState(null);
    const [loading, setLoading] = useState(true);
    const loadData = async () => {
        setLoading(true);
        const [evList, integ] = await Promise.all([
            SaaSApiClient.listAuditEvents('tenant_acme_corp'),
            SaaSApiClient.verifyAuditIntegrity('tenant_acme_corp'),
        ]);
        setEvents(evList);
        setIntegrity(integ);
        setLoading(false);
    };
    useEffect(() => {
        loadData();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx(ShieldAlert, { className: "w-7 h-7 text-indigo-400" }), "Immutable Enterprise Audit Ledger & SOC2 Proof"] }), _jsx("p", { className: "text-sm text-slate-400 mt-1", children: "Cryptographic SHA-256 hash-chained tamper-evident audit trail for enterprise governance." })] }), _jsxs("div", { className: "flex items-center gap-3", children: [integrity && integrity.valid ? (_jsxs(Badge, { variant: "success", className: "px-3 py-1 flex items-center gap-1.5", children: [_jsx(CheckCircle2, { className: "w-4 h-4" }), " Hash Chain Verified"] })) : (_jsx(Badge, { variant: "error", className: "px-3 py-1", children: "Integrity Compromised" })), _jsx(Button, { variant: "outline", onClick: loadData, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: "w-4 h-4" }), " Re-Verify Chain"] }) })] })] }), _jsxs(Card, { className: "bg-slate-900/80 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base text-white flex items-center gap-2", children: [_jsx(FileCheck, { className: "w-4 h-4 text-emerald-400" }), " Cryptographic Event Trail (", events.length, ")"] }) }), _jsx(CardContent, { className: "space-y-3", children: loading ? (_jsx("div", { className: "p-8 text-center text-slate-400", children: "Loading audit ledger..." })) : (events.map((ev) => (_jsxs("div", { className: "p-4 bg-slate-800/40 rounded border border-slate-700/50 space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "intelligence", children: ev.action }), _jsx("span", { className: "text-sm font-semibold text-white", children: ev.actor_email })] }), _jsx("span", { className: "text-xs text-slate-400", children: new Date(ev.timestamp).toLocaleString() })] }), _jsxs("div", { className: "text-xs text-slate-400 grid grid-cols-2 gap-2", children: [_jsxs("div", { children: ["Resource: ", _jsxs("span", { className: "text-slate-200 font-mono", children: [ev.resource_type, ":", ev.resource_id] })] }), _jsxs("div", { children: ["IP Address: ", _jsx("span", { className: "text-slate-200 font-mono", children: ev.ip_address })] })] }), _jsxs("div", { className: "pt-2 border-t border-slate-700/40 text-[10px] text-slate-500 font-mono truncate", children: ["SHA-256 Hash: ", _jsx("span", { className: "text-cyan-400", children: ev.event_hash })] })] }, ev.audit_id)))) })] })] }));
};
