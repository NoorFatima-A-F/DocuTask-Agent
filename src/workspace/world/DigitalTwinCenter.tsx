import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Activity,
  RefreshCw,
  Cpu,
  Layers,
  ShieldCheck,
  CheckCircle2,
  Sparkles,
  Lock,
} from 'lucide-react';

interface SubsystemMirror {
  name: string;
  status: string;
  entitiesMirrored: number;
  syncLatencyMs: number;
  divergence: boolean;
}

export const DigitalTwinCenter: React.FC = () => {
  const [isSyncing, setIsSyncing] = useState<boolean>(false);

  const subsystems: SubsystemMirror[] = [
    { name: 'AGENT_SOCIETY', status: 'SYNCHRONIZED', entitiesMirrored: 21, syncLatencyMs: 12.5, divergence: false },
    { name: 'APDLE_PLANNER_DAG', status: 'SYNCHRONIZED', entitiesMirrored: 16, syncLatencyMs: 8.2, divergence: false },
    { name: 'COMMUNICATION_BUS', status: 'SYNCHRONIZED', entitiesMirrored: 12500, syncLatencyMs: 4.1, divergence: false },
    { name: 'TRUTH_LEDGER', status: 'SYNCHRONIZED', entitiesMirrored: 890, syncLatencyMs: 15.0, divergence: false },
    { name: 'REPLAY_FORENSICS', status: 'SYNCHRONIZED', entitiesMirrored: 450, syncLatencyMs: 18.2, divergence: false },
    { name: 'RESOURCE_ALLOCATOR', status: 'SYNCHRONIZED', entitiesMirrored: 8, syncLatencyMs: 6.4, divergence: false },
    { name: 'STRATEGIC_GOVERNANCE', status: 'SYNCHRONIZED', entitiesMirrored: 14, syncLatencyMs: 11.0, divergence: false },
  ];

  const handleSync = () => {
    setIsSyncing(true);
    setTimeout(() => {
      setIsSyncing(false);
    }, 1200);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Digital Twin Intelligence Center</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              TWIN SYNCHRONIZED
            </Badge>
            <Badge variant="outline" size="sm">
              AWM-PSDTIP Phase 13.10
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Real-time digital twin replica of multi-agent societies, DAG scheduler, truth ledger, memory, and infrastructure with zero synthetic divergence.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleSync} disabled={isSyncing}>
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isSyncing ? 'animate-spin' : ''}`} />
            {isSyncing ? 'Synchronizing State...' : 'Synchronize Digital Twin'}
          </Button>
          <Button variant="intelligence" size="sm">
            <Sparkles className="w-3.5 h-3.5 mr-1.5" />
            Trigger Twin Snapshot
          </Button>
        </div>
      </div>

      {/* Synchronized Twin Banner */}
      <Card className="p-5 bg-gradient-to-r from-emerald-950/30 via-purple-950/20 to-background border-emerald-500/30">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-start gap-4">
            <div className="p-3 bg-emerald-500/10 rounded-xl border border-emerald-500/20 text-emerald-400">
              <Activity className="w-6 h-6" />
            </div>
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider">
                  Live Enterprise Digital Twin Mirror
                </span>
                <Badge variant="success" size="sm">Fidelity 99.8%</Badge>
              </div>
              <p className="text-sm font-medium text-foreground">
                Continuous real-time mirror active across all 7 distributed operating subsystems.
              </p>
              <div className="flex flex-wrap items-center gap-4 text-xs text-muted-foreground pt-1 font-mono">
                <span>Sync Latency: <strong className="text-foreground">12.5ms</strong></span>
                <span>•</span>
                <span>Divergence: <strong className="text-emerald-400">0.0% (Zero Divergence)</strong></span>
              </div>
            </div>
          </div>
          <div className="flex flex-col sm:items-end gap-1 text-xs font-mono text-muted-foreground">
            <div className="flex items-center gap-1.5">
              <Lock className="w-3.5 h-3.5 text-purple-400" />
              <span>State Fingerprint: 0x8a9b7c...44e1</span>
            </div>
            <span className="text-emerald-400">● Verified Invariant</span>
          </div>
        </div>
      </Card>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-4 bg-purple-950/10 border-purple-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Mirrored Subsystems</span>
            <Layers className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-2">7 / 7 Active</div>
          <div className="text-[11px] text-muted-foreground mt-1">100% platform coverage</div>
        </Card>

        <Card className="p-4 bg-emerald-950/10 border-emerald-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Sync Latency</span>
            <Activity className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-2">12.5 ms</div>
          <div className="text-[11px] text-muted-foreground mt-1">Sub-20ms threshold</div>
        </Card>

        <Card className="p-4 bg-blue-950/10 border-blue-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Total Entities Mirrored</span>
            <Cpu className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-blue-400 mt-2">13,899</div>
          <div className="text-[11px] text-muted-foreground mt-1">Agents, tasks, telemetry facts</div>
        </Card>

        <Card className="p-4 bg-indigo-950/10 border-indigo-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Fidelity Score</span>
            <ShieldCheck className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-indigo-400 mt-2">0.998 / 1.0</div>
          <div className="text-[11px] text-muted-foreground mt-1">Calibrated on truth ledger</div>
        </Card>
      </div>

      {/* Subsystem Mirrors Table */}
      <Card className="p-5 border-border/40 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Layers className="w-4 h-4 text-purple-400" />
            <h2 className="text-base font-semibold">Subsystem Synchronization Status</h2>
          </div>
          <Badge variant="outline" size="sm">
            Live Stream
          </Badge>
        </div>

        <div className="space-y-3">
          {subsystems.map((sub, idx) => (
            <div
              key={idx}
              className="flex flex-col sm:flex-row sm:items-center justify-between p-3.5 rounded-lg border border-border/40 bg-secondary/20 hover:bg-secondary/40 transition-colors gap-3"
            >
              <div className="flex items-center gap-3">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                <div>
                  <span className="text-xs font-mono font-bold text-foreground">{sub.name}</span>
                  <div className="text-[11px] text-muted-foreground">
                    {sub.entitiesMirrored.toLocaleString()} live entities tracked
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-4 text-xs font-mono">
                <div className="text-muted-foreground">
                  Sync Latency: <span className="text-foreground font-bold">{sub.syncLatencyMs}ms</span>
                </div>
                <Badge variant="success" size="sm">
                  {sub.status}
                </Badge>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
