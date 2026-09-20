import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Radio, Pause, Play, RotateCcw } from 'lucide-react';

export const LiveEventStreamView: React.FC = () => {
  const [isStreaming, setIsStreaming] = useState<boolean>(true);
  const [streamEvents, setStreamEvents] = useState<Array<{ id: string; time: string; type: string; subsystem: string; summary: string }>>([
    { id: 'evt-s01', time: '14:20:00.120', type: 'MissionCreated', subsystem: 'MISSION_CONTROL', summary: 'Mission initialized for 4 invoice documents.' },
    { id: 'evt-s02', time: '14:20:00.350', type: 'PlannerStarted', subsystem: 'PLANNER', summary: 'Decomposing mission into dynamic DAG.' },
    { id: 'evt-s03', time: '14:20:00.890', type: 'PlannerFinished', subsystem: 'PLANNER', summary: 'Generated 6 DAG task nodes.' },
    { id: 'evt-s04', time: '14:20:01.100', type: 'TaskAssigned', subsystem: 'WORKER_POOL', summary: 'Assigned OCR Chunk 1 to worker-ocr-01.' },
    { id: 'evt-s05', time: '14:20:01.420', type: 'OCRCompleted', subsystem: 'OCR_SERVICE', summary: 'Extracted 4,520 chars with 0.994 confidence.' },
    { id: 'evt-s06', time: '14:20:01.750', type: 'ValidationPassed', subsystem: 'VALIDATION_ENGINE', summary: '12 business rules verified with 0 errors.' },
  ]);

  const handleToggleStream = () => {
    setIsStreaming(prev => !prev);
  };

  const handleClear = () => {
    setStreamEvents([]);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Live Domain Event Stream</h1>
            <Badge variant={isStreaming ? 'success' : 'warning'} size="sm">
              {isStreaming ? 'STREAMING ACTIVE' : 'STREAM PAUSED'}
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Real-time SSE event pipeline streaming domain events directly from the EventBus to the UI.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleToggleStream}>
            {isStreaming ? <Pause className="w-3.5 h-3.5 mr-1.5" /> : <Play className="w-3.5 h-3.5 mr-1.5" />}
            {isStreaming ? 'Pause Stream' : 'Resume Stream'}
          </Button>
          <Button variant="outline" size="sm" onClick={handleClear}>
            <RotateCcw className="w-3.5 h-3.5 mr-1.5" />
            Clear Buffer
          </Button>
        </div>
      </div>

      {/* Stream Overview Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <Card className="p-4 bg-emerald-950/10 border-emerald-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Event Ingestion Rate</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">8.4 Events/sec</div>
          <div className="text-[11px] text-muted-foreground mt-1">Zero dropped frames</div>
        </Card>
        <Card className="p-4 bg-blue-950/10 border-blue-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Active Socket Clients</div>
          <div className="text-2xl font-bold font-mono text-blue-400 mt-1">1 Client</div>
          <div className="text-[11px] text-muted-foreground mt-1">Direct SSE channel</div>
        </Card>
        <Card className="p-4 bg-purple-950/10 border-purple-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Stream Delivery Latency</div>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-1">1.2 ms</div>
          <div className="text-[11px] text-muted-foreground mt-1">EventBus to client</div>
        </Card>
        <Card className="p-4 bg-cyan-950/10 border-cyan-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Total Streamed</div>
          <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">{streamEvents.length} Events</div>
          <div className="text-[11px] text-muted-foreground mt-1">In active session</div>
        </Card>
      </div>

      {/* Stream Ticker Log */}
      <Card className="p-5 border-border/60 space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-muted-foreground uppercase flex items-center gap-1.5">
            <Radio className={`w-3.5 h-3.5 ${isStreaming ? 'text-emerald-400 animate-pulse' : 'text-muted-foreground'}`} />
            Live Event Stream Ticker
          </span>
          <span className="text-[11px] font-mono text-muted-foreground">Auto-scrolling FIFO</span>
        </div>

        <div className="space-y-2 font-mono text-xs max-h-96 overflow-y-auto pt-2">
          {streamEvents.map(ev => (
            <div key={ev.id} className="flex items-start gap-3 p-2.5 rounded bg-muted/40 border border-border/30 hover:border-primary/40 transition-colors">
              <span className="text-muted-foreground text-[11px] whitespace-nowrap pt-0.5">{ev.time}</span>
              <Badge variant="intelligence" size="sm">{ev.type}</Badge>
              <Badge variant="outline" size="sm">{ev.subsystem}</Badge>
              <div className="text-foreground flex-1 font-sans text-xs">
                {ev.summary}
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
