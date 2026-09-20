import React, { useState, useEffect } from 'react';
import {
  Gauge,
  Cpu,
  Zap,
  Activity,
  AlertTriangle,
  RefreshCw,
  Clock,
  HardDrive,
  Layers,
  Database,
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
import { PlatformHealthSnapshotPayload } from '../../types/evolutionPlatform';

export const ArchitectureProfilerCenter: React.FC = () => {
  const [snapshots, setSnapshots] = useState<PlatformHealthSnapshotPayload[]>([]);
  const [latestSnapshot, setLatestSnapshot] = useState<PlatformHealthSnapshotPayload | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [profiling, setProfiling] = useState<boolean>(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await EvolutionPlatformApiClient.listProfilerSnapshots();
      setSnapshots(data);
      if (data.length > 0) {
        const last = data[data.length - 1];
        if (last) setLatestSnapshot(last);
      }
    } catch (err) {
      console.error('Failed to load snapshots:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCollectSnapshot = async () => {
    setProfiling(true);
    try {
      const snap = await EvolutionPlatformApiClient.collectProfilerSnapshot();
      setLatestSnapshot(snap);
      setSnapshots((prev) => [...prev, snap]);
    } catch (err) {
      console.error('Profiling error:', err);
    } finally {
      setProfiling(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-cyan-500/10 border border-cyan-500/20 rounded-xl">
            <Gauge className="w-6 h-6 text-cyan-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-slate-100">Runtime Telemetry & Holistic Profiler</h1>
              <Badge variant="info" size="sm">Real-Time Continuous</Badge>
            </div>
            <p className="text-sm text-slate-400 mt-0.5">
              Deep profiling across CPU, GPU, memory fragmentation, token waste rate, queue contention, and latency percentiles.
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            onClick={loadData}
            disabled={loading}
          >
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button
            variant="intelligence"
            onClick={handleCollectSnapshot}
            disabled={profiling}
          >
            <span className="flex items-center gap-2">
              <Activity className={`w-4 h-4 ${profiling ? 'animate-spin' : ''}`} />
              {profiling ? 'Sampling Telemetry...' : 'Sample Real-time Snapshot'}
            </span>
          </Button>
        </div>
      </div>

      {/* Main Gauges Grid */}
      {latestSnapshot && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between text-slate-400">
              <span className="text-xs font-mono uppercase tracking-wider">Compute Utilization</span>
              <Cpu className="w-4 h-4 text-cyan-400" />
            </div>
            <div className="flex items-baseline justify-between">
              <span className="text-2xl font-bold text-slate-100">{latestSnapshot.cpu_utilization_pct.toFixed(1)}%</span>
              <span className="text-xs text-slate-400">GPU: {latestSnapshot.gpu_utilization_pct.toFixed(1)}%</span>
            </div>
            <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
              <div
                className="bg-cyan-400 h-full rounded-full transition-all"
                style={{ width: `${Math.min(100, latestSnapshot.cpu_utilization_pct)}%` }}
              />
            </div>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between text-slate-400">
              <span className="text-xs font-mono uppercase tracking-wider">Token Waste Rate</span>
              <Zap className="w-4 h-4 text-amber-400" />
            </div>
            <div className="flex items-baseline justify-between">
              <span className="text-2xl font-bold text-slate-100">{(latestSnapshot.token_waste_rate * 100).toFixed(2)}%</span>
              <Badge variant={latestSnapshot.token_waste_rate < 0.05 ? 'success' : 'warning'} size="sm">
                {latestSnapshot.token_waste_rate < 0.05 ? 'Optimal' : 'Elevated'}
              </Badge>
            </div>
            <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full transition-all ${latestSnapshot.token_waste_rate < 0.05 ? 'bg-emerald-400' : 'bg-amber-400'}`}
                style={{ width: `${Math.min(100, latestSnapshot.token_waste_rate * 1000)}%` }}
              />
            </div>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between text-slate-400">
              <span className="text-xs font-mono uppercase tracking-wider">P95 Latency</span>
              <Clock className="w-4 h-4 text-indigo-400" />
            </div>
            <div className="flex items-baseline justify-between">
              <span className="text-2xl font-bold text-slate-100">{latestSnapshot.latency_p95_ms.toFixed(1)}ms</span>
              <span className="text-xs text-slate-400">P99: {latestSnapshot.latency_p99_ms.toFixed(0)}ms</span>
            </div>
            <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
              <div
                className="bg-indigo-400 h-full rounded-full transition-all"
                style={{ width: `${Math.min(100, (latestSnapshot.latency_p95_ms / 300) * 100)}%` }}
              />
            </div>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between text-slate-400">
              <span className="text-xs font-mono uppercase tracking-wider">Cache Hit Rate</span>
              <Database className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="flex items-baseline justify-between">
              <span className="text-2xl font-bold text-slate-100">{(latestSnapshot.cache_hit_rate * 100).toFixed(1)}%</span>
              <Badge variant="success" size="sm">High Precision</Badge>
            </div>
            <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
              <div
                className="bg-emerald-400 h-full rounded-full transition-all"
                style={{ width: `${Math.min(100, latestSnapshot.cache_hit_rate * 100)}%` }}
              />
            </div>
          </div>
        </div>
      )}

      {/* Bottlenecks and Telemetry History */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Layers className="w-5 h-5 text-indigo-400" />
              <h2 className="text-base font-semibold text-slate-100">Historical Telemetry Samples</h2>
            </div>
            <span className="text-xs text-slate-400">Samples: {snapshots.length}</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-950/60 text-slate-400 border-b border-slate-800 uppercase font-mono tracking-wider">
                <tr>
                  <th className="py-2.5 px-3">Snapshot ID</th>
                  <th className="py-2.5 px-3">CPU</th>
                  <th className="py-2.5 px-3">P95 Latency</th>
                  <th className="py-2.5 px-3">Token Waste</th>
                  <th className="py-2.5 px-3">Cache Hit</th>
                  <th className="py-2.5 px-3">Health Grade</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono">
                {snapshots.slice(-6).reverse().map((s) => (
                  <tr key={s.snapshot_id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="py-2.5 px-3 text-slate-400 font-semibold">{s.snapshot_id}</td>
                    <td className="py-2.5 px-3">{s.cpu_utilization_pct.toFixed(1)}%</td>
                    <td className="py-2.5 px-3 text-indigo-300">{s.latency_p95_ms.toFixed(1)}ms</td>
                    <td className="py-2.5 px-3 text-amber-300">{(s.token_waste_rate * 100).toFixed(2)}%</td>
                    <td className="py-2.5 px-3 text-emerald-300">{(s.cache_hit_rate * 100).toFixed(1)}%</td>
                    <td className="py-2.5 px-3">
                      <Badge variant={s.health_grade === 'EXCELLENT' || s.health_grade === 'HEALTHY' ? 'success' : 'warning'} size="sm">
                        {s.health_grade}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Bottleneck Alerts */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            <h2 className="text-base font-semibold text-slate-100">Active Bottlenecks</h2>
          </div>

          <div className="space-y-3">
            {latestSnapshot?.active_bottlenecks && latestSnapshot.active_bottlenecks.length > 0 ? (
              latestSnapshot.active_bottlenecks.map((b, i) => (
                <div key={i} className="p-3 bg-amber-500/10 border border-amber-500/20 rounded-lg text-xs text-amber-200">
                  {b}
                </div>
              ))
            ) : (
              <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-xs text-emerald-300 flex items-center gap-2">
                <Activity className="w-4 h-4" />
                Zero critical bottlenecks detected in the active telemetry stream.
              </div>
            )}

            <div className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg space-y-1.5 text-xs text-slate-400">
              <div className="flex items-center justify-between text-slate-300 font-semibold">
                <span className="flex items-center gap-1.5">
                  <HardDrive className="w-3.5 h-3.5 text-indigo-400" />
                  Memory Fragmentation
                </span>
                <span>{latestSnapshot?.memory_fragmentation_pct.toFixed(1) ?? '4.8'}%</span>
              </div>
              <div className="flex items-center justify-between text-slate-300 font-semibold">
                <span>Queue Saturation</span>
                <span>{latestSnapshot?.queue_saturation_pct.toFixed(1) ?? '18.0'}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
