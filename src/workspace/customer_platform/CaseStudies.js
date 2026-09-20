import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
export const CaseStudies = () => {
    const [selectedScript, setSelectedScript] = useState('RECRUITER');
    const scripts = {
        RECRUITER: {
            title: '5-Minute Recruiter & Hiring Manager Script',
            duration: '5 Minutes',
            hook: '"I built DocuTask Agent—an enterprise-grade autonomous AI document automation platform that turns complex, messy business workflows into deterministic, self-healing multi-agent systems that save companies millions."',
            points: [
                'Demonstrated 99.0% extraction accuracy, sub-300ms P95 latency, and $2.28M annual ROI.',
                'Engineered complete multi-agent orchestration, SRE self-healing, and human-in-the-loop governance.',
                'Pure-Python synchronous execution guarantees 100% deterministic testability and reproducibility.',
            ],
            cta: '"I architected this to prove my ability as a Principal AI Automation Engineer who builds resilient, compliant, high-ROI enterprise systems."',
        },
        CLIENT: {
            title: '10-Minute Executive / Prospective Client Script',
            duration: '10 Minutes',
            hook: '"If your team spends thousands of hours manually reviewing invoices or contracts, you are losing money on labor and delays. Let me show you how DocuTask cuts processing costs by 92.8% without changing your existing ERP."',
            points: [
                'Turnkey onboarding in under 5 minutes using pre-configured industry templates.',
                'Zero rip-and-replace: Connects directly to Outlook, Google Drive, QuickBooks, and SAP.',
                'Human supervisors maintain complete control with visual bounding-box citations and custom approval thresholds.',
            ],
            cta: '"We can deploy a pilot template for your accounts payable or HR team in one afternoon. Let us schedule a proof of concept."',
        },
        ARCHITECT: {
            title: '30-Minute Principal Architect Deep-Dive',
            duration: '30 Minutes',
            hook: '"DocuTask is designed as a distributed, event-driven multi-agent cognitive architecture with deterministic execution guarantees and autonomous fault recovery."',
            points: [
                'Layered DAG builder with topological cycle detection and schema validation.',
                'SRE fault tolerance: MTTR < 2.2s, 100% automated fault recovery across chaos benchmarks.',
                'Cryptographic tenant isolation with KMS keys and immutable audit ledgers.',
            ],
            cta: '"I would be glad to dive deeper into our state management, vector retrieval strategies, or horizontal autoscaling designs."',
        },
    };
    const curr = scripts[selectedScript];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-[#0F172A] to-[#1E293B] border border-[#334155]/60 shadow-xl", children: [_jsxs("div", { children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: "PORTFOLIO PRESENTATION LAYER" }), _jsx("h1", { className: "text-2xl font-black text-white mt-1", children: "Enterprise Case Studies & Demo Scripts" }), _jsx("p", { className: "text-sm text-[#94A3B8]", children: "Audience-targeted presentation scripts and verified enterprise case studies." })] }), _jsx("div", { className: "flex gap-2", children: ['RECRUITER', 'CLIENT', 'ARCHITECT'].map((sc) => (_jsxs("button", { onClick: () => setSelectedScript(sc), className: `px-3.5 py-2 rounded-xl text-xs font-bold transition-all ${selectedScript === sc
                                ? 'bg-[#0066FF] text-white shadow-lg shadow-[#0066FF]/25'
                                : 'bg-[#0A0F1D] text-[#94A3B8] hover:text-white border border-[#1E293B]'}`, children: [sc === 'RECRUITER' && '5-Min Recruiter', sc === 'CLIENT' && '10-Min Client', sc === 'ARCHITECT' && '30-Min Tech Interview'] }, sc))) })] }), _jsxs("div", { className: "p-8 rounded-2xl bg-[#0F172A]/80 border border-[#1E293B] shadow-2xl space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-[#1E293B] pb-4", children: [_jsx("h2", { className: "text-lg font-bold text-white", children: curr.title }), _jsx(Badge, { variant: "outline", size: "sm", children: curr.duration })] }), _jsxs("div", { className: "p-5 rounded-xl bg-gradient-to-r from-[#0066FF]/10 to-transparent border border-[#0066FF]/30 space-y-2", children: [_jsx("span", { className: "text-xs font-bold text-cyan-400 uppercase font-mono", children: "Opening Hook" }), _jsx("p", { className: "text-sm italic text-white leading-relaxed", children: curr.hook })] }), _jsxs("div", { className: "space-y-3", children: [_jsx("span", { className: "text-xs font-bold text-[#94A3B8] uppercase font-mono block", children: "Key Talking Points" }), _jsx("div", { className: "space-y-2", children: curr.points.map((pt, idx) => (_jsxs("div", { className: "p-3.5 rounded-xl bg-[#0A0F1D] border border-[#1E293B] flex items-start gap-3", children: [_jsxs("span", { className: "text-cyan-400 font-bold font-mono", children: ["0", idx + 1, "."] }), _jsx("span", { className: "text-xs text-[#CBD5E1] leading-relaxed", children: pt })] }, idx))) })] }), _jsxs("div", { className: "p-4 rounded-xl bg-[#0A0F1D] border border-emerald-500/30 space-y-1", children: [_jsx("span", { className: "text-xs font-bold text-emerald-400 uppercase font-mono", children: "Closing Call to Action" }), _jsx("p", { className: "text-xs text-white italic", children: curr.cta })] })] })] }));
};
