import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Network, CheckCircle2, ArrowRight } from 'lucide-react';

export const PlannerDAGReplay: React.FC = () => {
  const dagNodes = [
    { id: 'node_ocr_01', name: 'OCR Text & Layout', worker: 'worker_gpu_ocr', status: 'COMPLETED', duration: '285ms' },
    { id: 'node_schema_01', name: 'Schema Matching & Field Extraction', worker: 'worker_schema_01', status: 'COMPLETED', duration: '190ms' },
    { id: 'node_smt_01', name: 'SMT Balance Verification', worker: 'worker_truth_01', status: 'COMPLETED', duration: '45ms' },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-indigo-500/20 to-blue-500/20 border border-indigo-500/30 rounded-xl text-indigo-400">
              <Network className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Planner & DAG Replay Studio
                <Badge variant="intelligence" size="sm">Wavefront Sequencing</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Event-driven reconstruction of planner state transitions, DAG topology, and worker scheduling.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" size="sm">Critical Path: 520ms</Badge>
        </div>
      </div>

      {/* DAG Flow Visualization */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
        {dagNodes.map((n, idx) => (
          <Card key={n.id} className="p-5 bg-[#0F172A] border-[#1E293B] space-y-3 relative hover:border-indigo-500/40 transition-all">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <span className="font-bold text-cyan-400">Step #{idx + 1}</span>
              <Badge variant="success" size="sm">
                <CheckCircle2 className="w-3 h-3 inline mr-1" />
                {n.status}
              </Badge>
            </div>

            <div>
              <div className="text-sm font-bold text-white">{n.name}</div>
              <div className="text-slate-400 text-[11px] mt-0.5">ID: {n.id}</div>
            </div>

            <div className="p-2.5 bg-slate-900/60 rounded border border-slate-800 space-y-1 text-[11px]">
              <div className="text-slate-400">Worker: <span className="text-purple-300 font-bold">{n.worker}</span></div>
              <div className="text-slate-400">Duration: <span className="text-emerald-400 font-bold">{n.duration}</span></div>
            </div>

            {idx < dagNodes.length - 1 && (
              <div className="hidden md:flex absolute -right-3 top-1/2 -translate-y-1/2 z-10 w-6 h-6 rounded-full bg-slate-800 border border-slate-700 items-center justify-center text-slate-400">
                <ArrowRight className="w-3 h-3" />
              </div>
            )}
          </Card>
        ))}
      </div>
    </div>
  );
};
