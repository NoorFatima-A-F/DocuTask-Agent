import React, { useState } from 'react';
import {
  RotateCcw,
  CheckCircle2,
  RefreshCw,
  Layers,
  Sparkles
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

interface RecoveryOrchestrationCenterProps {
  missionId?: string;
}

export const RecoveryOrchestrationCenter: React.FC<RecoveryOrchestrationCenterProps> = ({
  missionId = 'mission-current',
}) => {
  const [recoveries] = useState([
    {
      recoveryId: 'rec-chk-8b1a9c',
      missionId: missionId,
      strategy: 'CHECKPOINT_ROLLBACK',
      status: 'COMPLETED',
      restoredStep: 4,
      invariantsRestored: 12,
      elapsedMs: 180.0,
      timestamp: '2026-09-12T10:14:05Z',
    },
    {
      recoveryId: 'rec-opt-2f4e0d',
      missionId: 'mission-002',
      strategy: 'OPTIMIZATION_RETRY',
      status: 'COMPLETED',
      restoredStep: 1,
      invariantsRestored: 15,
      elapsedMs: 145.0,
      timestamp: '2026-09-12T09:30:12Z',
    },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <RotateCcw className="w-5 h-5 text-indigo-400" />
            Recovery Orchestration & Mission Continuation Center
          </h2>
          <p className="text-sm text-slate-400">
            Multi-tier checkpoint restoration (Phase 13.4), policy rollback (Phase 13.5), dynamic re-optimization (Phase 13.6), and mission continuation for: <code className="text-indigo-300 font-mono text-xs">{missionId}</code>
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" size="md">
            State Consistency: 100% VERIFIED
          </Badge>
          <button className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700">
            <RefreshCw className="w-3.5 h-3.5" />
            Scan Checkpoints
          </button>
        </div>
      </div>

      {/* Recovery Strategy Dispatcher */}
      <Card className="p-5 bg-slate-900 border-slate-800 space-y-4 font-mono">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <Layers className="w-4 h-4 text-cyan-400" />
          Multi-Tier Recovery Orchestrator
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div className="p-3.5 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
            <span className="text-xs font-bold text-slate-200 block">Tier 1: Checkpoint Snapshot</span>
            <p className="text-[11px] text-slate-400">Restores deterministic execution snapshot from Phase 13.4 timeline.</p>
            <Badge variant="intelligence" size="sm">Deterministic Restore</Badge>
          </div>

          <div className="p-3.5 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
            <span className="text-xs font-bold text-slate-200 block">Tier 2: Policy Fallback</span>
            <p className="text-[11px] text-slate-400">Rolls back learned heuristics to safe baseline guardrails (Phase 13.5).</p>
            <Badge variant="outline" size="sm">Policy Invariant</Badge>
          </div>

          <div className="p-3.5 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
            <span className="text-xs font-bold text-slate-200 block">Tier 3: Dynamic Re-Optimization</span>
            <p className="text-[11px] text-slate-400">Re-solves Pareto frontier under degraded capacity (Phase 13.6).</p>
            <Badge variant="success" size="sm">Pareto Frontier</Badge>
          </div>
        </div>
      </Card>

      {/* Recovery Execution History */}
      <div className="space-y-3 font-mono">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-emerald-400" />
          Recent Mission Recovery Invocations
        </h3>

        {recoveries.map((r) => (
          <Card key={r.recoveryId} className="p-4 bg-slate-900 border-slate-800 space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-indigo-400">{r.recoveryId}</span>
                <Badge variant="intelligence" size="sm">{r.strategy}</Badge>
                <span className="text-xs text-slate-300">Mission: {r.missionId}</span>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="success" size="sm">
                  <CheckCircle2 className="w-3 h-3 mr-1" />
                  {r.status}
                </Badge>
                <span className="text-xs text-slate-400">{r.elapsedMs}ms</span>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-2 text-[11px] bg-slate-950 p-2.5 rounded border border-slate-800 text-slate-400">
              <span>Restored Step: <strong className="text-slate-200">{r.restoredStep}</strong></span>
              <span>Invariants Restored: <strong className="text-emerald-400">{r.invariantsRestored}</strong></span>
              <span>Timestamp: <strong className="text-slate-300">{new Date(r.timestamp).toLocaleTimeString()}</strong></span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
