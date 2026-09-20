import React, { useState, useEffect } from 'react';
import {
  Search,
  Layers,
  Code2,
  RefreshCw,
} from 'lucide-react';
import { RuntimeObservabilityApiClient } from '../../services/runtimeObservabilityApiClient';
import { RuntimeDashboardStatePayload, RuntimeEventPayload } from '../../types/runtimeObservability';

export const ObservabilityTraceExplorer: React.FC = () => {
  const [dashboard, setDashboard] = useState<RuntimeDashboardStatePayload | null>(null);
  const [selectedEvent, setSelectedEvent] = useState<RuntimeEventPayload | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);

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
    } catch (e) {
      console.error('Failed to load traces:', e);
    } finally {
      setLoading(false);
    }
  };

  const filteredEvents = (dashboard?.recent_events || []).filter((e) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      e.event_id.toLowerCase().includes(q) ||
      e.event_type.toLowerCase().includes(q) ||
      e.stage.toLowerCase().includes(q) ||
      (e.trace_context?.trace_id || '').toLowerCase().includes(q)
    );
  });

  return (
    <div className="space-y-6 font-mono">
      {/* Header Banner */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-sm font-bold text-cyan-300 flex items-center gap-2">
              <Layers className="w-4 h-4 text-cyan-400" />
              Distributed Trace Explorer & Event Sourcing Inspector
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Inspect OpenTelemetry distributed trace spans, parent-child lineages, and cryptographic SHA-256 signatures.
            </p>
          </div>

          <button
            onClick={loadData}
            disabled={loading}
            className="text-slate-400 hover:text-cyan-400 p-1.5 rounded"
            title="Refresh"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>

        {/* Search Bar */}
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search by Trace ID, Event ID, Stage, or Event Type..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-slate-950/90 border border-slate-800 rounded-lg pl-9 pr-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
          />
        </div>
      </div>

      {/* Split Viewer: Events List & Event Details */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Events List */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3">
          <div className="text-xs uppercase text-slate-300 tracking-wider flex items-center justify-between border-b border-slate-800 pb-2">
            <span>Indexed Execution Events</span>
            <span className="text-cyan-400 font-bold">{filteredEvents.length} Events</span>
          </div>

          <div className="space-y-2 max-h-[500px] overflow-y-auto pr-1">
            {filteredEvents.length === 0 ? (
              <div className="p-4 text-center text-slate-500 text-xs">
                No events match query. Total stored in AROL EventStore: {dashboard?.total_events_stored || 0}
              </div>
            ) : (
              filteredEvents.map((evt) => (
                <div
                  key={evt.event_id}
                  onClick={() => setSelectedEvent(evt)}
                  className={`p-3 rounded-lg border text-xs cursor-pointer transition-all ${
                    selectedEvent?.event_id === evt.event_id
                      ? 'bg-slate-800 border-cyan-500 text-cyan-200'
                      : 'bg-slate-950/80 border-slate-800 text-slate-300 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold">{evt.event_type}</span>
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
                      {evt.stage}
                    </span>
                  </div>
                  <div className="text-[10px] text-slate-500 mt-1 flex justify-between">
                    <span>Trace: {(evt.trace_context?.trace_id || '').slice(0, 8)}...</span>
                    <span>{evt.duration_ms > 0 ? `${evt.duration_ms.toFixed(1)}ms` : 'Instant'}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right: Selected Event Raw Payload & Provenance */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3 font-mono">
          <div className="text-xs uppercase text-slate-300 tracking-wider flex items-center gap-2 border-b border-slate-800 pb-2">
            <Code2 className="w-4 h-4 text-emerald-400" />
            Event Provenance & Payload Inspector
          </div>

          {selectedEvent ? (
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-2 text-[11px] bg-slate-950/80 p-3 rounded-lg border border-slate-800">
                <div>
                  <span className="text-slate-500">Event ID: </span>
                  <span className="text-slate-200">{selectedEvent.event_id}</span>
                </div>
                <div>
                  <span className="text-slate-500">Status: </span>
                  <span className="text-emerald-400 font-bold">{selectedEvent.status}</span>
                </div>
                <div>
                  <span className="text-slate-500">Trace ID: </span>
                  <span className="text-cyan-300">{selectedEvent.trace_context?.trace_id}</span>
                </div>
                <div>
                  <span className="text-slate-500">Span ID: </span>
                  <span className="text-purple-300">{selectedEvent.trace_context?.span_id}</span>
                </div>
              </div>

              <div className="p-3 bg-slate-950/90 border border-slate-800 rounded-lg text-[11px] overflow-x-auto">
                <pre className="text-slate-300">{JSON.stringify(selectedEvent, null, 2)}</pre>
              </div>
            </div>
          ) : (
            <div className="p-8 text-center text-slate-500 text-xs">
              Select an event from the left pane to inspect its trace context and payload.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
