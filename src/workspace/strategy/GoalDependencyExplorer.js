import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Network, CheckCircle2, ArrowRight, ShieldCheck, } from 'lucide-react';
export const GoalDependencyExplorer = () => {
    const [nodes] = useState([
        {
            id: 'goal-root-scale-100k',
            title: 'Scale Multi-Swarm Processing to 100k Daily Documents',
            type: 'ROOT',
            priority: 'CRITICAL',
            status: 'ACTIVE',
            dependsOn: [],
        },
        {
            id: 'goal-sub-cache-warm',
            title: 'Deploy Speculative Zero-Copy Embedding Cache',
            type: 'SUBGOAL',
            priority: 'HIGH',
            status: 'ACTIVE',
            dependsOn: [
                {
                    targetId: 'goal-root-scale-100k',
                    type: 'ENABLING',
                    criticality: 0.95,
                },
            ],
        },
        {
            id: 'goal-sub-strike-teams',
            title: 'Form Triadic Specialist Swarm Strike Teams',
            type: 'SUBGOAL',
            priority: 'HIGH',
            status: 'ACTIVE',
            dependsOn: [
                {
                    targetId: 'goal-sub-cache-warm',
                    type: 'ENABLING',
                    criticality: 0.80,
                },
            ],
        },
        {
            id: 'goal-root-gov-integrity',
            title: 'Attain Continuous 100% Cryptographic Auditability',
            type: 'ROOT',
            priority: 'CRITICAL',
            status: 'ACTIVE',
            dependsOn: [],
        },
    ]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(Network, { className: "w-6 h-6 text-indigo-500" }), "Strategic Goal Dependency & Conflict Graph"] }), _jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: "Phase 13.11 \u2014 Cross-departmental goal topological ordering, blocking dependency resolution, and circular deadlock prevention." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Badge, { variant: "success", size: "md", children: [_jsx(ShieldCheck, { className: "w-3.5 h-3.5 mr-1" }), "Topologically Sorted \u2022 0 Deadlocks"] }) })] }), _jsx("div", { className: "grid grid-cols-1 gap-4", children: nodes.map((node) => (_jsxs(Card, { className: "p-5 hover:shadow-md transition-shadow", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-xs text-indigo-600 dark:text-indigo-400 font-semibold", children: node.id }), _jsx(Badge, { variant: node.type === 'ROOT' ? 'intelligence' : 'default', size: "sm", children: node.type }), _jsx(Badge, { variant: "warning", size: "sm", children: node.priority })] }), _jsx("h4", { className: "font-semibold text-gray-900 dark:text-white text-base mt-1", children: node.title })] }), _jsxs(Badge, { variant: "success", size: "sm", children: [_jsx(CheckCircle2, { className: "w-3 h-3 mr-1" }), node.status] })] }), _jsxs("div", { className: "mt-4 text-xs space-y-2", children: [_jsx("span", { className: "text-gray-400 block font-medium", children: "Topological Dependency Links:" }), node.dependsOn.length === 0 ? (_jsx("p", { className: "text-gray-500 italic", children: "No incoming blocking dependencies (Root node)." })) : (_jsx("div", { className: "space-y-1.5", children: node.dependsOn.map((dep, dIdx) => (_jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800 flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(ArrowRight, { className: "w-3.5 h-3.5 text-indigo-500" }), _jsx("span", { className: "text-gray-700 dark:text-gray-300", children: "Requires Target:" }), _jsx("span", { className: "font-mono text-indigo-600 dark:text-indigo-400 font-semibold", children: dep.targetId })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsxs("span", { className: "text-gray-400", children: ["Type: ", _jsx("strong", { className: "text-gray-700 dark:text-gray-300", children: dep.type })] }), _jsxs("span", { className: "text-gray-400", children: ["Criticality: ", _jsxs("strong", { className: "text-purple-600 dark:text-purple-400", children: [(dep.criticality * 100).toFixed(0), "%"] })] })] })] }, dIdx))) }))] })] }, node.id))) })] }));
};
