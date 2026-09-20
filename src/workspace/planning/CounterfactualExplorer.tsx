/**
 * Counterfactual Reasoning & Sensitivity Explorer Component.
 * Enables interactive parameter tuning, What-If counterfactual queries, and real-time tipping point analysis.
 */

import React, { useState, useEffect } from 'react';
import { CounterfactualExplanation, UtilityWeights } from '../../types/autonomousPlanning';
import { PlanningApiClient } from '../../services/planningApiClient';

interface CounterfactualExplorerProps {
  missionId?: string;
}

export const CounterfactualExplorerView: React.FC<CounterfactualExplorerProps> = ({
  missionId = 'mission_active_001',
}) => {
  const [weights, setWeights] = useState<UtilityWeights>({
    w_accuracy: 0.40,
    w_latency: 0.20,
    w_cost: 0.20,
    w_risk: 0.10,
    w_memory: 0.05,
    w_satisfaction: 0.05,
  });

  const [explanation, setExplanation] = useState<CounterfactualExplanation | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    runWhatIf();
  }, [weights]);

  const runWhatIf = async () => {
    setLoading(true);
    try {
      const res = await PlanningApiClient.queryCounterfactual(
        missionId,
        'WHAT_IF_WEIGHT_CHANGED',
        weights as unknown as Record<string, number>
      );
      setExplanation(res);
    } catch (err) {
      console.error('Failed to query counterfactuals', err);
    } finally {
      setLoading(false);
    }
  };

  const applyPreset = (name: string) => {
    if (name === 'AUDIT') {
      setWeights({ w_accuracy: 0.70, w_latency: 0.10, w_cost: 0.10, w_risk: 0.05, w_memory: 0.025, w_satisfaction: 0.025 });
    } else if (name === 'TURBO') {
      setWeights({ w_accuracy: 0.20, w_latency: 0.60, w_cost: 0.10, w_risk: 0.05, w_memory: 0.025, w_satisfaction: 0.025 });
    } else if (name === 'FRUGAL') {
      setWeights({ w_accuracy: 0.20, w_latency: 0.10, w_cost: 0.60, w_risk: 0.05, w_memory: 0.025, w_satisfaction: 0.025 });
    } else {
      setWeights({ w_accuracy: 0.40, w_latency: 0.20, w_cost: 0.20, w_risk: 0.10, w_memory: 0.05, w_satisfaction: 0.05 });
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-slate-100 shadow-2xl space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-slate-800 pb-4 gap-4">
        <div>
          <div className="flex items-center space-x-3">
            <span className="px-2.5 py-1 text-xs font-bold uppercase tracking-wider bg-purple-500/20 text-purple-400 border border-purple-500/30 rounded-md">
              Sensitivity & What-If Engine
            </span>
            <span className="text-xs text-slate-400 font-mono">Mission: {missionId}</span>
            {loading && (
              <span className="text-xs text-indigo-400 animate-pulse">Calculating sensitivity...</span>
            )}
          </div>
          <h2 className="text-xl font-bold text-white mt-1">Counterfactual Explainability Explorer</h2>
          <p className="text-sm text-slate-400">
            Dynamically adjust utility weights to observe decision boundaries, ranking inversions, and tipping points.
          </p>
        </div>

        {/* Presets */}
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => applyPreset('DEFAULT')}
            className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-xs font-medium rounded border border-slate-700 transition"
          >
            Pareto Balanced
          </button>
          <button
            onClick={() => applyPreset('AUDIT')}
            className="px-2.5 py-1 bg-indigo-900/50 hover:bg-indigo-800/60 text-indigo-300 text-xs font-medium rounded border border-indigo-700/50 transition"
          >
            Deep Audit (Accuracy)
          </button>
          <button
            onClick={() => applyPreset('TURBO')}
            className="px-2.5 py-1 bg-cyan-900/50 hover:bg-cyan-800/60 text-cyan-300 text-xs font-medium rounded border border-cyan-700/50 transition"
          >
            Realtime SLA (Turbo)
          </button>
          <button
            onClick={() => applyPreset('FRUGAL')}
            className="px-2.5 py-1 bg-emerald-900/50 hover:bg-emerald-800/60 text-emerald-300 text-xs font-medium rounded border border-emerald-700/50 transition"
          >
            Bulk Frugal (Cost)
          </button>
        </div>
      </div>

      {/* Sliders Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 bg-slate-950/50 p-4 rounded-lg border border-slate-800">
        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="text-slate-400">Accuracy Weight (w_acc)</span>
            <span className="font-mono text-emerald-400 font-bold">{weights.w_accuracy.toFixed(2)}</span>
          </div>
          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={weights.w_accuracy}
            onChange={(e) => setWeights({ ...weights, w_accuracy: parseFloat(e.target.value) })}
            className="w-full accent-emerald-500 cursor-pointer"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="text-slate-400">Latency Penalty (w_lat)</span>
            <span className="font-mono text-rose-400 font-bold">{weights.w_latency.toFixed(2)}</span>
          </div>
          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={weights.w_latency}
            onChange={(e) => setWeights({ ...weights, w_latency: parseFloat(e.target.value) })}
            className="w-full accent-rose-500 cursor-pointer"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="text-slate-400">Cost Penalty (w_cost)</span>
            <span className="font-mono text-amber-400 font-bold">{weights.w_cost.toFixed(2)}</span>
          </div>
          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={weights.w_cost}
            onChange={(e) => setWeights({ ...weights, w_cost: parseFloat(e.target.value) })}
            className="w-full accent-amber-500 cursor-pointer"
          />
        </div>

        <div>
          <div className="flex justify-between text-xs mb-1">
            <span className="text-slate-400">Risk Penalty (w_risk)</span>
            <span className="font-mono text-purple-400 font-bold">{weights.w_risk.toFixed(2)}</span>
          </div>
          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={weights.w_risk}
            onChange={(e) => setWeights({ ...weights, w_risk: parseFloat(e.target.value) })}
            className="w-full accent-purple-500 cursor-pointer"
          />
        </div>
      </div>

      {/* Simulated Winner & Rankings */}
      {explanation && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Winner Card */}
          <div className="md:col-span-1 bg-gradient-to-br from-indigo-950/40 to-slate-900 border border-indigo-500/30 rounded-lg p-4 flex flex-col justify-between">
            <div>
              <span className="text-[10px] uppercase font-bold text-indigo-400 tracking-wider block">
                Counterfactual Winner
              </span>
              <h3 className="text-lg font-bold text-white mt-1">
                {explanation.alternative_ranking?.[0]?.name || 'Strategy Delta'}
              </h3>
              <p className="text-xs text-slate-300 mt-2 leading-relaxed">
                {explanation.summary_explanation}
              </p>
            </div>

            {explanation.tipping_point && (
              <div className="mt-4 pt-3 border-t border-indigo-900/50 bg-indigo-950/30 -mx-4 -mb-4 p-3 rounded-b-lg">
                <span className="text-[10px] font-bold text-amber-400 uppercase tracking-wider block mb-0.5">
                  Analytical Tipping Point
                </span>
                <span className="text-xs text-slate-300 font-mono block">
                  {explanation.tipping_point.condition}
                </span>
              </div>
            )}
          </div>

          {/* Alternative Rankings Table */}
          <div className="md:col-span-2 bg-slate-950/60 border border-slate-800 rounded-lg p-4">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
              Recalculated Strategy Order
            </h4>
            <div className="space-y-2 font-mono text-xs">
              {explanation.alternative_ranking?.map((rankItem, idx) => (
                <div
                  key={rankItem.strategy_id}
                  className={`flex items-center justify-between p-2 rounded border ${
                    idx === 0
                      ? 'bg-emerald-950/30 border-emerald-500/40 text-emerald-200'
                      : 'bg-slate-900/60 border-slate-800 text-slate-300'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <span className="font-bold w-4">{idx + 1}.</span>
                    <span className="font-sans font-medium">{rankItem.name}</span>
                    <span className="text-[10px] text-slate-500">({rankItem.archetype})</span>
                  </div>
                  <div className="font-bold">
                    U = {rankItem.new_utility.toFixed(4)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
