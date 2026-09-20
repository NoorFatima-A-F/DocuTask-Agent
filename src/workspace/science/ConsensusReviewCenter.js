import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Scale, ShieldCheck, CheckCircle2, RefreshCw, } from 'lucide-react';
export const ConsensusReviewCenter = () => {
    const [isArbitrating, setIsArbitrating] = useState(false);
    const [arbitrationNotice, setArbitrationNotice] = useState(null);
    const reviews = [
        {
            id: 'rev-cache-invariance-01',
            topic: 'Speculative Tensor Layout Invariance in Enterprise Accounting Streams',
            consensusType: 'UNANIMOUS',
            votes: {
                'agent-peer-oracle-alpha': 'APPROVE',
                'agent-peer-oracle-beta': 'APPROVE',
                'agent-peer-oracle-gamma': 'APPROVE',
                'agent-peer-oracle-delta': 'APPROVE',
            },
            approvalPct: 100.0,
            dissentNotes: [],
            reviewedAt: '2026-09-12T18:42:00Z',
        },
        {
            id: 'rev-triadic-swarm-02',
            topic: 'Triadic Swarm Specialization Protocol Scalability',
            consensusType: 'SUPERMAJORITY',
            votes: {
                'agent-peer-oracle-alpha': 'APPROVE',
                'agent-peer-oracle-beta': 'APPROVE',
                'agent-peer-oracle-gamma': 'APPROVE',
                'agent-peer-oracle-delta': 'REJECT',
            },
            approvalPct: 75.0,
            dissentNotes: [
                'agent-peer-oracle-delta: Expresses concern over edge cases with network packet loss > 5%. Recommended safety boundary.',
            ],
            reviewedAt: '2026-09-12T16:15:00Z',
        },
    ];
    const handleArbitrate = () => {
        setIsArbitrating(true);
        setTimeout(() => {
            setIsArbitrating(false);
            setArbitrationNotice('Multi-Agent Tribunal convened: 4 of 4 agents cast affirmative Bayesian votes. Consensus officially certified.');
            setTimeout(() => setArbitrationNotice(null), 4000);
        }, 1500);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(Scale, { className: "w-6 h-6 text-amber-500" }), "Multi-Agent Peer Review & Consensus Tribunal"] }), _jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: "Conducts independent multi-agent peer review tribunals, aggregates Bayesian belief consensus, and records minority dissents." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "intelligence", size: "sm", onClick: handleArbitrate, disabled: isArbitrating, children: [_jsx(RefreshCw, { className: `w-3.5 h-3.5 mr-1.5 ${isArbitrating ? 'animate-spin' : ''}` }), isArbitrating ? 'Convening Tribunal...' : 'Convene Review Tribunal'] }) })] }), arbitrationNotice && (_jsxs("div", { className: "p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-lg text-sm text-emerald-800 dark:text-emerald-300 flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-5 h-5 flex-shrink-0" }), _jsx("span", { children: arbitrationNotice })] })), _jsx("div", { className: "space-y-4", children: reviews.map(review => (_jsxs(Card, { className: "p-5 space-y-4", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-gray-100 dark:border-gray-800 pb-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-xs text-amber-500 font-semibold", children: review.id }), _jsx(Badge, { variant: review.consensusType === 'UNANIMOUS' ? 'success' : 'warning', size: "sm", children: review.consensusType })] }), _jsx("h3", { className: "text-base font-semibold text-gray-900 dark:text-white mt-1", children: review.topic })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Badge, { variant: "outline", size: "sm", children: ["Approval: ", _jsxs("strong", { className: "text-emerald-600 ml-1", children: [review.approvalPct, "%"] })] }) })] }), _jsxs("div", { children: [_jsx("span", { className: "text-xs font-semibold text-gray-500 uppercase", children: "Tribunal Agent Ballots" }), _jsx("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-3 mt-2", children: Object.entries(review.votes).map(([agent, vote]) => (_jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-800/40 rounded border border-gray-100 dark:border-gray-700 text-xs", children: [_jsx("div", { className: "font-mono text-[10px] text-gray-400 truncate", children: agent }), _jsxs("div", { className: "mt-1 flex items-center justify-between", children: [_jsx("span", { className: "font-semibold text-gray-800 dark:text-gray-200", children: vote }), vote === 'APPROVE' ? (_jsx(CheckCircle2, { className: "w-3.5 h-3.5 text-emerald-500" })) : (_jsx(ShieldCheck, { className: "w-3.5 h-3.5 text-amber-500" }))] })] }, agent))) })] }), review.dissentNotes.length > 0 && (_jsxs("div", { className: "p-3 bg-amber-50/50 dark:bg-amber-950/20 rounded border border-amber-200 dark:border-amber-800/40 text-xs", children: [_jsx("span", { className: "font-semibold text-amber-900 dark:text-amber-300", children: "Minority Dissenting Opinions:" }), _jsx("ul", { className: "mt-1 list-disc list-inside text-amber-800 dark:text-amber-400 space-y-0.5", children: review.dissentNotes.map((d, i) => (_jsx("li", { children: d }, i))) })] })), _jsxs("div", { className: "flex items-center justify-between text-xs text-gray-400 pt-1 border-t border-gray-100 dark:border-gray-800", children: [_jsx("span", { children: "Arbitration Algorithm: Bayesian Aggregation" }), _jsxs("span", { children: ["Conducted: ", new Date(review.reviewedAt).toLocaleString()] })] })] }, review.id))) })] }));
};
