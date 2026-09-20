import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Search, Layers, Code2, RefreshCw, } from 'lucide-react';
import { RuntimeObservabilityApiClient } from '../../services/runtimeObservabilityApiClient';
export const ObservabilityTraceExplorer = () => {
    const [dashboard, setDashboard] = useState(null);
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        loadData();
    }, []);
    const loadData = async () => {
        setLoading(true);
        try {
            const data = await RuntimeObservabilityApiClient.getDashboard();
            setDashboard(data);
            if (data.recent_events && data.recent_events.length > 0) {
                setSelectedEvent(data.recent_events[0] || null);
            }
        }
        catch (e) {
            console.error('Failed to load traces:', e);
        }
        finally {
            setLoading(false);
        }
    };
    const filteredEvents = (dashboard?.recent_events || []).filter((e) => {
        if (!searchQuery)
            return true;
        const q = searchQuery.toLowerCase();
        return (e.event_id.toLowerCase().includes(q) ||
            e.event_type.toLowerCase().includes(q) ||
            e.stage.toLowerCase().includes(q) ||
            (e.trace_context?.trace_id || '').toLowerCase().includes(q));
    });
    return (_jsxs("div", { className: "space-y-6 font-mono", children: [_jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-bold text-cyan-300 flex items-center gap-2", children: [_jsx(Layers, { className: "w-4 h-4 text-cyan-400" }), "Distributed Trace Explorer & Event Sourcing Inspector"] }), _jsx("p", { className: "text-xs text-slate-400 mt-0.5", children: "Inspect OpenTelemetry distributed trace spans, parent-child lineages, and cryptographic SHA-256 signatures." })] }), _jsx("button", { onClick: loadData, disabled: loading, className: "text-slate-400 hover:text-cyan-400 p-1.5 rounded", title: "Refresh", children: _jsx(RefreshCw, { className: `w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}` }) })] }), _jsxs("div", { className: "relative", children: [_jsx(Search, { className: "w-4 h-4 text-slate-400 absolute left-3 top-2.5" }), _jsx("input", { type: "text", placeholder: "Search by Trace ID, Event ID, Stage, or Event Type...", value: searchQuery, onChange: (e) => setSearchQuery(e.target.value), className: "w-full bg-slate-950/90 border border-slate-800 rounded-lg pl-9 pr-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500" })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-2 gap-6", children: [_jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3", children: [_jsxs("div", { className: "text-xs uppercase text-slate-300 tracking-wider flex items-center justify-between border-b border-slate-800 pb-2", children: [_jsx("span", { children: "Indexed Execution Events" }), _jsxs("span", { className: "text-cyan-400 font-bold", children: [filteredEvents.length, " Events"] })] }), _jsx("div", { className: "space-y-2 max-h-[500px] overflow-y-auto pr-1", children: filteredEvents.length === 0 ? (_jsxs("div", { className: "p-4 text-center text-slate-500 text-xs", children: ["No events match query. Total stored in AROL EventStore: ", dashboard?.total_events_stored || 0] })) : (filteredEvents.map((evt) => (_jsxs("div", { onClick: () => setSelectedEvent(evt), className: `p-3 rounded-lg border text-xs cursor-pointer transition-all ${selectedEvent?.event_id === evt.event_id
                                        ? 'bg-slate-800 border-cyan-500 text-cyan-200'
                                        : 'bg-slate-950/80 border-slate-800 text-slate-300 hover:border-slate-700'}`, children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-bold", children: evt.event_type }), _jsx("span", { className: "text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400", children: evt.stage })] }), _jsxs("div", { className: "text-[10px] text-slate-500 mt-1 flex justify-between", children: [_jsxs("span", { children: ["Trace: ", (evt.trace_context?.trace_id || '').slice(0, 8), "..."] }), _jsx("span", { children: evt.duration_ms > 0 ? `${evt.duration_ms.toFixed(1)}ms` : 'Instant' })] })] }, evt.event_id)))) })] }), _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3 font-mono", children: [_jsxs("div", { className: "text-xs uppercase text-slate-300 tracking-wider flex items-center gap-2 border-b border-slate-800 pb-2", children: [_jsx(Code2, { className: "w-4 h-4 text-emerald-400" }), "Event Provenance & Payload Inspector"] }), selectedEvent ? (_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "grid grid-cols-2 gap-2 text-[11px] bg-slate-950/80 p-3 rounded-lg border border-slate-800", children: [_jsxs("div", { children: [_jsx("span", { className: "text-slate-500", children: "Event ID: " }), _jsx("span", { className: "text-slate-200", children: selectedEvent.event_id })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500", children: "Status: " }), _jsx("span", { className: "text-emerald-400 font-bold", children: selectedEvent.status })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500", children: "Trace ID: " }), _jsx("span", { className: "text-cyan-300", children: selectedEvent.trace_context?.trace_id })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500", children: "Span ID: " }), _jsx("span", { className: "text-purple-300", children: selectedEvent.trace_context?.span_id })] })] }), _jsx("div", { className: "p-3 bg-slate-950/90 border border-slate-800 rounded-lg text-[11px] overflow-x-auto", children: _jsx("pre", { className: "text-slate-300", children: JSON.stringify(selectedEvent, null, 2) }) })] })) : (_jsx("div", { className: "p-8 text-center text-slate-500 text-xs", children: "Select an event from the left pane to inspect its trace context and payload." }))] })] })] }));
};
