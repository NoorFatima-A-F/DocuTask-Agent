import React from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  ShieldCheck,
  Lock,
  UserCheck,
} from 'lucide-react';

interface ApprovalItem {
  id: string;
  targetProposalId: string;
  proposalType: string;
  approverRole: string;
  decision: 'APPROVED' | 'PENDING' | 'REJECTED';
  rationale: string;
  signature: string;
  timestamp: string;
}

export const GovernanceApprovalCenter: React.FC = () => {
  const approvals: ApprovalItem[] = [
    {
      id: 'appr-301',
      targetProposalId: 'pol-prop-701',
      proposalType: 'POLICY_UPGRADE',
      approverRole: 'EXECUTIVE_DIRECTOR',
      decision: 'APPROVED',
      rationale: 'Empirically proven via historical replay experiment with p < 0.001 and 44% latency reduction.',
      signature: '0x3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b',
      timestamp: '2026-09-12 09:30:15 UTC',
    },
    {
      id: 'appr-302',
      targetProposalId: 'arch-opt-601',
      proposalType: 'ARCHITECTURE_REFACTOR',
      approverRole: 'SECURITY_AUDITOR',
      decision: 'APPROVED',
      rationale: 'Multicast bus refactoring validated against chaos fault injection tests.',
      signature: '0x9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2e1f0d9c8b7a6e5f4d3c2b1a0f9e8d',
      timestamp: '2026-09-12 09:45:22 UTC',
    },
    {
      id: 'appr-303',
      targetProposalId: 'pol-prop-703',
      proposalType: 'SECURITY_QUORUM',
      approverRole: 'CHIEF_ARCHITECT',
      decision: 'PENDING',
      rationale: 'Pending second threshold cryptographic signature verification.',
      signature: '0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b',
      timestamp: '2026-09-12 10:05:00 UTC',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Governance Approval Center</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              DUAL-SIGNATURE THRESHOLD ACTIVE
            </Badge>
            <Badge variant="outline" size="sm">
              AMRS-RSIP Phase 13.9
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Cryptographic digital signature verification, anti-usurpation guardrails, and audit ledger for autonomous platform mutations.
          </p>
        </div>
      </div>

      {/* Invariant Policy Banner */}
      <Card className="p-4 bg-purple-950/20 border-purple-500/30 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-purple-500/10 rounded-lg border border-purple-500/20 text-purple-400">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-semibold text-purple-400 uppercase tracking-wider">Anti-Usurpation Core Invariant</span>
            <div className="text-xs text-foreground font-medium mt-0.5">
              No autonomous policy or structural change may self-deploy without valid cryptographic multi-signature quorum.
            </div>
          </div>
        </div>
        <Badge variant="success" size="sm">Invariant 100% Intact</Badge>
      </Card>

      {/* Approvals List */}
      <div className="space-y-4">
        {approvals.map((appr) => (
          <Card key={appr.id} className="p-5 border-border/40 space-y-3 hover:border-purple-500/30 transition-colors">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold text-foreground">{appr.targetProposalId}</span>
                  <Badge
                    variant={
                      appr.decision === 'APPROVED'
                        ? 'success'
                        : appr.decision === 'PENDING'
                        ? 'warning'
                        : 'error'
                    }
                    size="sm"
                  >
                    {appr.decision}
                  </Badge>
                </div>
                <span className="text-xs text-purple-300 font-semibold">{appr.proposalType}</span>
              </div>
              <div className="flex items-center gap-2 text-xs font-mono text-muted-foreground">
                <UserCheck className="w-3.5 h-3.5 text-purple-400" />
                <span>Approver: {appr.approverRole}</span>
              </div>
            </div>

            <p className="text-xs text-muted-foreground">{appr.rationale}</p>

            <div className="flex flex-col sm:flex-row sm:items-center justify-between text-[11px] text-muted-foreground pt-3 border-t border-border/30 font-mono gap-2">
              <div className="flex items-center gap-1.5 truncate max-w-md">
                <Lock className="w-3.5 h-3.5 text-purple-400 flex-shrink-0" />
                <span className="truncate">Digital Signature: {appr.signature}</span>
              </div>
              <div className="flex items-center gap-2">
                <span>{appr.timestamp}</span>
                {appr.decision === 'PENDING' && (
                  <Button variant="primary" size="sm">
                    Sign & Authorize
                  </Button>
                )}
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
