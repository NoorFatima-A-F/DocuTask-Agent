import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { ListFilter } from 'lucide-react';

export const QueueMonitorView: React.FC = () => {
  const queues = [
    { name: 'RUNNING', count: 1, color: 'text-indigo-400', border: 'border-indigo-500/40', tasks: [{ id: 'node_merge_ocr', name: 'Merge OCR Texts', worker: 'worker-extract-01' }] },
    { name: 'WAITING', count: 4, color: 'text-cyan-400', border: 'border-cyan-500/40', tasks: [{ id: 'node_extract_schema', name: 'Extract Financial Schema', worker: 'Unassigned' }, { id: 'node_validate_invariants', name: 'Scientific Validation Check', worker: 'Unassigned' }, { id: 'node_barrier_governance', name: 'Governance Sync Barrier', worker: 'Unassigned' }, { id: 'node_join_finalize', name: 'Join & Truth Ledger Commit', worker: 'Unassigned' }] },
    { name: 'COMPLETED', count: 4, color: 'text-emerald-400', border: 'border-emerald-500/40', tasks: [{ id: 'node_goal_ingress', name: 'Mission Goal Ingress', worker: 'worker-planner-01' }, { id: 'node_split_ocr', name: 'Split OCR Chunks', worker: 'worker-dag-01' }, { id: 'node_ocr_chunk_1', name: 'OCR Page 1-2 (Raster)', worker: 'worker-ocr-01' }, { id: 'node_ocr_chunk_2', name: 'OCR Page 3-4 (Tables)', worker: 'worker-ocr-02' }] },
    { name: 'BLOCKED', count: 0, color: 'text-amber-400', border: 'border-amber-500/40', tasks: [] },
    { name: 'RETRY', count: 0, color: 'text-orange-400', border: 'border-orange-500/40', tasks: [] },
    { name: 'RECOVERY', count: 0, color: 'text-purple-400', border: 'border-purple-500/40', tasks: [] },
    { name: 'FAILED', count: 0, color: 'text-red-400', border: 'border-red-500/40', tasks: [] },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-cyan-500/20 to-teal-500/20 border border-cyan-500/30 rounded-xl text-cyan-400">
              <ListFilter className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Runtime Execution Queues & Task Distribution
                <Badge variant="success" size="sm">7 Queues Active</Badge>
              </h1>
              <p className="text-xs text-[#94A3B8] font-mono">
                Real-time queue partitions: Waiting, Running, Blocked, Retry, Recovery, Completed, Failed
              </p>
            </div>
          </div>
        </div>

        <Badge variant="intelligence" size="md">9 Tasks Total</Badge>
      </div>

      {/* Queue Columns */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 font-mono">
        {queues.map(q => (
          <Card key={q.name} className={`p-4 rounded-xl border ${q.border} bg-[#0F172A] space-y-3`}>
            <div className="flex items-center justify-between">
              <span className={`text-xs font-bold ${q.color}`}>{q.name}</span>
              <Badge variant="outline" size="sm">{q.count}</Badge>
            </div>

            <div className="space-y-2">
              {q.tasks.length === 0 ? (
                <div className="text-[11px] text-[#64748B] italic py-2 text-center">No tasks in queue</div>
              ) : (
                q.tasks.map(t => (
                  <div key={t.id} className="p-2.5 bg-[#131D35] rounded-lg border border-[#1E293B] space-y-1 text-xs">
                    <div className="font-bold text-white text-[11px]">{t.name}</div>
                    <div className="text-[10px] text-[#64748B] flex justify-between">
                      <span>{t.id}</span>
                      <span className="text-[#94A3B8]">{t.worker}</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
