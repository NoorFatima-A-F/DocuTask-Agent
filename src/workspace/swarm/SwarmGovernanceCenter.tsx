import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import {
  Key,
  Lock,
  ArrowRight,
} from 'lucide-react';

interface DelegationGrantItem {
  id: string;
  delegator: string;
  delegatorRole: string;
  delegatee: string;
  delegateeRole: string;
  scope: string;
  depth: number;
  signature: string;
  grantedAt: string;
}

export const SwarmGovernanceCenter: React.FC = () => {
  const [grants] = useState<DelegationGrantItem[]>([
    {
      id: 'grant_001',
      delegator: 'agent-exec-01',
      delegatorRole: 'EXECUTIVE (Tier 1)',
      delegatee: 'agent-plan-01',
      delegateeRole: 'PLANNER (Tier 2)',
      scope: 'MISSION_DECOMPOSITION',
      depth: 1,
      signature: 'a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2',
      grantedAt: '14:22:00.050',
    },
    {
      id: 'grant_002',
      delegator: 'agent-plan-01',
      delegatorRole: 'PLANNER (Tier 2)',
      delegatee: 'agent-coord-01',
      delegateeRole: 'COORDINATOR (Tier 2)',
      scope: 'DAG_TASK_DISPATCH',
      depth: 2,
      signature: 'c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4',
      grantedAt: '14:22:00.080',
    },
    {
      id: 'grant_003',
      delegator: 'agent-coord-01',
      delegatorRole: 'COORDINATOR (Tier 2)',
      delegatee: 'agent-spec-ocr',
      delegateeRole: 'SPECIALIST (Tier 4)',
      scope: 'IMAGE_PARSE_EXECUTE',
      depth: 3,
      signature: 'e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6',
      grantedAt: '14:22:00.120',
    },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Swarm Governance Center</h1>
            <Badge variant="success" size="sm">
              ANTI-USURPATION ENFORCED
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Tiered authority hierarchy (Tiers 1-5), cryptographic delegation contracts, and invariant audit logs.
          </p>
        </div>
      </div>

      {/* Authority Tiers Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-5 gap-3">
        <Card className="p-3 bg-purple-950/20 border-purple-500/30">
          <span className="text-[10px] font-bold text-purple-400 uppercase tracking-wider block">Tier 1 Executive</span>
          <span className="text-xs font-semibold mt-1 block">Executive Director</span>
          <span className="text-[10px] text-muted-foreground mt-0.5 block">Mission Authority</span>
        </Card>

        <Card className="p-3 bg-indigo-950/20 border-indigo-500/30">
          <span className="text-[10px] font-bold text-indigo-400 uppercase tracking-wider block">Tier 2 Orchestrator</span>
          <span className="text-xs font-semibold mt-1 block">Planner & Coord</span>
          <span className="text-[10px] text-muted-foreground mt-0.5 block">DAG Dispatch</span>
        </Card>

        <Card className="p-3 bg-blue-950/20 border-blue-500/30">
          <span className="text-[10px] font-bold text-blue-400 uppercase tracking-wider block">Tier 3 Governor</span>
          <span className="text-xs font-semibold mt-1 block">Resource & Security</span>
          <span className="text-[10px] text-muted-foreground mt-0.5 block">Policy Control</span>
        </Card>

        <Card className="p-3 bg-emerald-950/20 border-emerald-500/30">
          <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">Tier 4 Operator</span>
          <span className="text-xs font-semibold mt-1 block">Specialists</span>
          <span className="text-[10px] text-muted-foreground mt-0.5 block">Task Execution</span>
        </Card>

        <Card className="p-3 bg-teal-950/20 border-teal-500/30">
          <span className="text-[10px] font-bold text-teal-400 uppercase tracking-wider block">Tier 5 Auditor</span>
          <span className="text-xs font-semibold mt-1 block">Observers</span>
          <span className="text-[10px] text-muted-foreground mt-0.5 block">Zero Authority / Audit</span>
        </Card>
      </div>

      {/* Active Delegation Grants */}
      <Card className="p-5 border-border/60">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Key className="w-4 h-4 text-primary" />
            <h3 className="font-semibold text-sm">Active Delegation Grants</h3>
          </div>
          <span className="text-xs text-muted-foreground">Max Depth: 3 Enforced</span>
        </div>

        <div className="space-y-3">
          {grants.map(g => (
            <div key={g.id} className="p-4 rounded-lg bg-muted/20 border border-border/40 space-y-2">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <Badge variant="outline" size="sm" className="font-mono">{g.id}</Badge>
                  <span className="font-bold text-xs">Scope: {g.scope}</span>
                </div>
                <Badge variant="success" size="sm">DEPTH {g.depth} / 3</Badge>
              </div>

              <div className="flex items-center gap-2 text-xs font-mono">
                <div>
                  <span className="font-bold text-foreground">{g.delegator}</span>
                  <span className="text-[10px] text-muted-foreground block">{g.delegatorRole}</span>
                </div>
                <ArrowRight className="w-3.5 h-3.5 text-primary shrink-0" />
                <div>
                  <span className="font-bold text-foreground">{g.delegatee}</span>
                  <span className="text-[10px] text-muted-foreground block">{g.delegateeRole}</span>
                </div>
              </div>

              <div className="p-2 rounded bg-background/60 border border-border/30 text-[10px] font-mono text-muted-foreground flex items-center gap-2">
                <Lock className="w-3 h-3 text-primary shrink-0" />
                <span className="truncate">Delegation Grant Signature: {g.signature}</span>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
