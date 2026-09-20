import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { GitBranch, ShieldCheck, CheckCircle2, ArrowRight } from 'lucide-react';

interface LineageNode {
  hash: string;
  parentHash: string | null;
  timestamp: string;
  operation: string;
  formulaVersion: string;
  resultingScore: number;
  evidenceCount: number;
  verified: boolean;
}

const lineageHistory: LineageNode[] = [
  {
    hash: 'c8a1f492...e109',
    parentHash: 'b712c980...f881',
    timestamp: '2026-09-11T22:45:21Z',
    operation: 'FINAL_POSTERIOR_EVALUATION',
    formulaVersion: 'WeightedEnsemble (v1.3.0)',
    resultingScore: 98.42,
    evidenceCount: 14,
    verified: true,
  },
  {
    hash: 'b712c980...f881',
    parentHash: 'a90184aa...c234',
    timestamp: '2026-09-11T22:45:15Z',
    operation: 'INVARIANT_CHECK_UPDATE',
    formulaVersion: 'WeightedEnsemble (v1.3.0)',
    resultingScore: 97.50,
    evidenceCount: 11,
    verified: true,
  },
  {
    hash: 'a90184aa...c234',
    parentHash: 'f0023da9...8812',
    timestamp: '2026-09-11T22:45:08Z',
    operation: 'SCHEMA_EXTRACTION_UPDATE',
    formulaVersion: 'WeightedEnsemble (v1.3.0)',
    resultingScore: 94.20,
    evidenceCount: 8,
    verified: true,
  },
  {
    hash: 'f0023da9...8812',
    parentHash: null,
    timestamp: '2026-09-11T22:45:00Z',
    operation: 'PRIOR_INITIALIZATION',
    formulaVersion: 'WeightedEnsemble (v1.3.0)',
    resultingScore: 85.00,
    evidenceCount: 2,
    verified: true,
  },
];

export const ConfidenceLineageExplorer: React.FC = () => {
  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-amber-500/20 to-orange-500/20 border border-amber-500/30 rounded-xl text-amber-400">
              <GitBranch className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Confidence Lineage & Provenance Chain
                <Badge variant="success" size="sm">Merkle Root Verified</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Cryptographically linked hash chains proving the exact computational history of every confidence metric.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="outline" size="sm">Chain Length: 4 Blocks</Badge>
        </div>
      </div>

      {/* Lineage Tree */}
      <div className="space-y-4">
        {lineageHistory.map((node, idx) => (
          <Card key={node.hash} className="p-5 bg-[#0F172A] border-[#1E293B] hover:border-amber-500/40 transition-all font-mono">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="space-y-1.5">
                <div className="flex items-center gap-3">
                  <span className="text-amber-400 font-bold text-sm">#{lineageHistory.length - idx}</span>
                  <span className="text-white font-bold text-sm">{node.operation}</span>
                  <Badge variant="intelligence" size="sm">{node.formulaVersion}</Badge>
                </div>
                <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400">
                  <span>Current Hash: <span className="text-slate-200 bg-slate-900 px-1.5 py-0.5 rounded border border-slate-700">{node.hash}</span></span>
                  {node.parentHash && (
                    <span className="flex items-center gap-1">
                      <ArrowRight className="w-3 h-3 text-slate-500" />
                      Parent: <span className="text-slate-400 bg-slate-900 px-1.5 py-0.5 rounded border border-slate-800">{node.parentHash}</span>
                    </span>
                  )}
                </div>
              </div>

              <div className="flex items-center gap-6">
                <div className="text-right">
                  <div className="text-lg font-bold text-white">{node.resultingScore.toFixed(2)}%</div>
                  <div className="text-[11px] text-slate-400">{node.evidenceCount} Evidences</div>
                </div>
                {node.verified ? (
                  <Badge variant="success" size="sm" className="flex items-center gap-1">
                    <CheckCircle2 className="w-3 h-3" />
                    Verified
                  </Badge>
                ) : (
                  <Badge variant="warning" size="sm">Unverified</Badge>
                )}
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Cryptographic Proof Verification Card */}
      <Card className="p-4 bg-gradient-to-r from-amber-950/20 to-slate-900/60 border border-amber-500/30 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <ShieldCheck className="w-5 h-5 text-amber-400 shrink-0" />
          <div className="text-xs text-slate-300">
            <span className="font-bold text-white">Truth Ledger Seal: </span>
            Root Hash <code className="text-amber-300 bg-black/40 px-1 py-0.5 rounded">sha256:c8a1f492e109...</code> confirmed immutable in event store.
          </div>
        </div>
      </Card>
    </div>
  );
};
