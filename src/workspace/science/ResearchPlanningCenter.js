import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { MapPin, Cpu, TrendingUp, Compass, CheckCircle2, Calendar, } from 'lucide-react';
export const ResearchPlanningCenter = () => {
    const [allocationNotice, setAllocationNotice] = useState(null);
    const streams = [
        {
            id: 'stream-01',
            name: 'Low-Latency Speculative Acceleration',
            domain: 'Memory & Caching',
            priority: 'BREAKTHROUGH',
            computeUnits: 64,
            activeHypotheses: 2,
            completedExperiments: 5,
            deliverable: 'Sub-150ms P95 universal document extraction across all schemas.',
        },
        {
            id: 'stream-02',
            name: 'Swarm Triadic Coordination Dynamics',
            domain: 'Swarm Intelligence',
            priority: 'HIGH',
            computeUnits: 48,
            activeHypotheses: 1,
            completedExperiments: 3,
            deliverable: 'Elimination of auction bidding latency under >10,000 tasks/min.',
        },
        {
            id: 'stream-03',
            name: 'Deterministic Memory Provenance & Replay',
            domain: 'Resilience & Truth',
            priority: 'HIGH',
            computeUnits: 32,
            activeHypotheses: 1,
            completedExperiments: 4,
            deliverable: 'Zero-overhead continuous audit replay verification.',
        },
    ];
    const handleReallocateCompute = () => {
        setAllocationNotice('Autonomous Research Scheduler dynamically re-allocated 64 compute units to Breakthrough Stream-01 based on high EIG score (0.915).');
        setTimeout(() => setAllocationNotice(null), 4000);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(MapPin, { className: "w-6 h-6 text-indigo-500" }), "Strategic Research Planning & Roadmap Center"] }), _jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: "Coordinates parallel scientific research streams, schedules autonomous compute unit budgets, and tracks strategic milestones." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "intelligence", size: "sm", onClick: handleReallocateCompute, children: [_jsx(Cpu, { className: "w-3.5 h-3.5 mr-1.5" }), "Optimize Compute Allocation"] }) })] }), allocationNotice && (_jsxs("div", { className: "p-4 bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800 rounded-lg text-sm text-indigo-800 dark:text-indigo-300 flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-5 h-5 flex-shrink-0" }), _jsx("span", { children: allocationNotice })] })), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 border-l-4 border-l-indigo-500", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-gray-500", children: [_jsx("span", { children: "Total Compute Budget" }), _jsx(Cpu, { className: "w-4 h-4 text-indigo-500" })] }), _jsx("div", { className: "text-2xl font-bold text-gray-900 dark:text-white mt-1", children: "192 Units" }), _jsx("span", { className: "text-xs text-indigo-600", children: "144 Allocated / 48 Buffer" })] }), _jsxs(Card, { className: "p-4 border-l-4 border-l-emerald-500", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-gray-500", children: [_jsx("span", { children: "Active Scientific Streams" }), _jsx(Compass, { className: "w-4 h-4 text-emerald-500" })] }), _jsx("div", { className: "text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1", children: "3 Streams" }), _jsx("span", { className: "text-xs text-emerald-500", children: "1 Breakthrough Priority" })] }), _jsxs(Card, { className: "p-4 border-l-4 border-l-purple-500", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-gray-500", children: [_jsx("span", { children: "Research ROI Multiplier" }), _jsx(TrendingUp, { className: "w-4 h-4 text-purple-500" })] }), _jsx("div", { className: "text-2xl font-bold text-purple-600 dark:text-purple-400 mt-1", children: "4.10x" }), _jsx("span", { className: "text-xs text-purple-500", children: "Value of verified laws vs compute cost" })] }), _jsxs(Card, { className: "p-4 border-l-4 border-l-amber-500", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-gray-500", children: [_jsx("span", { children: "Roadmap Horizon" }), _jsx(Calendar, { className: "w-4 h-4 text-amber-500" })] }), _jsx("div", { className: "text-2xl font-bold text-amber-600 dark:text-amber-400 mt-1", children: "2026-Q4" }), _jsx("span", { className: "text-xs text-amber-500", children: "3 of 5 Milestones Achieved" })] })] }), _jsx("div", { className: "space-y-4", children: streams.map(stream => (_jsxs(Card, { className: "p-5 space-y-4", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-gray-100 dark:border-gray-800 pb-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-xs text-indigo-500 font-semibold", children: stream.id }), _jsxs(Badge, { variant: "outline", size: "sm", children: ["Domain: ", stream.domain] }), _jsx(Badge, { variant: stream.priority === 'BREAKTHROUGH' ? 'warning' : 'info', size: "sm", children: stream.priority })] }), _jsx("h3", { className: "text-base font-semibold text-gray-900 dark:text-white mt-1", children: stream.name })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Badge, { variant: "intelligence", size: "sm", children: [_jsx(Cpu, { className: "w-3.5 h-3.5 mr-1" }), stream.computeUnits, " Compute Units"] }) })] }), _jsxs("p", { className: "text-xs text-gray-600 dark:text-gray-300", children: [_jsx("strong", { className: "text-gray-800 dark:text-gray-200", children: "Target Deliverable:" }), " ", stream.deliverable] }), _jsxs("div", { className: "grid grid-cols-2 gap-4 bg-gray-50 dark:bg-gray-800/40 p-3 rounded-lg text-xs", children: [_jsxs("div", { children: [_jsx("span", { className: "text-gray-400", children: "Active Hypotheses:" }), _jsx("div", { className: "font-bold text-gray-900 dark:text-white text-sm", children: stream.activeHypotheses })] }), _jsxs("div", { children: [_jsx("span", { className: "text-gray-400", children: "Completed Empirical Experiments:" }), _jsx("div", { className: "font-bold text-emerald-600 dark:text-emerald-400 text-sm", children: stream.completedExperiments })] })] })] }, stream.id))) })] }));
};
