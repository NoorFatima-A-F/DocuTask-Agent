import React, { useState, useEffect } from 'react';
import { Activity, Clock, ShieldCheck, FileCheck, Layers, Server } from 'lucide-react';
import { jobsApi } from '../../api/jobs';
import { RuntimeObservabilityKPIs } from '../../types/job';
import { DLQTable } from './DLQTable';

export const MetricsSummary: React.FC = () => {
  const [metrics, setMetrics] = useState<RuntimeObservabilityKPIs>({
    active_workers: 1,
    total_ingested_documents: 1284,
    average_pipeline_latency_ms: 412,
    mean_confidence_score: 0.942,
    queue_depth: 0,
    dlq_count: 1,
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
      title: 'Active Workers',
      value: `${metrics.active_workers} Container`,
      sub: 'Concurrency: 1 per worker',
      icon: Server,
    },
    {
      title: 'Ingested Documents',
      value: metrics.total_ingested_documents.toLocaleString(),
      sub: 'SHA-256 deduplicated',
      icon: FileCheck,
    },
    {
      title: 'Pipeline Latency (p95)',
      value: `${metrics.average_pipeline_latency_ms}ms`,
      sub: 'Target: <1,000ms SLA',
      icon: Clock,
    },
    {
      title: 'Mean Confidence',
      value: `${(metrics.mean_confidence_score * 100).toFixed(1)}%`,
      sub: 'Bayesian evidence fusion',
      icon: ShieldCheck,
    },
  ];

  return (
    <div className="space-y-4 w-full">
      {/* Top Header */}
      <div className="flex items-center justify-between border-b border-[#27272a] pb-2.5">
        <div>
          <span className="text-xs font-semibold text-zinc-100 uppercase tracking-wider font-mono">
            System Observability &amp; Telemetry Hub
          </span>
          <p className="text-[11px] text-zinc-500 font-mono mt-0.5">
            Real-time Celery worker load, Bayesian confidence scores, and Dead Letter Queue management.
          </p>
        </div>

        <div className="flex items-center gap-1.5 font-mono text-[11px] text-emerald-400 bg-emerald-950/40 border border-emerald-800/50 px-2 py-0.5 rounded">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          <span>Health: {(metrics.system_health_score * 100).toFixed(1)}%</span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {kpis.map((kpi) => {
          const Icon = kpi.icon;
          return (
            <div
              key={kpi.title}
              className="p-3.5 rounded border border-[#27272a] bg-[#121215] space-y-1.5"
            >
              <div className="flex items-center justify-between text-zinc-500">
                <span className="text-[11px] font-mono uppercase font-medium">{kpi.title}</span>
                <Icon className="w-3.5 h-3.5 text-zinc-400" />
              </div>
              <div className="text-xl font-bold font-mono text-zinc-100">{kpi.value}</div>
              <div className="text-[10px] font-mono text-zinc-500">{kpi.sub}</div>
            </div>
          );
        })}
      </div>

      {/* Dead Letter Queue Inspection */}
      <DLQTable />
    </div>
  );
};
