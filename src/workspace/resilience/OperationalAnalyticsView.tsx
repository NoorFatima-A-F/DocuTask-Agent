import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const OperationalAnalyticsView: React.FC = () => {

  const metrics = [
    { label: '30-Day Mean Time Between Failures', value: '720 Hours', change: '+14% vs last mo', status: 'optimal' },
    { label: '30-Day Mean Time To Recovery', value: '45.2 ms', change: '-32% faster', status: 'optimal' },
    { label: 'SLA Budget Adherence Rate', value: '99.98%', change: '+0.04%', status: 'optimal' },
    { label: 'Cumulative Self-Healing Savings', value: '$4,120 USD', change: '85 eng hours saved', status: 'optimal' },
  ];

  const operationalLogs = [
    { timestamp: '2026-09-10 14:20:00', event: 'Gemini 504 Failover', mttr: '45.0 ms', deltaCost: '-$0.0015', result: 'Zero Parity Loss' },
    { timestamp: '2026-09-09 18:12:30', event: 'Redis Circuit Breaker Fallback', mttr: '8.5 ms', deltaCost: '$0.0000', result: 'Zero Read Drop' },
    { timestamp: '2026-09-08 09:45:12', event: 'OCR Worker Sandbox Respawn', mttr: '180.0 ms', deltaCost: '+$0.0001', result: 'Task Resumed' },
    { timestamp: '2026-09-07 22:04:18', event: 'Memory Checkpoint Warm Reload', mttr: '95.0 ms', deltaCost: '$0.0000', result: 'State Restored' },
    { timestamp: '2026-09-06 11:30:44', event: 'DAG Deadlock Branch Prune', mttr: '140.0 ms', deltaCost: '+$0.0003', result: 'Graph Re-synthesized' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Operational Reliability Analytics</h1>
            <Badge variant="intelligence" size="sm">Long-Term Telemetry</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Historical reliability trends, MTBF expansion curves, autonomous failover efficiencies, and operational cost savings.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            Operational Uptime: 99.9988%
          </Badge>
        </div>
      </div>

      {/* Top Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        {metrics.map((m, idx) => (
          <Card key={idx} className="p-4 border-border/60 space-y-1">
            <div className="text-xs font-semibold text-muted-foreground">{m.label}</div>
            <div className="text-2xl font-bold font-mono text-foreground mt-1">{m.value}</div>
            <div className="text-[11px] text-emerald-400 font-semibold mt-1">{m.change}</div>
          </Card>
        ))}
      </div>

      {/* Historical Self-Healing Events Table */}
      <div className="space-y-3">
        <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Autonomous Self-Healing Event Telemetry</h2>
        <div className="border border-border/40 rounded-lg overflow-hidden">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-muted/40 text-muted-foreground border-b border-border/40">
              <tr>
                <th className="p-2.5 font-medium font-sans">Timestamp (UTC)</th>
                <th className="p-2.5 font-medium font-sans">Trigger Event</th>
                <th className="p-2.5 font-medium text-right font-sans">Recovery MTTR</th>
                <th className="p-2.5 font-medium text-right font-sans">Cost Delta</th>
                <th className="p-2.5 font-medium text-center font-sans">Outcome</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/20">
              {operationalLogs.map((log, idx) => (
                <tr key={idx} className="hover:bg-muted/20">
                  <td className="p-2.5 text-muted-foreground">{log.timestamp}</td>
                  <td className="p-2.5 text-foreground font-sans font-semibold">{log.event}</td>
                  <td className="p-2.5 text-right text-blue-400 font-bold">{log.mttr}</td>
                  <td className="p-2.5 text-right text-emerald-400">{log.deltaCost}</td>
                  <td className="p-2.5 text-center font-sans">
                    <Badge variant="success" size="sm">{log.result}</Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
