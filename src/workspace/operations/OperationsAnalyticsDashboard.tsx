import React, { useState } from 'react';
import {
  BarChart3,
  TrendingUp,
  RefreshCw,
  Zap,
  Activity,
  Award,
  Layers
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

interface OperationsAnalyticsDashboardProps {
  missionId?: string;
}

export const OperationsAnalyticsDashboard: React.FC<OperationsAnalyticsDashboardProps> = ({
  missionId = 'cluster-primary-master',
}) => {
  const [analytics] = useState({
    totalHealedIncidents: 142,
    avgHealingDurationMs: 110.5,
    savedDowntimeSec: 1840.0,
    costSavingsUsd: 1420.50,
    uptime30DayPct: 99.99,
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-purple-400" />
            Operations Analytics & Executive SRE Performance Dashboard
          </h2>
          <p className="text-sm text-slate-400">
            Historical recovery analytics, financial downtime savings, capacity trends, and executive SRE KPIs for: <code className="text-purple-300 font-mono text-xs">{missionId}</code>
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="intelligence" size="md">
            SRE Report: 100% OPERATIONAL
          </Badge>
          <button className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700">
            <RefreshCw className="w-3.5 h-3.5" />
            Export SRE Report
          </button>
        </div>
      </div>

      {/* Primary KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 font-mono">
        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400">Autonomic Remediations</span>
            <Zap className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-emerald-400">
            {analytics.totalHealedIncidents}
          </div>
          <span className="text-[10px] text-slate-400 mt-2 block">Zero human intervention</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400">Avg Self-Healing Time</span>
            <Activity className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-amber-400">
            {analytics.avgHealingDurationMs} ms
          </div>
          <span className="text-[10px] text-emerald-400 mt-2 block">Sub-200ms target met</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400">Prevented Downtime</span>
            <TrendingUp className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold text-cyan-400">
            {analytics.savedDowntimeSec} s
          </div>
          <span className="text-[10px] text-slate-400 mt-2 block">99.99% Availability Preserved</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400">Downtime Loss Avoided</span>
            <Award className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold text-purple-400">
            ${analytics.costSavingsUsd.toFixed(2)}
          </div>
          <span className="text-[10px] text-slate-400 mt-2 block">SLA penalty risk mitigated</span>
        </Card>
      </div>

      {/* SRE Operational Breakdown */}
      <Card className="p-5 bg-slate-900 border-slate-800 space-y-4 font-mono">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <Layers className="w-4 h-4 text-indigo-400" />
          Autonomic Operations Performance Decomposition
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div className="p-3.5 bg-slate-950 rounded-lg border border-slate-800 space-y-2">
            <span className="text-slate-400 block">Worker Fault Restarts</span>
            <span className="text-lg font-bold text-slate-200">88 Actions (100% Success)</span>
            <p className="text-[11px] text-slate-500">Average MTTR: 120ms</p>
          </div>

          <div className="p-3.5 bg-slate-950 rounded-lg border border-slate-800 space-y-2">
            <span className="text-slate-400 block">Fallback Model Engagements</span>
            <span className="text-lg font-bold text-cyan-400">32 Actions (100% Success)</span>
            <p className="text-[11px] text-slate-500">Average MTTR: 75ms</p>
          </div>

          <div className="p-3.5 bg-slate-950 rounded-lg border border-slate-800 space-y-2">
            <span className="text-slate-400 block">Memory Cache Repairs</span>
            <span className="text-lg font-bold text-purple-400">22 Actions (100% Success)</span>
            <p className="text-[11px] text-slate-500">Average MTTR: 65ms</p>
          </div>
        </div>
      </Card>
    </div>
  );
};
