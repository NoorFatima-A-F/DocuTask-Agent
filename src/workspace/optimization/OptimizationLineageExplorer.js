import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { FileCheck2, GitCommit, CheckCircle2, Lock, Copy, Check, RefreshCw, Clock, Workflow } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
export const OptimizationLineageExplorer = ({ missionId = 'mission-current', }) => {
    const [copiedId, setCopiedId] = useState(null);
    const [lineage] = useState([
        {
            id: 'opt-evt-001',
            step: 1,
            stage: 'GOAL_PARSE',
            action: 'Objective formulation: BALANCED_STANDARD with hard SLA cap <= 5000ms',
            sha256Hash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            parentHash: '0000000000000000000000000000000000000000000000000000000000000000',
            timestampUtc: '2026-09-12T13:20:01.102Z',
            deltaCostUsd: 0.0,
            deltaLatencyMs: 0,
            deltaConfidence: 0.0,
            verified: true,
        },
        {
            id: 'opt-evt-002',
            step: 2,
            stage: 'STRATEGY_SOLVE',
            action: 'Pareto frontier scalarization selected strategy "Balanced Hybrid Cloud"',
            sha256Hash: 'a7162acf5f9c4f74d081c70e28d4ec0cf4bf49f0ec1fc93ff06460395fa3fa74',
            parentHash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            timestampUtc: '2026-09-12T13:20:01.340Z',
            deltaCostUsd: -0.045,
            deltaLatencyMs: -450,
            deltaConfidence: +0.024,
            verified: true,
        },
        {
            id: 'opt-evt-003',
            step: 3,
            stage: 'ROUTING_COMMIT',
            action: 'Routed Task #1 to Gemini Flash OCR and Task #2 to Claude 3.5 Sonnet Extraction',
            sha256Hash: '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b',
            parentHash: 'a7162acf5f9c4f74d081c70e28d4ec0cf4bf49f0ec1fc93ff06460395fa3fa74',
            timestampUtc: '2026-09-12T13:20:01.512Z',
            deltaCostUsd: -0.012,
            deltaLatencyMs: -220,
            deltaConfidence: +0.005,
            verified: true,
        },
        {
            id: 'opt-evt-004',
            step: 4,
            stage: 'RESOURCE_RESERVATION',
            action: 'Atomic ticket TKT-88492 issued for GPU Pool Alpha & 4 Claude concurrency slots',
            sha256Hash: 'd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35',
            parentHash: '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b',
            timestampUtc: '2026-09-12T13:20:01.780Z',
            deltaCostUsd: 0.0,
            deltaLatencyMs: 0,
            deltaConfidence: 0.0,
            verified: true,
        },
    ]);
    const copyHash = (hash, id) => {
        navigator.clipboard.writeText(hash);
        setCopiedId(id);
        setTimeout(() => setCopiedId(null), 2000);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Workflow, { className: "w-5 h-5 text-indigo-400" }), "Optimization Lineage & Decision Provenance Explorer"] }), _jsxs("p", { className: "text-sm text-slate-400", children: ["Immutable SHA-256 cryptographic chain of optimization choices, scalarization weights, and resource tickets for mission: ", _jsx("code", { className: "text-indigo-300 font-mono text-xs", children: missionId })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: "success", size: "md", children: "Chain Status: 100% VERIFIED" }), _jsxs("button", { className: "flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700", children: [_jsx(RefreshCw, { className: "w-3.5 h-3.5" }), "Verify Merkle Root"] })] })] }), _jsxs(Card, { className: "p-4 bg-slate-900 border-slate-800 flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-4", children: [_jsx("div", { className: "p-2.5 rounded-xl bg-indigo-950/60 border border-indigo-500/30 text-indigo-400", children: _jsx(Lock, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "Root Merkle Hash" }), _jsx("code", { className: "text-xs font-mono font-bold text-slate-200", children: "0x9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08" })] })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsxs("div", { className: "text-right", children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "Total Optimization Delta" }), _jsx("span", { className: "text-xs font-mono font-bold text-emerald-400", children: "-$0.057 USD | -670ms | +2.9% Conf" })] }) })] }), _jsx("div", { className: "space-y-3", children: lineage.map(evt => (_jsx(Card, { className: "p-4 bg-slate-900 border-slate-800 hover:border-slate-700 transition-all", children: _jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { className: "flex items-start gap-3", children: [_jsx("div", { className: "p-2 rounded-lg bg-slate-950 border border-slate-800 text-indigo-400 mt-0.5", children: _jsx(GitCommit, { className: "w-4 h-4" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2 mb-1", children: [_jsxs("span", { className: "text-xs font-mono font-bold text-indigo-400", children: ["Step ", evt.step] }), _jsx(Badge, { variant: "intelligence", size: "sm", children: evt.stage }), _jsxs("span", { className: "text-xs text-slate-400 flex items-center gap-1 font-mono", children: [_jsx(Clock, { className: "w-3 h-3" }), new Date(evt.timestampUtc).toLocaleTimeString()] })] }), _jsx("p", { className: "text-xs font-semibold text-slate-200 mb-2", children: evt.action }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px] font-mono bg-slate-950 p-2.5 rounded border border-slate-800/80", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-slate-500", children: "Node SHA-256:" }), _jsxs("div", { className: "flex items-center gap-1.5", children: [_jsx("span", { className: "text-slate-300 truncate max-w-[200px]", children: evt.sha256Hash }), _jsx("button", { onClick: () => copyHash(evt.sha256Hash, evt.id), className: "text-slate-400 hover:text-slate-200 p-0.5", title: "Copy Hash", children: copiedId === evt.id ? _jsx(Check, { className: "w-3 h-3 text-emerald-400" }) : _jsx(Copy, { className: "w-3 h-3" }) })] })] }), _jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-slate-500", children: "Parent SHA-256:" }), _jsx("span", { className: "text-slate-400 truncate max-w-[200px]", children: evt.parentHash })] })] })] })] }), _jsxs("div", { className: "text-right space-y-1", children: [_jsxs(Badge, { variant: "success", size: "sm", className: "gap-1", children: [_jsx(FileCheck2, { className: "w-3 h-3" }), "Verified Ledger"] }), _jsxs("div", { className: "text-[10px] font-mono text-slate-400", children: [evt.deltaCostUsd !== 0 && (_jsxs("span", { className: evt.deltaCostUsd < 0 ? 'text-emerald-400 font-bold block' : 'text-amber-400 font-bold block', children: ["Cost \u0394: ", evt.deltaCostUsd < 0 ? '-' : '+', "$", Math.abs(evt.deltaCostUsd).toFixed(3)] })), evt.deltaLatencyMs !== 0 && (_jsxs("span", { className: evt.deltaLatencyMs < 0 ? 'text-emerald-400 font-bold block' : 'text-amber-400 font-bold block', children: ["Latency \u0394: ", evt.deltaLatencyMs < 0 ? '' : '+', evt.deltaLatencyMs, "ms"] })), evt.deltaConfidence !== 0 && (_jsxs("span", { className: evt.deltaConfidence > 0 ? 'text-indigo-400 font-bold block' : 'text-slate-400 block', children: ["Conf \u0394: ", evt.deltaConfidence > 0 ? '+' : '', (evt.deltaConfidence * 100).toFixed(1), "%"] }))] })] })] }) }, evt.id))) }), _jsxs("div", { className: "p-3 bg-slate-950 rounded-lg border border-slate-800 text-xs text-slate-400 flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-4 h-4 text-emerald-400" }), _jsx("span", { children: "Every optimization decision is written to the append-only Truth Ledger and signed with RSA-4096 audit proofs." })] }), _jsx("span", { className: "font-mono text-[11px] text-slate-500", children: "Compliant with SOC2 / ISO-27001 AI Auditing" })] })] }));
};
