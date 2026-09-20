import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const RetryOptimizerView: React.FC = () => {
  const retryEvaluation = {
    decision: 'RETRY',
    expectedImprovement: '+0.850 Utility',
    probabilityOfRecovery: '72.3%',
    retryCostUsd: '$0.005',
    expectedDelayMs: '800.0ms',
    marginalBenefit: '+0.548',
    currentRetryCount: 1,
    maxAllowedRetries: 3,
  };

  const retryDecayTrajectory = [
    { retry: 0, pRecovery: 0.85, marginalBenefit: +0.68, decision: 'RETRY' },
    { retry: 1, pRecovery: 0.55, marginalBenefit: +0.38, decision: 'RETRY' },
    { retry: 2, pRecovery: 0.36, marginalBenefit: +0.12, decision: 'FALLBACK' },
    { retry: 3, pRecovery: 0.23, marginalBenefit: -0.04, decision: 'ESCALATE' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">🔄</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Quantitative Retry Optimization Engine
              </h2>
              <Badge variant="success" size="sm">
                MARGINAL BENEFIT &gt; 0
              </Badge>
            </div>
            <p className="text-xs text-[#94A3B8] mt-1">
              Decides whether to Retry, Fallback, or Escalate based on Expected Improvement, Recovery Probability, and Delay Cost.
            </p>
          </div>
          <div className="text-right">
            <div className="text-xs font-mono text-[#94A3B8]">Active Decision (Retry #{retryEvaluation.currentRetryCount + 1})</div>
            <div className="text-xl font-mono font-extrabold text-emerald-400">
              {retryEvaluation.decision} (Marginal Benefit = {retryEvaluation.marginalBenefit})
            </div>
          </div>
        </div>

        <div className="mt-4 pt-3 border-t border-[#1E293B] grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-mono text-center">
          <div className="bg-[#131D35]/50 p-2 rounded-lg">
            <span className="text-[#64748B] block text-[10px]">Expected Impr.</span>
            <span className="text-cyan-400 font-bold">{retryEvaluation.expectedImprovement}</span>
          </div>
          <div className="bg-[#131D35]/50 p-2 rounded-lg">
            <span className="text-[#64748B] block text-[10px]">Recovery Prob.</span>
            <span className="text-emerald-400 font-bold">{retryEvaluation.probabilityOfRecovery}</span>
          </div>
          <div className="bg-[#131D35]/50 p-2 rounded-lg">
            <span className="text-[#64748B] block text-[10px]">Incremental Cost</span>
            <span className="text-[#F8FAFC] font-bold">{retryEvaluation.retryCostUsd}</span>
          </div>
          <div className="bg-[#131D35]/50 p-2 rounded-lg">
            <span className="text-[#64748B] block text-[10px]">Backoff Delay</span>
            <span className="text-amber-400 font-bold">{retryEvaluation.expectedDelayMs}</span>
          </div>
        </div>
      </div>

      {/* Trajectory Table */}
      <Card className="p-5 bg-[#0F172A] border border-[#1E293B] space-y-4">
        <h3 className="text-sm font-bold font-mono text-[#F8FAFC]">
          Marginal Benefit Decay Schedule across Retry Horizon
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="border-b border-[#1E293B] text-[#64748B]">
                <th className="pb-2">Attempt</th>
                <th className="pb-2">P(Recovery)</th>
                <th className="pb-2">Marginal Benefit ($MB$)</th>
                <th className="pb-2">Quantitative Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E293B]/60">
              {retryDecayTrajectory.map((t) => (
                <tr key={t.retry}>
                  <td className="py-2.5 text-[#F8FAFC]">Retry #{t.retry + 1}</td>
                  <td className="py-2.5 text-cyan-400">{(t.pRecovery * 100).toFixed(1)}%</td>
                  <td className={`py-2.5 font-bold ${t.marginalBenefit > 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                    {t.marginalBenefit > 0 ? `+${t.marginalBenefit.toFixed(2)}` : t.marginalBenefit.toFixed(2)}
                  </td>
                  <td className="py-2.5">
                    <Badge
                      variant={t.decision === 'RETRY' ? 'success' : t.decision === 'FALLBACK' ? 'intelligence' : 'warning'}
                      size="sm"
                    >
                      {t.decision}
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
