import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Compass, Calendar, CheckCircle2, Clock, } from 'lucide-react';
export const StrategicRoadmapStudio = () => {
    const [selectedHorizon, setSelectedHorizon] = useState('90d');
    const roadmapData = {
        '30d': {
            title: '30-Day Rapid Throughput & Speculative Cache Rollout',
            theme: 'Low-Latency Cache Ingestion & Specialist Coalition Pre-Warming',
            budgetUsd: 4200.0,
            roiMultiplier: 3.80,
            milestones: [
                {
                    id: 'ms-30d-01',
                    title: 'Speculative Layout Cache Activation',
                    description: 'Zero-copy tensor cache for recurrent corporate invoice headers.',
                    targetDayOffset: 5,
                    durationDays: 5,
                    deliverables: ['Pre-warmed tensor buffer', 'Sub-50ms cache hit path'],
                    confidence: 0.988,
                    status: 'COMPLETED',
                    assignedSwarm: 'Optimization Swarm Alpha',
                    isCriticalPath: true,
                },
                {
                    id: 'ms-30d-02',
                    title: 'Triadic Strike Team Pre-Warming',
                    description: 'Pre-cluster extraction workers to eliminate runtime bidding latency.',
                    targetDayOffset: 12,
                    durationDays: 7,
                    deliverables: ['Triadic agent coalition template', '18% latency reduction'],
                    confidence: 0.975,
                    status: 'IN_PROGRESS',
                    assignedSwarm: 'Swarm Coalition Beta',
                    isCriticalPath: true,
                },
                {
                    id: 'ms-30d-03',
                    title: '30-Day Benchmark Audit & Certification',
                    description: 'Run automated stress benchmarks and export truth verification certificate.',
                    targetDayOffset: 28,
                    durationDays: 4,
                    deliverables: ['Signed provenance audit', '100k doc/day throughput verification'],
                    confidence: 0.992,
                    status: 'PENDING',
                    assignedSwarm: 'Executive Governance Oracle',
                    isCriticalPath: true,
                },
            ],
        },
        '90d': {
            title: '90-Day Enterprise Strategic Expansion',
            theme: 'Multi-Swarm Autonomous Governance & Digital Twin Decisioning',
            budgetUsd: 14500.0,
            roiMultiplier: 3.45,
            milestones: [
                {
                    id: 'ms-90d-01',
                    title: 'Predictive Digital Twin Synchronization Sub-20ms',
                    description: 'Live twin state telemetry across all active worker swarms.',
                    targetDayOffset: 20,
                    durationDays: 15,
                    deliverables: ['Sub-20ms twin sync', 'Pareto optimal Monte Carlo engine'],
                    confidence: 0.980,
                    status: 'COMPLETED',
                    assignedSwarm: 'World Model Core',
                    isCriticalPath: true,
                },
                {
                    id: 'ms-90d-02',
                    title: 'Autonomous Multi-Swarm Resource Negotiation',
                    description: 'Nash-equilibrium auction protocols for GPU and token distribution.',
                    targetDayOffset: 45,
                    durationDays: 20,
                    deliverables: ['Decentralized token exchange', 'Dynamic GPU priority scheduler'],
                    confidence: 0.965,
                    status: 'IN_PROGRESS',
                    assignedSwarm: 'Swarm Negotiation Bus',
                    isCriticalPath: true,
                },
                {
                    id: 'ms-90d-03',
                    title: 'Executive Strategic Decision Support System',
                    description: 'AI Chief Strategy Officer (CSO) dashboard with continuous MCDA.',
                    targetDayOffset: 85,
                    durationDays: 25,
                    deliverables: ['Executive Cockpit UI', '100% cryptographically audited approvals'],
                    confidence: 0.970,
                    status: 'PENDING',
                    assignedSwarm: 'Executive Strategy Runtime',
                    isCriticalPath: true,
                },
            ],
        },
        '180d': {
            title: '180-Day Semi-Annual Scale & Self-Improvement',
            theme: 'Institutional Memory Synthesis & Long-Horizon Policy Evolution',
            budgetUsd: 28000.0,
            roiMultiplier: 4.10,
            milestones: [
                {
                    id: 'ms-180d-01',
                    title: 'Institutional Knowledge Graph Expansion',
                    description: 'Consolidate 100,000+ mission traces into reusable organizational playbooks.',
                    targetDayOffset: 60,
                    durationDays: 30,
                    deliverables: ['Playbook knowledge store', 'Continuous anti-pattern detector'],
                    confidence: 0.955,
                    status: 'PENDING',
                    assignedSwarm: 'Institutional Memory Core',
                    isCriticalPath: true,
                },
                {
                    id: 'ms-180d-02',
                    title: 'Continuous Multi-Year Goal Evolution Engine',
                    description: 'Autonomous strategy mutation and Pareto rebalancing.',
                    targetDayOffset: 150,
                    durationDays: 45,
                    deliverables: ['Self-updating roadmaps', 'Automated budget reallocation'],
                    confidence: 0.940,
                    status: 'PENDING',
                    assignedSwarm: 'Cognitive Evolution Swarm',
                    isCriticalPath: true,
                },
            ],
        },
        '365d': {
            title: '365-Day Fully Autonomous Cognitive Enterprise',
            theme: 'Zero-Human-Intervention Autonomous Enterprise Strategy Execution',
            budgetUsd: 55000.0,
            roiMultiplier: 5.50,
            milestones: [
                {
                    id: 'ms-365d-01',
                    title: 'Autonomous Corporate Strategy Orchestration',
                    description: 'End-to-end mission portfolio decomposition and self-executing governance.',
                    targetDayOffset: 300,
                    durationDays: 65,
                    deliverables: ['Autonomous CSO agent runtime', 'Multi-datacenter swarm federation'],
                    confidence: 0.925,
                    status: 'PENDING',
                    assignedSwarm: 'Global Enterprise Federation',
                    isCriticalPath: true,
                },
            ],
        },
    };
    const currentRoadmap = roadmapData[selectedHorizon];
    const getStatusBadge = (status) => {
        switch (status) {
            case 'COMPLETED':
                return (_jsxs(Badge, { variant: "success", size: "sm", children: [_jsx(CheckCircle2, { className: "w-3 h-3 mr-1" }), "COMPLETED"] }));
            case 'IN_PROGRESS':
                return (_jsxs(Badge, { variant: "warning", size: "sm", children: [_jsx(Clock, { className: "w-3 h-3 mr-1" }), "IN PROGRESS"] }));
            case 'PENDING':
                return (_jsx(Badge, { variant: "default", size: "sm", children: "PENDING" }));
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(Compass, { className: "w-6 h-6 text-indigo-500" }), "Strategic Multi-Horizon Roadmap Studio"] }), _jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: "Phase 13.11 \u2014 Autonomous 30d, 90d, 180d, and 365-day strategic execution roadmaps with weighted interval critical path analysis." })] }), _jsx("div", { className: "flex items-center gap-2 bg-gray-100 dark:bg-gray-800 p-1 rounded-lg", children: ['30d', '90d', '180d', '365d'].map((h) => (_jsxs("button", { onClick: () => setSelectedHorizon(h), className: `px-3 py-1.5 text-xs font-semibold rounded-md transition-colors ${selectedHorizon === h
                                ? 'bg-indigo-600 text-white shadow-sm'
                                : 'text-gray-600 dark:text-gray-300 hover:text-indigo-600'}`, children: [h.toUpperCase(), " Roadmap"] }, h))) })] }), _jsx(Card, { className: "p-5 border-l-4 border-l-indigo-600 bg-indigo-50/20 dark:bg-indigo-950/20", children: _jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Badge, { variant: "intelligence", size: "sm", children: [selectedHorizon.toUpperCase(), " HORIZON"] }), _jsx("h3", { className: "text-lg font-bold text-gray-900 dark:text-white", children: currentRoadmap.title })] }), _jsxs("p", { className: "text-xs text-gray-500 dark:text-gray-400 mt-1", children: ["Theme: ", currentRoadmap.theme] })] }), _jsxs("div", { className: "flex items-center gap-6", children: [_jsxs("div", { className: "text-right", children: [_jsx("span", { className: "text-xs text-gray-400 block", children: "Estimated Budget" }), _jsxs("span", { className: "text-lg font-bold text-gray-900 dark:text-white font-mono", children: ["$", currentRoadmap.budgetUsd.toLocaleString()] })] }), _jsxs("div", { className: "text-right", children: [_jsx("span", { className: "text-xs text-gray-400 block", children: "Projected ROI" }), _jsxs("span", { className: "text-lg font-bold text-emerald-600 dark:text-emerald-400 font-mono", children: [currentRoadmap.roiMultiplier, "x"] })] })] })] }) }), _jsxs("div", { className: "space-y-4", children: [_jsxs("h3", { className: "text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider flex items-center gap-2", children: [_jsx(Calendar, { className: "w-4 h-4 text-indigo-500" }), "Milestones & Critical Path Timeline"] }), _jsx("div", { className: "relative border-l-2 border-indigo-200 dark:border-indigo-900 ml-4 space-y-6 pb-2", children: currentRoadmap.milestones.map((ms) => (_jsxs("div", { className: "relative pl-6", children: [_jsx("div", { className: "absolute -left-[9px] top-1.5 w-4 h-4 rounded-full bg-indigo-600 border-2 border-white dark:border-gray-900" }), _jsxs(Card, { className: "p-5 hover:shadow-md transition-shadow", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-xs text-indigo-600 dark:text-indigo-400 font-semibold", children: ms.id }), _jsxs("span", { className: "text-xs text-gray-400", children: ["Day +", ms.targetDayOffset, " (", ms.durationDays, "d duration)"] }), ms.isCriticalPath && (_jsx(Badge, { variant: "warning", size: "sm", children: "CRITICAL PATH" }))] }), _jsx("h4", { className: "font-semibold text-gray-900 dark:text-white text-base mt-1", children: ms.title }), _jsx("p", { className: "text-xs text-gray-500 dark:text-gray-400 mt-0.5", children: ms.description })] }), _jsx("div", { className: "flex items-center gap-3", children: getStatusBadge(ms.status) })] }), _jsxs("div", { className: "mt-4 grid grid-cols-1 md:grid-cols-2 gap-4 text-xs", children: [_jsxs("div", { children: [_jsx("span", { className: "text-gray-400 block mb-1", children: "Key Deliverables:" }), _jsx("div", { className: "space-y-1", children: ms.deliverables.map((d, dIdx) => (_jsxs("div", { className: "flex items-center gap-1.5 text-gray-700 dark:text-gray-300", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5 text-emerald-500 flex-shrink-0" }), _jsx("span", { children: d })] }, dIdx))) })] }), _jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-gray-400", children: "Assigned Swarm:" }), _jsx("span", { className: "font-semibold text-indigo-600 dark:text-indigo-400", children: ms.assignedSwarm })] }), _jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-gray-400", children: "Bayesian Confidence:" }), _jsxs("span", { className: "font-semibold text-purple-600 dark:text-purple-400", children: [(ms.confidence * 100).toFixed(1), "%"] })] })] })] })] })] }, ms.id))) })] })] }));
};
