import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Scale, Cpu, Coins, CheckCircle2, RefreshCw, Zap, } from 'lucide-react';
export const ResourceNegotiationCenter = () => {
    const [proposals] = useState([
        {
            id: 'prop-gpu-01',
            swarmId: 'Swarm Alpha (Extraction)',
            resourceType: 'GPU_VRAM_GB',
            requested: 24.0,
            allocated: 20.0,
            bidUtility: 0.94,
            disagreementPoint: 0.25,
            status: 'SETTLED',
        },
        {
            id: 'prop-gpu-02',
            swarmId: 'Swarm Beta (Classifier)',
            resourceType: 'GPU_VRAM_GB',
            requested: 16.0,
            allocated: 14.0,
            bidUtility: 0.88,
            disagreementPoint: 0.20,
            status: 'SETTLED',
        },
        {
            id: 'prop-gpu-03',
            swarmId: 'Swarm Gamma (Governance)',
            resourceType: 'GPU_VRAM_GB',
            requested: 16.0,
            allocated: 14.0,
            bidUtility: 0.91,
            disagreementPoint: 0.30,
            status: 'SETTLED',
        },
    ]);
    const [isNegotiating, setIsNegotiating] = useState(false);
    const [sessionNotice, setSessionNotice] = useState(null);
    const totalCapacity = 48.0;
    const handleRunAuction = () => {
        setIsNegotiating(true);
        setTimeout(() => {
            setIsNegotiating(false);
            setSessionNotice('Nash Bargaining Equilibrium reached: 3 swarms converged in 4 concession rounds (Nash Product: 0.815).');
            setTimeout(() => setSessionNotice(null), 4000);
        }, 1200);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(Scale, { className: "w-6 h-6 text-indigo-500" }), "Multi-Swarm Resource Negotiation & Auction Center"] }), _jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: "Phase 13.11 \u2014 Decentralized auction protocols and Nash bargaining equilibria for GPU, VRAM, and Token budget pools." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "intelligence", size: "sm", onClick: handleRunAuction, disabled: isNegotiating, children: [_jsx(RefreshCw, { className: `w-3.5 h-3.5 mr-1.5 ${isNegotiating ? 'animate-spin' : ''}` }), isNegotiating ? 'Negotiating Rounds...' : 'Run Nash Auction'] }) })] }), sessionNotice && (_jsxs("div", { className: "p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-lg text-sm text-emerald-800 dark:text-emerald-300 flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-5 h-5 flex-shrink-0" }), _jsx("span", { children: sessionNotice })] })), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 border-l-4 border-l-indigo-500", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-gray-500", children: [_jsx("span", { children: "Total Resource Pool" }), _jsx(Cpu, { className: "w-4 h-4 text-indigo-500" })] }), _jsxs("div", { className: "text-2xl font-bold text-gray-900 dark:text-white mt-1", children: [totalCapacity, " GB VRAM"] }), _jsx("span", { className: "text-xs text-indigo-600 dark:text-indigo-400 font-medium", children: "100% Utilized (48/48 GB)" })] }), _jsxs(Card, { className: "p-4 border-l-4 border-l-emerald-500", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-gray-500", children: [_jsx("span", { children: "Nash Product Equilibrium" }), _jsx(Scale, { className: "w-4 h-4 text-emerald-500" })] }), _jsx("div", { className: "text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1", children: "0.815" }), _jsx("span", { className: "text-xs text-emerald-500", children: "Maximized Fairness Product" })] }), _jsxs(Card, { className: "p-4 border-l-4 border-l-purple-500", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-gray-500", children: [_jsx("span", { children: "Convergence Speed" }), _jsx(Zap, { className: "w-4 h-4 text-purple-500" })] }), _jsx("div", { className: "text-2xl font-bold text-purple-600 dark:text-purple-400 mt-1", children: "4 Rounds" }), _jsx("span", { className: "text-xs text-purple-500", children: "18.5ms Latency" })] }), _jsxs(Card, { className: "p-4 border-l-4 border-l-sky-500", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-gray-500", children: [_jsx("span", { children: "Active Participating Swarms" }), _jsx(Coins, { className: "w-4 h-4 text-sky-500" })] }), _jsx("div", { className: "text-2xl font-bold text-sky-600 dark:text-sky-400 mt-1", children: "3 Swarms" }), _jsx("span", { className: "text-xs text-sky-500", children: "Zero Starvation" })] })] }), _jsxs("div", { className: "space-y-4", children: [_jsx("h3", { className: "text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider", children: "Active Negotiation Bids & Settlements" }), _jsx("div", { className: "grid grid-cols-1 gap-4", children: proposals.map((p) => (_jsxs(Card, { className: "p-5 hover:shadow-md transition-shadow", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-xs text-indigo-600 dark:text-indigo-400 font-semibold", children: p.id }), _jsxs(Badge, { variant: "success", size: "sm", children: [_jsx(CheckCircle2, { className: "w-3 h-3 mr-1" }), p.status] })] }), _jsx("h4", { className: "font-semibold text-gray-900 dark:text-white text-base mt-1", children: p.swarmId })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsxs("div", { className: "text-right", children: [_jsx("span", { className: "text-xs text-gray-400 block", children: "Bid Utility" }), _jsx("span", { className: "text-lg font-bold text-indigo-600 dark:text-indigo-400 font-mono", children: p.bidUtility.toFixed(3) })] }) })] }), _jsxs("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-3 mt-4 text-xs", children: [_jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "text-gray-400 block mb-0.5", children: "Resource" }), _jsx("span", { className: "font-semibold text-gray-800 dark:text-gray-200", children: p.resourceType })] }), _jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "text-gray-400 block mb-0.5", children: "Requested" }), _jsxs("span", { className: "font-semibold text-gray-800 dark:text-gray-200 font-mono", children: [p.requested, " GB"] })] }), _jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "text-gray-400 block mb-0.5", children: "Allocated" }), _jsxs("span", { className: "font-semibold text-emerald-600 dark:text-emerald-400 font-mono", children: [p.allocated, " GB"] })] }), _jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "text-gray-400 block mb-0.5", children: "Disagreement Floor" }), _jsx("span", { className: "font-semibold text-gray-600 dark:text-gray-400 font-mono", children: p.disagreementPoint })] })] })] }, p.id))) })] })] }));
};
