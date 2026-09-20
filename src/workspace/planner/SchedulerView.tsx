import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Cpu } from 'lucide-react';

export const SchedulerView: React.FC = () => {
  const workers = [
    { id: 'worker-ocr-01', role: 'OCR_EXTRACTION', status: 'BUSY', cpu: 28.5, mem: '256 MB', activeTask: 'node_ocr_chunk_1', completed: 18 },
    { id: 'worker-ocr-02', role: 'OCR_EXTRACTION', status: 'BUSY', cpu: 34.0, mem: '256 MB', activeTask: 'node_ocr_chunk_2', completed: 14 },
    { id: 'worker-extract-01', role: 'SCHEMA_EXTRACTION', status: 'RUNNING', cpu: 18.0, mem: '512 MB', activeTask: 'node_merge_ocr', completed: 22 },
    { id: 'worker-validate-01', role: 'SCIENTIFIC_VALIDATION', status: 'IDLE', cpu: 5.0, mem: '128 MB', activeTask: 'None', completed: 20 },
    { id: 'worker-gov-01', role: 'GOVERNANCE_AUDIT', status: 'IDLE', cpu: 3.0, mem: '128 MB', activeTask: 'None', completed: 8 },
    { id: 'worker-trust-01', role: 'TRUTH_LEDGER_COMMIT', status: 'IDLE', cpu: 4.0, mem: '256 MB', activeTask: 'None', completed: 12 },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 rounded-xl text-emerald-400">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Runtime DAG Scheduler & Concurrency Wavefronts
                <Badge variant="success" size="sm">6 Workers Online</Badge>
              </h1>
              <p className="text-xs text-[#94A3B8] font-mono">
                Load balancing, queue latencies, and capability matching heuristics
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3 font-mono text-xs">
          <Badge variant="intelligence" size="md">Concurrency Limit: 8</Badge>
          <Badge variant="outline" size="md">Avg Queue: 14.5ms</Badge>
        </div>
      </div>

      {/* Worker Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 font-mono">
        {workers.map(w => (
          <Card key={w.id} className="p-4 rounded-xl border border-[#1E293B] bg-[#0F172A] space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-white">{w.id}</span>
              <Badge variant={w.status === 'BUSY' ? 'warning' : w.status === 'RUNNING' ? 'intelligence' : 'success'} size="sm">
                {w.status}
              </Badge>
            </div>

            <div className="text-[11px] text-[#94A3B8]">Role: <span className="text-white font-semibold">{w.role}</span></div>

            <div className="p-2.5 bg-[#131D35] rounded-lg border border-[#1E293B] space-y-1 text-xs">
              <div className="flex justify-between text-[#64748B]">
                <span>Active Task:</span>
                <span className="text-cyan-400 font-bold">{w.activeTask}</span>
              </div>
              <div className="flex justify-between text-[#64748B]">
                <span>CPU / Mem:</span>
                <span className="text-white">{w.cpu}% • {w.mem}</span>
              </div>
            </div>

            <div className="flex justify-between items-center text-[10px] text-[#64748B] pt-2 border-t border-[#1E293B]">
              <span>Tasks Completed: {w.completed}</span>
              <span className="text-emerald-400 font-semibold">Healthy</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
