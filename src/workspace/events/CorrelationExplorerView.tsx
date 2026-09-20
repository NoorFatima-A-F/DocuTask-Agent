import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { CornerDownRight } from 'lucide-react';

export const CorrelationExplorerView: React.FC = () => {
  const correlationId = 'corr-mission-fin-001';

  const traceSteps = [
    { id: 'evt-001', type: 'MissionCreated', actor: 'Operator', time: '14:20:00.120', causationId: 'cause-root', latency: '0ms', depth: 0 },
    { id: 'evt-002', type: 'PlannerStarted', actor: 'ChiefPlanner', time: '14:20:00.350', causationId: 'cause-evt-001', latency: '230ms', depth: 1 },
    { id: 'evt-003', type: 'PlannerFinished', actor: 'ChiefPlanner', time: '14:20:00.890', causationId: 'cause-evt-002', latency: '540ms', depth: 2 },
    { id: 'evt-004', type: 'TaskAssigned', actor: 'DAGScheduler', time: '14:20:01.100', causationId: 'cause-evt-003', latency: '210ms', depth: 3 },
    { id: 'evt-005', type: 'OCRCompleted', actor: 'worker-ocr-01', time: '14:20:01.420', causationId: 'cause-evt-004', latency: '320ms', depth: 4 },
    { id: 'evt-006', type: 'ValidationPassed', actor: 'ScientificValidator', time: '14:20:01.750', causationId: 'cause-evt-005', latency: '330ms', depth: 5 },
    { id: 'evt-007', type: 'MissionCompleted', actor: 'MissionCommander', time: '14:20:02.100', causationId: 'cause-evt-006', latency: '350ms', depth: 6 },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Correlation & Distributed Trace Explorer</h1>
            <Badge variant="intelligence" size="sm">Causation DAG</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Visualizes distributed parent-child causation trees and end-to-end execution lineages.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            Trace Verified: 7 Nodes Linked
          </Badge>
        </div>
      </div>

      {/* Trace Card */}
      <Card className="p-5 border-border/60 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border/40 pb-3">
          <div>
            <div className="text-xs font-semibold text-muted-foreground uppercase">Correlation Identifier</div>
            <div className="text-sm font-mono font-bold text-primary mt-0.5">{correlationId}</div>
          </div>
          <div className="text-right">
            <div className="text-xs text-muted-foreground">Total Span Duration</div>
            <div className="text-sm font-mono font-bold text-emerald-400">1.98 seconds</div>
          </div>
        </div>

        {/* Tree Hierarchy */}
        <div className="space-y-2 pt-2">
          {traceSteps.map((step, idx) => (
            <div
              key={step.id}
              className="flex items-center gap-3 p-3 rounded-lg bg-muted/40 border border-border/30 font-mono text-xs"
              style={{ marginLeft: `${step.depth * 14}px` }}
            >
              <CornerDownRight className="w-4 h-4 text-muted-foreground shrink-0" />
              <Badge variant="intelligence" size="sm">Step {idx + 1}</Badge>
              <span className="font-bold text-foreground">{step.type}</span>
              <span className="text-muted-foreground">•</span>
              <span className="text-muted-foreground text-[11px]">{step.actor}</span>
              <span className="text-muted-foreground">•</span>
              <span className="text-primary text-[11px]">+{step.latency}</span>
              <span className="ml-auto text-[10px] text-muted-foreground">{step.id}</span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
