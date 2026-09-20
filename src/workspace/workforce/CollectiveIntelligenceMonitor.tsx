import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { workforceApiClient } from '../../services/workforceApiClient';
import { CollectiveMemoryRecord, ConflictResolutionRecord } from '../../types/workforce';
import { Database, Scale } from 'lucide-react';

export const CollectiveIntelligenceMonitor: React.FC = () => {
  const [memories, setMemories] = useState<CollectiveMemoryRecord[]>([]);
  const [conflicts, setConflicts] = useState<ConflictResolutionRecord[]>([]);

  useEffect(() => {
    workforceApiClient.getCollectiveMemories().then(setMemories);
    workforceApiClient.getConflicts().then(setConflicts);
  }, []);

  return (
    <div className="space-y-6">
      <div className="bg-slate-900/60 p-5 rounded-2xl border border-slate-800">
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <span className="p-2 bg-sky-500/20 text-sky-400 rounded-xl">🧠</span>
          Collective Intelligence & Conflict Resolution
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Shared Organizational Knowledge, Cross-Department Protocols, and Automated Dispute Arbitration
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
            <Database className="w-4 h-4 text-indigo-400" /> Collective Memory Records
          </h3>
          <div className="space-y-3">
            {memories.map((m) => (
              <div key={m.id} className="p-4 bg-slate-950/60 rounded-xl border border-slate-800">
                <div className="flex justify-between items-start mb-1">
                  <div className="text-sm font-bold text-white">{m.title}</div>
                  <Badge variant="outline">{m.scope}</Badge>
                </div>
                <p className="text-xs text-slate-300 mb-2">{m.content}</p>
                <div className="text-[10px] text-slate-500">Author: {m.author_employee_id} • Trust Weight: {m.trust_weight}</div>
              </div>
            ))}
          </div>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
            <Scale className="w-4 h-4 text-amber-400" /> Conflict Resolution Ledger
          </h3>
          <div className="space-y-3">
            {conflicts.map((c) => (
              <div key={c.id} className="p-4 bg-slate-950/60 rounded-xl border border-slate-800">
                <div className="flex justify-between items-start mb-1">
                  <div className="text-sm font-bold text-white">{c.dispute_subject}</div>
                  <Badge variant="default">{c.status}</Badge>
                </div>
                <div className="text-xs text-slate-400 my-1">
                  Parties: <strong className="text-indigo-300">{c.party_a_id}</strong> vs <strong className="text-indigo-300">{c.party_b_id}</strong> (Mediator: {c.mediator_employee_id})
                </div>
                <p className="text-xs text-emerald-400 mb-2 font-medium">{c.resolution_summary}</p>
                <div className="text-[10px] text-slate-500">
                  Agreements: {c.binding_agreements.join(', ')}
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};
