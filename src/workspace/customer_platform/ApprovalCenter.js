import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
export const ApprovalCenter = () => {
    const [selectedApproval, setSelectedApproval] = useState('APP-2026-001');
    const pendingApprovals = [
        {
            id: 'APP-2026-001',
            doc: 'Invoice_GlobalLogistics_INV-8891.pdf',
            type: 'Vendor Invoice',
            confidence: 0.982,
            vendor: 'Acme Global Solutions Inc.',
            amount: '$14,500.50',
            reason: 'Standard AP Fast-Track. Matched PO #PO-9912.',
        },
        {
            id: 'APP-2026-002',
            doc: 'Master_Services_Agreement_Nexus.pdf',
            type: 'Legal Contract',
            confidence: 0.945,
            vendor: 'Nexus Enterprise Corp',
            amount: 'N/A',
            reason: 'Non-standard indemnification clause detected (Page 4).',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-[#0F172A] to-[#1E293B] border border-[#334155]/60 shadow-xl", children: [_jsxs("div", { children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: "HUMAN-AI COLLABORATION WORKSPACE" }), _jsx("h1", { className: "text-2xl font-black text-white mt-1", children: "Supervisory Approval & Exception Center" }), _jsx("p", { className: "text-sm text-[#94A3B8]", children: "Review visual bounding-box citations, resolve edge cases, and train agent policies with single-click feedback." })] }), _jsx(Badge, { variant: "warning", size: "md", children: "2 Pending Reviews" })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "p-5 rounded-2xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xl space-y-3", children: [_jsx("h2", { className: "text-sm font-bold text-white uppercase tracking-wider text-[#94A3B8]", children: "Pending Queue" }), _jsx("div", { className: "space-y-2.5", children: pendingApprovals.map((item) => (_jsxs("div", { onClick: () => setSelectedApproval(item.id), className: `p-4 rounded-xl border transition-all cursor-pointer space-y-2 ${selectedApproval === item.id
                                        ? 'bg-[#0066FF]/10 border-[#00D2FF] shadow-[0_0_12px_rgba(0,210,255,0.2)]'
                                        : 'bg-[#0A0F1D] border-[#1E293B] hover:border-gray-600'}`, children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx(Badge, { variant: "default", size: "sm", children: item.type }), _jsxs("span", { className: "text-xs font-mono text-emerald-400 font-bold", children: [(item.confidence * 100).toFixed(1), "% Conf"] })] }), _jsx("h3", { className: "text-xs font-bold text-white truncate", children: item.doc }), _jsx("span", { className: "text-[11px] text-[#94A3B8] block", children: item.vendor })] }, item.id))) })] }), _jsxs("div", { className: "lg:col-span-2 p-6 rounded-2xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xl space-y-5", children: [_jsxs("div", { className: "flex items-center justify-between pb-3 border-b border-[#1E293B]", children: [_jsxs("div", { children: [_jsx("h2", { className: "text-base font-bold text-white", children: "Invoice_GlobalLogistics_INV-8891.pdf" }), _jsx("span", { className: "text-xs text-[#94A3B8]", children: "Acme Global Solutions Inc. \u2022 Total: $14,500.50" })] }), _jsx("span", { className: "text-xs font-mono text-emerald-400 bg-emerald-950 px-2.5 py-1 rounded-lg border border-emerald-800", children: "Matched PO #PO-9912" })] }), _jsxs("div", { className: "p-6 rounded-xl bg-[#0A0F1D] border border-[#1E293B] space-y-4 font-mono text-xs text-[#CBD5E1]", children: [_jsxs("div", { className: "p-3 rounded bg-blue-950/40 border border-blue-500/50 flex items-center justify-between", children: [_jsx("span", { children: "[Bounding Box P1:L2] Vendor Name:" }), _jsx("span", { className: "text-cyan-300 font-bold", children: "Acme Global Solutions Inc. (99.8% Conf)" })] }), _jsxs("div", { className: "p-3 rounded bg-emerald-950/40 border border-emerald-500/50 flex items-center justify-between", children: [_jsx("span", { children: "[Bounding Box P1:L8] Invoice Total Amount:" }), _jsx("span", { className: "text-emerald-300 font-bold", children: "$14,500.50 USD (99.5% Conf)" })] }), _jsxs("div", { className: "p-3 rounded bg-purple-950/40 border border-purple-500/50 flex items-center justify-between", children: [_jsx("span", { children: "[Bounding Box P1:L15] 3-Way NetSuite Match:" }), _jsx("span", { className: "text-purple-300 font-bold", children: "PO-9912 Verified (100.0% Match)" })] })] }), _jsxs("div", { className: "flex flex-col sm:flex-row gap-3 pt-2", children: [_jsx(Button, { variant: "primary", size: "md", className: "w-full sm:w-auto flex-1 bg-emerald-600 hover:bg-emerald-500", children: "\u2713 Approve & Post to ERP" }), _jsx(Button, { variant: "secondary", size: "md", className: "w-full sm:w-auto flex-1", children: "\u270F\uFE0F Edit Extracted Fields" }), _jsx(Button, { variant: "outline", size: "md", className: "w-full sm:w-auto text-rose-400 border-rose-800/60 hover:bg-rose-950/30", children: "\u2715 Reject Invoice" })] })] })] })] }));
};
