import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
export const TemplateMarketplace = () => {
    const [selectedIndustry, setSelectedIndustry] = useState('ALL');
    const templates = [
        {
            id: 'TMPL-FIN-01',
            title: 'Autonomous Invoice Processing & ERP Sync',
            industry: 'Finance',
            rating: 4.95,
            deployTime: '5 min',
            desc: 'Automates PDF email invoice parsing, line-item extraction, 3-way PO matching, and QuickBooks/SAP posting.',
            impact: '92.8% cost reduction • 4.5s processing time',
            featured: true,
        },
        {
            id: 'TMPL-HR-02',
            title: 'Candidate Resume Screening & Competency Matcher',
            industry: 'Human Resources',
            rating: 4.90,
            deployTime: '4 min',
            desc: 'Parses bulk candidate CVs, generates semantic vector rankings against job descriptions, and triggers calendar invites.',
            impact: '99.3% faster shortlisting • 96.5% matching accuracy',
            featured: true,
        },
        {
            id: 'TMPL-LEG-03',
            title: 'Commercial Contract Clause Risk & Compliance Review',
            industry: 'Legal',
            rating: 4.92,
            deployTime: '6 min',
            desc: 'Analyzes master agreements for non-standard indemnification, liability caps, and compliance obligations.',
            impact: '99.0% review cycle reduction • 98.5% risk coverage',
            featured: true,
        },
        {
            id: 'TMPL-HLT-04',
            title: 'Clinical Prior Authorization & Claims Triage',
            industry: 'Healthcare',
            rating: 4.88,
            deployTime: '7 min',
            desc: 'Validates clinical notes against ICD-10/CPT guidelines with HIPAA-compliant cryptographic partitioning.',
            impact: '72 hours to 12 seconds • 97.8% clinical precision',
            featured: false,
        },
        {
            id: 'TMPL-SUP-05',
            title: 'Customer Support Ticket Multi-Agent Triage',
            industry: 'Customer Operations',
            rating: 4.85,
            deployTime: '3 min',
            desc: 'Classifies inbound inquiries, retrieves account context via RAG, and drafts high-confidence responses.',
            impact: '99.5% faster response • +36% first-contact resolution',
            featured: false,
        },
    ];
    const filtered = selectedIndustry === 'ALL' ? templates : templates.filter((t) => t.industry.toUpperCase().includes(selectedIndustry));
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-[#0F172A] to-[#1E293B] border border-[#334155]/60 shadow-xl", children: [_jsxs("div", { children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: "AI AUTOMATION MARKETPLACE" }), _jsx("h1", { className: "text-2xl font-black text-white mt-1", children: "Turnkey Enterprise Solution Templates" }), _jsx("p", { className: "text-sm text-[#94A3B8]", children: "Pre-configured, production-certified multi-agent workflows ready for 1-click deployment." })] }), _jsx("div", { className: "flex gap-2", children: ['ALL', 'FINANCE', 'HR', 'LEGAL', 'HEALTHCARE'].map((ind) => (_jsx("button", { onClick: () => setSelectedIndustry(ind), className: `px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${selectedIndustry === ind
                                ? 'bg-[#0066FF] text-white shadow-md'
                                : 'bg-[#0A0F1D] text-[#94A3B8] hover:text-white border border-[#1E293B]'}`, children: ind }, ind))) })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6", children: filtered.map((tmpl) => (_jsxs("div", { className: "p-6 rounded-2xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xl hover:border-[#00D2FF]/40 transition-all flex flex-col justify-between space-y-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx(Badge, { variant: "default", size: "sm", children: tmpl.industry }), _jsxs("span", { className: "text-xs text-amber-400 font-mono", children: ["\u2605 ", tmpl.rating] })] }), _jsx("h3", { className: "text-base font-bold text-white mb-2", children: tmpl.title }), _jsx("p", { className: "text-xs text-[#94A3B8] leading-relaxed mb-3", children: tmpl.desc }), _jsxs("div", { className: "p-2.5 rounded-xl bg-[#0A0F1D] border border-[#1E293B] text-[11px] text-emerald-400 font-medium", children: ["\uD83C\uDFAF ", tmpl.impact] })] }), _jsxs("div", { className: "pt-2 flex items-center justify-between border-t border-[#1E293B]", children: [_jsxs("span", { className: "text-xs text-[#64748B]", children: ["Deploy in ", tmpl.deployTime] }), _jsx(Button, { variant: "primary", size: "sm", children: "Deploy Solution" })] })] }, tmpl.id))) })] }));
};
