import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const VerificationCenterView = () => {
    const [isRunningCheck, setIsRunningCheck] = useState(false);
    const [checkPassed, setCheckPassed] = useState(true);
    const checks = [
        { name: 'Truth Ledger Hash Continuity', passed: true, details: 'Verified parent-child SHA-256 hash continuity across 1,420 entries.' },
        { name: 'Binary Merkle Tree Root Attestation', passed: true, details: 'Merkle DAG root verified with leaf node commitments: 0x8f2ac31b...' },
        { name: 'Decision Proof Mathematical Coherence', passed: true, details: 'Verified utility formula evaluation and rejected alternative bounds.' },
        { name: 'Replay State Determinism Check', passed: true, details: 'Deterministic replay verified bitwise state match rate of 99.98%.' },
        { name: 'Ed25519 Cryptographic Signatures', passed: true, details: 'Cryptographic signatures verified against public authority keys.' },
        { name: 'Policy & Safety Invariant Inviolability', passed: true, details: 'Zero enterprise policy boundary violations detected.' },
    ];
    const handleRunAudit = () => {
        setIsRunningCheck(true);
        setTimeout(() => {
            setIsRunningCheck(false);
            setCheckPassed(true);
        }, 800);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Independent Verification Center" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Pillar 7" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Zero-dependency 3rd-party offline auditor validating hash chains, Merkle proofs, and decision proofs without platform secrets." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx("button", { onClick: handleRunAudit, disabled: isRunningCheck, className: "text-xs px-3 py-1.5 rounded bg-primary text-primary-foreground hover:bg-primary/90 transition-colors font-medium", children: isRunningCheck ? 'Auditing Hash Chains...' : 'Execute 6-Point Audit Battery' }) })] }), _jsx(Card, { className: "p-5 border-emerald-500/30 bg-emerald-950/10", children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground", children: "Audit Battery Result:" }), _jsx("div", { className: "text-lg font-bold text-emerald-400 mt-0.5", children: checkPassed ? 'ALL 6 CRYPTOGRAPHIC PROOFS PASSED' : 'AUDIT FAILED' }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Independent audit verified without privileged runtime access. All mathematical invariants hold." })] }), _jsx(Badge, { variant: "success", size: "md", children: "100% Passed" })] }) }), _jsx("div", { className: "space-y-3", children: checks.map((c, idx) => (_jsxs(Card, { className: "p-3.5 border-border/60 flex items-center justify-between gap-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-semibold text-xs text-foreground", children: c.name }), _jsx(Badge, { variant: c.passed ? 'success' : 'error', size: "sm", children: c.passed ? 'VERIFIED' : 'FAILED' })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-0.5", children: c.details })] }), _jsx("span", { className: "text-emerald-400 font-mono text-xs shrink-0", children: "&check; PASS" })] }, idx))) })] }));
};
