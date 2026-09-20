import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { GitBranch, CheckCircle2, RefreshCw, Layers, } from 'lucide-react';
export const GoalEvolutionCenter = () => {
    const [goals, setGoals] = useState([
        {
            id: 'goal-root-scale-100k',
            title: 'Scale Multi-Swarm Processing to 100k Daily Documents',
            description: 'Expand agentic extraction capacity with sub-250ms SLA and zero accuracy degradation.',
            priority: 'CRITICAL',
            status: 'ACTIVE',
            horizon: 'DAYS_90',
            utilityScore: 0.965,
            confidence: 0.982,
            ageDays: 12,
            costUsd: 2400.0,
            latencyGainPct: 35.0,
            subgoalsCount: 2,
            tags: ['scalability', 'swarm', 'throughput'],
        },
        {
            id: 'goal-sub-cache-warm',
            title: 'Deploy Speculative Zero-Copy Embedding Cache',
            description: 'Pre-compute document layout representations across recurrent corporate invoice templates.',
            priority: 'HIGH',
            status: 'ACTIVE',
            horizon: 'DAYS_30',
            utilityScore: 0.920,
            confidence: 0.990,
            ageDays: 5,
            costUsd: 450.0,
            latencyGainPct: 22.0,
            subgoalsCount: 0,
            tags: ['caching', 'latency', 'gpu'],
        },
        {
            id: 'goal-sub-strike-teams',
            title: 'Form Triadic Specialist Swarm Strike Teams',
            description: 'Pre-cluster extraction workers by document taxonomy to reduce inter-agent bidding friction.',
            priority: 'HIGH',
            status: 'ACTIVE',
            horizon: 'DAYS_30',
            utilityScore: 0.895,
            confidence: 0.975,
            ageDays: 7,
            costUsd: 600.0,
            latencyGainPct: 18.0,
            subgoalsCount: 0,
            tags: ['swarm', 'coalition', 'specialist'],
        },
        {
            id: 'goal-root-gov-integrity',
            title: 'Attain Continuous 100% Cryptographic Auditability',
            description: 'Ensure all autonomous interventions have SHA-256 state proofs and instant rollback points.',
            priority: 'CRITICAL',
            status: 'ACTIVE',
            horizon: 'DAYS_180',
            utilityScore: 0.980,
            confidence: 0.995,
            ageDays: 25,
            costUsd: 1200.0,
            latencyGainPct: 0.0,
            subgoalsCount: 0,
            tags: ['governance', 'cryptography', 'safety'],
        },
    ]);
    const [isEvolving, setIsEvolving] = useState(false);
    const [statusMessage, setStatusMessage] = useState(null);
    const handleEvolve = () => {
        setIsEvolving(true);
        setTimeout(() => {
            setGoals((prev) => prev.map((g) => ({
                ...g,
                ageDays: g.ageDays + 1,
                utilityScore: Math.min(0.99, g.utilityScore + 0.005),
            })));
            setIsEvolving(false);
            setStatusMessage('Goal Evolution Cycle executed: 4 goals updated with refreshed utility and aging scores.');
            setTimeout(() => setStatusMessage(null), 4000);
        }, 1000);
    };
    const getPriorityBadgeVariant = (priority) => {
        switch (priority) {
            case 'CRITICAL':
                return 'error';
            case 'HIGH':
                return 'warning';
            case 'MEDIUM':
                return 'info';
            default:
                return 'default';
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(GitBranch, { className: "w-6 h-6 text-indigo-500" }), "Autonomous Goal Evolution & HTN Decomposition Center"] }), _jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: "Phase 13.11 \u2014 Hierarchical Task Network (HTN) & GOAP goal trees, utility scoring, and dynamic priority reprioritization." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsxs(Button, { variant: "intelligence", size: "sm", onClick: handleEvolve, disabled: isEvolving, children: [_jsx(RefreshCw, { className: `w-3.5 h-3.5 mr-1.5 ${isEvolving ? 'animate-spin' : ''}` }), isEvolving ? 'Evolving Generation...' : 'Trigger Goal Evolution'] }) })] }), statusMessage && (_jsxs("div", { className: "p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-lg text-sm text-emerald-800 dark:text-emerald-300 flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-5 h-5 flex-shrink-0" }), _jsx("span", { children: statusMessage })] })), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 border-l-4 border-l-indigo-500", children: [_jsx("span", { className: "text-xs font-medium text-gray-500", children: "Active Strategic Goals" }), _jsx("div", { className: "text-2xl font-bold text-gray-900 dark:text-white mt-1", children: goals.length }), _jsx("span", { className: "text-xs text-indigo-600 dark:text-indigo-400 font-medium", children: "HTN Decomposed" })] }), _jsxs(Card, { className: "p-4 border-l-4 border-l-emerald-500", children: [_jsx("span", { className: "text-xs font-medium text-gray-500", children: "Avg Composite Utility" }), _jsx("div", { className: "text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1", children: (goals.reduce((acc, g) => acc + g.utilityScore, 0) / goals.length).toFixed(3) }), _jsx("span", { className: "text-xs text-gray-400", children: "Max: 1.000" })] }), _jsxs(Card, { className: "p-4 border-l-4 border-l-purple-500", children: [_jsx("span", { className: "text-xs font-medium text-gray-500", children: "Bayesian Confidence" }), _jsx("div", { className: "text-2xl font-bold text-purple-600 dark:text-purple-400 mt-1", children: "98.5%" }), _jsx("span", { className: "text-xs text-purple-500", children: "Empirical Provenance" })] }), _jsxs(Card, { className: "p-4 border-l-4 border-l-amber-500", children: [_jsx("span", { className: "text-xs font-medium text-gray-500", children: "Goal Conflict Status" }), _jsx("div", { className: "text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1", children: "0 CONFLICTS" }), _jsx("span", { className: "text-xs text-emerald-500", children: "Deadlock-Free Tree" })] })] }), _jsxs("div", { className: "space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("h3", { className: "text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider flex items-center gap-2", children: [_jsx(Layers, { className: "w-4 h-4 text-indigo-500" }), "Hierarchical Strategic Goal Tree"] }), _jsx("span", { className: "text-xs text-gray-500", children: "Automatic Reprioritization Active" })] }), _jsx("div", { className: "grid grid-cols-1 gap-4", children: goals.map((goal) => (_jsxs(Card, { className: "p-5 hover:shadow-md transition-shadow", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-xs text-indigo-600 dark:text-indigo-400 font-semibold", children: goal.id }), _jsx(Badge, { variant: getPriorityBadgeVariant(goal.priority), size: "sm", children: goal.priority }), _jsx(Badge, { variant: "outline", size: "sm", children: goal.horizon })] }), _jsx("h4", { className: "font-semibold text-gray-900 dark:text-white text-base mt-1", children: goal.title }), _jsx("p", { className: "text-xs text-gray-500 dark:text-gray-400 mt-0.5", children: goal.description })] }), _jsx("div", { className: "flex items-center gap-3 flex-shrink-0", children: _jsxs("div", { className: "text-right", children: [_jsx("span", { className: "text-xs text-gray-400 block", children: "Utility Score" }), _jsx("span", { className: "text-lg font-bold text-indigo-600 dark:text-indigo-400 font-mono", children: goal.utilityScore.toFixed(3) })] }) })] }), _jsxs("div", { className: "grid grid-cols-2 md:grid-cols-5 gap-3 mt-4 text-xs", children: [_jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "text-gray-400 block mb-0.5", children: "Budget Req" }), _jsxs("span", { className: "font-semibold text-gray-800 dark:text-gray-200 font-mono", children: ["$", goal.costUsd.toLocaleString()] })] }), _jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "text-gray-400 block mb-0.5", children: "Latency Reduction" }), _jsxs("span", { className: "font-semibold text-emerald-600 dark:text-emerald-400 font-mono", children: ["+", goal.latencyGainPct, "%"] })] }), _jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "text-gray-400 block mb-0.5", children: "Confidence" }), _jsxs("span", { className: "font-semibold text-purple-600 dark:text-purple-400 font-mono", children: [(goal.confidence * 100).toFixed(1), "%"] })] }), _jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "text-gray-400 block mb-0.5", children: "Goal Age" }), _jsxs("span", { className: "font-semibold text-gray-700 dark:text-gray-300 font-mono", children: [goal.ageDays, " days"] })] }), _jsxs("div", { className: "p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800", children: [_jsx("span", { className: "text-gray-400 block mb-0.5", children: "Subgoals Decomposed" }), _jsxs("span", { className: "font-semibold text-indigo-600 dark:text-indigo-400 font-mono", children: [goal.subgoalsCount, " subtasks"] })] })] }), _jsxs("div", { className: "mt-3 flex items-center justify-between text-xs pt-2", children: [_jsx("div", { className: "flex items-center gap-1.5 flex-wrap", children: goal.tags.map((t, idx) => (_jsxs("span", { className: "px-2 py-0.5 bg-indigo-50 dark:bg-indigo-950/30 text-indigo-600 dark:text-indigo-400 rounded-full font-mono text-[10px]", children: ["#", t] }, idx))) }), _jsxs("span", { className: "text-emerald-600 dark:text-emerald-400 flex items-center gap-1 font-medium", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5" }), "Status: ", goal.status] })] })] }, goal.id))) })] })] }));
};
