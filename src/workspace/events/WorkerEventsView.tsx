import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const WorkerEventsView: React.FC = () => {
  const workers = [
    { id: 'worker-ocr-01', status: 'IDLE', activeTasks: 0, completedTasks: 18, cpu: 14.5, mem: 256, durationMs: 4200, tokens: 12500 },
    { id: 'worker-ocr-02', status: 'BUSY', activeTasks: 1, completedTasks: 14, cpu: 32.0, mem: 512, durationMs: 3800, tokens: 9800 },
    { id: 'worker-extract-01', status: 'IDLE', activeTasks: 0, completedTasks: 22, cpu: 18.2, mem: 384, durationMs: 5100, tokens: 18400 },
    { id: 'worker-validate-01', status: 'IDLE', activeTasks: 0, completedTasks: 20, cpu: 8.5, mem: 128, durationMs: 1200, tokens: 4200 },
  ];

  const workerEvents = [
    { id: 'evt-wk-001', time: '14:20:01.100', type: 'TaskAssigned', workerId: 'worker-ocr-01', task: 'OCR_CHUNK_1', details: 'Assigned page 1-2 raster chunk extraction.' },
    { id: 'evt-wk-002', time: '14:20:01.420', type: 'TaskCompleted', workerId: 'worker-ocr-01', task: 'OCR_CHUNK_1', details: 'Completed in 320ms. Extracted 4,520 chars with 0.994 confidence.' },
    { id: 'evt-wk-003', time: '14:20:01.450', type: 'WorkerHeartbeat', workerId: 'worker-ocr-02', task: 'HEARTBEAT', details: 'CPU: 32.0%, RAM: 512MB, Active: 1 task.' },
    { id: 'evt-wk-004', time: '14:20:01.600', type: 'TaskAssigned', workerId: 'worker-extract-01', task: 'EXTRACT_ENTITIES', details: 'Assigned table & schema boundary extraction.' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Worker Pool Domain Events & Projections</h1>
            <Badge variant="intelligence" size="sm">Read Model</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Real-time projection of worker pool allocations, task queues, resource heartbeats, and token metrics.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            4/4 Workers Operational
          </Badge>
        </div>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <Card className="p-4 bg-emerald-950/10 border-emerald-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Active Worker Replicas</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">4 Workers</div>
          <div className="text-[11px] text-muted-foreground mt-1">1 Busy, 3 Idle</div>
        </Card>
        <Card className="p-4 bg-blue-950/10 border-blue-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Total Tasks Completed</div>
          <div className="text-2xl font-bold font-mono text-blue-400 mt-1">74 Tasks</div>
          <div className="text-[11px] text-muted-foreground mt-1">100% Zero worker panics</div>
        </Card>
        <Card className="p-4 bg-purple-950/10 border-purple-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Cumulative Tokens</div>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-1">44,900 Tokens</div>
          <div className="text-[11px] text-muted-foreground mt-1">Processed across pool</div>
        </Card>
        <Card className="p-4 bg-cyan-950/10 border-cyan-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Avg Task Duration</div>
          <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">193 ms</div>
          <div className="text-[11px] text-muted-foreground mt-1">Sub-second throughput</div>
        </Card>
      </div>

      {/* Workers Grid */}
      <div className="space-y-3">
        <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Worker Nodes Allocation</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {workers.map(w => (
            <Card key={w.id} className="p-4 border-border/60 space-y-3">
              <div className="flex items-start justify-between">
                <div>
                  <div className="text-sm font-bold text-foreground">{w.id}</div>
                  <div className="text-[10px] text-muted-foreground font-mono mt-0.5">Tasks Completed: {w.completedTasks}</div>
                </div>
                <Badge variant={w.status === 'BUSY' ? 'warning' : 'success'} size="sm">
                  {w.status}
                </Badge>
              </div>

              <div className="grid grid-cols-3 gap-2 pt-2 border-t border-border/40 font-mono text-xs text-center">
                <div>
                  <div className="text-[10px] text-muted-foreground">CPU</div>
                  <div className="font-semibold text-foreground mt-0.5">{w.cpu}%</div>
                </div>
                <div>
                  <div className="text-[10px] text-muted-foreground">RAM</div>
                  <div className="font-semibold text-foreground mt-0.5">{w.mem} MB</div>
                </div>
                <div>
                  <div className="text-[10px] text-muted-foreground">Tokens</div>
                  <div className="font-semibold text-primary mt-0.5">{w.tokens}</div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* Worker Event Log */}
      <div className="space-y-3">
        <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Recent Worker Domain Events</h2>
        <div className="border border-border/40 rounded-lg overflow-hidden">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-muted/40 text-muted-foreground border-b border-border/40">
              <tr>
                <th className="p-2.5 font-medium font-sans">Timestamp</th>
                <th className="p-2.5 font-medium font-sans">Event Type</th>
                <th className="p-2.5 font-medium font-sans">Worker ID</th>
                <th className="p-2.5 font-medium font-sans">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/20">
              {workerEvents.map(ev => (
                <tr key={ev.id} className="hover:bg-muted/20">
                  <td className="p-2.5 text-muted-foreground">{ev.time}</td>
                  <td className="p-2.5 text-primary font-bold">{ev.type}</td>
                  <td className="p-2.5 text-foreground">{ev.workerId}</td>
                  <td className="p-2.5 text-muted-foreground font-sans">{ev.details}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
