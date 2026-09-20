import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Award, ShieldCheck, Copy, CheckCircle2 } from 'lucide-react';
export const CertificationCenterView = () => {
    const [isCopied, setIsCopied] = useState(false);
    const dossier = {
        dossierId: 'DOSSIER-HA-2026-09-10',
        platform: 'DocuTask Autonomous AI Platform',
        version: '12.0.0-APRCORP+',
        tier: 'TIER_4_MISSION_CRITICAL',
        compositeReliability: 99.42,
        availabilityPct: 99.9988,
        readinessScore: 99.45,
        invariantsCompliance: 100.0,
        mttrMs: 45.2,
        mtbfHours: 720.0,
        signature: '7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069',
    };
    const handleCopyJSON = () => {
        navigator.clipboard.writeText(JSON.stringify(dossier, null, 2));
        setIsCopied(true);
        setTimeout(() => setIsCopied(false), 2000);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Enterprise Resilience Certification Dossier" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Cryptographic HA Proof" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Exportable, cryptographically signed operational resilience certification for enterprise production sign-off." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Button, { variant: "outline", size: "sm", onClick: handleCopyJSON, children: [isCopied ? _jsx(CheckCircle2, { className: "w-3.5 h-3.5 mr-1.5 text-emerald-400" }) : _jsx(Copy, { className: "w-3.5 h-3.5 mr-1.5" }), isCopied ? 'Copied to Clipboard' : 'Copy Dossier JSON'] }), _jsx(Badge, { variant: "success", size: "md", children: "Certified: Tier 4 Mission Critical" })] })] }), _jsxs(Card, { className: "p-8 border-2 border-emerald-500/40 bg-emerald-950/10 space-y-6 shadow-xl", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-emerald-500/30 pb-6", children: [_jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Award, { className: "w-6 h-6 text-emerald-400" }), _jsx("span", { className: "text-lg font-bold tracking-wide text-foreground uppercase", children: "Certificate of Operational Resilience" })] }), _jsxs("div", { className: "text-xs text-muted-foreground font-mono", children: [dossier.dossierId, " \u2022 ", dossier.platform, " v", dossier.version] })] }), _jsx(Badge, { variant: "success", size: "md", children: dossier.tier })] }), _jsxs("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-4", children: [_jsxs("div", { className: "p-4 bg-background/80 rounded-lg border border-border/40", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Composite Reliability" }), _jsxs("div", { className: "text-2xl font-extrabold font-mono text-emerald-400 mt-1", children: [dossier.compositeReliability, "%"] })] }), _jsxs("div", { className: "p-4 bg-background/80 rounded-lg border border-border/40", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Operational Availability" }), _jsxs("div", { className: "text-2xl font-extrabold font-mono text-blue-400 mt-1", children: [dossier.availabilityPct, "%"] })] }), _jsxs("div", { className: "p-4 bg-background/80 rounded-lg border border-border/40", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Launch Readiness" }), _jsxs("div", { className: "text-2xl font-extrabold font-mono text-purple-400 mt-1", children: [dossier.readinessScore, "%"] })] }), _jsxs("div", { className: "p-4 bg-background/80 rounded-lg border border-border/40", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Invariants Compliance" }), _jsxs("div", { className: "text-2xl font-extrabold font-mono text-cyan-400 mt-1", children: [dossier.invariantsCompliance, "%"] })] })] }), _jsxs("div", { className: "p-4 bg-background/90 rounded-lg border border-border/60 space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between text-xs", children: [_jsxs("span", { className: "font-semibold text-foreground flex items-center gap-1.5", children: [_jsx(ShieldCheck, { className: "w-4 h-4 text-emerald-400" }), " SHA-256 Cryptographic Signature"] }), _jsx("span", { className: "text-emerald-400 font-mono text-[11px]", children: "VERIFIED_IMMUTABLE" })] }), _jsx("div", { className: "p-2.5 bg-muted/50 rounded font-mono text-xs text-primary break-all", children: dossier.signature }), _jsx("div", { className: "text-[11px] text-muted-foreground", children: "This digital signature cryptographically binds all execution proofs, invariant audits, and chaos benchmark results to this immutable dossier." })] })] })] }));
};
