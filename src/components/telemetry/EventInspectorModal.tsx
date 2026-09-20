/**
 * Temporal / OpenTelemetry Event Inspector Modal
 * 
 * Inspects any live RuntimeEvent in detail, displaying its OpenTelemetry trace context,
 * causation lineage, monotonic sequence number, duration, execution metadata, and raw JSON payload.
 */

import React, { useState } from 'react';
import type { RuntimeEvent } from '../../types/runtimeTelemetry';

interface EventInspectorModalProps {
  event: RuntimeEvent | null;
  onClose: () => void;
}

export const EventInspectorModal: React.FC<EventInspectorModalProps> = ({ event, onClose }) => {
  const [activeTab, setActiveTab] = useState<'PAYLOAD' | 'METADATA' | 'TRACE'>('PAYLOAD');
  const [copiedField, setCopiedField] = useState<string | null>(null);

  if (!event) return null;

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    setCopiedField(label);
    setTimeout(() => setCopiedField(null), 2000);
  };

  const getBadgeColor = (eventType: string) => {
    if (eventType.includes('Worker')) return 'bg-emerald-950 text-emerald-300 border-emerald-700/50';
    if (eventType.includes('Planner')) return 'bg-indigo-950 text-indigo-300 border-indigo-700/50';
    if (eventType.includes('Memory')) return 'bg-purple-950 text-purple-300 border-purple-700/50';
    if (eventType.includes('Reflection') || eventType.includes('Critique')) return 'bg-amber-950 text-amber-300 border-amber-700/50';
    if (eventType.includes('Validation')) return 'bg-teal-950 text-teal-300 border-teal-700/50';
    if (eventType.includes('Human')) return 'bg-cyan-950 text-cyan-300 border-cyan-700/50';
    if (eventType.includes('Failed')) return 'bg-rose-950 text-rose-300 border-rose-700/50';
    return 'bg-slate-800 text-slate-300 border-slate-700';
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-fade-in"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="event-inspector-title"
    >
      <div
        className="relative w-full max-w-3xl bg-slate-900 border border-slate-800 rounded-xl shadow-2xl overflow-hidden flex flex-col max-h-[85vh]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/60">
          <div className="flex items-center gap-3">
            <span className={`px-2.5 py-1 text-xs font-mono font-semibold rounded border ${getBadgeColor(event.event_type)}`}>
              {event.event_type}
            </span>
            <h2 id="event-inspector-title" className="text-base font-semibold text-slate-100">
              Event #{event.sequence_number} Inspector
            </h2>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-100 p-1.5 rounded-lg hover:bg-slate-800 transition-colors"
            aria-label="Close modal"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Quick Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 p-4 bg-slate-950/30 border-b border-slate-800/80 text-xs">
          <div>
            <span className="text-slate-400 block font-medium">Status</span>
            <span className="text-emerald-400 font-mono font-semibold">{event.status}</span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Duration</span>
            <span className="text-slate-200 font-mono">
              {event.duration_ms != null ? `${event.duration_ms.toFixed(1)} ms` : '—'}
            </span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Agent / Worker</span>
            <span className="text-indigo-300 font-mono truncate block">
              {event.agent_id || event.worker_id || 'SYSTEM'}
            </span>
          </div>
          <div>
            <span className="text-slate-400 block font-medium">Timestamp</span>
            <span className="text-slate-300 font-mono text-[11px] truncate block" title={event.timestamp}>
              {new Date(event.timestamp).toLocaleTimeString()}
            </span>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex border-b border-slate-800 px-6 gap-6 bg-slate-900/90 text-sm">
          <button
            onClick={() => setActiveTab('PAYLOAD')}
            className={`py-2.5 font-medium border-b-2 transition-colors ${
              activeTab === 'PAYLOAD'
                ? 'border-indigo-500 text-indigo-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Payload JSON
          </button>
          <button
            onClick={() => setActiveTab('METADATA')}
            className={`py-2.5 font-medium border-b-2 transition-colors ${
              activeTab === 'METADATA'
                ? 'border-indigo-500 text-indigo-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Metadata
          </button>
          <button
            onClick={() => setActiveTab('TRACE')}
            className={`py-2.5 font-medium border-b-2 transition-colors ${
              activeTab === 'TRACE'
                ? 'border-indigo-500 text-indigo-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            OpenTelemetry Traces
          </button>
        </div>

        {/* Modal Body */}
        <div className="flex-1 p-6 overflow-y-auto font-mono text-xs text-slate-300 space-y-4">
          {activeTab === 'PAYLOAD' && (
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-slate-400 font-sans font-medium">Event Payload ({Object.keys(event.payload || {}).length} keys):</span>
                <button
                  onClick={() => copyToClipboard(JSON.stringify(event.payload, null, 2), 'payload')}
                  className="px-2.5 py-1 text-[11px] bg-slate-800 hover:bg-slate-700 text-slate-300 rounded font-sans transition-colors"
                >
                  {copiedField === 'payload' ? '✓ Copied' : 'Copy JSON'}
                </button>
              </div>
              <pre className="p-4 bg-slate-950 rounded-lg border border-slate-800 text-slate-200 overflow-x-auto max-h-80 leading-relaxed font-mono">
                {JSON.stringify(event.payload, null, 2)}
              </pre>
            </div>
          )}

          {activeTab === 'METADATA' && (
            <div className="space-y-3">
              <div className="flex justify-between items-center mb-1">
                <span className="text-slate-400 font-sans font-medium">Execution Metadata:</span>
                <button
                  onClick={() => copyToClipboard(JSON.stringify(event.metadata, null, 2), 'metadata')}
                  className="px-2.5 py-1 text-[11px] bg-slate-800 hover:bg-slate-700 text-slate-300 rounded font-sans transition-colors"
                >
                  {copiedField === 'metadata' ? '✓ Copied' : 'Copy JSON'}
                </button>
              </div>
              <pre className="p-4 bg-slate-950 rounded-lg border border-slate-800 text-slate-200 overflow-x-auto max-h-80 leading-relaxed font-mono">
                {JSON.stringify(event.metadata, null, 2)}
              </pre>
            </div>
          )}

          {activeTab === 'TRACE' && (
            <div className="space-y-4">
              <div className="p-4 bg-slate-950 rounded-lg border border-slate-800 space-y-3">
                <div>
                  <span className="text-slate-400 block text-[11px]">Trace ID (OpenTelemetry)</span>
                  <div className="flex items-center justify-between text-indigo-400 font-mono mt-0.5">
                    <span className="select-all">{event.trace_id}</span>
                    <button
                      onClick={() => copyToClipboard(event.trace_id, 'trace_id')}
                      className="text-[11px] text-slate-400 hover:text-slate-200 underline font-sans"
                    >
                      {copiedField === 'trace_id' ? 'Copied' : 'Copy'}
                    </button>
                  </div>
                </div>

                <div>
                  <span className="text-slate-400 block text-[11px]">Span ID</span>
                  <div className="flex items-center justify-between text-indigo-300 font-mono mt-0.5">
                    <span className="select-all">{event.span_id || 'root-span'}</span>
                    {event.span_id && (
                      <button
                        onClick={() => copyToClipboard(event.span_id!, 'span_id')}
                        className="text-[11px] text-slate-400 hover:text-slate-200 underline font-sans"
                      >
                        {copiedField === 'span_id' ? 'Copied' : 'Copy'}
                      </button>
                    )}
                  </div>
                </div>

                <div>
                  <span className="text-slate-400 block text-[11px]">Correlation ID</span>
                  <div className="flex items-center justify-between text-slate-300 font-mono mt-0.5">
                    <span className="select-all">{event.correlation_id}</span>
                    <button
                      onClick={() => copyToClipboard(event.correlation_id, 'corr_id')}
                      className="text-[11px] text-slate-400 hover:text-slate-200 underline font-sans"
                    >
                      {copiedField === 'corr_id' ? 'Copied' : 'Copy'}
                    </button>
                  </div>
                </div>

                <div>
                  <span className="text-slate-400 block text-[11px]">Parent Event ID</span>
                  <div className="text-slate-400 font-mono mt-0.5">
                    {event.parent_event_id || 'None (Root Execution Node)'}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="flex items-center justify-between px-6 py-3 border-t border-slate-800 bg-slate-950/40 text-xs">
          <span className="text-slate-400 font-mono text-[11px]">
            Event ID: <span className="text-slate-300">{event.event_id}</span>
          </span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-sans font-medium rounded-lg transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
