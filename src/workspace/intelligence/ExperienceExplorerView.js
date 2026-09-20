import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const ExperienceExplorerView = () => {
    const [selectedDomain, setSelectedDomain] = useState('ALL');
    const experiences = [
        {
            id: 'exp_001_inv',
            missionId: 'msn_1001',
            domain: 'Invoice',
            task: 'Extraction & Compliance',
            latency: 940.5,
            cost: 0.0084,
            confidence: 0.978,
            retries: 0,
            evidenceRoot: '0x8f2a...c31b',
            status: 'SUCCESS',
            plannerVer: 'v2.1.0',
            timestamp: '2 mins ago',
        },
        {
            id: 'exp_002_con',
            missionId: 'msn_1002',
            domain: 'Contract',
            task: 'Clause & Indemnity Audit',
            latency: 2150.0,
            cost: 0.0342,
            confidence: 0.942,
            retries: 0,
            evidenceRoot: '0x3c7e...b44a',
            status: 'SUCCESS',
            plannerVer: 'v2.0.4',
            timestamp: '6 mins ago',
        },
        {
            id: 'exp_003_med',
            missionId: 'msn_1003',
            domain: 'Medical',
            task: 'HIPAA & Clinical Trials',
            latency: 1820.0,
            cost: 0.0265,
            confidence: 0.965,
            retries: 1,
            evidenceRoot: '0x991a...fe82',
            status: 'RECOVERED',
            plannerVer: 'v2.0.4',
            timestamp: '12 mins ago',
        },
        {
            id: 'exp_004_inv',
            missionId: 'msn_1004',
            domain: 'Invoice',
            task: 'Multi-Line Item Tax Extraction',
            latency: 1020.0,
            cost: 0.0092,
            confidence: 0.985,
            retries: 0,
            evidenceRoot: '0x661d...009a',
            status: 'SUCCESS',
            plannerVer: 'v2.1.0',
            timestamp: '18 mins ago',
        },
    ];
    const filtered = selectedDomain === 'ALL' ? experiences : experiences.filter((e) => e.domain.toUpperCase() === selectedDomain);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Experience Intelligence Explorer" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Pillar 1" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Immutable repository of operational experiences with cryptographic hash chaining and Merkle root evidence linkage." })] }), _jsx("div", { className: "flex items-center gap-2", children: ['ALL', 'INVOICE', 'CONTRACT', 'MEDICAL'].map((dom) => (_jsx("button", { onClick: () => setSelectedDomain(dom), className: `text-xs px-2.5 py-1 rounded transition-colors font-medium ${selectedDomain === dom ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground hover:bg-muted/80'}`, children: dom }, dom))) })] }), _jsx(Card, { className: "p-0 overflow-hidden", children: _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left text-xs border-collapse", children: [_jsx("thead", { children: _jsxs("tr", { className: "border-b border-border/40 bg-muted/20 font-semibold text-muted-foreground", children: [_jsx("th", { className: "p-3", children: "Experience ID" }), _jsx("th", { className: "p-3", children: "Mission ID" }), _jsx("th", { className: "p-3", children: "Domain & Task" }), _jsx("th", { className: "p-3", children: "Latency (ms)" }), _jsx("th", { className: "p-3", children: "Cost ($)" }), _jsx("th", { className: "p-3", children: "Confidence" }), _jsx("th", { className: "p-3", children: "Evidence Merkle Root" }), _jsx("th", { className: "p-3", children: "Status" })] }) }), _jsx("tbody", { className: "divide-y divide-border/20", children: filtered.map((exp) => (_jsxs("tr", { className: "hover:bg-muted/10 transition-colors", children: [_jsx("td", { className: "p-3 font-mono text-primary font-semibold", children: exp.id }), _jsx("td", { className: "p-3 font-mono text-foreground", children: exp.missionId }), _jsxs("td", { className: "p-3", children: [_jsx("div", { className: "font-medium text-foreground", children: exp.domain }), _jsx("div", { className: "text-[11px] text-muted-foreground", children: exp.task })] }), _jsx("td", { className: "p-3 font-mono", children: exp.latency }), _jsxs("td", { className: "p-3 font-mono", children: ["$", exp.cost.toFixed(4)] }), _jsx("td", { className: "p-3 font-mono", children: _jsxs("span", { className: "text-emerald-400", children: [(exp.confidence * 100).toFixed(1), "%"] }) }), _jsx("td", { className: "p-3 font-mono text-xs text-muted-foreground", children: exp.evidenceRoot }), _jsx("td", { className: "p-3", children: _jsx(Badge, { variant: exp.status === 'SUCCESS' ? 'success' : 'warning', size: "sm", children: exp.status }) })] }, exp.id))) })] }) }) })] }));
};
