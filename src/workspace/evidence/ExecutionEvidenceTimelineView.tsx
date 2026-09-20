import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ExecutionEvidenceTimelineView: React.FC = () => {
  const [filterType, setFilterType] = useState<string>('ALL');

  const timelineEvents = [
    {
      timeOffsetMs: 0,
      timestamp: '18:22:10.142',
      type: 'PLANNER_DECISION',
      title: 'Optimal Trajectory Selection',
      summary: 'Chief Planner selected Gemini Flash with parallelism=3 across 4 candidate plans.',
      evidenceId: 'ev-node-001',
      costUsd: 0.0018,
      durationMs: 14.2,
      hash: 'a8f3b20c91e847ad3ef0192a83c7482910fae12089bb3c17820aedfa9102bc45',
    },
    {
      timeOffsetMs: 180,
      timestamp: '18:22:10.322',
      type: 'RESOURCE_AUCTION',
      title: 'GPU Compute Token Auction',
      summary: 'OCR Department won Vickrey auction for 4x GPU workers with $0.00042 bid.',
      evidenceId: 'ev-node-002',
      costUsd: 0.00042,
      durationMs: 4.8,
      hash: 'd4e9102fae89bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c748',
    },
    {
      timeOffsetMs: 380,
      timestamp: '18:22:10.522',
      type: 'TOOL_EXECUTION',
      title: 'Tesseract V5 OCR Execution',
      summary: 'Processed invoice image in 124.5ms; extracted 142 tokens and 28 bounding boxes.',
      evidenceId: 'ev-node-003',
      costUsd: 0.00042,
      durationMs: 124.5,
      hash: '7c3f810dae99120bc45a8f3b20c91e847ad3ef0192a83c748d4e9102fae89bb3c',
    },
    {
      timeOffsetMs: 520,
      timestamp: '18:22:10.662',
      type: 'VALIDATION_CHECK',
      title: 'Financial Invariant Reconciliation',
      summary: 'Reconciled subtotal + tax = $4,850.00 with p=0.0001 statistical confidence.',
      evidenceId: 'ev-node-004',
      costUsd: 0.0,
      durationMs: 18.2,
      hash: '3b20c91e847ad3ef0192a83c748d4e9102fae89bb3c7c3f810dae99120bc45a8f',
    },
    {
      timeOffsetMs: 650,
      timestamp: '18:22:10.792',
      type: 'ARTIFACT_MUTATION',
      title: 'Content-Addressable Registry Store',
      summary: 'Stored certified extraction JSON sealed with SHA-256 digest in artifact catalog.',
      evidenceId: 'ev-node-005',
      costUsd: 0.0,
      durationMs: 2.1,
      hash: 'f81d4fae7dec11d0a76500a0c91e6bf6012a8f3b20c91e847ad3ef0192a83c748',
    },
  ];

  const filtered = filterType === 'ALL' ? timelineEvents : timelineEvents.filter((e) => e.type === filterType);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Execution Evidence Timeline</h1>
            <Badge variant="success" size="sm">Millisecond Timestamped</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Chronological, high-resolution timeline of every runtime event linked directly to immutable evidence blocks.
          </p>
        </div>
        <div className="flex items-center gap-2">
          {['ALL', 'PLANNER_DECISION', 'TOOL_EXECUTION', 'VALIDATION_CHECK'].map((f) => (
            <button
              key={f}
              onClick={() => setFilterType(f)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                filterType === f
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-muted/40 text-muted-foreground hover:bg-muted/80'
              }`}
            >
              {f.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Timeline Stream */}
      <div className="relative pl-6 space-y-4 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-border/60">
        {filtered.map((ev) => (
          <div key={ev.evidenceId} className="relative space-y-1">
            {/* Timeline Dot */}
            <div className="absolute -left-6 top-1.5 w-3 h-3 rounded-full bg-primary ring-4 ring-background" />

            <Card className="p-4 space-y-2">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs font-bold text-primary">+{ev.timeOffsetMs}ms</span>
                  <span className="text-sm font-semibold text-foreground">{ev.title}</span>
                  <Badge variant="outline" size="sm">{ev.type}</Badge>
                </div>
                <div className="flex items-center gap-3 text-xs font-mono text-muted-foreground">
                  <span>{ev.timestamp} UTC</span>
                  <span>{ev.durationMs} ms</span>
                  {ev.costUsd > 0 && <span className="text-emerald-400 font-bold">${ev.costUsd.toFixed(5)}</span>}
                </div>
              </div>
              <p className="text-xs text-muted-foreground">
                {ev.summary}
              </p>
              <div className="pt-2 border-t border-border/40 flex items-center justify-between text-[11px] font-mono text-muted-foreground">
                <span>Evidence ID: <span className="text-foreground">{ev.evidenceId}</span></span>
                <span className="truncate max-w-xs">Hash: {ev.hash.slice(0, 20)}...</span>
              </div>
            </Card>
          </div>
        ))}
      </div>
    </div>
  );
};
