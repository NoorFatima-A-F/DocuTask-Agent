import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { EsmrReplayApiClient } from '../../services/esmrReplayApiClient';
export const TimelineExplorerView = ({ missionId, onSelectEvent, }) => {
    const [timeline, setTimeline] = useState(null);
    const [selectedCategory, setSelectedCategory] = useState('ALL');
    const [selectedStage, setSelectedStage] = useState('ALL');
    const [searchQuery, setSearchQuery] = useState('');
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        EsmrReplayApiClient.getTimeline(missionId)
            .then(setTimeline)
            .catch(console.error)
            .finally(() => setLoading(false));
    }, [missionId]);
    if (loading || !timeline) {
        return (_jsx("div", { className: "p-6 bg-slate-900 border border-slate-800 rounded-xl text-slate-400 animate-pulse", children: "Reconstructing Chronological Event Stream from Immutable Event Log..." }));
    }
    const filteredEntries = timeline.entries.filter((e) => {
        if (selectedCategory !== 'ALL' && e.category !== selectedCategory)
            return false;
        if (selectedStage !== 'ALL' && e.stage !== selectedStage)
            return false;
        if (searchQuery.trim()) {
            const q = searchQuery.toLowerCase();
            return (e.summary.toLowerCase().includes(q) ||
                e.event_type.toLowerCase().includes(q) ||
                e.event_id.toLowerCase().includes(q) ||
                (e.task_id && e.task_id.toLowerCase().includes(q)));
        }
        return true;
    });
    const categories = ['ALL', ...Object.keys(timeline.categories)];
    const stages = ['ALL', ...timeline.stages];
    return (_jsxs("div", { className: "bg-slate-950 border border-slate-800 rounded-xl p-6 shadow-2xl space-y-6 text-slate-100", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4", children: [_jsxs("div", { children: [_jsxs("h3", { className: "text-lg font-bold text-white flex items-center gap-2", children: [_jsx("span", { children: "\uD83D\uDCDC" }), " Event-Sourced Mission Timeline Explorer"] }), _jsxs("p", { className: "text-xs text-slate-400 mt-1", children: ["Total Events: ", _jsx("span", { className: "font-mono text-cyan-400", children: timeline.total_events }), " | Duration:", ' ', _jsxs("span", { className: "font-mono text-emerald-400", children: [timeline.total_duration_ms.toFixed(1), " ms"] })] })] }), _jsxs("div", { className: "flex flex-wrap items-center gap-3", children: [_jsx("input", { type: "text", placeholder: "Search event type, summary...", value: searchQuery, onChange: (e) => setSearchQuery(e.target.value), className: "px-3 py-1.5 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-cyan-500" }), _jsx("select", { value: selectedCategory, onChange: (e) => setSelectedCategory(e.target.value), className: "px-3 py-1.5 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-mono", children: categories.map((c) => (_jsxs("option", { value: c, children: ["Category: ", c] }, c))) }), _jsx("select", { value: selectedStage, onChange: (e) => setSelectedStage(e.target.value), className: "px-3 py-1.5 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-mono", children: stages.map((s) => (_jsxs("option", { value: s, children: ["Stage: ", s] }, s))) })] })] }), _jsx("div", { className: "overflow-x-auto max-h-[500px] overflow-y-auto border border-slate-800 rounded-lg", children: _jsxs("table", { className: "w-full text-left border-collapse font-mono text-xs", children: [_jsx("thead", { className: "bg-slate-900/90 sticky top-0 border-b border-slate-800 text-slate-400", children: _jsxs("tr", { children: [_jsx("th", { className: "py-2.5 px-3", children: "#" }), _jsx("th", { className: "py-2.5 px-3", children: "Stage" }), _jsx("th", { className: "py-2.5 px-3", children: "Category" }), _jsx("th", { className: "py-2.5 px-3", children: "Event Type" }), _jsx("th", { className: "py-2.5 px-3", children: "Summary" }), _jsx("th", { className: "py-2.5 px-3", children: "Worker" }), _jsx("th", { className: "py-2.5 px-3", children: "Duration" }), _jsx("th", { className: "py-2.5 px-3", children: "Hash Pointer" })] }) }), _jsx("tbody", { className: "divide-y divide-slate-850", children: filteredEntries.map((e) => {
                                const categoryColor = {
                                    MISSION: 'text-cyan-400 bg-cyan-950/50 border-cyan-500/30',
                                    PLANNER: 'text-purple-400 bg-purple-950/50 border-purple-500/30',
                                    EXECUTION: 'text-emerald-400 bg-emerald-950/50 border-emerald-500/30',
                                    GOVERNANCE: 'text-amber-400 bg-amber-950/50 border-amber-500/30',
                                    REFLECTION: 'text-pink-400 bg-pink-950/50 border-pink-500/30',
                                    WORKER: 'text-blue-400 bg-blue-950/50 border-blue-500/30',
                                };
                                const badgeClass = categoryColor[e.category] || 'text-slate-400 bg-slate-900 border-slate-700';
                                return (_jsxs("tr", { onClick: () => onSelectEvent && onSelectEvent(e), className: "hover:bg-slate-900/60 cursor-pointer transition-colors", children: [_jsx("td", { className: "py-2.5 px-3 text-slate-400", children: e.sequence_number }), _jsx("td", { className: "py-2.5 px-3 font-semibold text-slate-200", children: e.stage }), _jsx("td", { className: "py-2.5 px-3", children: _jsx("span", { className: `px-2 py-0.5 rounded border text-[10px] ${badgeClass}`, children: e.category }) }), _jsx("td", { className: "py-2.5 px-3 text-slate-300", children: e.event_type }), _jsx("td", { className: "py-2.5 px-3 text-slate-200 font-sans", children: e.summary }), _jsx("td", { className: "py-2.5 px-3 text-slate-400", children: e.worker_id || '-' }), _jsx("td", { className: "py-2.5 px-3 text-emerald-400", children: e.duration_ms ? `${e.duration_ms.toFixed(1)} ms` : '-' }), _jsxs("td", { className: "py-2.5 px-3 text-slate-500 font-mono text-[10px]", children: [e.hash.slice(0, 8), "...", e.hash.slice(-6)] })] }, e.event_id));
                            }) })] }) })] }));
};
