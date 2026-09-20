import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Layers } from 'lucide-react';

export const TaskDecompositionView: React.FC = () => {
  const decompositionPipeline = [
    { step: 1, name: 'OCR Document Ingestion', type: 'PARALLEL', worker: 'worker-ocr-01', duration: '120ms', cost: '$0.0006', confidence: 0.992, status: 'COMPLETED' },
    { step: 2, name: 'OCR Table Segmentation', type: 'PARALLEL', worker: 'worker-ocr-02', duration: '140ms', cost: '$0.0006', confidence: 0.988, status: 'COMPLETED' },
    { step: 3, name: 'Extract Invoice Fields', type: 'SEQUENTIAL', worker: 'worker-extract-01', duration: '200ms', cost: '$0.0010', confidence: 0.980, status: 'COMPLETED' },
    { step: 4, name: 'Normalize Schema', type: 'SEQUENTIAL', worker: 'worker-extract-01', duration: '80ms', cost: '$0.0003', confidence: 0.995, status: 'RUNNING' },
    { step: 5, name: 'Cross Validation', type: 'PARALLEL', worker: 'worker-validate-01', duration: '110ms', cost: '$0.0004', confidence: 0.999, status: 'WAITING' },
    { step: 6, name: 'Evidence Verification', type: 'PARALLEL', worker: 'worker-validate-01', duration: '90ms', cost: '$0.0003', confidence: 0.995, status: 'WAITING' },
    { step: 7, name: 'Memory Retrieval', type: 'SEQUENTIAL', worker: 'worker-memory-01', duration: '60ms', cost: '$0.0002', confidence: 0.990, status: 'WAITING' },
    { step: 8, name: 'Trust Ledger Update', type: 'JOIN', worker: 'worker-trust-01', duration: '70ms', cost: '$0.0002', confidence: 1.000, status: 'WAITING' },
    { step: 9, name: 'Final Output Persistence', type: 'SEQUENTIAL', worker: 'worker-storage-01', duration: '50ms', cost: '$0.0001', confidence: 1.000, status: 'WAITING' },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-purple-500/20 to-indigo-500/20 border border-purple-500/30 rounded-xl text-purple-400">
              <Layers className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Hierarchical Task Decomposition Engine
                <Badge variant="success" size="sm">9 Tasks Generated</Badge>
              </h1>
              <p className="text-xs text-[#94A3B8] font-mono">
                Multi-stage task hierarchy with deterministic worker mapping and cost projections
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant="intelligence" size="md">Parallel Wavefront: 2.4x</Badge>
          <Badge variant="outline" size="md">Total Est: 920ms</Badge>
        </div>
      </div>

      {/* Task List */}
      <div className="space-y-3 font-mono">
        {decompositionPipeline.map((task) => (
          <Card key={task.step} className="p-4 rounded-xl border border-[#1E293B] bg-[#0F172A] flex flex-wrap items-center justify-between gap-4 hover:border-purple-500/40 transition-all">
            <div className="flex items-center gap-4">
              <div className="w-8 h-8 rounded-lg bg-[#131D35] border border-[#1E293B] flex items-center justify-center text-xs font-bold text-cyan-400">
                0{task.step}
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-xs font-bold text-white">{task.name}</h3>
                  <Badge variant={task.type === 'PARALLEL' ? 'info' : task.type === 'JOIN' ? 'intelligence' : 'default'} size="sm">
                    {task.type}
                  </Badge>
                </div>
                <div className="text-[11px] text-[#64748B]">Assigned: <span className="text-[#94A3B8]">{task.worker}</span></div>
              </div>
            </div>

            <div className="flex items-center gap-6 text-xs">
              <div>
                <span className="text-[10px] text-[#64748B] block">EST LATENCY</span>
                <span className="text-white font-semibold">{task.duration}</span>
              </div>
              <div>
                <span className="text-[10px] text-[#64748B] block">EST COST</span>
                <span className="text-emerald-400 font-semibold">{task.cost}</span>
              </div>
              <div>
                <span className="text-[10px] text-[#64748B] block">CONFIDENCE</span>
                <span className="text-purple-400 font-semibold">{(task.confidence * 100).toFixed(1)}%</span>
              </div>
              <Badge variant={task.status === 'COMPLETED' ? 'success' : task.status === 'RUNNING' ? 'intelligence' : 'outline'} size="sm">
                {task.status}
              </Badge>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
