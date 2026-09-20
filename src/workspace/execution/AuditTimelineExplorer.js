import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { ShieldCheck, RotateCw, } from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
export const AuditTimelineExplorer = () => {
    const [entries, setEntries] = useState([]);
    const [ledgerValid, setLedgerValid] = useState(true);
    const [loading, setLoading] = useState(true);
    const loadData = async () => {
        try {
            setLoading(true);
            const [eRes, vRes] = await Promise.all([
                executionPlatformApiClient.listAuditEntries({ limit: 100 }),
                executionPlatformApiClient.verifyAuditLedger(),
            ]);
            setEntries(eRes.entries || []);
            setLedgerValid(vRes.ledger_valid);
        }
        catch (err) {
            console.error('Failed to load audit ledger:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadData();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold text-white flex items-center gap-2", children: [_jsx(ShieldCheck, { className: "w-5 h-5 text-cyan-400" }), "Cryptographic Audit Timeline & Compliance Ledger"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Tamper-evident SHA-256 block chain verification, SOC2/HIPAA evidence trails & provenance records" })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: ledgerValid ? 'success' : 'error', className: "py-1 px-3 text-xs", children: ledgerValid ? 'Ledger Chain 100% Cryptographically Valid' : 'Ledger Inconsistency Detected' }), _jsx(Button, { variant: "outline", onClick: loadData, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: "w-4 h-4" }), "Re-Verify"] }) })] })] }), loading && entries.length === 0 && (_jsx("p", { className: "text-xs text-slate-500 py-4 text-center", children: "Loading audit ledger..." })), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base text-white", children: ["Chained Block Entries (", entries.length, ")"] }) }), _jsx(CardContent, { children: _jsx("div", { className: "space-y-3", children: entries.map((e, idx) => (_jsxs("div", { className: "p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-2 text-xs", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "w-5 h-5 rounded-full bg-cyan-950 border border-cyan-500 flex items-center justify-center font-mono font-bold text-[10px] text-cyan-200", children: idx + 1 }), _jsx("span", { className: "font-semibold text-white uppercase tracking-wider", children: e.action_type }), _jsxs("span", { className: "text-slate-400", children: ["by ", e.actor] })] }), _jsxs(Badge, { variant: "outline", children: [e.risk_level, " risk"] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px] font-mono pt-1", children: [_jsxs("div", { className: "text-slate-400 truncate", children: [_jsx("span", { className: "text-slate-600 block text-[9px]", children: "PREV HASH" }), e.prev_hash] }), _jsxs("div", { className: "text-cyan-400 truncate", children: [_jsx("span", { className: "text-slate-600 block text-[9px]", children: "BLOCK SIGNATURE SHA-256" }), e.hash_signature] })] }), e.payload_summary && Object.keys(e.payload_summary).length > 0 && (_jsx("pre", { className: "p-2 bg-slate-900 rounded text-slate-300 text-[10px] overflow-x-auto", children: JSON.stringify(e.payload_summary, null, 2) }))] }, e.entry_id))) }) })] })] }));
};
