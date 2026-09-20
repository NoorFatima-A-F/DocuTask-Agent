import React, { useState } from 'react';
import {
  Heart,
  TrendingUp,
  RefreshCw,
  GitFork,
  Activity,
  Sparkles
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

interface HealthIntelligenceDashboardProps {
  missionId?: string;
}

export const HealthIntelligenceDashboard: React.FC<HealthIntelligenceDashboardProps> = ({
  missionId = 'cluster-primary-master',
}) => {
  const [subsystems] = useState([
    { name: 'Planner (APDLE)', score: 99.2, errorRate: '0.00%', latency: '210ms', saturation: '18%', status: 'HEALTHY' },
    { name: 'Workers Pool', score: 98.0, errorRate: '0.01%', latency: '340ms', saturation: '32%', status: 'HEALTHY' },
    { name: 'Memory Vectors', score: 99.5, errorRate: '0.00%', latency: '45ms', saturation: '24%', status: 'HEALTHY' },
    { name: 'Optimization (ARIA)', score: 97.8, errorRate: '0.00%', latency: '120ms', saturation: '15%', status: 'HEALTHY' },
    { name: 'Replay Engine (ESMR)', score: 99.0, errorRate: '0.00%', latency: '85ms', saturation: '12%', status: 'HEALTHY' },
    { name: 'Learning & Reflection', score: 98.4, errorRate: '0.00%', latency: '190ms', saturation: '20%', status: 'HEALTHY' },
    { name: 'Truth Ledger (VAIRT)', score: 100.0, errorRate: '0.00%', latency: '30ms', saturation: '8%', status: 'HEALTHY' },
    { name: 'Telemetry & Events', score: 99.8, errorRate: '0.00%', latency: '15ms', saturation: '14%', status: 'HEALTHY' },
    { name: 'API Gateway', score: 98.9, errorRate: '0.01%', latency: '65ms', saturation: '28%', status: 'HEALTHY' },
    { name: 'PostgreSQL Database', score: 99.4, errorRate: '0.00%', latency: '18ms', saturation: '22%', status: 'HEALTHY' },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Heart className="w-5 h-5 text-rose-400" />
            Subsystem Health Intelligence & Dependency Topology
          </h2>
          <p className="text-sm text-slate-400">
            Weighted composite health metrics, dynamic dependency propagation, and EMA degradation trend analysis for node: <code className="text-rose-300 font-mono text-xs">{missionId}</code>
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="intelligence" size="md">
            Composite Score: 98.9 / 100
          </Badge>
          <button className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700">
            <RefreshCw className="w-3.5 h-3.5" />
            Recalculate Health
          </button>
        </div>
      </div>

      {/* Subsystem Health Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono">
        {subsystems.map((sub, idx) => (
          <Card key={idx} className="p-4 bg-slate-900 border-slate-800 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Activity className="w-4 h-4 text-emerald-400" />
                <span className="text-sm font-bold text-slate-200">{sub.name}</span>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="success" size="sm">{sub.status}</Badge>
                <span className="text-sm font-bold text-emerald-400">{sub.score}%</span>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-2 pt-2 border-t border-slate-800 text-[11px] text-slate-400">
              <div>
                <span className="block text-[10px] text-slate-500">Error Rate:</span>
                <span className="text-emerald-400 font-bold">{sub.errorRate}</span>
              </div>
              <div>
                <span className="block text-[10px] text-slate-500">Latency P95:</span>
                <span className="text-amber-400 font-bold">{sub.latency}</span>
              </div>
              <div>
                <span className="block text-[10px] text-slate-500">Saturation:</span>
                <span className="text-cyan-400 font-bold">{sub.saturation}</span>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Health Trend & Dependency Propagation Graph */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-5 bg-slate-900 border-slate-800 space-y-3 font-mono">
          <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-emerald-400" />
            EMA Health Trajectory & Drift Analyzer
          </h3>
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-400">Exponential Moving Average (EMA):</span>
              <span className="text-emerald-400 font-bold">98.85 / 100</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Trend Slope (10m):</span>
              <span className="text-cyan-400 font-bold">+0.0024 / min (Improving)</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Structural Drift:</span>
              <span className="text-emerald-400 font-bold">NONE_DETECTED</span>
            </div>
          </div>
        </Card>

        <Card className="p-5 bg-slate-900 border-slate-800 space-y-3 font-mono">
          <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
            <GitFork className="w-4 h-4 text-purple-400" />
            Dependency Degradation Propagation Matrix
          </h3>
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-400">Database Impairment Impact:</span>
              <span className="text-slate-200">Database → Truth → Replay</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Worker Impairment Impact:</span>
              <span className="text-slate-200">Worker → Planner → Mission</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Isolation Bounding Factor:</span>
              <span className="text-emerald-400 font-bold flex items-center gap-1">
                <Sparkles className="w-3 h-3" /> DAMPED_CASCADE_ENABLED
              </span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
