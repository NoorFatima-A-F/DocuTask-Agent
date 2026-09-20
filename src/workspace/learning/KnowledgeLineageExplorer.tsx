import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { ShieldCheck, ArrowDown, Lock } from 'lucide-react';

export const KnowledgeLineageExplorer: React.FC = () => {
  const lineageChain = [
    {
      id: 'lin-001',
      recordId: 'kn-ocr-shard',
      version: '1.0.0',
      parentHash: 'GENESIS_ROOT',
      lineageHash: 'sha256:7f9a2b1c4e0d98',
      sourceMission: 'mission-001',
      mutationNote: 'Initial knowledge extraction from high-throughput PDF batch execution.',
      timestamp: '2026-09-12 00:05 UTC',
    },
    {
      id: 'lin-002',
      recordId: 'kn-ocr-shard',
      version: '1.1.0',
      parentHash: 'sha256:7f9a2b1c4e0d98',
      lineageHash: 'sha256:8e1a3b5c7d9f02',
      sourceMission: 'mission-002',
      mutationNote: 'Added adaptive jitter retry parameter to prevent OCR 429 rate limit drops.',
      timestamp: '2026-09-12 00:18 UTC',
    },
    {
      id: 'lin-003',
      recordId: 'kn-ocr-shard',
      version: '1.2.0',
      parentHash: 'sha256:8e1a3b5c7d9f02',
      lineageHash: 'sha256:9c2b4e8a1f3d5e',
      sourceMission: 'mission-003',
      mutationNote: 'Calibrated worker concurrency ceiling from 6 to 8 based on low-drift wavefronts.',
      timestamp: '2026-09-12 00:32 UTC',
    },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 rounded-xl text-emerald-400">
            <Lock className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
              Cryptographic Knowledge Lineage Explorer
              <Badge variant="intelligence" size="sm">Tamper Evident</Badge>
            </h1>
            <p className="text-xs text-[#94A3B8] font-mono">
              Inspect SHA-256 parent-child cryptographic provenance chains proving verifiable knowledge evolution
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">Chain Integrity: 100% Valid</Badge>
        </div>
      </div>

      {/* Lineage Chain Visualizer */}
      <div className="space-y-4 font-mono max-w-4xl mx-auto">
        {lineageChain.map((entry, idx) => (
          <React.Fragment key={entry.id}>
            <Card className="p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-[#1E293B] pb-3 text-xs">
                <div className="flex items-center gap-2">
                  <span className="text-white font-bold">{entry.recordId}</span>
                  <Badge variant="outline" size="sm">v{entry.version}</Badge>
                </div>
                <div className="flex items-center gap-2 text-emerald-400 font-bold">
                  <ShieldCheck className="w-3.5 h-3.5" />
                  Tamper Proof
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                <div className="space-y-1">
                  <span className="text-[10px] text-[#64748B] block">PARENT HASH</span>
                  <span className="text-amber-400 font-bold block">{entry.parentHash}</span>
                </div>
                <div className="space-y-1">
                  <span className="text-[10px] text-[#64748B] block">LINEAGE HASH</span>
                  <span className="text-cyan-400 font-bold block">{entry.lineageHash}</span>
                </div>
              </div>

              <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl text-xs space-y-1">
                <span className="text-[10px] text-[#64748B] block">MUTATION RATIONALE:</span>
                <p className="text-[#94A3B8]">{entry.mutationNote}</p>
                <div className="text-[10px] text-[#64748B] pt-1">
                  Source Mission: <span className="text-indigo-400">{entry.sourceMission}</span> | Recorded: {entry.timestamp}
                </div>
              </div>
            </Card>

            {idx < lineageChain.length - 1 && (
              <div className="flex justify-center my-2">
                <div className="p-1.5 rounded-full bg-[#1E293B] text-cyan-400">
                  <ArrowDown className="w-4 h-4" />
                </div>
              </div>
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};
