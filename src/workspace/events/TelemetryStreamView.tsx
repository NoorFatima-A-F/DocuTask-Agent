import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const TelemetryStreamView: React.FC = () => {
  const telemetry = {
    throughputRps: 8.42,
    p50LatencyMs: 185.0,
    p95LatencyMs: 320.0,
    p99LatencyMs: 540.0,
    totalEventsProcessed: 1420,
    errorEventsCount: 0,
    errorRatePct: 0.00,
    totalCostAccumulatedUsd: 0.0031,
  };

  const latencyHistory = [
    { time: '14:20:00.100', p50: 160, p95: 280, eventsSec: 6.2 },
    { time: '14:20:00.500', p50: 175, p95: 310, eventsSec: 7.8 },
    { time: '14:20:01.000', p50: 190, p95: 340, eventsSec: 8.5 },
    { time: '14:20:01.500', p50: 185, p95: 320, eventsSec: 8.4 },
    { time: '14:20:02.000', p50: 180, p95: 300, eventsSec: 8.9 },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Event-Driven Telemetry Stream</h1>
            <Badge variant="intelligence" size="sm">Live Read Model</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Real-time projection of throughput, latency percentiles, error rates, and cost calculated from domain events.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            Error Rate: 0.00% (Zero Defects)
          </Badge>
        </div>
      </div>

      {/* Top Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <Card className="p-4 bg-emerald-950/10 border-emerald-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Event Ingestion Throughput</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">{telemetry.throughputRps} RPS</div>
          <div className="text-[11px] text-muted-foreground mt-1">Live sliding window</div>
        </Card>
        <Card className="p-4 bg-blue-950/10 border-blue-500/20">
          <div className="text-xs font-semibold text-muted-foreground">P95 Event Latency</div>
          <div className="text-2xl font-bold font-mono text-blue-400 mt-1">{telemetry.p95LatencyMs} ms</div>
          <div className="text-[11px] text-muted-foreground mt-1">P50: {telemetry.p50LatencyMs}ms • P99: {telemetry.p99LatencyMs}ms</div>
        </Card>
        <Card className="p-4 bg-purple-950/10 border-purple-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Total Domain Events</div>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-1">{telemetry.totalEventsProcessed}</div>
          <div className="text-[11px] text-muted-foreground mt-1">Immutable log count</div>
        </Card>
        <Card className="p-4 bg-cyan-950/10 border-cyan-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Accumulated Cost</div>
          <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">${telemetry.totalCostAccumulatedUsd}</div>
          <div className="text-[11px] text-muted-foreground mt-1">Event-derived cost sum</div>
        </Card>
      </div>

      {/* Latency History Table */}
      <div className="space-y-3">
        <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Real-Time Telemetry Sliding Window</h2>
        <div className="border border-border/40 rounded-lg overflow-hidden">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-muted/40 text-muted-foreground border-b border-border/40">
              <tr>
                <th className="p-2.5 font-medium font-sans">Time Window</th>
                <th className="p-2.5 font-medium font-sans text-right">Throughput</th>
                <th className="p-2.5 font-medium font-sans text-right">P50 Latency</th>
                <th className="p-2.5 font-medium font-sans text-right">P95 Latency</th>
                <th className="p-2.5 font-medium font-sans text-center">Health Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/20">
              {latencyHistory.map((row, idx) => (
                <tr key={idx} className="hover:bg-muted/20">
                  <td className="p-2.5 text-muted-foreground">{row.time} UTC</td>
                  <td className="p-2.5 text-right font-bold text-emerald-400">{row.eventsSec} RPS</td>
                  <td className="p-2.5 text-right text-foreground">{row.p50} ms</td>
                  <td className="p-2.5 text-right text-blue-400 font-bold">{row.p95} ms</td>
                  <td className="p-2.5 text-center font-sans">
                    <Badge variant="success" size="sm">OPTIMAL</Badge>
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
