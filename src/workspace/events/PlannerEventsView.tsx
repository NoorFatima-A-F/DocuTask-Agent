import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { BrainCircuit, Clock } from 'lucide-react';

export const PlannerEventsView: React.FC = () => {
  const plannerState = {
    state: 'EXECUTION_READY',
    activeMissionId: 'mission-fin-001',
    totalPlansGenerated: 42,
    totalReplansExecuted: 3,
    currentGoal: 'Process and validate 2026 Q3 vendor audit invoices',
    generatedTasksCount: 6,
    estimatedCostUsd: 0.0032,
    criticalPathMs: 185.4,
  };

  const plannerEvents = [
    {
      id: 'evt-pl-001',
      time: '14:20:00.350',
      type: 'PlannerStarted',
      goal: 'Process and validate 2026 Q3 vendor audit invoices',
      strategy: 'DYNAMIC_DAG_SYNTHESIS',
      actor: 'ChiefPlanner',
      details: 'Evaluated 4 sub-goal decomposition heuristics. Selected optimal DAG topology.',
    },
    {
      id: 'evt-pl-002',
      time: '14:20:00.520',
      type: 'PlannerHeuristicEvaluated',
      goal: 'Invoice Ingestion Sub-Graph',
      strategy: 'PARETO_UTILITY_MAXIMIZATION',
      actor: 'ChiefPlanner',
      details: 'Utility score U=0.985 for Gemini 1.5 Flash parallel routing.',
    },
    {
      id: 'evt-pl-003',
      time: '14:20:00.890',
      type: 'PlannerFinished',
      goal: 'DAG Synthesis Complete',
      strategy: 'DAG_COMPOSED',
      actor: 'ChiefPlanner',
      details: 'Synthesized 6 DAG execution nodes with critical path of 185.4ms.',
    },
    {
      id: 'evt-pl-004',
      time: '14:20:01.300',
      type: 'PlannerReplanned',
      goal: 'OCR Chunk 2 Worker Timeout',
      strategy: 'BRANCH_MUTATION_AND_REROUTE',
      actor: 'ChiefPlanner',
      details: 'Pruned stalled branch on worker-ocr-02 and spawned redundant replica.',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Planner Domain Events & Projections</h1>
            <Badge variant="intelligence" size="sm">Read Model</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Real-time projection of autonomous planning events, DAG synthesis decisions, and dynamic replanning triggers.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            Planner Status: {plannerState.state}
          </Badge>
        </div>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <Card className="p-4 bg-emerald-950/10 border-emerald-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Plans Generated</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">{plannerState.totalPlansGenerated} Plans</div>
          <div className="text-[11px] text-muted-foreground mt-1">Cumulative lifecycle</div>
        </Card>
        <Card className="p-4 bg-blue-950/10 border-blue-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Dynamic Replans</div>
          <div className="text-2xl font-bold font-mono text-blue-400 mt-1">{plannerState.totalReplansExecuted} Replans</div>
          <div className="text-[11px] text-muted-foreground mt-1">Fault-induced re-routes</div>
        </Card>
        <Card className="p-4 bg-purple-950/10 border-purple-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Critical Path Latency</div>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-1">{plannerState.criticalPathMs} ms</div>
          <div className="text-[11px] text-muted-foreground mt-1">Parallel execution bound</div>
        </Card>
        <Card className="p-4 bg-cyan-950/10 border-cyan-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Estimated Plan Cost</div>
          <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">${plannerState.estimatedCostUsd}</div>
          <div className="text-[11px] text-muted-foreground mt-1">6 Active tasks</div>
        </Card>
      </div>

      {/* Planner Event Log */}
      <div className="space-y-3">
        <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Planner Domain Event Log</h2>
        <div className="grid grid-cols-1 gap-3">
          {plannerEvents.map(ev => (
            <Card key={ev.id} className="p-4 border-border/60 hover:border-border transition-all space-y-2">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <BrainCircuit className="w-4 h-4 text-primary" />
                  <span className="text-sm font-bold text-foreground">{ev.type}</span>
                  <Badge variant="outline" size="sm">{ev.strategy}</Badge>
                </div>
                <div className="flex items-center gap-2 font-mono text-[11px] text-muted-foreground">
                  <Clock className="w-3.5 h-3.5" />
                  <span>{ev.time} UTC</span>
                </div>
              </div>
              <p className="text-xs text-muted-foreground">{ev.details}</p>
              <div className="text-[11px] text-muted-foreground font-mono pt-1 border-t border-border/30">
                Actor: <strong className="text-foreground">{ev.actor}</strong> • Goal: <strong className="text-primary">{ev.goal}</strong>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
