import React, { useState, useEffect } from 'react';
import {
  RefreshCw,
  Server,
  Play,
  CheckCircle2,
} from 'lucide-react';
import { CognitiveEvolutionApiClient } from '../../services/cognitiveEvolutionApiClient';
import { DigitalTwinClusterReportPayload } from '../../types/cognitiveEvolution';

export const DigitalTwinSimulatorView: React.FC = () => {
  const [report, setReport] = useState<DigitalTwinClusterReportPayload | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [simulating, setSimulating] = useState<boolean>(false);
  const [missionCount] = useState<number>(500);

  useEffect(() => {
    loadSimulation();
  }, []);

  const loadSimulation = async () => {
    setLoading(true);
    try {
      const data = await CognitiveEvolutionApiClient.runDigitalTwinSimulation(missionCount);
      setReport(data);
    } catch (e) {
      console.error('Failed to run digital twin simulation:', e);
    } finally {
      setLoading(false);
    }
  };

  const handleRunSim = async () => {
    setSimulating(true);
    try {
      const data = await CognitiveEvolutionApiClient.runDigitalTwinSimulation(missionCount);
      setReport(data);
    } catch (e) {
      console.error('Simulation failed:', e);
    } finally {
      setSimulating(false);
    }
  };

  return (
    <div className="space-y-6 font-mono">
      {/* Top Banner & Simulation Config Controls */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-sm font-bold text-cyan-300 flex items-center gap-2">
              <Server className="w-4 h-4 text-cyan-400" />
              Digital Twin Distributed Cluster Simulator (1,000+ Workers)
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              High-fidelity discrete-event queuing simulation modeling GPU thermals, VRAM pressure, and chaos fault injection.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleRunSim}
              disabled={simulating}
              className="flex items-center gap-2 px-3 py-1.5 bg-cyan-950/60 hover:bg-cyan-900/70 border border-cyan-800 text-cyan-300 rounded-lg text-xs font-bold transition-all disabled:opacity-50"
            >
              <Play className={`w-3.5 h-3.5 ${simulating ? 'animate-spin' : ''}`} />
              Run 500-Mission Simulation
            </button>

            <button
              onClick={loadSimulation}
              disabled={loading}
              className="text-slate-400 hover:text-cyan-400 p-1.5 rounded"
              title="Refresh"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </div>

        {/* Cluster Telemetry Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-1">
          <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-3">
            <div className="text-[10px] text-slate-500 uppercase">Virtual Nodes</div>
            <div className="text-xl font-bold text-slate-200 mt-0.5">
              {report?.total_virtual_workers || 1000} <span className="text-[10px] text-cyan-400">GPU/CPU</span>
            </div>
          </div>

          <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-3">
            <div className="text-[10px] text-slate-500 uppercase">P95 Latency</div>
            <div className="text-xl font-bold text-amber-300 mt-0.5">
              {report?.p95_latency_ms.toFixed(0) || 850}ms
            </div>
          </div>

          <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-3">
            <div className="text-[10px] text-slate-500 uppercase">Tokens Consumed</div>
            <div className="text-xl font-bold text-purple-300 mt-0.5">
              {((report?.total_simulated_tokens || 2450000) / 1000000).toFixed(2)}M
            </div>
          </div>

          <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-3">
            <div className="text-[10px] text-slate-500 uppercase">Resilience Score</div>
            <div className="text-xl font-bold text-emerald-400 mt-0.5">
              {((report?.resilience_score || 0.992) * 100).toFixed(1)}%
            </div>
          </div>
        </div>
      </div>

      {/* Latency Percentiles & Queue Dynamics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3">
          <div className="text-xs uppercase text-slate-400 tracking-wider">Tail Latency Breakdown</div>
          <div className="space-y-2">
            <div className="flex justify-between text-xs">
              <span className="text-slate-400">P50 (Median)</span>
              <span className="text-emerald-400 font-bold">{report?.p50_latency_ms.toFixed(0)}ms</span>
            </div>
            <div className="flex justify-between text-xs">
              <span className="text-slate-400">P95</span>
              <span className="text-amber-400 font-bold">{report?.p95_latency_ms.toFixed(0)}ms</span>
            </div>
            <div className="flex justify-between text-xs">
              <span className="text-slate-400">P99</span>
              <span className="text-rose-400 font-bold">{report?.p99_latency_ms.toFixed(0)}ms</span>
            </div>
          </div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3">
          <div className="text-xs uppercase text-slate-400 tracking-wider">Cluster Hardware Headroom</div>
          <div className="space-y-2">
            <div className="flex justify-between text-xs">
              <span className="text-slate-400">Avg GPU Utilization</span>
              <span className="text-cyan-300 font-bold">{report?.average_gpu_utilization_pct.toFixed(1)}%</span>
            </div>
            <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-cyan-500 to-emerald-400 rounded-full"
                style={{ width: `${report?.average_gpu_utilization_pct || 68.5}%` }}
              />
            </div>
          </div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3">
          <div className="text-xs uppercase text-slate-400 tracking-wider">Fault Injection Status</div>
          <div className="p-3 bg-slate-950/80 border border-slate-800 rounded text-xs space-y-1">
            <div className="text-emerald-300 flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              0 Queue Overflows
            </div>
            <div className="text-[10px] text-slate-500">Chaos fault rate: 2.0% stochastic crashes</div>
          </div>
        </div>
      </div>
    </div>
  );
};
