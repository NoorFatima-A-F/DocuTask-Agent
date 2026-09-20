import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { workforceApiClient } from '../../services/workforceApiClient';
import { HiringRequisition } from '../../types/workforce';
import { UserPlus } from 'lucide-react';

export const HiringPromotionStudio: React.FC = () => {
  const [reqs, setReqs] = useState<HiringRequisition[]>([]);

  useEffect(() => {
    workforceApiClient.getRequisitions().then(setReqs);
  }, []);

  return (
    <div className="space-y-6">
      <div className="bg-slate-900/60 p-5 rounded-2xl border border-slate-800">
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <span className="p-2 bg-teal-500/20 text-teal-400 rounded-xl">🎯</span>
          Autonomous Hiring & Requisition Studio
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Demand-Triggered Agent Requisitions, Profile Generation & Fleet Expansion
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {reqs.map((r) => (
          <Card key={r.id} className="p-5 bg-slate-900/50 border-slate-800">
            <div className="flex justify-between items-start mb-3">
              <div>
                <div className="text-base font-bold text-white">{r.target_role} Requisition</div>
                <div className="text-xs text-slate-400">{r.department} • Reason: {r.reason}</div>
              </div>
              <Badge variant="default">{r.status}</Badge>
            </div>

            <div className="space-y-2 my-4">
              <div className="text-[11px] font-semibold text-slate-400 uppercase">Top Automated Candidates</div>
              {r.candidate_profiles.map((c, idx) => (
                <div key={idx} className="p-3 bg-slate-950/60 rounded-xl border border-slate-800 flex justify-between items-center text-xs">
                  <div>
                    <strong className="text-white">{c.name}</strong>
                    <div className="text-[10px] text-slate-400">Match Score: {Math.round(c.score * 100)}%</div>
                  </div>
                  <Button size="sm" variant="outline">
                    <span className="flex items-center gap-1">
                      <UserPlus className="w-3.5 h-3.5" /> Auto-Hire
                    </span>
                  </Button>
                </div>
              ))}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
