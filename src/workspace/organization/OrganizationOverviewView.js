import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const OrganizationOverviewView = () => {
    const [selectedDept, setSelectedDept] = useState(null);
    const departments = [
        {
            id: 'dept_executive',
            name: 'Executive Coordination & Strategy',
            head: 'Chief Executive Agent',
            workers: 2,
            concurrency: 8,
            queue: 1,
            health: 99.2,
            budget: '$50.00',
            spent: '$2.14',
            status: 'ACTIVE',
            slaTarget: '100 ms',
            responsibilities: ['Mission intake & portfolio arbitration', 'Organization-wide budgeting', 'Root escalation handling'],
        },
        {
            id: 'dept_ocr',
            name: 'Optical Perception & Ingestion',
            head: 'Lead Vision Agent',
            workers: 4,
            concurrency: 12,
            queue: 3,
            health: 96.5,
            budget: '$30.00',
            spent: '$4.82',
            status: 'ACTIVE',
            slaTarget: '250 ms',
            responsibilities: ['Multi-format document ingestion', 'Bilateral filter de-skewing', 'LayoutLM token bounding boxes'],
        },
        {
            id: 'dept_extraction',
            name: 'Structured Intelligence & Extraction',
            head: 'Lead Extraction Specialist',
            workers: 6,
            concurrency: 20,
            queue: 4,
            health: 98.1,
            budget: '$80.00',
            spent: '$12.45',
            status: 'ACTIVE',
            slaTarget: '600 ms',
            responsibilities: ['Key-value entity resolution', 'Line-item table parsing', 'Pareto model routing (Flash vs Pro)'],
        },
        {
            id: 'dept_validation',
            name: 'Mathematical & Invariant Validation',
            head: 'Lead Verification Auditor',
            workers: 3,
            concurrency: 16,
            queue: 1,
            health: 99.8,
            budget: '$20.00',
            spent: '$1.12',
            status: 'ACTIVE',
            slaTarget: '80 ms',
            responsibilities: ['Subtotal + Tax == Total verification', 'Zero-Fabrication bounding-box checks', 'Z3 SMT solver proving'],
        },
        {
            id: 'dept_memory',
            name: 'Enterprise Memory & Context',
            head: 'Chief Knowledge Custodian',
            workers: 2,
            concurrency: 10,
            queue: 0,
            health: 99.5,
            budget: '$25.00',
            spent: '$1.95',
            status: 'ACTIVE',
            slaTarget: '50 ms',
            responsibilities: ['Vector similarity lookup', 'Vendor historical graph indexing', 'Episodic memory recall'],
        },
        {
            id: 'dept_research',
            name: 'Research & Policy Synthesis',
            head: 'Director of Autonomous Research',
            workers: 2,
            concurrency: 6,
            queue: 1,
            health: 97.4,
            budget: '$40.00',
            spent: '$5.60',
            status: 'ACTIVE',
            slaTarget: '1200 ms',
            responsibilities: ['Counterfactual digital twin replays', 'Causal graph discovery', 'Prompt adaptation benchmarking'],
        },
        {
            id: 'dept_governance',
            name: 'Corporate Governance & Compliance',
            head: 'Chief Governance Officer',
            workers: 2,
            concurrency: 8,
            queue: 0,
            health: 100.0,
            budget: '$15.00',
            spent: '$0.85',
            status: 'ACTIVE',
            slaTarget: '75 ms',
            responsibilities: ['Dual-key cryptographic sign-off', 'ED25519 audit trail vaulting', 'Data privacy policy enforcement'],
        },
        {
            id: 'dept_qa',
            name: 'Continuous Quality Assurance',
            head: 'Lead QA Sentinel',
            workers: 3,
            concurrency: 12,
            queue: 2,
            health: 98.9,
            budget: '$30.00',
            spent: '$3.40',
            status: 'ACTIVE',
            slaTarget: '150 ms',
            responsibilities: ['Corpus-wide benchmark scoring', 'Confidence calibration & ECE', 'Data distribution drift detection'],
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-2xl", children: "\uD83C\uDFDB\uFE0F" }), _jsx("h2", { className: "text-xl font-bold text-[#F8FAFC]", children: "Autonomous Enterprise Organization (AMAEOP)" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Phase 7 Live Digital Org" })] }), _jsx("p", { className: "text-sm text-[#94A3B8] mt-1", children: "Enterprise multi-agent organization with specialized departmental hierarchy, resource ownership, and autonomous governance." })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsxs("div", { className: "text-right", children: [_jsx("div", { className: "text-xs text-[#94A3B8]", children: "Organization Health Index" }), _jsx("div", { className: "text-lg font-bold font-mono text-[#10B981]", children: "98.7% (Tier 1 Optimal)" })] }), _jsx("div", { className: "w-px h-8 bg-[#1E293B]" }), _jsxs("div", { className: "text-right", children: [_jsx("div", { className: "text-xs text-[#94A3B8]", children: "Active AI Workforce" }), _jsx("div", { className: "text-lg font-bold font-mono text-[#00D2FF]", children: "24 Agents (8 Depts)" })] })] })] }), _jsxs("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 bg-[#0F172A]/80 border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8] uppercase", children: "Macro SLA Compliance" }), _jsx("div", { className: "text-2xl font-bold font-mono text-[#10B981] mt-1", children: "99.7%" }), _jsx("div", { className: "text-[11px] text-[#64748B] mt-1", children: "Target: > 99.0%" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A]/80 border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8] uppercase", children: "Zero-Fabrication Rate" }), _jsx("div", { className: "text-2xl font-bold font-mono text-[#00D2FF] mt-1", children: "100.0%" }), _jsx("div", { className: "text-[11px] text-[#64748B] mt-1", children: "Invariant-verified arithmetic" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A]/80 border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8] uppercase", children: "Total Org Budget" }), _jsx("div", { className: "text-2xl font-bold font-mono text-[#F59E0B] mt-1", children: "$290.00" }), _jsx("div", { className: "text-[11px] text-[#64748B] mt-1", children: "Spent: $32.33 (11.1% burn)" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A]/80 border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8] uppercase", children: "Queued Workload" }), _jsx("div", { className: "text-2xl font-bold font-mono text-[#A855F7] mt-1", children: "12 Tasks" }), _jsx("div", { className: "text-[11px] text-[#64748B] mt-1", children: "Max cluster depth: 92 slots" })] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4", children: departments.map((dept) => {
                    const isSelected = selectedDept === dept.id;
                    return (_jsxs("div", { onClick: () => setSelectedDept(isSelected ? null : dept.id), className: `p-4 rounded-xl border transition-all cursor-pointer flex flex-col justify-between ${isSelected
                            ? 'bg-[#131D35] border-[#00D2FF] shadow-[0_0_15px_rgba(0,210,255,0.2)]'
                            : 'bg-[#0F172A] border-[#1E293B] hover:border-[#334155]'}`, children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between gap-2", children: [_jsx("span", { className: "text-xs font-mono font-bold text-[#F8FAFC] truncate", children: dept.name }), _jsxs(Badge, { variant: dept.health >= 98 ? 'success' : 'warning', size: "sm", children: [dept.health, "%"] })] }), _jsxs("div", { className: "text-[11px] text-[#94A3B8] mt-1", children: ["Head: ", _jsx("span", { className: "text-[#38BDF8] font-medium", children: dept.head })] }), _jsxs("div", { className: "grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-[#1E293B]/60 text-xs font-mono", children: [_jsxs("div", { children: [_jsx("span", { className: "text-[#64748B] text-[10px] block", children: "AGENTS / SLOTS" }), _jsxs("span", { className: "text-[#F8FAFC]", children: [dept.workers, " / ", dept.concurrency] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[#64748B] text-[10px] block", children: "QUEUE DEPTH" }), _jsxs("span", { className: "text-[#F59E0B]", children: [dept.queue, " items"] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[#64748B] text-[10px] block", children: "SLA TARGET" }), _jsx("span", { className: "text-[#10B981]", children: dept.slaTarget })] }), _jsxs("div", { children: [_jsx("span", { className: "text-[#64748B] text-[10px] block", children: "BUDGET SPENT" }), _jsxs("span", { className: "text-[#CBD5E1]", children: [dept.spent, " / ", dept.budget] })] })] })] }), _jsxs("div", { className: "mt-3 pt-2 border-t border-[#1E293B]/40", children: [_jsx("div", { className: "text-[10px] text-[#64748B] uppercase font-mono mb-1", children: "Key Responsibility" }), _jsx("div", { className: "text-[11px] text-[#94A3B8] line-clamp-1", children: dept.responsibilities[0] })] })] }, dept.id));
                }) }), selectedDept && (_jsx(Card, { className: "p-5 bg-[#0F172A] border-[#00D2FF]/40 animate-fadeIn", children: (() => {
                    const d = departments.find((dept) => dept.id === selectedDept);
                    return (_jsxs("div", { className: "space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-lg font-bold text-[#F8FAFC]", children: d.name }), _jsx(Badge, { variant: "intelligence", size: "sm", children: d.id })] }), _jsx("button", { onClick: () => setSelectedDept(null), className: "text-xs text-[#94A3B8] hover:text-[#F8FAFC] font-mono px-2 py-1 rounded bg-[#1E293B]", children: "\u2715 Close" })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: [_jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8] uppercase", children: "Department Leadership" }), _jsx("div", { className: "text-sm font-semibold text-[#38BDF8] mt-1", children: d.head }), _jsx("div", { className: "text-xs text-[#64748B] mt-1", children: "Autonomous decision authority under Delegation Policy" })] }), _jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8] uppercase", children: "SLA & Health Governance" }), _jsxs("div", { className: "text-sm font-semibold text-[#10B981] mt-1", children: [d.health, "% Operational Health"] }), _jsxs("div", { className: "text-xs text-[#64748B] mt-1", children: ["Target latency ceiling: ", d.slaTarget] })] }), _jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8] uppercase", children: "Fiscal Allocation" }), _jsxs("div", { className: "text-sm font-semibold text-[#F59E0B] mt-1", children: [d.spent, " spent of ", d.budget] }), _jsx("div", { className: "text-xs text-[#64748B] mt-1", children: "Vickrey Auction bidding credits active" })] })] }), _jsxs("div", { children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8] uppercase mb-2", children: "Charter & Responsibilities" }), _jsx("ul", { className: "grid grid-cols-1 md:grid-cols-2 gap-2 text-xs text-[#CBD5E1]", children: d.responsibilities.map((resp, idx) => (_jsxs("li", { className: "flex items-center gap-2 p-2 rounded bg-[#020617]/50 border border-[#1E293B]/60", children: [_jsx("span", { className: "text-[#00D2FF]", children: "\u2713" }), _jsx("span", { children: resp })] }, idx))) })] })] }));
                })() }))] }));
};
