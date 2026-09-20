import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const MissionCertificationView = () => {
    const certificates = [
        {
            certId: 'cert_msn_1001',
            missionId: 'msn_1001',
            domain: 'Invoice',
            tier: 'ENTERPRISE_HIGHEST_ASSURANCE',
            trustScore: 98.4,
            completeness: '100.0%',
            replayFidelity: '99.98%',
            invariants: '100.0%',
            issuedAt: 'Today, 14:20 UTC',
            seal: '0x8f2ac31b4e5d6a7b',
        },
        {
            certId: 'cert_msn_1002',
            missionId: 'msn_1002',
            domain: 'Contract',
            tier: 'SCIENTIFIC_REPRODUCIBLE',
            trustScore: 96.2,
            completeness: '100.0%',
            replayFidelity: '99.92%',
            invariants: '100.0%',
            issuedAt: 'Today, 14:15 UTC',
            seal: '0x3c7eb44a1d9e2f8c',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Mission Execution Certification" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Pillar 8" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Official certification tiers derived strictly from mathematical thresholds: Bronze (\u226570), Silver (\u226580), Gold (\u226590), Scientific (\u226595), Enterprise (\u226598)." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx(Badge, { variant: "success", size: "md", children: "Issuer: DACA Authority" }) })] }), _jsx("div", { className: "space-y-4", children: certificates.map((cert) => (_jsxs(Card, { className: "p-5 border-border/60", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 border-b border-border/40 pb-3 mb-4", children: [_jsxs("div", { children: [_jsx("span", { className: "font-mono text-xs text-primary font-semibold", children: cert.certId }), _jsxs("h3", { className: "text-sm font-semibold text-foreground mt-0.5", children: ["Certification Dossier for Mission ", _jsx("strong", { className: "font-mono text-primary", children: cert.missionId })] }), _jsxs("span", { className: "text-xs text-muted-foreground", children: ["Domain: ", _jsx("strong", { children: cert.domain })] })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx(Badge, { variant: cert.tier.includes('ENTERPRISE') ? 'success' : 'intelligence', size: "sm", children: cert.tier }) })] }), _jsxs("div", { className: "grid grid-cols-2 sm:grid-cols-4 gap-3 text-center text-xs mb-4", children: [_jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Trust Score" }), _jsxs("div", { className: "font-mono font-bold text-emerald-400 text-sm mt-0.5", children: [cert.trustScore, " / 100"] })] }), _jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Evidence Completeness" }), _jsx("div", { className: "font-mono font-bold text-foreground text-sm mt-0.5", children: cert.completeness })] }), _jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Replay State Fidelity" }), _jsx("div", { className: "font-mono font-bold text-emerald-400 text-sm mt-0.5", children: cert.replayFidelity })] }), _jsxs("div", { className: "p-3 rounded bg-muted/20 border border-border/40", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Invariant Pass Rate" }), _jsx("div", { className: "font-mono font-bold text-primary text-sm mt-0.5", children: cert.invariants })] })] }), _jsxs("div", { className: "text-xs text-muted-foreground flex items-center justify-between border-t border-border/40 pt-3 font-mono", children: [_jsxs("span", { children: ["Cryptographic Seal: ", _jsx("strong", { className: "text-foreground", children: cert.seal })] }), _jsx("button", { className: "text-primary hover:underline font-medium font-sans", children: "Download Signed Certificate \u2192" })] })] }, cert.certId))) })] }));
};
