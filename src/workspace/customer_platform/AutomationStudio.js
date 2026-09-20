import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
export const AutomationStudio = () => {
    const [activeTab, setActiveTab] = useState('ACTIVE');
    const pipelines = [
        {
            id: 'PIPE-01',
            name: 'AP Autonomous Invoice Ingestion & ERP Posting',
            industry: 'Finance',
            status: 'LIVE',
            processedToday: 1420,
            accuracy: '99.4%',
            avgSpeed: '4.5s',
            guardrails: 'Confidence > 95%',
        },
        {
            id: 'PIPE-02',
            name: 'Technical Candidate Screening & Vector Ranking',
            industry: 'Human Resources',
            status: 'LIVE',
            processedToday: 240,
            accuracy: '96.5%',
            avgSpeed: '3.2s',
            guardrails: 'Strict Anonymization',
        },
        {
            id: 'PIPE-03',
            name: 'Commercial Contract Clause Risk Review',
            industry: 'Legal',
            status: 'PAUSED',
            processedToday: 45,
            accuracy: '98.5%',
            avgSpeed: '12.0s',
            guardrails: 'Legal Counsel Signoff',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-[#0F172A] to-[#1E293B] border border-[#334155]/60 shadow-xl", children: [_jsxs("div", { children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: "ENTERPRISE AUTOMATION STUDIO" }), _jsx("h1", { className: "text-2xl font-black text-white mt-1", children: "Autonomous AI Pipelines" }), _jsx("p", { className: "text-sm text-[#94A3B8]", children: "Configure, deploy, and govern end-to-end multi-agent document intelligence workflows." })] }), _jsxs("div", { className: "flex gap-3", children: [_jsx(Button, { variant: "secondary", size: "md", children: "+ Import Template" }), _jsx(Button, { variant: "primary", size: "md", children: "+ Create Workflow" })] })] }), _jsx("div", { className: "flex gap-2 border-b border-[#1E293B] pb-3", children: ['ACTIVE', 'DRAFT', 'MARKETPLACE'].map((tab) => (_jsxs("button", { onClick: () => setActiveTab(tab), className: `px-4 py-2 rounded-xl text-xs font-bold transition-all ${activeTab === tab
                        ? 'bg-[#0066FF] text-white shadow-lg shadow-[#0066FF]/25'
                        : 'bg-[#0F172A] text-[#94A3B8] hover:text-white border border-[#1E293B]'}`, children: [tab === 'ACTIVE' && 'Active Pipelines (3)', tab === 'DRAFT' && 'Drafts & Revisions (2)', tab === 'MARKETPLACE' && 'Template Library (5)'] }, tab))) }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6", children: pipelines.map((pipe) => (_jsxs("div", { className: "p-6 rounded-2xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xl hover:border-[#00D2FF]/40 transition-all flex flex-col justify-between space-y-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx(Badge, { variant: "default", size: "sm", children: pipe.industry }), _jsx("span", { className: `px-2 py-0.5 rounded text-[10px] font-bold ${pipe.status === 'LIVE' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800/40' : 'bg-gray-800 text-gray-400'}`, children: pipe.status })] }), _jsx("h3", { className: "text-base font-bold text-white mb-2", children: pipe.name }), _jsxs("p", { className: "text-xs text-[#94A3B8] font-mono", children: ["Guardrails: ", pipe.guardrails] })] }), _jsxs("div", { className: "grid grid-cols-3 gap-2 py-3 border-y border-[#1E293B] text-center", children: [_jsxs("div", { children: [_jsx("span", { className: "text-[10px] text-[#94A3B8] block", children: "Today" }), _jsx("span", { className: "text-xs font-bold text-white", children: pipe.processedToday })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[10px] text-[#94A3B8] block", children: "Accuracy" }), _jsx("span", { className: "text-xs font-bold text-emerald-400", children: pipe.accuracy })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[10px] text-[#94A3B8] block", children: "Latency" }), _jsx("span", { className: "text-xs font-bold text-cyan-400", children: pipe.avgSpeed })] })] }), _jsxs("div", { className: "flex gap-2", children: [_jsx(Button, { variant: "secondary", size: "sm", className: "w-full", children: "Edit DAG" }), _jsx(Button, { variant: "outline", size: "sm", className: "w-full", children: "Analytics" })] })] }, pipe.id))) })] }));
};
