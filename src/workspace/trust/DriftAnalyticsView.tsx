import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const DriftAnalyticsView: React.FC = () => {
  const metrics = [
    {
      name: 'Execution Latency (ms)',
      baseline: '930.0 ms',
      current: '928.0 ms',
      shift: '-0.21%',
      pValue: 'p = 0.45',
      alert: 'NORMAL',
    },
    {
      name: 'Cost ($/mission)',
      baseline: '$0.0083',
      current: '$0.0084',
      shift: '+1.20%',
      pValue: 'p = 0.38',
      alert: 'NORMAL',
    },
    {
      name: 'Confidence Score',
      baseline: '97.8%',
      current: '98.1%',
      shift: '+0.31%',
      pValue: 'p = 0.52',
      alert: 'NORMAL',
    },
    {
      name: 'Downstream Retry Frequency',
      baseline: '0.050 / msn',
      current: '0.048 / msn',
      shift: '-4.00%',
      pValue: 'p = 0.60',
      alert: 'NORMAL',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Runtime Drift Analytics</h1>
            <Badge variant="intelligence" size="sm">Pillar 9</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Continuous online statistical comparison between 30-day baseline distributions and 24-hour active runtime telemetry.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            System Status: HEALTHY_STABLE
          </Badge>
        </div>
      </div>

      {/* Overview Status Card */}
      <Card className="p-4 bg-emerald-950/20 border-emerald-500/30 text-xs text-emerald-300">
        <strong>Monitoring Summary:</strong> All operational metrics remain within &plusmn;2% statistical tolerance of baseline. Zero regression drift detected across active pipelines.
      </Card>

      {/* Metrics Table */}
      <Card className="p-0 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-border/40 bg-muted/20 font-semibold text-muted-foreground">
                <th className="p-3">Tracked Metric</th>
                <th className="p-3">30-Day Baseline (N=1420)</th>
                <th className="p-3">Active 24h Window (N=120)</th>
                <th className="p-3">Distribution Shift</th>
                <th className="p-3">Significance (p-value)</th>
                <th className="p-3">Drift Alert Level</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/20">
              {metrics.map((m, idx) => (
                <tr key={idx} className="hover:bg-muted/10 transition-colors">
                  <td className="p-3 font-semibold text-foreground">{m.name}</td>
                  <td className="p-3 font-mono text-muted-foreground">{m.baseline}</td>
                  <td className="p-3 font-mono font-bold text-foreground">{m.current}</td>
                  <td className="p-3 font-mono text-emerald-400">{m.shift}</td>
                  <td className="p-3 font-mono text-muted-foreground">{m.pValue}</td>
                  <td className="p-3">
                    <Badge variant={m.alert === 'NORMAL' ? 'success' : 'warning'} size="sm">
                      {m.alert}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
