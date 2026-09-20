import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { GitFork, RotateCcw, CheckCircle2 } from 'lucide-react';

export const MissionTimeMachineView: React.FC = () => {
  const [selectedStep, setSelectedStep] = useState<number>(2);
  const [rewindMessage, setRewindMessage] = useState<string | null>(null);
  const [forkMessage, setForkMessage] = useState<string | null>(null);

  const checkpoints = [
    {
      step: 0,
      id: 'chk-01',
      time: '14:00:00 UTC',
      hash: 'a1b2c3d4e5f6001',
      health: 100.0,
      tasks: 1,
      memoryNodes: 12,
      cost: '$0.0000',
      summary: 'Mission initialized. PDF document chunks queued for ingestion.',
    },
    {
      step: 1,
      id: 'chk-02',
      time: '14:00:45 UTC',
      hash: 'a1b2c3d4e5f6002',
      health: 100.0,
      tasks: 4,
      memoryNodes: 28,
      cost: '$0.0012',
      summary: 'OCR extraction parallelized across 4 DAG workers.',
    },
    {
      step: 2,
      id: 'chk-03',
      time: '14:01:30 UTC',
      hash: 'a1b2c3d4e5f6003',
      health: 65.0,
      tasks: 4,
      memoryNodes: 35,
      cost: '$0.0025',
      summary: 'Gemini 504 Timeout injected. Incident declared. Flash failover active.',
    },
    {
      step: 3,
      id: 'chk-04',
      time: '14:02:20 UTC',
      hash: 'a1b2c3d4e5f6004',
      health: 100.0,
      tasks: 2,
      memoryNodes: 48,
      cost: '$0.0031',
      summary: 'Failover resolved. Invariant verification 100% passed. Mission finalized.',
    },
  ];

  const currentChk = (checkpoints.find(c => c.step === selectedStep) || checkpoints[0])!;


  const handleRewind = () => {
    setForkMessage(null);
    setRewindMessage(`Restored mission execution state to Step ${currentChk.step} (${currentChk.id}). State hash verified.`);
  };

  const handleFork = () => {
    setRewindMessage(null);
    setForkMessage(`Forked counterfactual mission branch 'mission-fork-7b9a2c' starting from Step ${currentChk.step}.`);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Runtime Time Machine & State Restoration</h1>
            <Badge variant="intelligence" size="sm">Deterministic Rewind</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Explore past execution states, rewind mission context to any historical step, and fork counterfactual execution branches.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            4 Checkpoints Available
          </Badge>
        </div>
      </div>

      {/* Scrub-Bar Timeline */}
      <Card className="p-6 border-border/60 space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-muted-foreground uppercase">Execution Scrub-Bar</span>
          <span className="text-xs font-mono text-primary font-bold">Current Point: Step {selectedStep}</span>
        </div>

        <div className="grid grid-cols-4 gap-2 pt-2">
          {checkpoints.map(c => (
            <button
              key={c.step}
              onClick={() => {
                setSelectedStep(c.step);
                setRewindMessage(null);
                setForkMessage(null);
              }}
              className={`p-3 rounded-lg border text-left transition-all ${
                selectedStep === c.step
                  ? 'border-primary bg-primary/10 shadow'
                  : 'border-border/40 bg-muted/20 hover:border-border'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-foreground">Step {c.step}</span>
                <Badge variant={c.health < 100 ? 'warning' : 'success'} size="sm">
                  {c.health}%
                </Badge>
              </div>
              <div className="text-[10px] text-muted-foreground font-mono mt-1">{c.time}</div>
            </button>
          ))}
        </div>
      </Card>

      {/* Selected Step Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Historical State Payload</h2>
          <Card className="p-5 border-border/60 space-y-4">
            <div className="flex items-center justify-between border-b border-border/40 pb-3">
              <div>
                <div className="text-base font-bold text-foreground">Step {currentChk.step}: {currentChk.summary}</div>
                <div className="text-xs font-mono text-muted-foreground mt-0.5">
                  State Hash: <strong className="text-primary">{currentChk.hash}</strong>
                </div>
              </div>
              <Badge variant="intelligence" size="md">{currentChk.id}</Badge>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-1">
              <div className="p-3 bg-muted/40 rounded border border-border/30 text-center">
                <div className="text-[10px] text-muted-foreground">Twin Health</div>
                <div className="text-sm font-mono font-bold text-foreground mt-0.5">{currentChk.health}%</div>
              </div>
              <div className="p-3 bg-muted/40 rounded border border-border/30 text-center">
                <div className="text-[10px] text-muted-foreground">Active Tasks</div>
                <div className="text-sm font-mono font-bold text-foreground mt-0.5">{currentChk.tasks}</div>
              </div>
              <div className="p-3 bg-muted/40 rounded border border-border/30 text-center">
                <div className="text-[10px] text-muted-foreground">Memory Nodes</div>
                <div className="text-sm font-mono font-bold text-foreground mt-0.5">{currentChk.memoryNodes}</div>
              </div>
              <div className="p-3 bg-muted/40 rounded border border-border/30 text-center">
                <div className="text-[10px] text-muted-foreground">Cost Accumulated</div>
                <div className="text-sm font-mono font-bold text-emerald-400 mt-0.5">{currentChk.cost}</div>
              </div>
            </div>

            {rewindMessage && (
              <div className="p-3 bg-emerald-950/10 rounded border border-emerald-500/20 text-xs text-emerald-400 font-mono flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                <span>{rewindMessage}</span>
              </div>
            )}

            {forkMessage && (
              <div className="p-3 bg-blue-950/10 rounded border border-blue-500/20 text-xs text-blue-400 font-mono flex items-center gap-2">
                <GitFork className="w-4 h-4 text-blue-400 shrink-0" />
                <span>{forkMessage}</span>
              </div>
            )}
          </Card>
        </div>

        {/* Time Travel Controls */}
        <div className="space-y-4">
          <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Time-Travel Actions</h2>
          <Card className="p-5 border-border/60 space-y-3">
            <Button
              variant="outline"
              size="sm"
              className="w-full justify-start"
              onClick={handleRewind}
            >
              <RotateCcw className="w-4 h-4 mr-2 text-amber-400" />
              Rewind Mission to Step {currentChk.step}
            </Button>
            <Button
              variant="primary"
              size="sm"
              className="w-full justify-start"
              onClick={handleFork}
            >
              <GitFork className="w-4 h-4 mr-2" />
              Fork Counterfactual Branch
            </Button>

            <div className="p-3 bg-muted/40 rounded border border-border/40 text-[11px] text-muted-foreground leading-relaxed">
              Forking creates a clean sandbox branch from this exact point in time, enabling hypothetical chaos tests without altering the primary truth ledger.
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
