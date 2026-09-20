import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Radio, Activity, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
export const DistributedEventStreamView = () => {
    const [events, setEvents] = useState([]);
    const [filterType, setFilterType] = useState('ALL');
    useEffect(() => {
        // Initial mock events
        const initialEvents = [
            {
                event_id: 'evt_001',
                event_type: 'WORKER_HEARTBEAT_ACK',
                source_node: 'node_us_east_01',
                region: 'us-east-1',
                details: 'Heartbeat received. CPU: 18.5%, RAM: 24.0%, active slots: 2/8',
                timestamp: new Date(Date.now() - 5000).toISOString(),
                severity: 'INFO',
            },
            {
                event_id: 'evt_002',
                event_type: 'JOB_SCHEDULED_CAPACITY',
                source_node: 'scheduler_master_01',
                region: 'us-east-1',
                details: 'Scheduled job_doc_9941 to node_us_east_01 via capacity weighted score (score=0.88)',
                timestamp: new Date(Date.now() - 4000).toISOString(),
                severity: 'SUCCESS',
            },
            {
                event_id: 'evt_003',
                event_type: 'CHECKPOINT_COMMITTED',
                source_node: 'node_us_east_01',
                region: 'us-east-1',
                details: 'Workflow wf_invoice_proc_01 committed step 1 snapshot with fencing token #1',
                timestamp: new Date(Date.now() - 3000).toISOString(),
                severity: 'INFO',
            },
            {
                event_id: 'evt_004',
                event_type: 'DISTRIBUTED_LOCK_ACQUIRED',
                source_node: 'lock_manager_01',
                region: 'global',
                details: 'Acquired exclusive lease lock:workflow:wf_invoice_proc_01 for 30s',
                timestamp: new Date(Date.now() - 2000).toISOString(),
                severity: 'INFO',
            },
            {
                event_id: 'evt_005',
                event_type: 'AUTOSCALING_EVALUATED',
                source_node: 'autoscaling_engine_01',
                region: 'global',
                details: 'Autoscaler evaluated cluster state: queue depth 14, target 5 workers (action: STABLE)',
                timestamp: new Date(Date.now() - 1000).toISOString(),
                severity: 'SUCCESS',
            },
        ];
        setEvents(initialEvents);
        // Periodic stream additions
        const interval = setInterval(() => {
            const types = [
                { type: 'WORKER_HEARTBEAT_ACK', sev: 'INFO', detail: 'Worker heartbeat sync OK' },
                { type: 'JOB_DISPATCHED', sev: 'SUCCESS', detail: 'Dispatched priority task to healthy edge' },
                { type: 'REPLICATION_SYNC', sev: 'INFO', detail: 'Asynchronous snapshot replicated to EU secondary' },
            ];
            const pick = types[Math.floor(Math.random() * types.length)];
            const newEvt = {
                event_id: `evt_${Date.now().toString().slice(-4)}`,
                event_type: pick.type,
                source_node: 'node_us_east_01',
                region: 'us-east-1',
                details: pick.detail,
                timestamp: new Date().toISOString(),
                severity: pick.sev,
            };
            setEvents((prev) => [newEvt, ...prev.slice(0, 30)]);
        }, 5000);
        return () => clearInterval(interval);
    }, []);
    const filteredEvents = filterType === 'ALL'
        ? events
        : events.filter((e) => e.event_type.includes(filterType));
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(Radio, { className: "w-6 h-6 animate-pulse" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "Distributed Event Stream" }), _jsx("p", { className: "text-sm text-slate-400", children: "Live telemetry stream of cluster heartbeats, job dispatches, locks, and checkpoints" })] })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsxs("select", { value: filterType, onChange: (e) => setFilterType(e.target.value), className: "bg-slate-800 border border-slate-700 text-slate-200 text-sm rounded-lg px-3 py-2", children: [_jsx("option", { value: "ALL", children: "All Event Types" }), _jsx("option", { value: "HEARTBEAT", children: "Heartbeats" }), _jsx("option", { value: "JOB", children: "Job Dispatches" }), _jsx("option", { value: "CHECKPOINT", children: "Checkpoints" }), _jsx("option", { value: "LOCK", children: "Locks" }), _jsx("option", { value: "AUTOSCALING", children: "Autoscaling" })] }) })] }), _jsxs(Card, { className: "p-6 bg-slate-900/40 border-slate-800 space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-slate-800 pb-3", children: [_jsxs("span", { className: "text-xs uppercase tracking-wider text-slate-400 font-semibold flex items-center gap-2", children: [_jsx(Activity, { className: "w-4 h-4 text-emerald-400" }), "Live Event Feed (", filteredEvents.length, " events)"] }), _jsxs("span", { className: "text-xs text-emerald-400 font-mono flex items-center gap-1.5", children: [_jsx("span", { className: "w-2 h-2 rounded-full bg-emerald-400 animate-ping" }), "Streaming Live"] })] }), _jsx("div", { className: "space-y-2.5 font-mono text-xs", children: filteredEvents.map((evt) => (_jsxs("div", { className: "p-3 bg-slate-800/40 rounded-xl border border-slate-800 hover:border-slate-700 flex flex-col md:flex-row md:items-center justify-between gap-3 transition-colors", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: evt.severity === 'SUCCESS'
                                                ? 'success'
                                                : evt.severity === 'WARNING'
                                                    ? 'warning'
                                                    : 'intelligence', children: evt.event_type }), _jsx("span", { className: "text-slate-300 font-sans text-xs", children: evt.details })] }), _jsxs("div", { className: "flex items-center gap-4 text-slate-400 text-[11px] shrink-0", children: [_jsx("span", { className: "text-cyan-400", children: evt.source_node }), _jsx("span", { className: "text-slate-500", children: evt.region }), _jsx("span", { className: "text-slate-500", children: new Date(evt.timestamp).toLocaleTimeString() })] })] }, evt.event_id))) })] })] }));
};
