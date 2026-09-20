import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { FileCheck2, RotateCw, } from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
export const VerificationWorkbench = () => {
    const [certificates, setCertificates] = useState([]);
    const [selectedCert, setSelectedCert] = useState(null);
    const [loading, setLoading] = useState(true);
    const loadCertificates = async () => {
        try {
            setLoading(true);
            const res = await executionPlatformApiClient.listVerifications();
            setCertificates(res.certificates || []);
            if (res.certificates && res.certificates.length > 0 && !selectedCert) {
                setSelectedCert(res.certificates[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load certificates:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadCertificates();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold text-white flex items-center gap-2", children: [_jsx(FileCheck2, { className: "w-5 h-5 text-cyan-400" }), "Verification Workbench & Cryptographic Proofs"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Post-execution state invariant assertions, external API/DB diff verification & SHA-256 signatures" })] }), _jsx(Button, { variant: "outline", onClick: loadCertificates, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: "w-4 h-4" }), "Refresh"] }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "lg:col-span-1 bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-sm font-semibold text-white", children: ["Issued Proofs (", certificates.length, ")"] }) }), _jsx(CardContent, { className: "space-y-2 max-h-[600px] overflow-y-auto", children: loading && certificates.length === 0 ? (_jsx("p", { className: "text-xs text-slate-500 py-4 text-center", children: "Loading certificates..." })) : certificates.map((c) => (_jsxs("div", { onClick: () => setSelectedCert(c), className: `p-3 rounded-lg border cursor-pointer transition-all ${selectedCert?.certificate_id === c.certificate_id
                                        ? 'bg-purple-950/40 border-purple-600'
                                        : 'bg-slate-800/40 border-slate-800 hover:border-slate-700'}`, children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-mono text-cyan-300", children: c.certificate_id }), _jsx(Badge, { variant: c.passed ? 'success' : 'error', children: c.passed ? 'VERIFIED' : 'FAILED' })] }), _jsxs("p", { className: "text-[11px] text-slate-300 mt-1 font-mono", children: ["Tool: ", c.tool_id] }), _jsxs("span", { className: "text-[10px] text-slate-500 block truncate mt-1", children: ["SHA: ", c.state_signature_sha256.slice(0, 20), "..."] })] }, c.certificate_id))) })] }), _jsxs(Card, { className: "lg:col-span-2 bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsx(CardTitle, { className: "text-base text-white", children: selectedCert ? `Certificate ${selectedCert.certificate_id}` : 'Select a Certificate' }), selectedCert && (_jsx(Badge, { variant: "outline", className: "font-mono text-xs text-cyan-400", children: selectedCert.mission_id }))] }) }), _jsx(CardContent, { className: "space-y-6", children: selectedCert && (_jsxs(_Fragment, { children: [_jsxs("div", { className: "p-3.5 bg-slate-950 border border-slate-800 rounded-xl space-y-1", children: [_jsx("span", { className: "text-[10px] font-semibold text-slate-500 uppercase tracking-wider block", children: "Cryptographic SHA-256 State Signature" }), _jsx("p", { className: "text-xs font-mono text-cyan-300 break-all select-all", children: selectedCert.state_signature_sha256 })] }), _jsxs("div", { children: [_jsx("h4", { className: "text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2", children: "Verified State Invariant Checks" }), _jsx("div", { className: "space-y-3", children: selectedCert.checks.map((chk) => (_jsxs("div", { className: "p-3 bg-slate-800/40 border border-slate-700/60 rounded-xl space-y-1.5", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-sm font-semibold text-white", children: chk.name }), _jsx(Badge, { variant: chk.passed ? 'success' : 'error', children: "Passed" })] }), _jsxs("p", { className: "text-xs text-slate-400 font-mono", children: ["Target: ", _jsx("span", { className: "text-slate-200", children: chk.target_resource })] }), _jsxs("p", { className: "text-xs text-emerald-400 font-mono", children: ["Actual: ", chk.actual_condition] })] }, chk.check_id))) })] })] })) })] })] })] }));
};
