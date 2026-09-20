import React, { useState, useEffect } from 'react';
import {
  Layers,
  ShieldCheck,
  Play,
  RefreshCw,
  Flame,
  CheckCircle2,
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
import { SimulationReportPayload } from '../../types/evolutionPlatform';

export const EvolutionSimulationStudio: React.FC = () => {
  const [latestReport, setLatestReport] = useState<SimulationReportPayload | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [simulating, setSimulating] = useState<boolean>(false);

  // Simulation controls
  const [mode, setMode] = useState<string>('SHADOW_REPLAY');
  const [traceCount, setTraceCount] = useState<number>(2000);

  useEffect(() => {
    loadSimulations();
  }, []);

  const loadSimulations = async () => {
    setLoading(true);
    try {
      const data = await EvolutionPlatformApiClient.listSimulations();
      if (data.length > 0) {
        const last = data[data.length - 1];
        if (last) setLatestReport(last);
      }
    } catch (err) {
      console.error('Failed to load simulations:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunSimulation = async () => {
    setSimulating(true);
    try {
      const res = await EvolutionPlatformApiClient.runSimulation({
        simulation_mode: mode,
        traces_count: traceCount,
      });
      setLatestReport(res);
    } catch (err) {
      console.error('Simulation error:', err);
    } finally {
      setSimulating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-cyan-500/10 border border-cyan-500/20 rounded-xl">
            <Layers className="w-6 h-6 text-cyan-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-slate-100">Evolution Simulation & Digital Twin Sandbox</h1>
              <Badge variant="info" size="sm">Shadow Replay & Chaos</Badge>
            </div>
            <p className="text-sm text-slate-400 mt-0.5">
              Simulates candidate architecture modifications against thousands of production traces and chaos injections before rollout.
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            onClick={loadSimulations}
            disabled={loading}
          >
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button
            variant="intelligence"
            onClick={handleRunSimulation}
            disabled={simulating}
          >
            <span className="flex items-center gap-2">
              <Play className={`w-4 h-4 ${simulating ? 'animate-spin' : ''}`} />
              {simulating ? 'Simulating Replay...' : 'Run Digital Twin Simulation'}
            </span>
          </Button>
        </div>
      </div>

      {/* Control Panel */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-sm font-semibold text-slate-200">Simulation Configuration</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div>
            <label className="text-xs font-medium text-slate-400 block mb-1">Simulation Mode</label>
            <select
              value={mode}
              onChange={(e) => setMode(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-cyan-500"
            >
              <option value="SHADOW_REPLAY">Shadow Replay (Historical Real Traces)</option>
              <option value="DIGITAL_TWIN">Digital Twin Predictive World Model</option>
              <option value="CHAOS_FAULT_INJECTION">Chaos Fault Injection (Worker Crashes & Lag)</option>
              <option value="MONTE_CARLO">Monte Carlo Extreme Stress Load</option>
            </select>
          </div>

          <div>
            <div className="flex justify-between text-xs font-medium text-slate-400 mb-1">
              <span>Historical Request Traces</span>
              <span className="font-mono text-cyan-400">{traceCount} Traces</span>
            </div>
            <input
              type="range"
              min="500"
              max="10000"
              step="500"
              value={traceCount}
              onChange={(e) => setTraceCount(parseInt(e.target.value))}
              className="w-full accent-cyan-400 cursor-pointer mt-2"
            />
          </div>
        </div>
      </div>

      {/* Latest Simulation Report */}
      {latestReport && (
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-5">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-4 border-b border-slate-800">
            <div>
              <div className="flex items-center gap-3">
                <h2 className="text-base font-bold text-slate-100">
                  Simulation Report: {latestReport.simulation_id}
                </h2>
                <Badge variant={latestReport.verified_safe ? 'success' : 'warning'} size="sm">
                  {latestReport.verified_safe ? 'Verified Safe' : 'Safety Warning'}
                </Badge>
              </div>
              <span className="text-xs text-slate-400 font-mono mt-0.5 block">
                Mode: {latestReport.simulation_mode} • Traces: {latestReport.traces_replayed}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-400">Confidence:</span>
              <span className="text-xl font-bold text-cyan-400 font-mono">
                {(latestReport.stability_confidence * 100).toFixed(1)}%
              </span>
            </div>
          </div>

          {/* 3 Metric Tiles */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono">
            <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-4 space-y-2">
              <div className="flex items-center justify-between text-xs text-slate-400">
                <span className="flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  Success Rate
                </span>
                <span className="text-emerald-400 font-bold">{(latestReport.success_rate * 100).toFixed(2)}%</span>
              </div>
              <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div className="bg-emerald-400 h-full rounded-full" style={{ width: `${latestReport.success_rate * 100}%` }} />
              </div>
            </div>

            <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-4 space-y-2">
              <div className="flex items-center justify-between text-xs text-slate-400">
                <span className="flex items-center gap-1.5">
                  <Flame className="w-4 h-4 text-amber-400" />
                  Chaos Resilience
                </span>
                <span className="text-amber-400 font-bold">{(latestReport.chaos_resilience_score * 100).toFixed(1)}%</span>
              </div>
              <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div className="bg-amber-400 h-full rounded-full" style={{ width: `${latestReport.chaos_resilience_score * 100}%` }} />
              </div>
            </div>

            <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-4 space-y-2">
              <div className="flex items-center justify-between text-xs text-slate-400">
                <span className="flex items-center gap-1.5">
                  <ShieldCheck className="w-4 h-4 text-purple-400" />
                  Invariant Violations
                </span>
                <span className="text-emerald-400 font-bold">{latestReport.safety_invariant_violations} Violations</span>
              </div>
              <div className="text-[11px] text-slate-500 pt-0.5">
                Zero security guardrail boundary breaches
              </div>
            </div>
          </div>

          <div className="p-3 bg-slate-950/80 border border-slate-800/80 rounded-lg text-xs font-mono text-slate-400">
            <span className="text-slate-300 font-bold block mb-1">Execution Notes:</span>
            {latestReport.execution_notes}
          </div>
        </div>
      )}
    </div>
  );
};
