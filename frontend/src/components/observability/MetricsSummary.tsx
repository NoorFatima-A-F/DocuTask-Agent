import React, { useState, useEffect } from 'react';
import {
  Users,
  FileCheck,
  Clock,
  ShieldCheck,
  Activity,
  BarChart3,
  Sparkles,
} from 'lucide-react';
import { jobsApi } from '../../api/jobs';
import { RuntimeObservabilityKPIs } from '../../types/job';
import { ConfidenceGauge } from './ConfidenceGauge';
import { DLQTable } from './DLQTable';

export const MetricsSummary: React.FC = () => {
  const [metrics, setMetrics] = useState<RuntimeObservabilityKPIs>({
    active_workers: 4,
    total_ingested_documents: 1284,
    average_pipeline_latency_ms: 412,
    mean_confidence_score: 0.942,
    queue_depth: 2,
    dlq_count: 0,
    system_health_score: 0.998,
  });

  useEffect(() => {
    const loadMetrics = async () => {
      const data = await jobsApi.getDashboardMetrics();
      setMetrics(data);
    };
    loadMetrics();
    const interval = setInterval(loadMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  const kpis = [
    {
      title: 'Active Celery Workers',
      value: `${metrics.active_workers} Pools`,
      sub: 'Concurrency: 1 per container',
      icon: Users,
      color: 'text-indigo-400 bg-indigo-500/10 border-indigo-500/30',
    },
    {
      title: 'Total Ingested Documents',
      value: metrics.total_ingested_documents.toLocaleString(),
      sub: 'SHA-256 deduplicated',
      icon: FileCheck,
      color: 'text-cyan-400 bg-cyan-500/10 border-cyan-500/30',
    },
    {
      title: 'Avg Pipeline Latency (p95)',
      value: `${metrics.average_pipeline_latency_ms}ms`,
      sub: 'SLA target: <1000ms',
      icon: Clock,
      color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30',
    },
    {
      title: 'Mean Confidence Score',
      value: `${(metrics.mean_confidence_score * 100).toFixed(1)}%`,
      sub: 'Bayesian evidence fusion',
      icon: ShieldCheck,
      color: 'text-amber-400 bg-amber-500/10 border-amber-500/30',
    },
  ];

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-indigo-400" />
            Operational Observability & Health Center
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Real-time telemetry, worker concurrency, Bayesian evidence fusion, and Dead Letter Queue management.
          </p>
        </div>

        <div className="flex items-center gap-2 font-mono text-[11px]">
          <span className="px-2.5 py-1 rounded-md bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center gap-1.5 font-semibold">
            <Activity className="w-3.5 h-3.5" />
            System Health: {(metrics.system_health_score * 100).toFixed(1)}%
          </span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map((kpi) => {
          const Icon = kpi.icon;
          return (
            <div
              key={kpi.title}
              className="p-4 rounded-xl border border-slate-800 bg-slate-900/40 space-y-2 hover:border-slate-700 transition-colors"
            >
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-mono text-slate-400 uppercase">
                  {kpi.title}
                </span>
                <div className={`p-1.5 rounded-lg border ${kpi.color}`}>
                  <Icon className="w-3.5 h-3.5" />
                </div>
              </div>
              <div className="text-xl font-bold font-mono text-slate-100">
                {kpi.value}
              </div>
              <div className="text-[10px] font-mono text-slate-400">
                {kpi.sub}
              </div>
            </div>
          );
        })}
      </div>

      {/* Bayesian Evidence Fusion Breakdown */}
      <ConfidenceGauge score={metrics.mean_confidence_score} />

      {/* Dead Letter Queue (DLQ) Table */}
      <DLQTable />
    </div>
  );
};
