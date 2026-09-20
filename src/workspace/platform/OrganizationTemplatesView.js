import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const OrganizationTemplatesView = () => {
    const [deployedId, setDeployedId] = useState(null);
    const templates = [
        {
            id: 'tpl-healthcare-hospital',
            name: 'Regional Hospital Health System',
            industry: 'HEALTHCARE',
            icon: '🏥',
            description: 'Configures Clinical Ingestion, Medical Billing, HIPAA Privacy Shield, and Patient Record OCR.',
            departments: ['Executive', 'OCR', 'Clinical Extraction', 'HIPAA Compliance', 'QA'],
            plugins: ['plugin.medical.records', 'plugin.invoice.processing'],
            sla: '400 ms',
        },
        {
            id: 'tpl-finance-bank',
            name: 'Commercial & Investment Bank',
            industry: 'BANKING',
            icon: '🏦',
            description: 'Configures KYB/KYC Verification, Loan Application Parsing, Treasury Reconciliation, and Four-Eyes Governance.',
            departments: ['Executive', 'OCR', 'Financial Extraction', 'AML Compliance', 'Governance'],
            plugins: ['plugin.invoice.processing', 'plugin.legal.contracts'],
            sla: '250 ms',
        },
        {
            id: 'tpl-legal-lawfirm',
            name: 'Corporate Law & M&A Firm',
            industry: 'LEGAL',
            icon: '⚖️',
            description: 'Deploys Clause Risk Analyzer, Regulatory Redlining, Non-Compete Reviewers, and Forensic Evidence DAG.',
            departments: ['Executive', 'Perception', 'Clause Analysis', 'Risk Review', 'Forensic Audit'],
            plugins: ['plugin.legal.contracts'],
            sla: '500 ms',
        },
        {
            id: 'tpl-insurance-carrier',
            name: 'P&C Insurance Carrier',
            industry: 'INSURANCE',
            icon: '🛡️',
            description: 'Automates First Notice of Loss (FNOL), Medical Injury Extraction, Adjuster Fraud Detection, and Payout Validation.',
            departments: ['Executive', 'Perception', 'Claims Extraction', 'Fraud Detection', 'QA'],
            plugins: ['plugin.medical.records', 'plugin.invoice.processing'],
            sla: '350 ms',
        },
    ];
    const handleDeploy = (tplId) => {
        setDeployedId(tplId);
        setTimeout(() => {
            setDeployedId(null);
        }, 2500);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Organization Blueprint Templates" }), _jsx(Badge, { variant: "success", size: "sm", children: "1-Click Enterprise Deployment" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Instantiate full-scale multi-department autonomous organizations with pre-configured plugins, policies, and SLA targets." })] }), _jsxs(Badge, { variant: "outline", size: "md", children: [templates.length, " Industry Blueprints"] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6", children: templates.map((tpl) => {
                    const isJustDeployed = deployedId === tpl.id;
                    return (_jsxs(Card, { className: "p-6 space-y-4 flex flex-col justify-between", children: [_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("span", { className: "text-3xl", children: tpl.icon }), _jsxs("div", { children: [_jsx("h2", { className: "text-base font-bold text-foreground", children: tpl.name }), _jsxs("div", { className: "text-xs text-muted-foreground mt-0.5", children: [tpl.industry, " Blueprint"] })] })] }), _jsxs(Badge, { variant: "intelligence", size: "sm", children: ["SLA: ", tpl.sla] })] }), _jsx("p", { className: "text-xs text-muted-foreground leading-relaxed", children: tpl.description }), _jsxs("div", { className: "space-y-1 text-xs", children: [_jsx("div", { className: "font-semibold text-muted-foreground", children: "Pre-Configured Departments:" }), _jsx("div", { className: "flex flex-wrap gap-1", children: tpl.departments.map((d) => (_jsx("span", { className: "px-2 py-0.5 bg-muted/40 rounded text-[11px] font-mono text-foreground", children: d }, d))) })] })] }), _jsxs("div", { className: "pt-4 border-t border-border/40 flex items-center justify-between", children: [_jsxs("div", { className: "text-xs font-mono text-muted-foreground", children: ["Bundles ", tpl.plugins.length, " Plugins"] }), _jsx("button", { onClick: () => handleDeploy(tpl.id), disabled: isJustDeployed, className: `px-4 py-2 rounded-lg text-xs font-bold font-mono transition-all cursor-pointer ${isJustDeployed
                                            ? 'bg-emerald-600 text-white'
                                            : 'bg-primary hover:bg-primary/90 text-primary-foreground'}`, children: isJustDeployed ? '✓ Organization Deployed!' : '🚀 1-Click Provision' })] })] }, tpl.id));
                }) })] }));
};
