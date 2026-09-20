import React, { useState, useEffect } from 'react';
import {
  TrendingUp,
  Cpu,
  Clock,
  AlertOctagon,
  CheckCircle2,
  RefreshCw,
  Sliders,
} from 'lucide-react';
import { DecisionIntelligenceApiClient } from '../../services/decisionIntelligenceApiClient';
import { WorldStateHorizonPayload } from '../../types/decisionIntelligence';

export const WorldPredictionDashboard: React.FC = () => {
  const [forecasts, setForecasts] = useState<Record<string, WorldStateHorizonPayload>>({});
  const [loading, setLoading] = useState<boolean>(true);
  const [loadFactor, setLoadFactor] = useState<number>(1.2);
  const [concurrency, setConcurrency] = useState<number>(6);

  useEffect(() => {
    loadForecast();
  }, [loadFactor, concurrency]);

  const loadForecast = async () => {
    setLoading(true);
    try {
      const data = await DecisionIntelligenceApiClient.getWorldForecast();
      setForecasts(data.horizons);
    } catch (e) {
      console.error('Failed to load world forecasts:', e);
    } finally {
      setLoading(false);
    }
  };

  const horizonKeys = ['5m', '10m', '30m'];

  return (
    <div className="space-y-6">
      {/* Top Controls & Simulation Sliders */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-sm font-bold font-mono text-cyan-300 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-cyan-400" />
              World Model Forward Simulator
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Simulates forward cluster physics across 5m, 10m, and 30m prediction horizons using Queuing Theory & Markov Chains.
            </p>
          </div>

          <button
            onClick={loadForecast}
            disabled={loading}
            className="flex items-center gap-2 px-3 py-1.5 bg-cyan-950/40 hover:bg-cyan-900/50 border border-cyan-800 text-cyan-300 rounded-lg text-xs font-mono transition-all disabled:opacity-50 self-start sm:self-auto"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            Re-simulate Physics
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-1">
          {/* Mission Load Slider */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs font-mono">
              <span className="text-slate-300 flex items-center gap-1.5">
                <Sliders className="w-3.5 h-3.5 text-purple-400" />
                Mission Arrival Load Factor
              </span>
              <span className="text-purple-300 font-bold">{loadFactor.toFixed(1)}x</span>
            </div>
            <input
              type="range"
              min="0.5"
              max="3.0"
              step="0.1"
              value={loadFactor}
              onChange={(e) => setLoadFactor(parseFloat(e.target.value))}
              className="w-full accent-purple-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
            />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono">
              <span>0.5x (Idle)</span>
              <span>1.0x (Nominal)</span>
              <span>3.0x (Peak Burst)</span>
            </div>
          </div>

          {/* Cluster Concurrency Slider */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs font-mono">
              <span className="text-slate-300 flex items-center gap-1.5">
                <Cpu className="w-3.5 h-3.5 text-cyan-400" />
                Active Worker Concurrency
              </span>
              <span className="text-cyan-300 font-bold">{concurrency} Nodes</span>
            </div>
            <input
              type="range"
              min="1"
              max="16"
              step="1"
              value={concurrency}
              onChange={(e) => setConcurrency(parseInt(e.target.value))}
              className="w-full accent-cyan-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
            />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono">
              <span>1 Node</span>
              <span>8 Nodes</span>
              <span>16 Nodes</span>
            </div>
          </div>
        </div>
      </div>

      {/* Multi-Horizon Cards Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {horizonKeys.map((key) => {
          const f = forecasts[key];
          if (!f) return null;

          const isWarning = f.predicted_gpu_utilization > 0.8 || f.predicted_budget_exhaustion_probability > 0.05;
          const gpuPct = (f.predicted_gpu_utilization * 100).toFixed(1);
          const exhaustPct = (f.predicted_budget_exhaustion_probability * 100).toFixed(1);

          return (
            <div
              key={key}
              className={`bg-slate-900/90 border rounded-xl p-5 space-y-4 transition-all ${
                isWarning
                  ? 'border-amber-500/50 shadow-lg shadow-amber-950/20'
                  : 'border-slate-800 hover:border-slate-700'
              }`}
            >
              {/* Horizon Header */}
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4 text-cyan-400" />
                  <span className="text-base font-bold font-mono text-slate-100">
                    T + {f.horizon_minutes}m Horizon
                  </span>
                </div>
                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-mono border ${
                    isWarning
                      ? 'bg-amber-950/60 text-amber-300 border-amber-800'
                      : 'bg-emerald-950/60 text-emerald-300 border-emerald-800'
                  }`}
                >
                  {isWarning ? 'CAPACITY STRAIN' : 'STABLE STATE'}
                </span>
              </div>

              {/* Metric Breakdown */}
              <div className="space-y-3">
                {/* GPU Load */}
                <div>
                  <div className="flex items-center justify-between text-xs font-mono mb-1">
                    <span className="text-slate-400 flex items-center gap-1">
                      <Cpu className="w-3.5 h-3.5 text-cyan-400" />
                      Predicted GPU Load
                    </span>
                    <span className="font-bold text-slate-200">{gpuPct}%</span>
                  </div>
                  <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ${
                        f.predicted_gpu_utilization > 0.8
                          ? 'bg-gradient-to-r from-amber-500 to-rose-500'
                          : 'bg-gradient-to-r from-cyan-500 to-emerald-400'
                      }`}
                      style={{ width: `${Math.min(100, f.predicted_gpu_utilization * 100)}%` }}
                    />
                  </div>
                </div>

                {/* Queue Depth & Token Burn */}
                <div className="grid grid-cols-2 gap-2 pt-1">
                  <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-2.5">
                    <div className="text-[10px] font-mono text-slate-400 uppercase">Queue Depth</div>
                    <div className="text-base font-bold font-mono text-slate-200 mt-0.5">
                      {f.predicted_queue_depth} <span className="text-[10px] text-slate-500 font-normal">items</span>
                    </div>
                  </div>

                  <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-2.5">
                    <div className="text-[10px] font-mono text-slate-400 uppercase">Token Velocity</div>
                    <div className="text-base font-bold font-mono text-purple-300 mt-0.5">
                      {f.predicted_token_burn_velocity.toFixed(0)}{' '}
                      <span className="text-[10px] text-slate-500 font-normal">t/s</span>
                    </div>
                  </div>
                </div>

                {/* Budget Exhaustion Risk */}
                <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-2.5">
                  <div className="flex items-center justify-between text-[10px] font-mono">
                    <span className="text-slate-400 uppercase">Budget Breach Risk</span>
                    <span
                      className={`font-bold ${
                        f.predicted_budget_exhaustion_probability > 0.05
                          ? 'text-rose-400'
                          : 'text-emerald-400'
                      }`}
                    >
                      {exhaustPct}%
                    </span>
                  </div>
                  <div className="text-[9px] text-slate-500 font-mono mt-1">
                    95% CI: [{(f.confidence_interval_lower * 100).toFixed(0)}% -{' '}
                    {(f.confidence_interval_upper * 100).toFixed(0)}%]
                  </div>
                </div>
              </div>

              {/* Status Footer */}
              <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] font-mono text-slate-400">
                <span className="flex items-center gap-1">
                  {isWarning ? (
                    <AlertOctagon className="w-3.5 h-3.5 text-amber-400" />
                  ) : (
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  )}
                  {isWarning ? 'Auto-scaling triggered' : 'Nominal headroom'}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
