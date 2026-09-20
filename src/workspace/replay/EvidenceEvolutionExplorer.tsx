import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Database, CheckCircle2, Hash, Layers } from 'lucide-react';

interface EvidenceItem {
  id: string;
  cursor: number;
  type: string;
  sourceEvent: string;
  confidenceContribution: string;
  truthSeal: string;
  status: string;
}

const evidenceTimeline: EvidenceItem[] = [
  { id: 'EVID-001', cursor: 4, type: 'OCR_QUALITY_SCORE', sourceEvent: 'worker.completed', confidenceContribution: '+0.18', truthSeal: 'sha256:7f9a12c8...', status: 'VERIFIED' },
  { id: 'EVID-002', cursor: 5, type: 'SCHEMA_FIELD_MATCH', sourceEvent: 'worker.completed', confidenceContribution: '+0.22', truthSeal: 'sha256:4b219cf1...', status: 'VERIFIED' },
  { id: 'EVID-003', cursor: 7, type: 'SMT_INVARIANT_PROOF', sourceEvent: 'truth.invariant.checked', confidenceContribution: '+0.25', truthSeal: 'sha256:88e09f21...', status: 'SEALED' },
];

export const EvidenceEvolutionExplorer: React.FC = () => {
  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 rounded-xl text-emerald-400">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Evidence Evolution Explorer
                <Badge variant="success" size="sm">Immutable Ledger</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Timeline of evidence accumulation, verification, invalidation, and Truth Ledger linkage.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="intelligence" size="sm">3 Evidence Items Sealed</Badge>
        </div>
      </div>

      {/* Evidence Table */}
      <Card className="bg-[#0F172A] border-[#1E293B] overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-[#1E293B]/60 text-slate-400 border-b border-[#1E293B]">
              <tr>
                <th className="p-3">Evidence ID / Frame</th>
                <th className="p-3">Evidence Type</th>
                <th className="p-3">Source Event</th>
                <th className="p-3">Confidence Marginal Impact</th>
                <th className="p-3">Cryptographic Truth Seal</th>
                <th className="p-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E293B]/40">
              {evidenceTimeline.map((item) => (
                <tr key={item.id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="p-3">
                    <div className="font-semibold text-emerald-400 flex items-center gap-1">
                      <Hash className="w-3.5 h-3.5" />
                      {item.id}
                    </div>
                    <div className="text-[10px] text-slate-500">At Frame #{item.cursor}</div>
                  </td>
                  <td className="p-3 text-slate-200 font-bold">{item.type}</td>
                  <td className="p-3">
                    <div className="text-slate-300 flex items-center gap-1">
                      <Layers className="w-3 h-3 text-cyan-400" />
                      {item.sourceEvent}
                    </div>
                  </td>
                  <td className="p-3 text-emerald-400 font-bold">{item.confidenceContribution}</td>
                  <td className="p-3 text-[10px] text-slate-400">
                    <span className="bg-slate-900/80 px-1.5 py-0.5 rounded border border-slate-700">
                      {item.truthSeal}
                    </span>
                  </td>
                  <td className="p-3">
                    <Badge variant="success" size="sm" className="flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" />
                      {item.status}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
