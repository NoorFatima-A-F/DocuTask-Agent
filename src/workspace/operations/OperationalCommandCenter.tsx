import React, { useState } from 'react';
import {
  Activity,
  Heart,
  AlertTriangle,
  RefreshCw,
  Zap,
  Server,
  TrendingUp,
  Sliders
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

interface OperationalCommandCenterProps {
  missionId?: string;
}

export const OperationalCommandCenter: React.FC<OperationalCommandCenterProps> = ({
  missionId = 'cluster-primary-master',
}) => {
  const [healthScore] = useState(98.5);
  const [availability] = useState(99.99);
  const [activeIncidents] = useState(0);
  const [activeWorkers] = useState(14);
  const [p95Latency] = useState(380);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            Operational Command Center (AOIS-HROP)
          </h2>
          <p className="text-sm text-slate-400">
            Autonomous live operations, autonomic self-healing supervisor, and cluster resilience for node: <code className="text-emerald-300 font-mono text-xs">{missionId}</code>
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" size="md">
            AUTONOMIC ENGINE: ACTIVE
          </Badge>
          <button className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700">
            <RefreshCw className="w-3.5 h-3.5" />
            Poll Runtime Pulse
          </button>
        </div>
      </div>

      {/* Primary KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 font-mono">
        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400">Composite Health</span>
            <Heart className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-2xl font-bold text-emerald-400">
            {healthScore}%
          </div>
          <div className="mt-2 w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div className="bg-emerald-500 h-full rounded-full" style={{ width: `${healthScore}%` }} />
          </div>
          <span className="text-[10px] text-slate-400 mt-1 block">All 10 subsystems healthy</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400">System Availability</span>
            <Server className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold text-cyan-400">
            {availability}%
          </div>
          <p className="text-[11px] text-slate-400 mt-2">30-day window • 0 outages</p>
          <span className="text-[10px] text-emerald-400 mt-1 block">Four-Nines SLA Met</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400">Active Incidents</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-slate-100">
            {activeIncidents}
          </div>
          <p className="text-[11px] text-slate-400 mt-2">12 resolved automatically</p>
          <span className="text-[10px] text-indigo-400 mt-1 block">Self-Healing Success: 100%</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400">P95 Cluster Latency</span>
            <TrendingUp className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold text-purple-400">
            {p95Latency} ms
          </div>
          <p className="text-[11px] text-slate-400 mt-2">Workers: {activeWorkers} active</p>
          <span className="text-[10px] text-slate-500 mt-1 block">Queue Backlog: 0</span>
        </Card>
      </div>

      {/* Subsystem Heartbeat & Operational Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card className="p-5 bg-slate-900 border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
                <Zap className="w-4 h-4 text-amber-400" />
                Live Subsystem Supervision Matrix
              </h3>
              <Badge variant="intelligence" size="sm">Supervised Threads: 18</Badge>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs font-mono">
              {[
                { name: 'Planner (APDLE)', score: 99.2, status: 'HEALTHY' },
                { name: 'Worker Cluster', score: 98.0, status: 'HEALTHY' },
                { name: 'Memory Vectors', score: 99.5, status: 'HEALTHY' },
                { name: 'Optimization (ARIA)', score: 97.8, status: 'HEALTHY' },
                { name: 'Truth Ledger (VAIRT)', score: 100.0, status: 'HEALTHY' },
                { name: 'Replay Engine (ESMR)', score: 99.0, status: 'HEALTHY' },
              ].map((sub, idx) => (
                <div key={idx} className="p-3 rounded-lg bg-slate-950 border border-slate-800 space-y-1">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-300 font-bold">{sub.name}</span>
                    <Badge variant="success" size="sm">{sub.status}</Badge>
                  </div>
                  <div className="text-right text-emerald-400 font-bold text-sm">
                    {sub.score}%
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        <div>
          <Card className="p-5 bg-slate-900 border-slate-800 space-y-4">
            <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <Sliders className="w-4 h-4 text-indigo-400" />
              Autonomic Remediation Controller
            </h3>

            <div className="space-y-2.5 text-xs text-slate-300">
              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 flex justify-between items-center">
                <span>Auto-Restart Hung Workers:</span>
                <span className="text-emerald-400 font-bold font-mono">ENABLED</span>
              </div>
              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 flex justify-between items-center">
                <span>Checkpoint Rollback Guard:</span>
                <span className="text-emerald-400 font-bold font-mono">ZERO_DATA_LOSS</span>
              </div>
              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 flex justify-between items-center">
                <span>SLA Latency Breaker:</span>
                <span className="text-indigo-400 font-bold font-mono">ADAPTIVE_FALLBACK</span>
              </div>
            </div>

            <button className="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold transition-all shadow-lg shadow-emerald-600/20">
              Trigger Cluster Self-Test Probe
            </button>
          </Card>
        </div>
      </div>
    </div>
  );
};
