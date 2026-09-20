import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const NegotiationStudioView = () => {
    const [selectedTab, setSelectedTab] = useState('AUCTIONS');
    const auctions = [
        {
            id: 'auc_gpu_2026_01',
            resource: 'GPU_OCR_SLOT (4 Units)',
            winner: 'Extraction Department',
            winningBid: '85.0 Credits',
            clearingPrice: '62.0 Credits (Vickrey 2nd Price)',
            status: 'SETTLED',
            bids: [
                { dept: 'Extraction Department', amount: '85.0', utility: '0.95' },
                { dept: 'OCR Department', amount: '62.0', utility: '0.80' },
                { dept: 'Research Department', amount: '45.0', utility: '0.65' },
            ],
        },
    ];
    const trades = [
        {
            id: 'prop_trade_001',
            initiator: 'OCR Department',
            target: 'Research Department',
            offered: '2x OCR Worker Threads',
            requested: '50,000 Gemini Pro Tokens',
            duration: '300 seconds',
            status: 'ACCEPTED',
            rationale: 'Trading idle night worker threads for research token quota to parse multi-page dense ledger.',
        },
    ];
    const contracts = [
        {
            id: 'ctr_ocr_ext_001',
            provider: 'OCR Department',
            consumer: 'Extraction Department',
            resource: 'OCR_BOUNDING_BOX_STREAM',
            committedCapacity: '10.0 docs/sec',
            slaLatency: '< 250 ms',
            penaltyRate: '2.5 credits/sec',
            signature: 'ED25519_SIG_8F3A20B1',
            status: 'ACTIVE',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-2xl", children: "\u2696\uFE0F" }), _jsx("h2", { className: "text-xl font-bold text-[#F8FAFC]", children: "Autonomous Resource Negotiation & Market Floor" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Game-Theoretic Economy" })] }), _jsx("p", { className: "text-sm text-[#94A3B8] mt-1", children: "Vickrey second-price auctions, bilateral resource trades, Nash Bargaining allocations, and signed SLA contracts." })] }), _jsxs("div", { className: "flex gap-2", children: [_jsx("button", { onClick: () => setSelectedTab('AUCTIONS'), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${selectedTab === 'AUCTIONS' ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'}`, children: "Vickrey Auctions" }), _jsx("button", { onClick: () => setSelectedTab('TRADES'), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${selectedTab === 'TRADES' ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'}`, children: "Bilateral Trades" }), _jsx("button", { onClick: () => setSelectedTab('CONTRACTS'), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${selectedTab === 'CONTRACTS' ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'}`, children: "SLA Contracts" }), _jsx("button", { onClick: () => setSelectedTab('NASH'), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${selectedTab === 'NASH' ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'}`, children: "Nash Bargaining" })] })] }), selectedTab === 'AUCTIONS' && (_jsx("div", { className: "space-y-4", children: auctions.map((auc) => (_jsxs(Card, { className: "p-5 bg-[#0F172A] border-[#1E293B] space-y-4", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-base font-bold text-[#F8FAFC]", children: auc.resource }), _jsx(Badge, { variant: "success", size: "sm", children: auc.status })] }), _jsxs("div", { className: "text-xs text-[#94A3B8] font-mono mt-1", children: ["Winner: ", _jsx("span", { className: "text-[#38BDF8] font-bold", children: auc.winner }), " | Winning Bid: ", auc.winningBid] })] }), _jsxs("div", { className: "text-right", children: [_jsx("div", { className: "text-xs text-[#64748B] font-mono uppercase", children: "Vickrey Clearing Price" }), _jsx("div", { className: "text-sm font-bold font-mono text-[#10B981] mt-0.5", children: auc.clearingPrice })] })] }), _jsxs("div", { children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8] uppercase mb-2", children: "Sealed Bids Received" }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-3", children: auc.bids.map((b, idx) => (_jsxs("div", { className: "p-3 rounded-lg bg-[#020617] border border-[#1E293B] text-xs font-mono", children: [_jsx("div", { className: "text-[#F8FAFC] font-semibold", children: b.dept }), _jsxs("div", { className: "text-[#F59E0B] font-bold mt-1", children: [b.amount, " Credits"] }), _jsxs("div", { className: "text-[#64748B] text-[10px] mt-0.5", children: ["Utility Weight: ", b.utility] })] }, idx))) })] })] }, auc.id))) })), selectedTab === 'TRADES' && (_jsx("div", { className: "space-y-3", children: trades.map((t) => (_jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B] space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsxs("span", { className: "text-sm font-bold text-[#F8FAFC]", children: [t.initiator, " \u21C4 ", t.target] }), _jsx(Badge, { variant: "success", size: "sm", children: t.status })] }), _jsxs("span", { className: "text-xs text-[#64748B] font-mono", children: ["Duration: ", t.duration] })] }), _jsx("div", { className: "text-xs text-[#94A3B8]", children: t.rationale }), _jsxs("div", { className: "grid grid-cols-2 gap-4 p-2 rounded bg-[#020617] border border-[#1E293B]/60 text-xs font-mono", children: [_jsxs("div", { children: ["Offered: ", _jsx("span", { className: "text-[#10B981]", children: t.offered })] }), _jsxs("div", { children: ["Requested: ", _jsx("span", { className: "text-[#00D2FF]", children: t.requested })] })] })] }, t.id))) })), selectedTab === 'CONTRACTS' && (_jsx("div", { className: "space-y-3", children: contracts.map((c) => (_jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B] space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-sm font-bold text-[#F8FAFC]", children: c.resource }), _jsx(Badge, { variant: "intelligence", size: "sm", children: c.status })] }), _jsx("span", { className: "text-xs text-[#10B981] font-mono font-semibold", children: c.signature })] }), _jsxs("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-2 text-xs font-mono text-[#94A3B8]", children: [_jsxs("div", { children: ["Provider: ", _jsx("span", { className: "text-[#F8FAFC]", children: c.provider })] }), _jsxs("div", { children: ["Consumer: ", _jsx("span", { className: "text-[#F8FAFC]", children: c.consumer })] }), _jsxs("div", { children: ["Committed Capacity: ", _jsx("span", { className: "text-[#00D2FF]", children: c.committedCapacity })] }), _jsxs("div", { children: ["SLA Guarantee: ", _jsx("span", { className: "text-[#F59E0B]", children: c.slaLatency })] })] })] }, c.id))) })), selectedTab === 'NASH' && (_jsxs(Card, { className: "p-5 bg-[#0F172A] border-[#1E293B] space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsx("span", { className: "text-sm font-bold text-[#F8FAFC]", children: "Nash Bargaining Pareto Frontier Allocation" }), _jsx("p", { className: "text-xs text-[#94A3B8] mt-1", children: "Maximizes joint surplus product: max (U_A - d_A)^0.6 * (U_B - d_B)^0.4 over 100 available GPU slots." })] }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "PARETO OPTIMAL" })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: [_jsxs("div", { className: "p-4 rounded-xl bg-[#020617] border border-[#1E293B] space-y-2", children: [_jsx("div", { className: "text-xs font-mono text-[#38BDF8] font-bold", children: "Extraction Department (Weight 0.6)" }), _jsx("div", { className: "text-2xl font-bold font-mono text-[#F8FAFC]", children: "58.0 Units" }), _jsx("div", { className: "text-[11px] text-[#64748B]", children: "Disagreement fallback payoff: 10.0 units" })] }), _jsxs("div", { className: "p-4 rounded-xl bg-[#020617] border border-[#1E293B] space-y-2", children: [_jsx("div", { className: "text-xs font-mono text-[#10B981] font-bold", children: "OCR Department (Weight 0.4)" }), _jsx("div", { className: "text-2xl font-bold font-mono text-[#F8FAFC]", children: "42.0 Units" }), _jsx("div", { className: "text-[11px] text-[#64748B]", children: "Disagreement fallback payoff: 10.0 units" })] })] })] }))] }));
};
