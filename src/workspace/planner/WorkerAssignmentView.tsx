import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Users } from 'lucide-react';

export const WorkerAssignmentView: React.FC = () => {
  const assignments = [
    {
      taskId: 'node_ocr_chunk_1',
      taskName: 'OCR Page 1-2 (Raster)',
      workerId: 'worker-ocr-01',
      role: 'OCR_SPECIALIST',
      matchScore: '99.2%',
      reason: 'Highest throughput on rasterized multi-column invoice scans',
      latency: '180ms',
      cost: '$0.0006',
      status: 'COMPLETED',
    },
    {
      taskId: 'node_ocr_chunk_2',
      taskName: 'OCR Page 3-4 (Tables)',
      workerId: 'worker-ocr-02',
      role: 'TABLE_EXTRACTION_SPECIALIST',
      matchScore: '98.5%',
      reason: 'Optimized bounding box table detector with high OCR accuracy',
      latency: '210ms',
      cost: '$0.0006',
      status: 'COMPLETED',
    },
    {
      taskId: 'node_merge_ocr',
      taskName: 'Merge OCR Texts',
      workerId: 'worker-extract-01',
      role: 'TRANSFORM_ENGINE',
      matchScore: '99.5%',
      reason: 'Low memory footprint JSON and markdown schema normalizer',
      latency: '60ms',
      cost: '$0.0002',
      status: 'RUNNING',
    },
    {
      taskId: 'node_validate_invariants',
      taskName: 'Scientific Validation Check',
      workerId: 'worker-validate-01',
      role: 'INVARIANT_VALIDATOR',
      matchScore: '99.9%',
      reason: 'Formal verification of arithmetic and schema constraints',
      latency: '90ms',
      cost: '$0.0003',
      status: 'ASSIGNED',
    },
    {
      taskId: 'node_join_finalize',
      taskName: 'Join & Truth Ledger Commit',
      workerId: 'worker-trust-01',
      role: 'LEDGER_AUTHENTICATOR',
      matchScore: '100.0%',
      reason: 'Authorized hardware-backed Merkle signature signer',
      latency: '40ms',
      cost: '$0.0002',
      status: 'ASSIGNED',
    },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-purple-500/20 to-pink-500/20 border border-purple-500/30 rounded-xl text-purple-400">
              <Users className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Worker Assignment & Capability Matching Justification
                <Badge variant="success" size="sm">Evidence-Backed</Badge>
              </h1>
              <p className="text-xs text-[#94A3B8] font-mono">
                Inspect deterministic worker capability scoring, resource quotas, and selection proofs
              </p>
            </div>
          </div>
        </div>

        <Badge variant="intelligence" size="md">Average Match: 99.4%</Badge>
      </div>

      {/* Assignment Cards */}
      <div className="space-y-3 font-mono">
        {assignments.map(a => (
          <Card key={a.taskId} className="p-4 rounded-xl border border-[#1E293B] bg-[#0F172A] space-y-3 hover:border-purple-500/40 transition-all">
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-[#1E293B] pb-2">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-white">{a.taskName}</span>
                <Badge variant="outline" size="sm">{a.taskId}</Badge>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="info" size="sm">Match: {a.matchScore}</Badge>
                <Badge variant={a.status === 'COMPLETED' ? 'success' : a.status === 'RUNNING' ? 'intelligence' : 'default'} size="sm">
                  {a.status}
                </Badge>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
              <div className="p-2.5 bg-[#131D35] rounded-lg border border-[#1E293B]">
                <span className="text-[10px] text-[#64748B] block">ASSIGNED WORKER</span>
                <span className="text-cyan-400 font-bold">{a.workerId}</span>
                <span className="text-[10px] text-[#94A3B8] block">{a.role}</span>
              </div>
              <div className="p-2.5 bg-[#131D35] rounded-lg border border-[#1E293B] md:col-span-2">
                <span className="text-[10px] text-[#64748B] block">SELECTION JUSTIFICATION</span>
                <span className="text-[#F8FAFC] text-[11px]">{a.reason}</span>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
