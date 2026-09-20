import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const PluginMarketplaceView = () => {
    const [installedMap, setInstalledMap] = useState({
        'pkg.fintech.invoice_pro': true,
        'pkg.hr.talent_matcher': true,
        'pkg.health.hipaa_shield': true,
        'pkg.legal.lexis_covenant': true,
    });
    const packages = [
        {
            id: 'pkg.fintech.invoice_pro',
            name: 'InvoicePro Elite Agent',
            version: '1.4.0',
            author: 'DocuTask Labs',
            category: 'FINANCE',
            description: 'State-of-the-art multi-lingual invoice extraction with Mod11 VAT checksum verification.',
            securityAuditScore: 99.4,
            downloadCount: 14200,
            rating: 4.95,
            tags: ['invoices', 'ocr', 'reconciliation'],
        },
        {
            id: 'pkg.hr.talent_matcher',
            name: 'TalentMatcher ATS Screener',
            version: '1.2.0',
            author: 'TalentAI Labs',
            category: 'HUMAN_RESOURCES',
            description: 'Parses complex multi-column resumes and scores talent against job requisitions.',
            securityAuditScore: 98.1,
            downloadCount: 8900,
            rating: 4.88,
            tags: ['resumes', 'ats', 'hiring'],
        },
        {
            id: 'pkg.health.hipaa_shield',
            name: 'HIPAA Clinical Shield',
            version: '2.0.1',
            author: 'MedSecure Systems',
            category: 'HEALTHCARE',
            description: 'Zero-leakage PHI redactor and ICD-10 diagnostic coding extractor.',
            securityAuditScore: 100.0,
            downloadCount: 6400,
            rating: 4.98,
            tags: ['healthcare', 'hipaa', 'phi'],
        },
        {
            id: 'pkg.legal.lexis_covenant',
            name: 'LexisCovenant Contract Reviewer',
            version: '1.1.5',
            author: 'LexisCorp AI',
            category: 'LEGAL',
            description: 'Identifies risky indemnities, non-competes, and liabilities in MSAs and NDAs.',
            securityAuditScore: 97.8,
            downloadCount: 11200,
            rating: 4.91,
            tags: ['contracts', 'legal', 'indemnity'],
        },
    ];
    const handleToggleInstall = (pkgId) => {
        setInstalledMap((prev) => ({ ...prev, [pkgId]: !prev[pkgId] }));
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Agent Marketplace" }), _jsx(Badge, { variant: "success", size: "sm", children: "Verified Ecosystem" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Discover, install, and update certified domain agent plugins with 1-click sandboxed deployment." })] }), _jsxs(Badge, { variant: "outline", size: "md", children: [packages.length, " Packages Verified"] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6", children: packages.map((pkg) => {
                    const isInstalled = !!installedMap[pkg.id];
                    return (_jsxs(Card, { className: "p-6 space-y-4 flex flex-col justify-between", children: [_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx(Badge, { variant: "outline", size: "sm", className: "mb-1", children: pkg.category }), _jsx("h2", { className: "text-base font-bold text-foreground", children: pkg.name }), _jsxs("div", { className: "text-xs text-muted-foreground mt-0.5", children: ["by ", _jsx("span", { className: "text-foreground font-semibold", children: pkg.author }), " \u2022 v", pkg.version] })] }), _jsxs("div", { className: "text-right", children: [_jsxs(Badge, { variant: "success", size: "sm", children: ["\u2605 ", pkg.rating] }), _jsxs("div", { className: "text-[10px] text-muted-foreground mt-1", children: [pkg.downloadCount.toLocaleString(), " installs"] })] })] }), _jsx("p", { className: "text-xs text-muted-foreground leading-relaxed", children: pkg.description }), _jsx("div", { className: "flex flex-wrap gap-1.5 pt-1", children: pkg.tags.map((tag) => (_jsxs("span", { className: "px-2 py-0.5 bg-muted/40 text-muted-foreground rounded text-[10px] font-mono", children: ["#", tag] }, tag))) })] }), _jsxs("div", { className: "pt-4 border-t border-border/40 flex items-center justify-between", children: [_jsxs("div", { className: "text-xs font-mono", children: [_jsx("span", { className: "text-muted-foreground", children: "Security Audit: " }), _jsxs("span", { className: "text-emerald-400 font-bold", children: [pkg.securityAuditScore, "%"] })] }), _jsx("button", { onClick: () => handleToggleInstall(pkg.id), className: `px-4 py-1.5 rounded-lg text-xs font-bold font-mono transition-all cursor-pointer ${isInstalled
                                            ? 'bg-muted/40 hover:bg-red-500/20 text-muted-foreground hover:text-red-400 border border-border/40'
                                            : 'bg-primary hover:bg-primary/90 text-primary-foreground'}`, children: isInstalled ? '✓ Installed (Uninstall)' : '⬇ 1-Click Install' })] })] }, pkg.id));
                }) })] }));
};
