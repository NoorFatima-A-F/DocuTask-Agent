import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { History, CheckCircle2, FlaskConical, BookOpen, FileText, Compass, } from 'lucide-react';
export const DiscoveryTimeline = () => {
    const events = [
        {
            id: 'evt-01',
            time: '18:45 UTC',
            title: 'Publication Signed & Registered with DOI',
            description: 'Official paper "Empirical Proof of Speculative Invariance in Multi-Column Accounting Extraction" published under DOI: 10.ai-sci/2026.001 with SHA-256 seal.',
            type: 'PUBLICATION',
        },
        {
            id: 'evt-02',
            time: '18:42 UTC',
            title: 'Consensus Tribunal Ratification',
            description: 'Multi-Agent Tribunal achieved 100% unanimous approval across Sentinel, Statistician, and Architect agents.',
            type: 'VALIDATION',
        },
        {
            id: 'evt-03',
            time: '18:40 UTC',
            title: 'Empirical Law Formulated',
            description: 'Ratified "Law of Speculative Invariance in Structured Documents" with governing equation Latency_P95(H, C).',
            type: 'LAW',
        },
        {
            id: 'evt-04',
            time: '18:35 UTC',
            title: 'A/B Experiment Completed (p < 0.0001)',
            description: 'A/B controlled trial exp-cache-ab-01 evaluated 2,500 document traces, confirming 30.27% extraction latency reduction with Cohen\'s d = 1.42.',
            type: 'EXPERIMENT',
        },
        {
            id: 'evt-05',
            time: '18:30 UTC',
            title: 'Hypothesis Formulated (EIG = 0.915)',
            description: 'Autonomous Knowledge Gap Scanner detected uncharacterized memory eviction and formulated Speculative Layout Cache hypothesis.',
            type: 'HYPOTHESIS',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4", children: _jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2", children: [_jsx(History, { className: "w-6 h-6 text-indigo-500" }), "Autonomous Discovery Chronology & Provenance Timeline"] }), _jsx("p", { className: "text-sm text-gray-500 dark:text-gray-400", children: "Chronological audit trail of all hypothesis formulations, experimental benchmarks, statistical validations, and ratified governing laws." })] }) }), _jsx(Card, { className: "p-6", children: _jsx("div", { className: "relative border-l-2 border-indigo-200 dark:border-indigo-900 ml-4 space-y-6", children: events.map(event => (_jsxs("div", { className: "relative pl-6", children: [_jsxs("div", { className: "absolute -left-3 top-0.5 w-6 h-6 rounded-full bg-white dark:bg-gray-800 border-2 border-indigo-500 flex items-center justify-center", children: [event.type === 'PUBLICATION' && _jsx(FileText, { className: "w-3 h-3 text-sky-500" }), event.type === 'VALIDATION' && _jsx(CheckCircle2, { className: "w-3 h-3 text-emerald-500" }), event.type === 'LAW' && _jsx(BookOpen, { className: "w-3 h-3 text-purple-500" }), event.type === 'EXPERIMENT' && _jsx(FlaskConical, { className: "w-3 h-3 text-amber-500" }), event.type === 'HYPOTHESIS' && _jsx(Compass, { className: "w-3 h-3 text-indigo-500" })] }), _jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono text-gray-400", children: event.time }), _jsx(Badge, { variant: "outline", size: "sm", children: event.type })] }), _jsx("h4", { className: "text-sm font-semibold text-gray-900 dark:text-white", children: event.title }), _jsx("p", { className: "text-xs text-gray-600 dark:text-gray-300", children: event.description })] })] }, event.id))) }) })] }));
};
