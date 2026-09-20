import React, { useState, useEffect } from 'react';
import {
  Target,
  RefreshCw,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { BusinessApiClient } from '../../services/businessApiClient';
import { BusinessGoal } from '../../types/businessPlatform';

export const GoalManagerStudio: React.FC = () => {
  const [goals, setGoals] = useState<BusinessGoal[]>([]);
  const [loading, setLoading] = useState(true);

  const loadGoals = async () => {
    try {
      setLoading(true);
      const res = await BusinessApiClient.listGoals();
      setGoals(res);
    } catch (err) {
      console.error('Failed to load goals:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadGoals();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <Target className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Business Goal & OKR Manager</h1>
            <p className="text-sm text-slate-400">
              HTN goal decomposition, milestone tracking, and autonomous KPI alignment
            </p>
          </div>
        </div>

        <Button variant="outline" onClick={loadGoals} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      {/* Goals Grid */}
      <div className="space-y-5">
        {goals.map((g) => (
          <Card key={g.goal_id} className="p-6 bg-slate-900/40 border-slate-800 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
              <div>
                <div className="flex items-center gap-2">
                  <h2 className="text-base font-bold text-white">{g.title}</h2>
                  <Badge variant="intelligence">{g.category}</Badge>
                </div>
                <span className="text-xs text-slate-400 font-mono">
                  Department: {g.target_department} | Aligned: {g.aligned_process_ids.join(', ')}
                </span>
              </div>

              <div className="flex items-center gap-3">
                <span className="text-sm font-bold text-emerald-400 font-mono">{g.progress_pct.toFixed(1)}%</span>
                <Badge variant={g.status === 'ACHIEVED' ? 'success' : 'default'}>{g.status}</Badge>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
              <div
                className="bg-emerald-500 h-full rounded-full transition-all"
                style={{ width: `${g.progress_pct}%` }}
              />
            </div>

            {/* Key Results */}
            <div className="space-y-2 pt-2">
              <span className="text-xs font-semibold text-slate-400 block">Quantitative Key Results (KRs)</span>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
                {g.key_results.map((kr) => (
                  <div
                    key={kr.kr_id}
                    className="p-3 bg-slate-800/40 rounded-xl border border-slate-700/60 flex items-center justify-between"
                  >
                    <div>
                      <span className="font-sans text-slate-200 block text-xs font-medium">{kr.description}</span>
                      <span className="text-slate-400 text-[11px]">
                        Target: {kr.target_value} {kr.unit} | Current: {kr.current_value} {kr.unit}
                      </span>
                    </div>
                    <Badge variant={kr.achieved ? 'success' : 'outline'}>
                      {kr.achieved ? 'Achieved' : 'In Progress'}
                    </Badge>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
