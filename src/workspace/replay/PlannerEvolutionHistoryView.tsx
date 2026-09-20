import React, { useState, useEffect } from 'react';
import type { DecisionRecord } from '../../types/esmrReplay';
import { EsmrReplayApiClient } from '../../services/esmrReplayApiClient';

interface PlannerEvolutionHistoryViewProps {
  missionId: string;
}

export const PlannerEvolutionHistoryView: React.FC<PlannerEvolutionHistoryViewProps> = ({ missionId }) => {
  const [decisions, setDecisions] = useState<DecisionRecord[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    EsmrReplayApiClient.getDecisions(missionId)
      .then(setDecisions)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [missionId]);

  if (loading) {
    return (
      <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl text-slate-400 animate-pulse">
        Loading Planner Generation History...
      </div>
    );
  }

  return (
    <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 shadow-2xl space-y-6 text-slate-100">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <span>🧬</span> Autonomous Planner Evolution & Mutation History
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Tracking multi-generational evolutionary planner mutations and strategy syntheses across execution cycles.
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {decisions.map((d) => (
          <div key={d.decision_id} className="bg-slate-900/80 border border-slate-800 p-5 rounded-xl space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="px-2.5 py-1 text-xs font-mono font-bold bg-indigo-950 border border-indigo-500/40 text-indigo-300 rounded">
                  Generation {d.planner_generation}
                </span>
                <span className="text-sm font-bold text-white">{d.selected_strategy}</span>
              </div>
              <span className="text-xs font-mono text-emerald-400">
                Utility: {d.utility_breakdown.total_utility.toFixed(4)}
              </span>
            </div>

            <p className="text-xs text-slate-300">{d.why}</p>

            {/* Alternatives comparison */}
            {d.alternatives_evaluated.length > 0 && (
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-2">
                <span className="text-[11px] font-bold text-slate-400 uppercase font-mono">
                  Candidate Strategies Competed in Generation {d.planner_generation}
                </span>
                <div className="space-y-1.5 text-xs">
                  {d.alternatives_evaluated.map((alt) => (
                    <div key={alt.strategy_name} className="flex items-center justify-between text-slate-300 border-b border-slate-850 pb-1">
                      <span className="font-semibold text-slate-200">{alt.strategy_name}</span>
                      <span className="font-mono text-slate-400">Score: {alt.utility_score.toFixed(3)}</span>
                      <span className="text-rose-400 text-[11px]">{alt.rejection_reason}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
