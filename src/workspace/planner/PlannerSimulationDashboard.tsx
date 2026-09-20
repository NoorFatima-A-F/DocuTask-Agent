import React, { useState, useEffect } from 'react';
import {
  TrendingUp,
  Sliders,
  RefreshCw,
} from 'lucide-react';
import { ApdlePlannerApiClient } from '../../services/apdlePlannerApiClient';
import { SimulationResultPayload } from '../../types/apdlePlanner';

export const PlannerSimulationDashboard: React.FC = () => {
  const [sim, setSim] = useState<SimulationResultPayload | null>(null);
  const [trials, setTrials] = useState<number>(100);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadSimulation();
  }, [trials]);

  const loadSimulation = async () => {
    setLoading(true);
    try {
      const data = await ApdlePlannerApiClient.getSimulation('default_mission', trials);
      setSim(data);
    } catch (e) {
      console.error('Failed to load simulation:', e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 font-mono">
      {/* Header Banner */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-sm font-bold text-cyan-300 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-cyan-400" />
              Pre-Execution Monte Carlo DAG Simulator
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Stochastic simulation over DAG variance. Estimates tail latencies (P90, P99), expected cost, and risk bottlenecks.
            </p>
          </div>

          <button
            onClick={loadSimulation}
            disabled={loading}
            className="text-slate-400 hover:text-cyan-400 p-1.5 rounded"
            title="Refresh"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>

        {/* Monte Carlo Trials Slider */}
        <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-4 space-y-2 text-xs">
          <div className="flex justify-between items-center">
            <span className="text-slate-300 flex items-center gap-2">
              <Sliders className="w-3.5 h-3.5 text-purple-400" />
              Monte Carlo Sample Size: <span className="text-purple-300 font-bold">{trials} Iterations</span>
            </span>
          </div>
          <input
            type="range"
            min="20"
            max="500"
            step="20"
            value={trials}
            onChange={(e) => setTrials(parseInt(e.target.value))}
            className="w-full accent-cyan-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
          />
        </div>

        {/* Percentile Latency Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
          <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center">
            <div className="text-[10px] text-slate-500 uppercase">Median Latency (P50)</div>
            <div className="text-xl font-bold text-emerald-400 mt-1">
              {(sim?.p50_completion_ms ?? 760).toFixed(0)}ms
            </div>
          </div>

          <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center">
            <div className="text-[10px] text-slate-500 uppercase">Tail Latency (P90)</div>
            <div className="text-xl font-bold text-amber-400 mt-1">
              {(sim?.p90_completion_ms ?? 880).toFixed(0)}ms
            </div>
          </div>

          <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center">
            <div className="text-[10px] text-slate-500 uppercase">Worst Case (P99)</div>
            <div className="text-xl font-bold text-red-400 mt-1">
              {(sim?.p99_completion_ms ?? 995).toFixed(0)}ms
            </div>
          </div>

          <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center">
            <div className="text-[10px] text-slate-500 uppercase">Expected Cost</div>
            <div className="text-xl font-bold text-cyan-300 mt-1">
              ${(sim?.expected_total_cost_usd ?? 0.0032).toFixed(4)}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
