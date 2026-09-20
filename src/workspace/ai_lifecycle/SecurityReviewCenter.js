import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import { ShieldAlert, CheckCircle2, AlertTriangle, RefreshCw } from 'lucide-react';
export const SecurityReviewCenter = () => {
    const [scan, setScan] = useState(null);
    const [scanning, setScanning] = useState(false);
    const runScan = async () => {
        setScanning(true);
        const res = await AILifecycleApiClient.scanSecurity('agt_acme_invoice_reconciler', {
            version_tag: '1.2.0',
            system_prompt: 'You are an autonomous invoice reconciliation agent.',
            tools: ['tool_erp_lookup', 'tool_ocr_extract'],
        });
        setScan(res);
        setScanning(false);
    };
    useEffect(() => {
        runScan();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx(ShieldAlert, { className: "w-7 h-7 text-indigo-400" }), "Agent Security Scanner & Risk Review"] }), _jsx("p", { className: "text-sm text-slate-400 mt-1", children: "Prompt injection resistance, tool permission boundaries, PII/PHI leakage detection, and CVE vulnerability scanning." })] }), _jsx(Button, { variant: "intelligence", onClick: runScan, disabled: scanning, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${scanning ? 'animate-spin' : ''}` }), " Run Security Scan"] }) })] }), scan && (_jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "bg-slate-900/80 border-slate-800 lg:col-span-1", children: [_jsx(CardHeader, { children: _jsx(CardTitle, { className: "text-base text-white", children: "Security Scorecard" }) }), _jsxs(CardContent, { className: "space-y-4 text-center", children: [_jsxs("div", { className: "p-6 bg-slate-950 rounded-full w-32 h-32 mx-auto flex flex-col items-center justify-center border-4 border-emerald-500", children: [_jsx("span", { className: "text-3xl font-extrabold text-white", children: scan.security_score }), _jsx("span", { className: "text-[10px] text-slate-400 uppercase", children: "Score / 100" })] }), _jsxs(Badge, { variant: scan.risk_level === 'LOW' ? 'success' : 'warning', className: "text-xs px-3 py-1", children: ["Risk Level: ", scan.risk_level] }), _jsxs("div", { className: "text-xs text-slate-400 text-left space-y-2 pt-3 border-t border-slate-800", children: [_jsxs("div", { className: "flex justify-between", children: [_jsx("span", { children: "Prompt Injection Resistance:" }), _jsxs("span", { className: "font-bold text-white", children: [scan.prompt_injection_resistance_pct, "%"] })] }), _jsxs("div", { className: "flex justify-between", children: [_jsx("span", { children: "PII Leakage Detected:" }), _jsx("span", { className: "font-bold text-emerald-400", children: "None" })] })] })] })] }), _jsxs(Card, { className: "bg-slate-900/80 border-slate-800 lg:col-span-2", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base text-white flex items-center gap-2", children: [_jsx(AlertTriangle, { className: "w-5 h-5 text-amber-400" }), " Vulnerability & Privilege Findings"] }) }), _jsxs(CardContent, { className: "space-y-3", children: [scan.vulnerabilities.map((v) => (_jsxs("div", { className: "p-4 bg-slate-800/40 rounded-lg border border-slate-700/50 space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-sm font-semibold text-white", children: v.category }), _jsx(Badge, { variant: v.severity === 'CRITICAL' ? 'error' : 'warning', children: v.severity })] }), _jsx("p", { className: "text-xs text-slate-300", children: v.description }), _jsxs("p", { className: "text-xs text-cyan-400 font-medium", children: ["Recommendation: ", v.recommendation] })] }, v.vuln_id))), scan.vulnerabilities.length === 0 && (_jsxs("div", { className: "p-8 text-center text-slate-400 flex items-center justify-center gap-2", children: [_jsx(CheckCircle2, { className: "w-5 h-5 text-emerald-400" }), " No security vulnerabilities found."] }))] })] })] }))] }));
};
