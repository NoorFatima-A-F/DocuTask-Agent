/**
 * Strategy Comparison Matrix Component.
 * Visualizes multi-objective candidate strategy evaluation, Pareto frontier, selection justification,
 * and rejection reasons with mathematical precision.
 */

import React, { useState, useEffect } from 'react';
import { StrategyComparisonMatrix, UtilityScore } from '../../types/autonomousPlanning';
import { PlanningApiClient } from '../../services/planningApiClient';

interface StrategyComparisonMatrixProps {
  missionId?: string;
  onSelectStrategy?: (strategyId: string) => void;
}

export const StrategyComparisonMatrixView: React.FC<StrategyComparisonMatrixProps> = ({
  missionId = 'mission_active_001',
  onSelectStrategy,
}) => {
  const [matrix, setMatrix] = useState<StrategyComparisonMatrix | null>(null);
  const [utilityBreakdown, setUtilityBreakdown] = useState<UtilityScore | null>(null);
  const [rejectionReasons, setRejectionReasons] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedRowId, setSelectedRowId] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, [missionId]);

  const loadData = async () => {
    setLoading(true);
    try {
      const plan = await PlanningApiClient.planMission(missionId, 'Extract invoice fields and cross-check totals');
      setMatrix(plan.selection_record.comparison_matrix);
      setUtilityBreakdown(plan.selection_record.utility_breakdown);
      setRejectionReasons(plan.selection_record.rejection_reasons);
      setSelectedRowId(plan.selection_record.selected_strategy_id);
    } catch (err) {
      console.error('Failed to load strategy matrix', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !matrix) {
    return (
      <div className="flex items-center justify-center p-12 text-slate-400">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500 mr-3"></div>
        <span>Evaluating Multi-Objective Strategy Space...</span>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-slate-100 shadow-2xl space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-slate-800 pb-4 gap-4">
        <div>
          <div className="flex items-center space-x-3">
            <span className="px-2.5 py-1 text-xs font-bold uppercase tracking-wider bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 rounded-md">
              Autonomous Planning Kernel v2.0
            </span>
            <span className="text-xs text-slate-400 font-mono">Mission: {matrix.mission_id}</span>
          </div>
          <h2 className="text-xl font-bold text-white mt-1">Multi-Objective Strategy Comparison Matrix</h2>
          <p className="text-sm text-slate-400">
            Mathematical ranking across Pareto frontier with deterministic utility equations and rejection provenance.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <div className="bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700/60 text-right">
            <span className="block text-[10px] uppercase text-slate-400 font-semibold tracking-wider">Winning Strategy</span>
            <span className="text-sm font-bold text-emerald-400">{matrix.selected_strategy_id}</span>
          </div>
          <button
            onClick={loadData}
            className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition"
          >
            Re-evaluate
          </button>
        </div>
      </div>

      {/* Comparison Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-800 text-xs font-semibold text-slate-400 uppercase tracking-wider bg-slate-950/40">
              <th className="py-3 px-4">Rank & Archetype</th>
              <th className="py-3 px-4">Utility Score (U)</th>
              <th className="py-3 px-4">Accuracy</th>
              <th className="py-3 px-4">Critical Path</th>
              <th className="py-3 px-4">Est. Cost</th>
              <th className="py-3 px-4">Risk</th>
              <th className="py-3 px-4">Pareto</th>
              <th className="py-3 px-4">Status & Decision</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-sm font-mono">
            {matrix.entries.map((entry) => {
              const isSelected = entry.strategy_id === matrix.selected_strategy_id;
              const isHighlighted = entry.strategy_id === selectedRowId;

              return (
                <tr
                  key={entry.strategy_id}
                  onClick={() => {
                    setSelectedRowId(entry.strategy_id);
                    onSelectStrategy?.(entry.strategy_id);
                  }}
                  className={`cursor-pointer transition-colors ${
                    isSelected
                      ? 'bg-emerald-950/20 hover:bg-emerald-950/30'
                      : isHighlighted
                      ? 'bg-slate-800/50'
                      : 'hover:bg-slate-800/30'
                  }`}
                >
                  <td className="py-3.5 px-4">
                    <div className="flex items-center space-x-2">
                      <span className={`w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold ${
                        entry.rank === 1 ? 'bg-emerald-500 text-black' : 'bg-slate-700 text-slate-300'
                      }`}>
                        {entry.rank}
                      </span>
                      <div>
                        <div className="font-semibold text-white font-sans">{entry.name}</div>
                        <div className="text-xs text-slate-400">{entry.archetype}</div>
                      </div>
                    </div>
                  </td>

                  <td className="py-3.5 px-4 font-bold text-indigo-300">
                    {entry.utility_score.toFixed(4)}
                  </td>

                  <td className="py-3.5 px-4 text-slate-200">
                    {(entry.accuracy * 100).toFixed(1)}%
                  </td>

                  <td className="py-3.5 px-4 text-slate-200">
                    {entry.critical_path_ms.toFixed(0)} ms
                  </td>

                  <td className="py-3.5 px-4 text-slate-200">
                    ${entry.total_cost_usd.toFixed(4)}
                  </td>

                  <td className="py-3.5 px-4">
                    <span className={`px-2 py-0.5 rounded text-xs ${
                      entry.risk_score < 0.08 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'
                    }`}>
                      {(entry.risk_score * 100).toFixed(1)}%
                    </span>
                  </td>

                  <td className="py-3.5 px-4">
                    {entry.is_pareto_optimal ? (
                      <span className="px-2 py-0.5 rounded text-xs bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                        Pareto Optimal
                      </span>
                    ) : (
                      <span className="text-xs text-slate-500">Dominated</span>
                    )}
                  </td>

                  <td className="py-3.5 px-4 font-sans">
                    {isSelected ? (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-500 text-black">
                        SELECTED
                      </span>
                    ) : (
                      <span className="text-xs text-slate-400">Rejected</span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Rationale & Mathematical Equation Breakdown */}
      {utilityBreakdown && (
        <div className="bg-slate-950/60 border border-slate-800 rounded-lg p-4 space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300">
              Utility Formulation & Selection Provenance
            </h4>
            <span className="text-[11px] font-mono text-slate-500">Model: v{utilityBreakdown.version}</span>
          </div>

          <div className="bg-slate-900/90 rounded p-2.5 font-mono text-xs text-indigo-300 border border-indigo-900/40">
            {utilityBreakdown.equation}
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs pt-1">
            <div className="bg-slate-900/60 p-2.5 rounded border border-slate-800">
              <span className="text-slate-400 block text-[10px] uppercase">Accuracy Term</span>
              <span className="text-emerald-400 font-bold font-mono">+{utilityBreakdown.accuracy_term.toFixed(4)}</span>
              <span className="text-slate-500 block text-[10px] mt-0.5">weight: {utilityBreakdown.weights.w_accuracy}</span>
            </div>
            <div className="bg-slate-900/60 p-2.5 rounded border border-slate-800">
              <span className="text-slate-400 block text-[10px] uppercase">Latency Penalty</span>
              <span className="text-rose-400 font-bold font-mono">-{utilityBreakdown.latency_penalty_term.toFixed(4)}</span>
              <span className="text-slate-500 block text-[10px] mt-0.5">weight: {utilityBreakdown.weights.w_latency}</span>
            </div>
            <div className="bg-slate-900/60 p-2.5 rounded border border-slate-800">
              <span className="text-slate-400 block text-[10px] uppercase">Cost Penalty</span>
              <span className="text-rose-400 font-bold font-mono">-{utilityBreakdown.cost_penalty_term.toFixed(4)}</span>
              <span className="text-slate-500 block text-[10px] mt-0.5">weight: {utilityBreakdown.weights.w_cost}</span>
            </div>
            <div className="bg-slate-900/60 p-2.5 rounded border border-slate-800">
              <span className="text-slate-400 block text-[10px] uppercase">Memory & Sat. Bonus</span>
              <span className="text-cyan-400 font-bold font-mono">+{(utilityBreakdown.memory_bonus_term + utilityBreakdown.satisfaction_bonus_term).toFixed(4)}</span>
              <span className="text-slate-500 block text-[10px] mt-0.5">synergy active</span>
            </div>
          </div>
        </div>
      )}

      {/* Rejection Justifications Card */}
      {selectedRowId && selectedRowId !== matrix.selected_strategy_id && rejectionReasons[selectedRowId] && (
        <div className="bg-amber-950/20 border border-amber-800/40 rounded-lg p-3.5 text-xs text-amber-200">
          <span className="font-bold text-amber-300 uppercase tracking-wider block mb-1">
            Rejection Provenance for {selectedRowId}:
          </span>
          <p className="font-sans">{rejectionReasons[selectedRowId]}</p>
        </div>
      )}
    </div>
  );
};
