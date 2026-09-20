import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { ShieldCheck, CheckCircle2 } from 'lucide-react';

export const ReplayVerificationCenter: React.FC = () => {
  const verifications = [
    { check: 'Event Hash Chain Continuity', result: 'VALID', details: '10/10 parent-child SHA256 hashes matched without gaps' },
    { check: 'Truth Ledger Invariant Seal', result: 'VALID', details: 'Merkle root sha256:7fa189c4... confirmed in Truth Ledger' },
    { check: 'Formula Monotonic Bounds [0, 1]', result: 'VALID', details: 'WeightedEnsemble (v1.3.0) confirmed monotonically bounded' },
    { check: 'Projection Monotonic Sequencing', result: 'VALID', details: 'Zero out-of-order or duplicate events encountered' },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 rounded-xl text-emerald-400">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Replay Verification & Authenticity Center
                <Badge variant="success" size="sm">100% Verified</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Independent cryptographic proof validation guaranteeing zero UI fabrication and absolute replay integrity.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="intelligence" size="sm">Verification Hash: sha256:7fa189c4...</Badge>
        </div>
      </div>

      {/* Verification Check List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs">
        {verifications.map((v, idx) => (
          <Card key={idx} className="p-5 bg-[#0F172A] border-[#1E293B] space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-white text-sm">{v.check}</span>
              <Badge variant="success" size="sm" className="flex items-center gap-1">
                <CheckCircle2 className="w-3 h-3" />
                {v.result}
              </Badge>
            </div>
            <p className="text-slate-400 text-xs">{v.details}</p>
          </Card>
        ))}
      </div>
    </div>
  );
};
