import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { workforceApiClient } from '../../services/workforceApiClient';
import { ExecutiveCouncilProposition } from '../../types/workforce';
import { Check, X } from 'lucide-react';

export const ExecutiveCouncil: React.FC = () => {
  const [props, setProps] = useState<ExecutiveCouncilProposition[]>([]);

  useEffect(() => {
    workforceApiClient.getCouncilPropositions().then(setProps);
  }, []);

  const handleVote = async (id: string, role: string, vote: string) => {
    const updated = await workforceApiClient.voteCouncilProposition(id, role, vote);
    setProps(props.map(p => p.id === id ? updated : p));
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-900/60 p-5 rounded-2xl border border-slate-800">
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <span className="p-2 bg-indigo-500/20 text-indigo-400 rounded-xl">🏛️</span>
          Executive AI Council Chamber
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Highest C-Suite Autonomous Decision Quorum & Constitutional Policies
        </p>
      </div>

      <div className="space-y-6">
        {props.map((p) => (
          <Card key={p.id} className="p-6 bg-slate-900/50 border-slate-800">
            <div className="flex justify-between items-start mb-3">
              <div>
                <div className="text-lg font-bold text-white">{p.title}</div>
                <div className="text-xs text-indigo-400 font-medium mt-0.5">Category: {p.category}</div>
              </div>
              <Badge variant={p.enacted ? "default" : "outline"}>
                {p.enacted ? "CONSTITUTIONALLY ENACTED" : "AWAITING QUORUM"}
              </Badge>
            </div>

            <p className="text-sm text-slate-300 my-4 bg-slate-950/60 p-4 rounded-xl border border-slate-800/80">
              {p.summary}
            </p>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 my-4">
              {['CEO', 'VP_ENG', 'SECURITY_DIR', 'FINANCE_DIR'].map((role) => {
                const currentVote = p.council_votes[role];
                return (
                  <div key={role} className="p-3 bg-slate-950 rounded-xl border border-slate-800 text-xs">
                    <div className="font-semibold text-slate-400 mb-1">{role}</div>
                    <div className="flex justify-between items-center">
                      <span className="text-emerald-400 font-bold">{currentVote || 'PENDING'}</span>
                      <div className="flex gap-1">
                        <button
                          onClick={() => handleVote(p.id, role, 'APPROVE')}
                          className="p-1 hover:bg-emerald-500/20 text-emerald-400 rounded"
                          title="Approve"
                        >
                          <Check className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => handleVote(p.id, role, 'REJECT')}
                          className="p-1 hover:bg-rose-500/20 text-rose-400 rounded"
                          title="Reject"
                        >
                          <X className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
