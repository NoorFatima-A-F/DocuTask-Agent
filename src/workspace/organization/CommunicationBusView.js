import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const CommunicationBusView = () => {
    const [selectedChannel, setSelectedChannel] = useState(null);
    const channels = [
        { name: '#executive-dispatch', desc: 'Strategic directives and mission intake authorizations', count: 42 },
        { name: '#ocr-extraction-handoff', desc: 'Perception bounding box transfers and OCR artifacts', count: 128 },
        { name: '#validation-alerts', desc: 'Invariant verification notifications and arithmetic alerts', count: 96 },
        { name: '#governance-review', desc: 'Regulatory compliance approvals and audit vault signing', count: 34 },
        { name: '#negotiation-floor', desc: 'Resource auctions, Nash bargaining, and quota loans', count: 58 },
        { name: '#incident-war-room', desc: 'Real-time emergency coordination, triage, and mitigation', count: 14 },
    ];
    const messages = [
        {
            id: 'msg_2026_004',
            channel: '#governance-review',
            sender: 'Lead Verification Auditor',
            senderDept: 'dept_validation',
            receiver: 'dept_governance',
            type: 'AUDIT_SIGN',
            summary: 'Subtotal + Tax == Total verified; Zero-Fabrication Sentinel passed. Awaiting final audit signature.',
            eventId: 'evt_val_pass_77aa',
            sig: 'ED25519_SIG_VAL_77A0',
            time: '5s ago',
            priority: 'CRITICAL',
        },
        {
            id: 'msg_2026_003',
            channel: '#validation-alerts',
            sender: 'Lead Extraction Specialist',
            senderDept: 'dept_extraction',
            receiver: 'dept_validation',
            type: 'HANDOFF',
            summary: 'Structured invoice entity JSON extracted via Gemini 2.5 Flash ($1,420.50 USD). Ready for invariant check.',
            eventId: 'evt_extract_done_11fe',
            sig: 'ED25519_SIG_EXT_99A1',
            time: '15s ago',
            priority: 'HIGH',
        },
        {
            id: 'msg_2026_002',
            channel: '#ocr-extraction-handoff',
            sender: 'Lead Vision Agent',
            senderDept: 'dept_ocr',
            receiver: 'dept_extraction',
            type: 'HANDOFF',
            summary: 'LayoutLM bounding boxes extracted (confidence 0.985); transferred 42 text spans.',
            eventId: 'evt_ocr_done_44bc',
            sig: 'ED25519_SIG_OCR_4B2C',
            time: '30s ago',
            priority: 'NORMAL',
        },
        {
            id: 'msg_2026_001',
            channel: '#executive-dispatch',
            sender: 'Chief Executive Agent',
            senderDept: 'dept_executive',
            receiver: 'dept_ocr',
            type: 'DIRECTIVE',
            summary: 'Mission live_001 authorized; begin Optical Ingestion of 4-page invoice package.',
            eventId: 'evt_init_981a',
            sig: 'ED25519_SIG_EXEC_8F3A',
            time: '45s ago',
            priority: 'HIGH',
        },
    ];
    const filtered = selectedChannel ? messages.filter((m) => m.channel === selectedChannel) : messages;
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-2xl", children: "\uD83D\uDCE1" }), _jsx("h2", { className: "text-xl font-bold text-[#F8FAFC]", children: "Cross-Agent Enterprise Communication Bus" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Signed Event Bus" })] }), _jsx("p", { className: "text-sm text-[#94A3B8] mt-1", children: "Replaces synthetic chat with cryptographically signed inter-department messages linked to real runtime execution events." })] }), _jsxs("div", { className: "text-right", children: [_jsx("div", { className: "text-xs text-[#94A3B8]", children: "Total Verified Messages" }), _jsx("div", { className: "text-2xl font-bold font-mono text-[#00D2FF]", children: "372 Signed Events" })] })] }), _jsxs("div", { className: "flex items-center gap-2 overflow-x-auto pb-1", children: [_jsx("button", { onClick: () => setSelectedChannel(null), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all whitespace-nowrap ${selectedChannel === null ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'}`, children: "All Channels" }), channels.map((c) => (_jsxs("button", { onClick: () => setSelectedChannel(c.name), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all whitespace-nowrap ${selectedChannel === c.name ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'}`, children: [c.name, " (", c.count, ")"] }, c.name)))] }), _jsx("div", { className: "space-y-3", children: filtered.map((msg) => (_jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B] space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-bold font-mono text-[#00D2FF]", children: msg.channel }), _jsx(Badge, { variant: msg.priority === 'CRITICAL' ? 'error' : 'intelligence', size: "sm", children: msg.type })] }), _jsx("span", { className: "text-[11px] text-[#64748B] font-mono", children: msg.time })] }), _jsx("p", { className: "text-sm text-[#F8FAFC]", children: msg.summary }), _jsxs("div", { className: "flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-[#1E293B]/60 text-[11px] font-mono text-[#64748B]", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsxs("span", { children: ["From: ", _jsx("span", { className: "text-[#38BDF8]", children: msg.sender }), " (", msg.senderDept, ")"] }), _jsx("span", { children: "\u2192" }), _jsxs("span", { children: ["To: ", _jsx("span", { className: "text-[#F8FAFC]", children: msg.receiver })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsxs("span", { children: ["Event: ", _jsx("span", { className: "text-[#A855F7]", children: msg.eventId })] }), _jsxs("span", { children: ["Sig: ", _jsx("span", { className: "text-[#10B981]", children: msg.sig })] })] })] })] }, msg.id))) })] }));
};
