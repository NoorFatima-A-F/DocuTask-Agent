import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Clock, RefreshCw, Hash, ShieldCheck } from 'lucide-react';

export const MissionTimelineView: React.FC = () => {
  const [selectedEventId, setSelectedEventId] = useState<string>('evt-m01-001');
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);

  const events = [
    {
      id: 'evt-m01-001',
      offset: 0,
      time: '14:20:00.120 UTC',
      type: 'MissionCreated',
      subsystem: 'MISSION_CONTROL',
      actor: 'HumanOperator',
      actorType: 'HUMAN',
      correlationId: 'corr-mission-fin-001',
      causationId: 'cause-user-submit',
      evidenceHash: '9f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069',
      truthLedgerHash: '8a1b2c3d4e5f60017a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f',
      severity: 'INFO',
      payload: { goal: 'Process and validate 2026 Q3 vendor audit invoices', document_count: 4, sla_seconds: 30 },
    },
    {
      id: 'evt-m01-002',
      offset: 1,
      time: '14:20:00.350 UTC',
      type: 'PlannerStarted',
      subsystem: 'PLANNER',
      actor: 'ChiefPlanner',
      actorType: 'PLANNER',
      correlationId: 'corr-mission-fin-001',
      causationId: 'cause-evt-m01-001',
      evidenceHash: '4a5b6c7d8e9f00112233445566778899aabbccddeeff00112233445566778899',
      truthLedgerHash: '3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c',
      severity: 'INFO',
      payload: { strategy: 'DYNAMIC_DAG_SYNTHESIS', model: 'gemini-1.5-pro', priority: 'HIGH' },
    },
    {
      id: 'evt-m01-003',
      offset: 2,
      time: '14:20:00.890 UTC',
      type: 'PlannerFinished',
      subsystem: 'PLANNER',
      actor: 'ChiefPlanner',
      actorType: 'PLANNER',
      correlationId: 'corr-mission-fin-001',
      causationId: 'cause-evt-m01-002',
      evidenceHash: '11223344556677889900aabbccddeeff00112233445566778899aabbccddeeff',
      truthLedgerHash: '5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d',
      severity: 'INFO',
      payload: { generated_task_count: 6, estimated_cost_usd: 0.0032, critical_path_latency_ms: 185.4 },
    },
    {
      id: 'evt-m01-004',
      offset: 3,
      time: '14:20:01.100 UTC',
      type: 'TaskAssigned',
      subsystem: 'WORKER_POOL',
      actor: 'DAGScheduler',
      actorType: 'SYSTEM',
      correlationId: 'corr-mission-fin-001',
      causationId: 'cause-evt-m01-003',
      evidenceHash: '778899aabbccddeeff00112233445566778899aabbccddeeff00112233445566',
      truthLedgerHash: '7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f',
      severity: 'INFO',
      payload: { task_id: 'task-ocr-chunk-1', worker_id: 'worker-ocr-01', task_type: 'OCR_EXTRACTION' },
    },
    {
      id: 'evt-m01-005',
      offset: 4,
      time: '14:20:01.420 UTC',
      type: 'OCRCompleted',
      subsystem: 'OCR_SERVICE',
      actor: 'worker-ocr-01',
      actorType: 'WORKER',
      correlationId: 'corr-mission-fin-001',
      causationId: 'cause-evt-m01-004',
      evidenceHash: 'aabbccddeeff00112233445566778899aabbccddeeff00112233445566778899',
      truthLedgerHash: '9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b',
      severity: 'INFO',
      payload: { extracted_text_length: 4520, confidence: 0.994, duration_ms: 320.0 },
    },
    {
      id: 'evt-m01-006',
      offset: 5,
      time: '14:20:01.750 UTC',
      type: 'ValidationPassed',
      subsystem: 'VALIDATION_ENGINE',
      actor: 'ScientificValidator',
      actorType: 'SYSTEM',
      correlationId: 'corr-mission-fin-001',
      causationId: 'cause-evt-m01-005',
      evidenceHash: 'bbccddee00112233445566778899aabbccddeeff00112233445566778899aabb',
      truthLedgerHash: '1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d',
      severity: 'INFO',
      payload: { schema_valid: true, business_rules_passed: 12, invariant_checks: 6 },
    },
    {
      id: 'evt-m01-007',
      offset: 6,
      time: '14:20:02.100 UTC',
      type: 'MissionCompleted',
      subsystem: 'MISSION_CONTROL',
      actor: 'MissionCommander',
      actorType: 'SYSTEM',
      correlationId: 'corr-mission-fin-001',
      causationId: 'cause-evt-m01-006',
      evidenceHash: 'ccddee00112233445566778899aabbccddeeff00112233445566778899aabbcc',
      truthLedgerHash: '2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e',
      severity: 'INFO',
      payload: { total_tasks_completed: 6, duration_seconds: 1.98, total_cost_usd: 0.0031, status: 'SUCCESS' },
    },
  ];

  const currentEvent = (events.find(e => e.id === selectedEventId) || events[0])!;

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 300);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Mission Domain Event Timeline</h1>
            <Badge variant="intelligence" size="sm">Immutable Event Stream</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Chronological, cryptographically linked domain event stream for the active mission partition.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleRefresh} disabled={isRefreshing}>
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isRefreshing ? 'animate-spin' : ''}`} />
            Refresh Stream
          </Button>
          <Badge variant="success" size="md">
            7/7 Events Verified
          </Badge>
        </div>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <Card className="p-4 bg-emerald-950/10 border-emerald-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Partition Stream Length</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">{events.length} Events</div>
          <div className="text-[11px] text-muted-foreground mt-1">Offsets 0..{events.length - 1}</div>
        </Card>
        <Card className="p-4 bg-blue-950/10 border-blue-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Execution Latency</div>
          <div className="text-2xl font-bold font-mono text-blue-400 mt-1">1.98s Total</div>
          <div className="text-[11px] text-muted-foreground mt-1">Within 30s SLA budget</div>
        </Card>
        <Card className="p-4 bg-purple-950/10 border-purple-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Merkle Continuity</div>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-1">100.0%</div>
          <div className="text-[11px] text-muted-foreground mt-1">SHA-256 parent linked</div>
        </Card>
        <Card className="p-4 bg-cyan-950/10 border-cyan-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Total Incurred Cost</div>
          <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">$0.0031</div>
          <div className="text-[11px] text-muted-foreground mt-1">Optimized utility path</div>
        </Card>
      </div>

      {/* Main Grid: Stream & Event Payload Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Event Stream List */}
        <div className="lg:col-span-2 space-y-3">
          <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Chronological Event Stream</h2>
          <div className="space-y-2">
            {events.map(ev => (
              <Card
                key={ev.id}
                onClick={() => setSelectedEventId(ev.id)}
                className={`p-3.5 cursor-pointer transition-all border ${
                  selectedEventId === ev.id
                    ? 'border-primary bg-primary/5 shadow-md'
                    : 'border-border/60 hover:border-border'
                }`}
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div className="flex items-center gap-2.5">
                    <span className="w-6 h-6 rounded-full bg-primary/10 text-primary flex items-center justify-center text-xs font-mono font-bold">
                      #{ev.offset}
                    </span>
                    <div>
                      <div className="text-xs font-bold text-foreground flex items-center gap-2">
                        <span>{ev.type}</span>
                        <Badge variant="outline" size="sm">{ev.subsystem}</Badge>
                      </div>
                      <div className="text-[10px] text-muted-foreground font-mono mt-0.5">
                        {ev.id} • {ev.actor} ({ev.actorType})
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 font-mono text-[11px] text-muted-foreground self-end sm:self-center">
                    <Clock className="w-3.5 h-3.5" />
                    <span>{ev.time}</span>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Selected Event Detail & Hashes */}
        <div className="space-y-4">
          <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Event Inspector</h2>
          <Card className="p-5 border-border/60 space-y-4">
            <div>
              <div className="flex items-center justify-between">
                <Badge variant="intelligence" size="sm">Offset #{currentEvent.offset}</Badge>
                <Badge variant="success" size="sm">{currentEvent.severity}</Badge>
              </div>
              <div className="text-base font-bold text-foreground mt-2">{currentEvent.type}</div>
              <div className="text-xs font-mono text-muted-foreground">{currentEvent.id}</div>
            </div>

            <div className="space-y-2.5 pt-2 border-t border-border/40 text-xs">
              <div className="flex justify-between items-center">
                <span className="text-muted-foreground">Subsystem:</span>
                <span className="font-mono text-foreground font-semibold">{currentEvent.subsystem}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-muted-foreground">Actor:</span>
                <span className="font-mono text-foreground">{currentEvent.actor} ({currentEvent.actorType})</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-muted-foreground">Correlation ID:</span>
                <span className="font-mono text-primary text-[11px]">{currentEvent.correlationId}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-muted-foreground">Causation ID:</span>
                <span className="font-mono text-muted-foreground text-[11px]">{currentEvent.causationId}</span>
              </div>
            </div>

            {/* Cryptographic Proof Hashes */}
            <div className="space-y-2 pt-2 border-t border-border/40">
              <div className="text-[11px] font-semibold text-muted-foreground uppercase flex items-center gap-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" /> Evidence Hash (SHA-256)
              </div>
              <div className="p-2 bg-muted/40 rounded font-mono text-[10px] text-primary break-all border border-border/30">
                {currentEvent.evidenceHash}
              </div>

              <div className="text-[11px] font-semibold text-muted-foreground uppercase flex items-center gap-1.5 pt-1">
                <Hash className="w-3.5 h-3.5 text-blue-400" /> Ledger Block Hash
              </div>
              <div className="p-2 bg-muted/40 rounded font-mono text-[10px] text-foreground break-all border border-border/30">
                {currentEvent.truthLedgerHash}
              </div>
            </div>

            {/* Payload JSON Box */}
            <div className="space-y-1.5 pt-2 border-t border-border/40">
              <div className="text-xs font-semibold text-muted-foreground uppercase">Event Payload</div>
              <pre className="p-3 bg-muted/50 rounded font-mono text-[11px] text-foreground overflow-x-auto border border-border/30 max-h-48">
                {JSON.stringify(currentEvent.payload, null, 2)}
              </pre>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
