import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { scientificApiClient } from '../../services/scientificApiClient';
import type { TraceTreeData, TraceSpanData } from '../../types/scientificMetrics';

const defaultTraceTrees: TraceTreeData[] = [
  {
    trace_id: '4bf92f3577b34da6a3ce929d0e0e4736',
    total_spans: 6,
    total_duration_ms: 382.5,
    critical_path_ms: 245.0,
    root_spans: [
      {
        span_id: 'span_root_0',
        trace_id: '4bf92f3577b34da6a3ce929d0e0e4736',
        parent_span_id: null,
        event_id: 'evt_goal_0',
        event_type: 'MissionCreated',
        agent_id: 'COORDINATOR',
        worker_id: null,
        timestamp: '2026-09-09T12:00:00Z',
        duration_ms: 12.0,
        status: 'COMPLETED',
        payload: { goal: 'Thermal Scan Extraction & Audit' },
        children: [
          {
            span_id: 'span_planner_1',
            trace_id: '4bf92f3577b34da6a3ce929d0e0e4736',
            parent_span_id: 'span_root_0',
            event_id: 'evt_plan_1',
            event_type: 'PlannerStarted',
            agent_id: 'PLANNER',
            worker_id: 'planner_engine_v2',
            timestamp: '2026-09-09T12:00:01Z',
            duration_ms: 85.0,
            status: 'COMPLETED',
            payload: { node_count: 8, algorithm: 'Bayesian_DAG_Optimization' },
            children: [
              {
                span_id: 'span_ocr_2',
                trace_id: '4bf92f3577b34da6a3ce929d0e0e4736',
                parent_span_id: 'span_planner_1',
                event_id: 'evt_ocr_2',
                event_type: 'WorkerStarted',
                agent_id: 'VISION',
                worker_id: 'ocr_pool_01',
                timestamp: '2026-09-09T12:00:02Z',
                duration_ms: 148.0,
                status: 'COMPLETED',
                payload: { task: 'Adaptive High-Pass OCR Binarization' },
                children: [],
              },
              {
                span_id: 'span_val_3',
                trace_id: '4bf92f3577b34da6a3ce929d0e0e4736',
                parent_span_id: 'span_planner_1',
                event_id: 'evt_val_3',
                event_type: 'ValidationStarted',
                agent_id: 'VALIDATION',
                worker_id: 'schema_validator',
                timestamp: '2026-09-09T12:00:03Z',
                duration_ms: 42.5,
                status: 'COMPLETED',
                payload: { sample_size: 53, power: 0.84 },
                children: [],
              },
            ],
          },
          {
            span_id: 'span_mem_4',
            trace_id: '4bf92f3577b34da6a3ce929d0e0e4736',
            parent_span_id: 'span_root_0',
            event_id: 'evt_mem_4',
            event_type: 'MemoryRetrieved',
            agent_id: 'MEMORY',
            worker_id: 'causal_memory_index',
            timestamp: '2026-09-09T12:00:01Z',
            duration_ms: 95.0,
            status: 'COMPLETED',
            payload: { matched_invariants: 4, recall_retention: 0.98 },
            children: [],
          },
        ],
      },
    ],
  },
];

export const RuntimeTraceGraph: React.FC = () => {
  const [traceTrees, setTraceTrees] = useState<TraceTreeData[]>(defaultTraceTrees);
  const [selectedSpan, setSelectedSpan] = useState<TraceSpanData | null>(null);
  const [collapsedSpans, setCollapsedSpans] = useState<Set<string>>(new Set());

  useEffect(() => {
    scientificApiClient
      .fetchRuntimeTraces()
      .then((trees) => {
        if (trees && trees.length > 0) {
          setTraceTrees(trees);
        }
      })
      .catch(() => {
        setTraceTrees(defaultTraceTrees);
      });
  }, []);

  const toggleCollapse = (spanId: string) => {
    setCollapsedSpans((prev) => {
      const next = new Set(prev);
      if (next.has(spanId)) next.delete(spanId);
      else next.add(spanId);
      return next;
    });
  };

  const getLatencyColor = (durationMs: number) => {
    if (durationMs > 200) return 'text-rose-400 border-rose-700/50 bg-rose-950/40';
    if (durationMs > 80) return 'text-amber-300 border-amber-700/50 bg-amber-950/40';
    return 'text-emerald-400 border-emerald-700/50 bg-emerald-950/40';
  };

  const renderSpan = (span: TraceSpanData, depth: number = 0) => {
    const isCollapsed = collapsedSpans.has(span.span_id);
    const hasChildren = span.children && span.children.length > 0;

    return (
      <div key={span.span_id} className="space-y-2">
        <div
          onClick={() => setSelectedSpan(span)}
          className={`flex items-center justify-between p-3 rounded-xl border transition-all cursor-pointer ${
            selectedSpan?.span_id === span.span_id
              ? 'bg-[#1e293b] border-cyan-400 shadow-lg'
              : 'bg-slate-950/70 border-slate-800 hover:border-slate-700'
          }`}
          style={{ marginLeft: `${depth * 24}px` }}
        >
          <div className="flex items-center gap-3">
            {hasChildren ? (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  toggleCollapse(span.span_id);
                }}
                className="text-slate-400 hover:text-slate-200 text-xs font-bold w-4 text-center"
              >
                {isCollapsed ? '▶' : '▼'}
              </button>
            ) : (
              <span className="w-4 text-center text-slate-600">•</span>
            )}

            <div>
              <div className="flex items-center gap-2">
                <span className="font-semibold text-slate-100 text-xs font-sans">{span.event_type}</span>
                <Badge variant="intelligence" size="sm">
                  {span.agent_id || 'ENGINE'}
                </Badge>
              </div>
              <span className="text-[11px] font-mono text-slate-400">Span: {span.span_id}</span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className={`px-2.5 py-1 rounded text-xs font-mono font-bold border ${getLatencyColor(span.duration_ms)}`}>
              {span.duration_ms.toFixed(1)} ms
            </span>
          </div>
        </div>

        {!isCollapsed && hasChildren && (
          <div className="space-y-2">
            {span.children.map((child) => renderSpan(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  const primaryTree = traceTrees[0];

  return (
    <Card className="w-full bg-[#0F172A]/90 border-[#1E293B] shadow-2xl overflow-hidden">
      <CardHeader className="flex flex-row items-center justify-between py-4 px-6 border-b border-[#1E293B] bg-[#131D35]/50">
        <div>
          <div className="flex items-center gap-2">
            <Badge variant="intelligence" size="sm">
              OPENTELEMETRY TRACE GRAPH
            </Badge>
            <span className="text-xs text-[#94A3B8] font-mono">
              Hierarchical Execution Spans
            </span>
          </div>
          <CardTitle className="mt-1 text-base font-bold text-[#F8FAFC]">
            Runtime Causal Execution & Trace Trees
          </CardTitle>
        </div>

        {primaryTree && (
          <div className="flex items-center gap-4 font-mono text-xs">
            <div>
              <span className="text-slate-400">Total Duration: </span>
              <strong className="text-slate-100">{primaryTree.total_duration_ms} ms</strong>
            </div>
            <div>
              <span className="text-slate-400">Critical Path: </span>
              <strong className="text-cyan-400">{primaryTree.critical_path_ms} ms</strong>
            </div>
          </div>
        )}
      </CardHeader>

      <CardContent className="p-6 space-y-6">
        {primaryTree ? (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Trace Tree Visualizer */}
            <div className="lg:col-span-2 space-y-2">
              <span className="text-xs font-mono text-slate-400 block mb-2">
                Execution Span Hierarchy ({primaryTree.total_spans} spans):
              </span>
              <div className="space-y-2 max-h-[500px] overflow-y-auto pr-2">
                {primaryTree.root_spans.map((root) => renderSpan(root, 0))}
              </div>
            </div>

            {/* Span Detail Inspector */}
            <div className="p-4 bg-slate-950 rounded-xl border border-slate-800 space-y-4 font-mono text-xs">
              <div className="border-b border-slate-800 pb-2">
                <span className="font-bold text-slate-100 text-sm font-sans block">Span Inspector</span>
                <span className="text-[11px] text-slate-400">
                  {selectedSpan ? selectedSpan.span_id : 'Select any span to inspect payload'}
                </span>
              </div>

              {selectedSpan ? (
                <div className="space-y-3">
                  <div>
                    <span className="text-slate-400 block text-[11px]">Event Type:</span>
                    <span className="text-cyan-300 font-semibold">{selectedSpan.event_type}</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[11px]">Duration:</span>
                    <span className="text-slate-200">{selectedSpan.duration_ms} ms</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[11px]">Agent / Worker:</span>
                    <span className="text-indigo-300">{selectedSpan.agent_id || selectedSpan.worker_id || 'ENGINE'}</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[11px]">Timestamp:</span>
                    <span className="text-slate-300">{selectedSpan.timestamp}</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[11px] mb-1">Payload JSON:</span>
                    <pre className="p-2.5 bg-slate-900 rounded border border-slate-800 text-[11px] text-slate-300 overflow-x-auto max-h-48 leading-relaxed">
                      {JSON.stringify(selectedSpan.payload, null, 2)}
                    </pre>
                  </div>
                </div>
              ) : (
                <div className="p-8 text-center text-slate-400">
                  Click any span row to view its OpenTelemetry execution context and payload metadata.
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="p-8 text-center text-slate-400 font-mono text-xs">
            Loading runtime trace tree...
          </div>
        )}
      </CardContent>
    </Card>
  );
};
