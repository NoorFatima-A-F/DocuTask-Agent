import React, { useState, useEffect } from 'react';
import {
  ListTree,
  Clock,
  Zap,
  CheckCircle,
  XCircle,
  Code,
  Search,
  RefreshCw,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';
import { ExecutionTrace, Span } from '../../types/aiOperations';

export const ExecutionTraceExplorer: React.FC = () => {
  const [traces, setTraces] = useState<ExecutionTrace[]>([]);
  const [selectedTrace, setSelectedTrace] = useState<ExecutionTrace | null>(null);
  const [selectedSpan, setSelectedSpan] = useState<Span | null>(null);
  const [loading, setLoading] = useState(true);
  const [filterQuery, setFilterQuery] = useState('');

  const loadTraces = async () => {
    try {
      setLoading(true);
      const data = await AIOperationsApiClient.getTraces(50);
      setTraces(data);
      const first = data[0];
      if (first && !selectedTrace) {
        setSelectedTrace(first);
        if (first.spans && first.spans.length > 0) {
          setSelectedSpan(first.spans[0] || null);
        }
      }
    } catch (err) {
      console.error('Failed to load traces:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTraces();
  }, []);

  const handleSelectTrace = (trace: ExecutionTrace) => {
    setSelectedTrace(trace);
    if (trace.spans && trace.spans.length > 0) {
      setSelectedSpan(trace.spans[0] || null);
    } else {
      setSelectedSpan(null);
    }
  };

  const filteredTraces = traces.filter(
    (t) =>
      t.root_span_name.toLowerCase().includes(filterQuery.toLowerCase()) ||
      t.agent_id.toLowerCase().includes(filterQuery.toLowerCase()) ||
      t.trace_id.toLowerCase().includes(filterQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-indigo-500/10 rounded-xl border border-indigo-500/20">
            <ListTree className="w-6 h-6 text-indigo-400" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Execution Trace Explorer</h1>
            <p className="text-xs text-slate-400">OpenTelemetry span waterfall, reasoning latency, and token breakdowns</p>
          </div>
        </div>
        <Button variant="outline" onClick={loadTraces} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Trace List (4 cols) */}
        <div className="lg:col-span-4 space-y-3">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
            <input
              type="text"
              placeholder="Filter by agent, trace ID, or name..."
              className="w-full bg-slate-900/60 border border-slate-800 rounded-xl pl-9 pr-4 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
              value={filterQuery}
              onChange={(e) => setFilterQuery(e.target.value)}
            />
          </div>

          <div className="space-y-2 max-h-[600px] overflow-y-auto pr-1">
            {filteredTraces.map((trace) => (
              <Card
                key={trace.trace_id}
                className={`p-3.5 cursor-pointer transition-all border ${
                  selectedTrace?.trace_id === trace.trace_id
                    ? 'bg-indigo-950/30 border-indigo-500/50 shadow-md shadow-indigo-950/20'
                    : 'bg-slate-900/40 border-slate-800/80 hover:bg-slate-800/40'
                }`}
                onClick={() => handleSelectTrace(trace)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    {trace.status === 'OK' ? (
                      <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                    ) : (
                      <XCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
                    )}
                    <h3 className="font-semibold text-white text-xs line-clamp-1">{trace.root_span_name}</h3>
                  </div>
                  <Badge variant={trace.status === 'OK' ? 'success' : 'error'}>{trace.status}</Badge>
                </div>
                <div className="flex items-center justify-between mt-2.5 text-[11px] text-slate-400">
                  <span className="font-mono">{trace.agent_id}</span>
                  <span className="flex items-center gap-1 font-semibold text-slate-300">
                    <Clock className="w-3 h-3 text-cyan-400" />
                    {trace.total_duration_ms.toFixed(1)} ms
                  </span>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Trace Details & Waterfall (8 cols) */}
        <div className="lg:col-span-8 space-y-4">
          {selectedTrace ? (
            <>
              <Card className="p-5 bg-slate-900/50 border-slate-800">
                <div className="flex items-start justify-between border-b border-slate-800 pb-3">
                  <div>
                    <h2 className="text-base font-bold text-white">{selectedTrace.root_span_name}</h2>
                    <p className="text-xs text-slate-400 font-mono mt-0.5">
                      Trace ID: {selectedTrace.trace_id} • Session: {selectedTrace.session_id}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant="intelligence">
                      <Zap className="w-3 h-3 inline mr-1 text-amber-400" />
                      {selectedTrace.total_prompt_tokens + selectedTrace.total_completion_tokens} Tokens
                    </Badge>
                    <Badge variant="default">${selectedTrace.total_cost_usd.toFixed(4)}</Badge>
                  </div>
                </div>

                {/* Waterfall Spans */}
                <div className="mt-4 space-y-2">
                  <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Span Waterfall</h4>
                  <div className="space-y-1.5">
                    {selectedTrace.spans.map((span) => {
                      const pct = Math.max(8, Math.min(100, (span.duration_ms / Math.max(1, selectedTrace.total_duration_ms)) * 100));
                      const isSelected = selectedSpan?.span_id === span.span_id;
                      return (
                        <div
                          key={span.span_id}
                          className={`p-2.5 rounded-xl border cursor-pointer transition-all ${
                            isSelected
                              ? 'bg-slate-800/80 border-indigo-500'
                              : 'bg-slate-950/40 border-slate-800/60 hover:bg-slate-800/40'
                          }`}
                          onClick={() => setSelectedSpan(span)}
                        >
                          <div className="flex items-center justify-between text-xs mb-1">
                            <div className="flex items-center gap-2">
                              <Badge variant={span.span_type === 'LLM_CALL' ? 'intelligence' : 'outline'}>
                                {span.span_type}
                              </Badge>
                              <span className="font-medium text-white">{span.name}</span>
                            </div>
                            <span className="text-slate-300 font-mono">{span.duration_ms.toFixed(1)} ms</span>
                          </div>
                          <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden">
                            <div
                              className={`h-full rounded-full ${
                                span.status === 'ERROR'
                                  ? 'bg-rose-500'
                                  : span.span_type === 'LLM_CALL'
                                  ? 'bg-indigo-500'
                                  : 'bg-cyan-500'
                              }`}
                              style={{ width: `${pct}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Span Inspector */}
                {selectedSpan && (
                  <div className="mt-5 border-t border-slate-800 pt-4 space-y-3">
                    <div className="flex items-center justify-between">
                      <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                        <Code className="w-3.5 h-3.5 text-indigo-400" /> Span Inspector ({selectedSpan.name})
                      </h4>
                      <Badge variant={selectedSpan.status === 'OK' ? 'success' : 'error'}>
                        {selectedSpan.status}
                      </Badge>
                    </div>

                    <div className="grid grid-cols-2 gap-3 text-xs bg-slate-950/60 p-3 rounded-xl border border-slate-800/80">
                      <div>
                        <span className="text-slate-500">Span ID:</span>{' '}
                        <span className="font-mono text-slate-300">{selectedSpan.span_id}</span>
                      </div>
                      <div>
                        <span className="text-slate-500">Duration:</span>{' '}
                        <span className="font-mono text-slate-300">{selectedSpan.duration_ms.toFixed(1)} ms</span>
                      </div>
                      <div>
                        <span className="text-slate-500">Token Usage:</span>{' '}
                        <span className="font-mono text-slate-300">
                          {selectedSpan.token_usage?.total_tokens ?? 0} ({selectedSpan.token_usage?.prompt_tokens ?? 0} prompt / {selectedSpan.token_usage?.completion_tokens ?? 0} comp)
                        </span>
                      </div>
                      <div>
                        <span className="text-slate-500">Cost:</span>{' '}
                        <span className="font-mono text-slate-300">${selectedSpan.cost_usd.toFixed(5)}</span>
                      </div>
                    </div>

                    {selectedSpan.error_message && (
                      <div className="p-3 bg-rose-950/30 border border-rose-500/30 rounded-xl text-xs text-rose-300">
                        <strong>Error:</strong> {selectedSpan.error_message}
                      </div>
                    )}
                  </div>
                )}
              </Card>
            </>
          ) : (
            <Card className="p-8 text-center text-slate-400 bg-slate-900/40 border-slate-800">
              <ListTree className="w-8 h-8 text-slate-600 mx-auto mb-2" />
              <p>Select an execution trace to inspect the distributed span call tree.</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
