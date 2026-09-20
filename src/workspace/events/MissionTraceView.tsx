import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const MissionTraceView: React.FC = () => {
  const spans = [
    { name: 'Mission Lifecycle (Root)', startMs: 0, durationMs: 1980, color: 'bg-emerald-500' },
    { name: 'Dynamic DAG Planning', startMs: 230, durationMs: 540, color: 'bg-blue-500' },
    { name: 'Task Queue & Worker Dispatch', startMs: 800, durationMs: 210, color: 'bg-purple-500' },
    { name: 'OCR Parallel Ingestion (Worker 1)', startMs: 1020, durationMs: 320, color: 'bg-amber-500' },
    { name: 'Scientific Invariant Validation', startMs: 1350, durationMs: 330, color: 'bg-cyan-500' },
    { name: 'Proof Commit & Finalization', startMs: 1690, durationMs: 290, color: 'bg-indigo-500' },
  ];

  const totalDuration = 1980;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Mission Distributed Flame Trace</h1>
            <Badge variant="intelligence" size="sm">Span Waterfall</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Deep waterfall trace breakdown of event latencies, child spans, and critical execution paths.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            Total Duration: 1.98s
          </Badge>
        </div>
      </div>

      {/* Waterfall Spans */}
      <Card className="p-6 border-border/60 space-y-4">
        <div className="flex justify-between items-center text-xs font-semibold text-muted-foreground uppercase">
          <span>Execution Spans</span>
          <span>Timeline (0ms - 1980ms)</span>
        </div>

        <div className="space-y-3 pt-2">
          {spans.map((s, idx) => {
            const leftPct = (s.startMs / totalDuration) * 100;
            const widthPct = Math.max(5, (s.durationMs / totalDuration) * 100);

            return (
              <div key={idx} className="space-y-1">
                <div className="flex justify-between text-xs">
                  <span className="font-semibold text-foreground">{s.name}</span>
                  <span className="font-mono text-muted-foreground">{s.durationMs} ms (+{s.startMs}ms)</span>
                </div>
                <div className="w-full bg-muted/40 h-4 rounded overflow-hidden relative border border-border/30">
                  <div
                    className={`${s.color} h-full rounded opacity-90 transition-all`}
                    style={{ marginLeft: `${leftPct}%`, width: `${widthPct}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
};
