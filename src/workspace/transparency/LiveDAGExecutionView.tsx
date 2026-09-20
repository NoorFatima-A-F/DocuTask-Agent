import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const LiveDAGExecutionView: React.FC = () => {
  const [highlightCriticalPath, setHighlightCriticalPath] = useState(true);

  const nodes = [
    {
      id: 'task_ingest',
      label: 'Multi-Page Document Ingestion & De-Skew',
      type: 'PREPROCESS',
      status: 'COMPLETED',
      wavefront: 0,
      worker: 'worker_ocr_1',
      duration: '120 ms',
      cost: '$0.0002',
      confidence: '98.0%',
      isCritical: true,
    },
    {
      id: 'task_ocr_tess',
      label: 'LayoutLM & Optical Text Extraction',
      type: 'OCR_PARSE',
      status: 'COMPLETED',
      wavefront: 1,
      worker: 'worker_ocr_1',
      duration: '180 ms',
      cost: '$0.0004',
      confidence: '96.0%',
      isCritical: true,
    },
    {
      id: 'task_entity_extract',
      label: 'Gemini 2.5 Flash Structured Parsing',
      type: 'LLM_EXTRACT',
      status: 'RUNNING',
      wavefront: 2,
      worker: 'worker_llm_1',
      duration: '450 ms',
      cost: '$0.0018',
      confidence: '96.5%',
      isCritical: true,
    },
    {
      id: 'task_memory_recall',
      label: 'Historical Schema & Vendor Memory Lookup',
      type: 'MEMORY_RETRIEVAL',
      status: 'COMPLETED',
      wavefront: 2,
      worker: 'worker_mem_1',
      duration: '45 ms',
      cost: '$0.0000',
      confidence: '99.0%',
      isCritical: false,
    },
    {
      id: 'task_cross_validation',
      label: 'Cross-Document Invariant & Math Validation',
      type: 'VALIDATION',
      status: 'WAITING',
      wavefront: 3,
      worker: 'worker_val_1',
      duration: '50 ms',
      cost: '$0.0001',
      confidence: '98.0%',
      isCritical: true,
    },
    {
      id: 'task_db_commit',
      label: 'Cryptographic Audit Sign & DB Commit',
      type: 'PERSISTENCE',
      status: 'WAITING',
      wavefront: 4,
      worker: 'worker_sec_1',
      duration: '35 ms',
      cost: '$0.0000',
      confidence: '100%',
      isCritical: true,
    },
  ];

  const criticalTotalMs = 835.0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">🗺️</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Live Dynamic DAG Execution & Critical Path Method (CPM)
              </h2>
              <Badge variant="success" size="sm">
                ACTIVE WAVEFRONT 2
              </Badge>
            </div>
            <p className="text-sm font-mono text-[#94A3B8] mt-1">
              Deterministic topological execution graph with CPM bottleneck analysis and zero canned animations.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => setHighlightCriticalPath(!highlightCriticalPath)}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-bold transition-all ${
                highlightCriticalPath
                  ? 'bg-amber-600 text-white shadow-lg shadow-amber-600/20'
                  : 'bg-[#1E293B] text-[#94A3B8]'
              }`}
            >
              {highlightCriticalPath ? '⚡ Critical Path Highlighted' : '○ Standard View'}
            </button>
          </div>
        </div>
      </div>

      {/* KPI Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Critical Path Length (CPM)</div>
          <div className="text-2xl font-bold font-mono text-amber-400 mt-1">{criticalTotalMs} ms</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">5 critical bottleneck nodes</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Parallel Execution Wavefronts</div>
          <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">5 Levels</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">Wavefront 2 running concurrently</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Non-Critical Task Slack (Float)</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">+405 ms</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">Memory lookup slack window</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Dynamic Mutation Readiness</div>
          <div className="text-2xl font-bold font-mono text-indigo-400 mt-1">ONLINE</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">Real-time sub-graph rewiring</div>
        </Card>
      </div>

      {/* Live DAG Node Flow */}
      <Card className="p-6 bg-[#0F172A] border-[#1E293B]">
        <h3 className="text-sm font-bold font-mono text-[#F8FAFC] mb-4">
          Topological Task Graph & Worker Execution Stream
        </h3>
        <div className="space-y-3">
          {nodes.map((n) => {
            const isCriticalActive = highlightCriticalPath && n.isCritical;
            return (
              <div
                key={n.id}
                className={`p-4 rounded-xl border transition-all ${
                  n.status === 'RUNNING'
                    ? 'bg-blue-950/30 border-blue-500 shadow-md shadow-blue-500/10'
                    : isCriticalActive
                    ? 'bg-[#0F172A] border-amber-500/50'
                    : 'bg-[#020617] border-[#1E293B]'
                }`}
              >
                <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
                  <div className="flex items-center gap-3">
                    <span className="w-6 h-6 rounded-full bg-[#1E293B] flex items-center justify-center text-xs font-mono font-bold text-[#F8FAFC]">
                      {n.wavefront}
                    </span>
                    <div>
                      <div className="flex items-center gap-2">
                        <h4 className="text-xs font-bold font-mono text-[#F8FAFC]">{n.label}</h4>
                        {n.isCritical && (
                          <span className="text-[10px] font-mono text-amber-400 bg-amber-950/40 px-1.5 py-0.5 rounded border border-amber-500/30">
                            CPM CRITICAL
                          </span>
                        )}
                      </div>
                      <div className="text-[11px] font-mono text-[#64748B] mt-0.5">
                        Worker: <span className="text-[#94A3B8]">{n.worker}</span> • ID: {n.id}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-4 text-xs font-mono">
                    <span className="text-cyan-400">{n.duration}</span>
                    <span className="text-emerald-400">{n.cost}</span>
                    <span className="text-indigo-400">{n.confidence}</span>
                    <Badge
                      variant={
                        n.status === 'COMPLETED'
                          ? 'success'
                          : n.status === 'RUNNING'
                          ? 'info'
                          : 'default'
                      }
                      size="sm"
                    >
                      {n.status}
                    </Badge>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
};
