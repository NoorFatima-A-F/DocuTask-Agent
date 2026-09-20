import React, { useState, useEffect } from 'react';
import {
  GitCommit,
  Clock,
  RefreshCw,
  ArrowRight,
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
import { EvolutionCycleResultPayload } from '../../types/evolutionPlatform';

export const RecursiveEvolutionTimeline: React.FC = () => {
  const [cycles, setCycles] = useState<EvolutionCycleResultPayload[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadTimeline();
  }, []);

  const loadTimeline = async () => {
    setLoading(true);
    try {
      const data = await EvolutionPlatformApiClient.listCycleHistory();
      setCycles(data);
    } catch (err) {
      console.error('Failed to load cycle history:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-indigo-500/10 border border-indigo-500/20 rounded-xl">
            <GitCommit className="w-6 h-6 text-indigo-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-slate-100">Recursive Evolution Timeline & Genealogy</h1>
              <Badge variant="intelligence" size="sm">Immutable Lineage</Badge>
            </div>
            <p className="text-sm text-slate-400 mt-0.5">
              Chronological log of closed-loop self-evolution cycles, empirical fitness gains, and promoted architecture generations.
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            onClick={loadTimeline}
            disabled={loading}
          >
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
        </div>
      </div>

      {/* Timeline List */}
      <div className="relative border-l-2 border-indigo-500/30 ml-4 pl-6 space-y-8 py-2">
        {cycles.map((c) => (
          <div key={c.cycle_id} className="relative group">
            {/* Timeline Dot */}
            <div className="absolute -left-[31px] top-1.5 w-4 h-4 rounded-full bg-slate-950 border-2 border-indigo-500 group-hover:bg-indigo-500 transition-colors" />

            <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3 hover:border-slate-700 transition-all">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-2">
                <div className="flex items-center gap-3">
                  <span className="font-mono text-sm font-bold text-indigo-400">{c.cycle_id}</span>
                  <span className="text-sm font-semibold text-slate-200">Target: {c.target_subsystem}</span>
                  <Badge variant={c.deployment_state === 'PROMOTED' ? 'success' : 'outline'} size="sm">
                    {c.stage}
                  </Badge>
                </div>
                <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
                  <Clock className="w-3.5 h-3.5" />
                  <span>{new Date(c.completed_at).toLocaleString()}</span>
                </div>
              </div>

              {/* Evolution Flow Diagram */}
              <div className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg flex flex-wrap items-center gap-2 text-xs font-mono text-slate-400">
                <span className="text-slate-300 font-semibold">Profile</span>
                <ArrowRight className="w-3.5 h-3.5 text-slate-600" />
                <span className="text-slate-300 font-semibold">{c.diagnosis_count} Diagnoses</span>
                <ArrowRight className="w-3.5 h-3.5 text-slate-600" />
                <span className="text-slate-300 font-semibold">{c.capability_gaps_found} Gaps</span>
                <ArrowRight className="w-3.5 h-3.5 text-slate-600" />
                <span className="text-amber-400 font-semibold">Pareto ({c.candidate_id})</span>
                <ArrowRight className="w-3.5 h-3.5 text-slate-600" />
                <span className="text-purple-400 font-semibold">Mutation ({c.mutation_id})</span>
                <ArrowRight className="w-3.5 h-3.5 text-slate-600" />
                <span className="text-cyan-400 font-semibold">Shadow Replay</span>
                <ArrowRight className="w-3.5 h-3.5 text-slate-600" />
                <span className="text-emerald-400 font-semibold">Gain +{c.benchmark_improvement_pct}%</span>
              </div>

              {/* Health Score Transition */}
              <div className="flex items-center justify-between text-xs font-mono pt-1">
                <div className="text-slate-400">
                  Health Delta: <span className="text-slate-300">{(c.health_score_before * 100).toFixed(1)}%</span> → <span className="text-emerald-400 font-bold">{(c.health_score_after * 100).toFixed(1)}%</span>
                </div>
                <div className="text-slate-400">
                  Governance: <span className="text-emerald-400 font-semibold">{c.governance_approved ? 'APPROVED' : 'PENDING'}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
