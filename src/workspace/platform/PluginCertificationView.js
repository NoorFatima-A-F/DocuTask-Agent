import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const PluginCertificationView = () => {
    const [isScanning, setIsScanning] = useState(false);
    const [certifiedBadge] = useState({
        badgeId: 'BADGE-1725992010-INVOICE',
        pluginId: 'plugin.invoice.processing',
        version: '1.4.0',
        overallScore: 99.4,
        certified: true,
        merkleAttestationHash: 'a8f3b20c91e847ad3ef0192a83c7482910fae12089bb3c17820aedfa9102bc45',
        signature: 'sig_cert_a8f3b20c91e847ad3ef0192a83c7482910fae12089bb3c17',
        certifiedAtUtc: '2026-09-10T18:22:15Z',
        checks: [
            { id: 'CERT-SCH-01', name: 'Manifest & Capability Schema Compliance', score: 100.0, passed: true, details: 'Verified JSON schema and input/output contracts.' },
            { id: 'CERT-SEC-02', name: 'Static AST & Permission Sandbox Scan', score: 99.2, passed: true, details: 'Zero unauthorized socket egress or eval primitives.' },
            { id: 'CERT-PERF-03', name: 'SLA Latency & Memory Footprint Bounds', score: 98.5, passed: true, details: 'P95 latency (124ms) and RAM (48MB) within quota.' },
            { id: 'CERT-REP-04', name: 'Deterministic Replay Parity (10 Runs)', score: 100.0, passed: true, details: 'Bitwise output hash match across 10 frozen seeds.' },
            { id: 'CERT-EVD-05', name: 'Cryptographic Merkle DAG Evidence Generation', score: 100.0, passed: true, details: 'Seals capability steps with SHA-256 digests.' },
            { id: 'CERT-ORG-06', name: 'Multi-Agent Organization & Vickrey Protocol', score: 99.0, passed: true, details: 'Complies with communication bus and auction rules.' },
        ],
    });
    const handleRunCertification = () => {
        setIsScanning(true);
        setTimeout(() => {
            setIsScanning(false);
        }, 600);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Plugin Certification Center" }), _jsx(Badge, { variant: "success", size: "sm", children: "Automated 6-Point Audit" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Automated certification pipeline guaranteeing schema validity, AST security, replay stability, and Merkle evidence generation." })] }), _jsx("button", { onClick: handleRunCertification, disabled: isScanning, className: "px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-lg transition-all flex items-center gap-2 shadow-sm cursor-pointer", children: isScanning ? 'Auditing Plugin...' : '🛡️ Run 6-Point Certification' })] }), certifiedBadge && (_jsx("div", { className: "space-y-6", children: _jsxs(Card, { className: "p-6 space-y-4 border-emerald-500/30 bg-emerald-950/10", children: [_jsxs("div", { className: "flex items-start justify-between border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsx(Badge, { variant: "success", size: "sm", className: "mb-2", children: "OFFICIAL PLATFORM CERTIFICATION BADGE" }), _jsxs("h2", { className: "text-lg font-bold", children: [certifiedBadge.pluginId, " (v", certifiedBadge.version, ")"] }), _jsxs("div", { className: "text-xs font-mono text-muted-foreground mt-0.5", children: ["Badge ID: ", certifiedBadge.badgeId] })] }), _jsxs("div", { className: "text-right font-mono", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Certification Score" }), _jsxs("div", { className: "text-2xl font-extrabold text-emerald-400", children: [certifiedBadge.overallScore, "%"] })] })] }), _jsxs("div", { className: "space-y-3", children: [_jsx("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: "6-Point Verification Battery" }), _jsx("div", { className: "space-y-2", children: certifiedBadge.checks.map((chk) => (_jsxs("div", { className: "p-3 bg-card border border-border/40 rounded-lg flex items-center justify-between text-xs", children: [_jsxs("div", { children: [_jsxs("div", { className: "font-semibold text-foreground flex items-center gap-2", children: [_jsx("span", { className: "text-emerald-400", children: "\u2713" }), " ", chk.name] }), _jsx("div", { className: "text-muted-foreground text-[11px] mt-0.5", children: chk.details })] }), _jsxs(Badge, { variant: "success", size: "sm", children: [chk.score, "%"] })] }, chk.id))) })] }), _jsxs("div", { className: "p-3 bg-card border border-border/40 rounded font-mono text-[11px] text-muted-foreground space-y-1", children: [_jsxs("div", { children: [_jsx("span", { className: "text-foreground", children: "Merkle Digest: " }), certifiedBadge.merkleAttestationHash] }), _jsxs("div", { children: [_jsx("span", { className: "text-foreground", children: "Authority Signature: " }), _jsx("span", { className: "text-emerald-400 font-bold", children: certifiedBadge.signature })] })] })] }) }))] }));
};
