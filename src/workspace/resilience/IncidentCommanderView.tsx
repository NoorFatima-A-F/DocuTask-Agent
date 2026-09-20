import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { CheckCircle2 } from 'lucide-react';

export const IncidentCommanderView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'INCIDENTS' | 'POSTMORTEMS'>('INCIDENTS');
  const [selectedIncidentId, setSelectedIncidentId] = useState<string>('inc-202609-001');

  const incidents = [
    {
      id: 'inc-202609-001',
      title: 'Upstream Gemini 1.5 Pro 504 Timeout Spike',
      severity: 'SEV2_HIGH',
      state: 'RESOLVED',
      rootCause: 'node-gemini (Google Cloud Gateway)',
      blastRadius: ['node-workers', 'node-planner'],
      duration: '90 seconds',
      mttr: '45.0 ms',
      strategy: 'strat-gemini-flash-fallback',
      postMortem: 'Upstream cloud gateway experienced momentary latency spike to 5.2s. Autonomous Incident Commander declared SEV2, tripped circuit breaker, and routed 100% of pending DAG worker prompts to Gemini 1.5 Flash in 45ms with 0 state loss.',
      timeline: [
        { time: '14:20:00 UTC', state: 'DETECTED', actor: 'COMMANDER', msg: 'Anomalous error rate (85%) detected on Gemini provider endpoint.' },
        { time: '14:20:12 UTC', state: 'TRIAGING', actor: 'DIAGNOSTIC_AGENT', msg: 'Diagnostic subagent confirmed upstream 504 Gateway Timeout.' },
        { time: '14:20:25 UTC', state: 'ISOLATING', actor: 'COMMANDER', msg: 'Circuit breaker tripped for node-gemini. In-flight requests rerouted.' },
        { time: '14:20:40 UTC', state: 'RECOVERING', actor: 'COMMANDER', msg: 'Activated strat-gemini-flash-fallback. Model swapped to Flash.' },
        { time: '14:20:70 UTC', state: 'VERIFYING', actor: 'COMMANDER', msg: 'Invariant check passed: replay parity 99.98%, zero data drop.' },
        { time: '14:21:30 UTC', state: 'RESOLVED', actor: 'COMMANDER', msg: 'Incident resolved autonomously. Health score restored to 100.0.' },
      ],
    },
    {
      id: 'inc-202609-002',
      title: 'OCR Worker Subsystem Memory Pressure',
      severity: 'SEV3_MEDIUM',
      state: 'RESOLVED',
      rootCause: 'node-workers (DAG Worker Pool)',
      blastRadius: ['node-planner'],
      duration: '45 seconds',
      mttr: '180.0 ms',
      strategy: 'strat-ocr-chunk-respawn',
      postMortem: 'Worker pool reached 85% memory threshold during large raster PDF processing. Commander isolated corrupted chunk, respawned sandboxed worker replica, and resumed pipeline.',
      timeline: [
        { time: '11:15:00 UTC', state: 'DETECTED', actor: 'COMMANDER', msg: 'Worker node-workers reported heap usage > 85%.' },
        { time: '11:15:10 UTC', state: 'ISOLATING', actor: 'COMMANDER', msg: 'Worker process isolated from active scheduler queue.' },
        { time: '11:15:25 UTC', state: 'RECOVERING', actor: 'COMMANDER', msg: 'Respawned worker sandbox. Chunk re-allocated.' },
        { time: '11:15:45 UTC', state: 'RESOLVED', actor: 'COMMANDER', msg: 'Worker heap stabilized at 18%. Zero document data dropped.' },
      ],
    },
  ];

  const currentInc = (incidents.find(i => i.id === selectedIncidentId) || incidents[0])!;


  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Autonomous Incident Commander</h1>
            <Badge variant="intelligence" size="sm">Auto-Triage & Recovery</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Self-governing incident commander that detects anomalies, isolates failing components, executes verified fallbacks, and authors formal post-mortems.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex bg-muted/40 p-1 rounded-lg border border-border/40 text-xs">
            <button
              onClick={() => setActiveTab('INCIDENTS')}
              className={`px-3 py-1 rounded font-medium transition-colors ${
                activeTab === 'INCIDENTS' ? 'bg-primary text-primary-foreground' : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              Live Incidents ({incidents.length})
            </button>
            <button
              onClick={() => setActiveTab('POSTMORTEMS')}
              className={`px-3 py-1 rounded font-medium transition-colors ${
                activeTab === 'POSTMORTEMS' ? 'bg-primary text-primary-foreground' : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              Post-Mortems
            </button>
          </div>
          <Badge variant="success" size="md">
            All Incidents Resolved (100%)
          </Badge>
        </div>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <Card className="p-4 bg-emerald-950/10 border-emerald-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Autonomous Resolution Rate</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">100.0%</div>
          <div className="text-[11px] text-muted-foreground mt-1">0 Human escalations needed</div>
        </Card>
        <Card className="p-4 bg-blue-950/10 border-blue-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Mean Time To Triage</div>
          <div className="text-2xl font-bold font-mono text-blue-400 mt-1">11.5 sec</div>
          <div className="text-[11px] text-muted-foreground mt-1">Autonomous diagnostic agent</div>
        </Card>
        <Card className="p-4 bg-purple-950/10 border-purple-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Mean Time To Recovery</div>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-1">67.5 sec</div>
          <div className="text-[11px] text-muted-foreground mt-1">End-to-end self-healing</div>
        </Card>
        <Card className="p-4 bg-cyan-950/10 border-cyan-500/20">
          <div className="text-xs font-semibold text-muted-foreground">Data Loss Under Incidents</div>
          <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">0 Bytes</div>
          <div className="text-[11px] text-muted-foreground mt-1">Truth ledger unbroken</div>
        </Card>
      </div>

      {/* Incident List and Detail View */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="space-y-3">
          <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Incident Log</h2>
          {incidents.map(inc => (
            <Card
              key={inc.id}
              onClick={() => setSelectedIncidentId(inc.id)}
              className={`p-4 cursor-pointer transition-all border ${
                selectedIncidentId === inc.id ? 'border-primary bg-primary/5 shadow-md' : 'border-border/60 hover:border-border'
              }`}
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="text-xs font-bold text-foreground">{inc.title}</div>
                  <div className="text-[10px] text-muted-foreground font-mono mt-0.5">{inc.id}</div>
                </div>
                <Badge variant={inc.severity === 'SEV2_HIGH' ? 'warning' : 'default'} size="sm">
                  {inc.severity}
                </Badge>
              </div>
              <div className="flex items-center justify-between text-[11px] text-muted-foreground mt-3 pt-2 border-t border-border/40">
                <span>Duration: <strong className="text-foreground">{inc.duration}</strong></span>
                <Badge variant="success" size="sm">{inc.state}</Badge>
              </div>
            </Card>
          ))}
        </div>

        {/* Selected Incident Detail & Timeline */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Incident Mitigation Timeline & Forensics</h2>
          <Card className="p-5 border-border/60 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border/40 pb-3">
              <div>
                <div className="text-base font-bold text-foreground">{currentInc.title}</div>
                <div className="text-xs text-muted-foreground font-mono mt-0.5">
                  Root Cause: <strong className="text-red-400">{currentInc.rootCause}</strong> • Failover: <strong className="text-primary">{currentInc.strategy}</strong>
                </div>
              </div>
              <Badge variant="success" size="md">Status: {currentInc.state}</Badge>
            </div>

            {/* Timeline Stream */}
            <div className="space-y-3 pt-2">
              <div className="text-xs font-semibold text-muted-foreground uppercase">Chronological Action Ledger</div>
              <div className="space-y-2 font-mono text-xs">
                {currentInc.timeline.map((entry, idx) => (
                  <div key={idx} className="flex items-start gap-3 p-2.5 rounded bg-muted/30 border border-border/30">
                    <div className="text-[11px] text-muted-foreground whitespace-nowrap pt-0.5">{entry.time}</div>
                    <Badge variant="intelligence" size="sm">{entry.state}</Badge>
                    <div className="text-xs text-foreground flex-1">
                      <strong className="text-primary">[{entry.actor}]</strong> {entry.msg}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Post Mortem Box */}
            <div className="p-4 bg-muted/40 rounded-lg border border-border/40 space-y-1.5 mt-4">
              <div className="text-xs font-bold text-foreground flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" /> Autonomous Post-Mortem Summary
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">
                {currentInc.postMortem}
              </p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
