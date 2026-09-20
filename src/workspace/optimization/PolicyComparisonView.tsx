import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const PolicyComparisonView: React.FC = () => {
  const comparisonStats = {
    activePolicy: 'Multi-Objective QDIOP v1.4 (Augmented Chebyshev)',
    baselinePolicy: 'Greedy First-Fit Heuristic',
    sampleSize: 100,
    winRate: 94.0,
    meanUtilityGain: '+22.4%',
    latencyReductionMs: '-420.0ms',
    costSavingsUsd: '+$0.014 / doc',
    regretReduction: '-88.5%',
  };

  const regretPoints = [
    { step: 'M1', instantRegret: 0.042, cumRegret: 0.042 },
    { step: 'M2', instantRegret: 0.018, cumRegret: 0.060 },
    { step: 'M3', instantRegret: 0.012, cumRegret: 0.072 },
    { step: 'M4', instantRegret: 0.008, cumRegret: 0.080 },
    { step: 'M5', instantRegret: 0.005, cumRegret: 0.085 },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">⚖️</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Planner Policy Evaluation & Regret Analysis
              </h2>
              <Badge variant="success" size="sm">
                SUBLINEAR REGRET (O(log T))
              </Badge>
            </div>
            <p className="text-xs text-[#94A3B8] mt-1">
              Evaluating active planner version against ex-post oracle decisions and legacy baseline planners.
            </p>
          </div>
          <div className="text-right">
            <div className="text-xs font-mono text-[#94A3B8]">Head-to-Head Win Rate</div>
            <div className="text-2xl font-mono font-extrabold text-emerald-400">
              {comparisonStats.winRate}%
            </div>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center font-mono">
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B]">
          <div className="text-xs text-[#94A3B8]">Mean Utility Gain</div>
          <div className="text-lg font-bold text-emerald-400 mt-1">{comparisonStats.meanUtilityGain}</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B]">
          <div className="text-xs text-[#94A3B8]">Latency Reduction</div>
          <div className="text-lg font-bold text-cyan-400 mt-1">{comparisonStats.latencyReductionMs}</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B]">
          <div className="text-xs text-[#94A3B8]">Cost Efficiency</div>
          <div className="text-lg font-bold text-[#F8FAFC] mt-1">{comparisonStats.costSavingsUsd}</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B]">
          <div className="text-xs text-[#94A3B8]">Planner Regret Drop</div>
          <div className="text-lg font-bold text-emerald-400 mt-1">{comparisonStats.regretReduction}</div>
        </Card>
      </div>

      {/* Regret Progression Table */}
      <Card className="p-5 bg-[#0F172A] border border-[#1E293B] space-y-3">
        <h3 className="text-sm font-bold font-mono text-[#F8FAFC]">
          Instantaneous & Cumulative Regret Trajectory ($R_t = U(\pi^*) - U(\pi_t)$)
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="border-b border-[#1E293B] text-[#64748B]">
                <th className="pb-2">Mission Horizon</th>
                <th className="pb-2">Instantaneous Regret ($r_t$)</th>
                <th className="pb-2">Cumulative Regret ($R_T$)</th>
                <th className="pb-2">Sublinear Decay Rate</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E293B]/60">
              {regretPoints.map((r) => (
                <tr key={r.step}>
                  <td className="py-2.5 text-[#F8FAFC]">{r.step}</td>
                  <td className="py-2.5 text-cyan-400">{r.instantRegret.toFixed(4)}</td>
                  <td className="py-2.5 text-amber-400">{r.cumRegret.toFixed(4)}</td>
                  <td className="py-2.5 text-emerald-400">Converging to 0</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
