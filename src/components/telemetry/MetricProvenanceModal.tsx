import React, { useState } from 'react';
import type { MetricProvenanceRecordData } from '../../types/scientificMetrics';

interface MetricProvenanceModalProps {
  provenance: MetricProvenanceRecordData | null;
  onClose: () => void;
}

export const MetricProvenanceModal: React.FC<MetricProvenanceModalProps> = ({ provenance, onClose }) => {
  const [activeTab, setActiveTab] = useState<'FORMULA' | 'STATISTICS' | 'LINEAGE' | 'RAW_EVENTS'>('FORMULA');
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  if (!provenance) return null;

  const copyToClipboard = (text: string, key: string) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  const isSentinel = Boolean(provenance.sentinel_state);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4 animate-fade-in"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="metric-provenance-title"
    >
      <div
        className="relative w-full max-w-3xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[88vh]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/70">
          <div className="flex items-center gap-3">
            <span className="px-2.5 py-1 text-xs font-mono font-bold rounded bg-indigo-950 text-indigo-300 border border-indigo-700/50">
              {provenance.metric_version}
            </span>
            <div>
              <h2 id="metric-provenance-title" className="text-base font-bold text-slate-100 flex items-center gap-2">
                <span>{provenance.metric_name}</span>
                <span className="text-xs font-mono font-normal text-slate-400">({provenance.metric_id})</span>
              </h2>
            </div>
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

        {/* Highlight Banner: Calculated Value & Integrity */}
        <div className="p-6 bg-gradient-to-r from-slate-950/90 to-indigo-950/40 border-b border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <span className="text-xs font-mono text-slate-400 block uppercase tracking-wider">Empirical Value</span>
            <div className="text-3xl font-extrabold text-cyan-400 font-mono mt-0.5">
              {provenance.formatted_value}
            </div>
            <div className="text-xs text-slate-400 mt-1 flex items-center gap-2">
              <span>Unit: <strong className="text-slate-200">{provenance.unit}</strong></span>
              <span>•</span>
              <span>Sample Size: <strong className="text-slate-200">n = {provenance.sample_size}</strong></span>
            </div>
          </div>

          <div className="flex flex-col items-end gap-1.5">
            <div className={`px-3 py-1 rounded-full text-xs font-mono font-bold flex items-center gap-1.5 border ${
              isSentinel
                ? 'bg-amber-950 text-amber-300 border-amber-600/50'
                : 'bg-emerald-950 text-emerald-300 border-emerald-600/50'
            }`}>
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
              {isSentinel ? provenance.sentinel_state : 'MATHEMATICALLY_VERIFIED'}
            </div>
            <span className="text-[11px] font-mono text-slate-400">
              Observation: {provenance.observation_window?.duration_seconds?.toFixed(2) || '0.00'}s
            </span>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-slate-800 px-6 gap-6 bg-slate-900/90 text-xs font-mono">
          <button
            onClick={() => setActiveTab('FORMULA')}
            className={`py-3 font-semibold border-b-2 transition-colors ${
              activeTab === 'FORMULA' ? 'border-cyan-400 text-cyan-300' : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Mathematical Formula
          </button>
          <button
            onClick={() => setActiveTab('STATISTICS')}
            className={`py-3 font-semibold border-b-2 transition-colors ${
              activeTab === 'STATISTICS' ? 'border-cyan-400 text-cyan-300' : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Distribution Statistics
          </button>
          <button
            onClick={() => setActiveTab('LINEAGE')}
            className={`py-3 font-semibold border-b-2 transition-colors ${
              activeTab === 'LINEAGE' ? 'border-cyan-400 text-cyan-300' : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Merkle Evidence Lineage
          </button>
          <button
            onClick={() => setActiveTab('RAW_EVENTS')}
            className={`py-3 font-semibold border-b-2 transition-colors ${
              activeTab === 'RAW_EVENTS' ? 'border-cyan-400 text-cyan-300' : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Raw Events ({provenance.raw_event_ids?.length || 0})
          </button>
        </div>

        {/* Modal Body */}
        <div className="flex-1 p-6 overflow-y-auto space-y-4 font-sans text-sm">
          {activeTab === 'FORMULA' && (
            <div className="space-y-4">
              <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
                <span className="text-xs font-mono text-slate-400 uppercase tracking-wider block">Mathematical Expression</span>
                <div className="font-mono text-base text-cyan-300 font-bold bg-slate-900/80 p-3 rounded-lg border border-slate-800">
                  {provenance.formula_expression}
                </div>
                {provenance.formula_latex && (
                  <div className="text-xs font-mono text-slate-400 mt-2 p-2.5 bg-slate-900/50 rounded border border-slate-800/60 overflow-x-auto">
                    <span className="text-slate-400 block mb-1">LaTeX Representation:</span>
                    <code className="text-indigo-300">{provenance.formula_latex}</code>
                  </div>
                )}
              </div>

              {/* Variable Bindings */}
              <div className="space-y-2">
                <span className="text-xs font-mono font-semibold text-slate-300 block">Evaluated Variables ({Object.keys(provenance.variables_used || {}).length})</span>
                <div className="bg-slate-950 rounded-xl border border-slate-800 divide-y divide-slate-800/60 font-mono text-xs">
                  {Object.entries(provenance.variables_used || {}).map(([key, val]) => (
                    <div key={key} className="flex justify-between items-center px-4 py-2.5">
                      <span className="text-indigo-300">{key}</span>
                      <span className="text-slate-200 font-bold">{String(val)}</span>
                    </div>
                  ))}
                  {Object.keys(provenance.variables_used || {}).length === 0 && (
                    <div className="p-4 text-center text-slate-400">No variable bindings required.</div>
                  )}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'STATISTICS' && (
            <div className="space-y-4">
              {provenance.statistical_summary ? (
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                  <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                    <span className="text-[11px] font-mono text-slate-400 block">Sample Mean (x̄)</span>
                    <span className="text-base font-mono font-bold text-slate-100">{provenance.statistical_summary.mean.toFixed(2)}</span>
                  </div>
                  <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                    <span className="text-[11px] font-mono text-slate-400 block">Median (p50)</span>
                    <span className="text-base font-mono font-bold text-slate-100">{provenance.statistical_summary.median.toFixed(2)}</span>
                  </div>
                  <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                    <span className="text-[11px] font-mono text-slate-400 block">Standard Deviation (s)</span>
                    <span className="text-base font-mono font-bold text-slate-100">{provenance.statistical_summary.standard_deviation.toFixed(2)}</span>
                  </div>
                  <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                    <span className="text-[11px] font-mono text-slate-400 block">95% Confidence Interval</span>
                    <span className="text-xs font-mono font-bold text-emerald-400">
                      [{provenance.statistical_summary.confidence_interval_95[0].toFixed(2)}, {provenance.statistical_summary.confidence_interval_95[1].toFixed(2)}]
                    </span>
                  </div>
                  <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                    <span className="text-[11px] font-mono text-slate-400 block">95th Percentile (p95)</span>
                    <span className="text-base font-mono font-bold text-slate-100">{provenance.statistical_summary.p95.toFixed(2)}</span>
                  </div>
                  <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
                    <span className="text-[11px] font-mono text-slate-400 block">Distribution Model</span>
                    <span className="text-xs font-mono font-bold text-cyan-300">{provenance.statistical_summary.distribution_model}</span>
                  </div>
                </div>
              ) : (
                <div className="p-8 text-center bg-slate-950 rounded-xl border border-slate-800 text-slate-400 font-mono text-xs">
                  Deterministic point calculation with n = {provenance.sample_size} raw events. Statistical dispersion analysis enabled on multi-sample latency and duration metrics.
                </div>
              )}
            </div>
          )}

          {activeTab === 'LINEAGE' && (
            <div className="space-y-4">
              <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
                <span className="text-xs font-mono text-slate-400 block">Merkle Event Lineage Root (SHA-256):</span>
                <div className="flex items-center justify-between font-mono text-xs text-cyan-400 bg-slate-900 p-2.5 rounded border border-slate-800">
                  <span className="truncate select-all">{provenance.merkle_events_root_sha256}</span>
                  <button
                    onClick={() => copyToClipboard(provenance.merkle_events_root_sha256, 'merkle')}
                    className="ml-2 text-slate-400 hover:text-slate-200 underline font-sans text-[11px]"
                  >
                    {copiedKey === 'merkle' ? 'Copied' : 'Copy'}
                  </button>
                </div>
              </div>

              <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-1 text-xs font-mono text-slate-300">
                <div className="flex justify-between">
                  <span className="text-slate-400">Calculation Timestamp:</span>
                  <span>{provenance.calculated_at_utc}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Formula Identifier:</span>
                  <span className="text-indigo-300">{provenance.formula_id}</span>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'RAW_EVENTS' && (
            <div className="space-y-2">
              <span className="text-xs font-mono text-slate-400 block">Contributing Raw Event IDs ({provenance.raw_event_ids?.length || 0}):</span>
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 max-h-60 overflow-y-auto space-y-1 font-mono text-xs">
                {provenance.raw_event_ids?.map((id, idx) => (
                  <div key={id} className="flex items-center justify-between py-1 border-b border-slate-900/80 text-slate-300">
                    <span>#{idx + 1} {id}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="flex items-center justify-between px-6 py-3 border-t border-slate-800 bg-slate-950/50 text-xs font-mono">
          <span className="text-slate-400">
            Audit Lineage: <span className="text-emerald-400">Verified Deterministic</span>
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
