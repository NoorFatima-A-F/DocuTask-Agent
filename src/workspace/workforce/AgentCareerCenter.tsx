import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { workforceApiClient } from '../../services/workforceApiClient';
import { CareerPromotionPath } from '../../types/workforce';
import { CheckCircle, ArrowUpRight } from 'lucide-react';

export const AgentCareerCenter: React.FC = () => {
  const [paths, setPaths] = useState<CareerPromotionPath[]>([]);

  useEffect(() => {
    workforceApiClient.getCareerPaths().then(setPaths);
  }, []);

  const handlePromote = async (id: string) => {
    const res = await workforceApiClient.executePromotion(id);
    setPaths(paths.map(p => p.id === id ? res : p));
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-900/60 p-5 rounded-2xl border border-slate-800">
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <span className="p-2 bg-emerald-500/20 text-emerald-400 rounded-xl">🎓</span>
          Agent Career Center & Skill Progression
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Autonomous Role Advancement, Skill Certification, and Career Track Progression
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {paths.map((p) => (
          <Card key={p.id} className="p-5 bg-slate-900/50 border-slate-800">
            <div className="flex justify-between items-start mb-3">
              <div>
                <div className="text-base font-bold text-white">{p.employee_id}</div>
                <div className="text-xs text-indigo-400 mt-0.5 flex items-center gap-1.5">
                  <span>{p.current_role}</span>
                  <span>→</span>
                  <span className="text-emerald-400 font-bold">{p.target_role}</span>
                </div>
              </div>
              <Badge variant={p.status === 'PROMOTED' ? 'default' : 'outline'}>{p.status}</Badge>
            </div>

            <div className="my-4 p-3 bg-slate-950/60 rounded-xl border border-slate-800/80">
              <div className="flex justify-between text-xs text-slate-400 mb-1">
                <span>Eligibility Score</span>
                <strong className="text-emerald-400">{Math.round(p.eligibility_score * 100)}%</strong>
              </div>
              <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div className="bg-emerald-500 h-full" style={{ width: `${p.eligibility_score * 100}%` }}></div>
              </div>
            </div>

            <div className="space-y-1.5 mb-4">
              <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Milestone Verification</div>
              {p.completed_milestones.map((m, idx) => (
                <div key={idx} className="text-xs text-slate-300 flex items-center gap-2">
                  <CheckCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  <span>{m}</span>
                </div>
              ))}
            </div>

            <div className="pt-2 flex justify-end">
              <Button
                size="sm"
                variant={p.status === 'PROMOTED' ? 'outline' : 'primary'}
                disabled={p.status === 'PROMOTED'}
                onClick={() => handlePromote(p.id)}
              >
                <span className="flex items-center gap-1">
                  <ArrowUpRight className="w-4 h-4" /> {p.status === 'PROMOTED' ? 'Promoted' : 'Authorize Promotion'}
                </span>
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
