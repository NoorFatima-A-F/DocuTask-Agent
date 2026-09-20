import React, { useState } from 'react';
import { useMissionControl } from '../../context/MissionControlContext';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';

export const HumanControlSection: React.FC = () => {
  const {
    state,
    pauseMission,
    resumeMission,
    abortMission,
    injectSentinelState,
    resetInitialState,
  } = useMissionControl();

  const { isPaused, humanAuditLogs } = state;
  const [abortReason, setAbortReason] = useState<string>('');
  const [showAbortPrompt, setShowAbortPrompt] = useState<boolean>(false);

  return (
    <section className="w-full mt-8 mb-12">
      <Card variant="default" className="border-[#1E293B] bg-[#0F172A]/80 backdrop-blur-md">
        <CardHeader className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="intelligence" size="sm">
                STAGE 10 • HUMAN + AI COLLABORATION
              </Badge>
              <span className="text-xs text-[#94A3B8] font-mono">
                {humanAuditLogs.length} Cryptographic Audit Receipts
              </span>
            </div>
            <CardTitle className="mt-2 text-lg lg:text-xl font-bold text-[#F8FAFC]">
              Human Control & Governance Cockpit
            </CardTitle>
            <p className="mt-1 text-xs text-[#94A3B8]">
              The operator retains full supervisory authority. Interrupt, pause, inspect, override, or inject Zero-Fabrication sentinels with deterministic audit logging.
            </p>
          </div>
        </CardHeader>

        <CardContent className="p-6 space-y-6">
          {/* Main Control Action Bar */}
          <div className="flex flex-wrap items-center gap-3 p-4 rounded-xl bg-[#131D35] border border-[#1E293B]">
            {isPaused ? (
              <Button
                variant="intelligence"
                size="md"
                onClick={() => resumeMission('Operator manual resume')}
              >
                ▶ Resume Autonomous Cognition
              </Button>
            ) : (
              <Button
                variant="secondary"
                size="md"
                onClick={() => pauseMission('Operator manual pause')}
              >
                ⏸ Pause Mission
              </Button>
            )}

            <Button
              variant="outline"
              size="md"
              onClick={injectSentinelState}
              className="text-amber-400 border-amber-500/40 hover:bg-amber-950/30"
            >
              ⚠ Simulate Zero-Fabrication Sentinel
            </Button>

            <Button
              variant="ghost"
              size="md"
              onClick={resetInitialState}
            >
              🔄 Reset Initial Demo State
            </Button>

            <Button
              variant="danger"
              size="md"
              onClick={() => setShowAbortPrompt(true)}
            >
              ⏹ Abort Mission
            </Button>
          </div>

          {/* Abort Confirmation Dialog */}
          {showAbortPrompt && (
            <div className="p-4 rounded-xl bg-red-950/40 border border-red-500/40 space-y-3">
              <h4 className="text-xs font-bold text-red-400 uppercase tracking-wider">
                Confirm Mission Abort Action
              </h4>
              <p className="text-xs text-[#94A3B8]">
                Please enter a formal reason for terminating this autonomous mission. An append-only audit receipt will be signed.
              </p>
              <input
                type="text"
                value={abortReason}
                onChange={(e) => setAbortReason(e.target.value)}
                placeholder="Reason for aborting mission..."
                className="w-full bg-[#131D35] border border-[#334155] rounded-lg px-3 py-2 text-xs font-mono text-[#F8FAFC] focus:outline-none focus:border-red-400"
              />
              <div className="flex justify-end gap-2">
                <Button variant="ghost" size="sm" onClick={() => setShowAbortPrompt(false)}>
                  Cancel
                </Button>
                <Button
                  variant="danger"
                  size="sm"
                  onClick={() => {
                    abortMission(abortReason || 'Operator termination');
                    setShowAbortPrompt(false);
                  }}
                >
                  Confirm Abort
                </Button>
              </div>
            </div>
          )}

          {/* Cryptographic Audit Receipts Timeline */}
          <div>
            <span className="text-[11px] font-bold uppercase tracking-wider text-[#64748B] block mb-3">
              Supervisory Audit Receipts (Signed & Immutable)
            </span>
            <div className="space-y-2">
              {humanAuditLogs.map((log) => (
                <div
                  key={log.id}
                  className="p-3 rounded-lg bg-[#131D35]/70 border border-[#1E293B] flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs font-mono"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-[#00D2FF] font-bold">[{log.timestampUtc}]</span>
                    <Badge variant="intelligence" size="sm">
                      {log.action}
                    </Badge>
                    <span className="text-[#F8FAFC]">{log.reason}</span>
                  </div>

                  <div className="flex items-center gap-3 text-[#64748B] text-[11px] shrink-0">
                    <span>By: {log.triggeredBy}</span>
                    <span className="text-[#A855F7] truncate max-w-[120px]" title={log.auditSha256Receipt}>
                      Receipt: {log.auditSha256Receipt.substring(0, 8)}...
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
    </section>
  );
};
