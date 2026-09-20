import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  PlusCircle,
  Lock,
} from 'lucide-react';

interface PolicyProposalItem {
  id: string;
  policyName: string;
  category: string;
  currentRule: string;
  proposedRule: string;
  rationale: string;
  evidence: string[];
  latencyGainPct: number;
  status: 'PENDING_APPROVAL' | 'CANARY' | 'APPROVED' | 'ACTIVE';
  sha256Hash: string;
}

export const PolicyEvolutionCenter: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'ALL' | 'PENDING' | 'ACTIVE'>('ALL');

  const proposals: PolicyProposalItem[] = [
    {
      id: 'pol-prop-701',
      policyName: 'Dynamic Worker Concurrency Quota',
      category: 'PLANNER_CONCURRENCY',
      currentRule: 'Limit worker pool max concurrency to 4 simultaneous tasks per DAG.',
      proposedRule: 'Dynamically scale worker pool concurrency up to 12 tasks when host memory utilization is < 60%.',
      rationale: 'Batch invoice extraction DAGs queue unnecessarily under low system memory load.',
      evidence: ['obs-latency-spike-ocr', 'exp-dynamic-fanout'],
      latencyGainPct: 44.0,
      status: 'APPROVED',
      sha256Hash: '4a9c8b7e6f5d4c3b2a1e0f9d8c7b6a5e4d3c2b1a0f9e8d7c6b5a4f3e2d1c0b9a',
    },
    {
      id: 'pol-prop-702',
      policyName: 'SLA Budget Ceiling Dynamic Scaling',
      category: 'RESOURCE_ALLOCATION',
      currentRule: 'Hard cap token budget at $0.05 per document across all tiers.',
      proposedRule: 'Dynamically allow budget scale up to $0.065 for verified high-complexity multi-page legal contracts.',
      rationale: 'Prevents false fallback degradation on highly complex documents without violating organization budget SLA.',
      evidence: ['obs-complex-legal-99', 'exp-triadic-consensus'],
      latencyGainPct: 18.5,
      status: 'CANARY',
      sha256Hash: '7b8a9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b',
    },
    {
      id: 'pol-prop-703',
      policyName: 'Zero-Knowledge Cryptographic Schema Caching',
      category: 'SECURITY_QUORUM',
      currentRule: 'Verify full Ed25519 signature chain on every intermediate sub-task state.',
      proposedRule: 'Cache cryptographic verification proofs for static document schemas within 5-minute zero-trust TTL.',
      rationale: 'Reduces repeated SHA-256 verification overhead by 85ms on bulk recurring invoices.',
      evidence: ['obs-zk-cache-proof', 'rrt-reflection-t5'],
      latencyGainPct: 22.0,
      status: 'PENDING_APPROVAL',
      sha256Hash: '1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d',
    },
  ];

  const filteredProposals = proposals.filter((p) => {
    if (activeTab === 'PENDING') return p.status === 'PENDING_APPROVAL';
    if (activeTab === 'ACTIVE') return p.status === 'ACTIVE' || p.status === 'APPROVED';
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Policy Evolution Center</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              GOVERNANCE ENFORCED
            </Badge>
            <Badge variant="outline" size="sm">
              AMRS-RSIP Phase 13.9
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Empirical runtime policy evolution, canary testing, SHA-256 cryptographic verification, and dual-signature approval workflows.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="intelligence" size="sm">
            <PlusCircle className="w-3.5 h-3.5 mr-1.5" />
            Propose Policy Evolution
          </Button>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 border-b border-border/40 pb-2">
        {(['ALL', 'PENDING', 'ACTIVE'] as const).map((tab) => (
          <Button
            key={tab}
            variant={activeTab === tab ? 'primary' : 'ghost'}
            size="sm"
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </Button>
        ))}
      </div>

      {/* Proposals List */}
      <div className="space-y-4">
        {filteredProposals.map((prop) => (
          <Card key={prop.id} className="p-5 border-border/40 space-y-4 hover:border-purple-500/30 transition-colors">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <h2 className="text-base font-semibold text-foreground">{prop.policyName}</h2>
                  <Badge
                    variant={
                      prop.status === 'APPROVED' || prop.status === 'ACTIVE'
                        ? 'success'
                        : prop.status === 'CANARY'
                        ? 'warning'
                        : 'default'
                    }
                    size="sm"
                  >
                    {prop.status}
                  </Badge>
                </div>
                <span className="text-xs font-mono text-muted-foreground">Category: {prop.category}</span>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="success" size="sm">
                  +{prop.latencyGainPct}% Efficiency
                </Badge>
              </div>
            </div>

            {/* Current vs Proposed Rules */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-3.5 rounded-lg border border-border/40 bg-secondary/20 space-y-1.5">
                <span className="text-xs font-semibold text-muted-foreground">Current Operating Rule</span>
                <p className="text-xs font-mono text-foreground">{prop.currentRule}</p>
              </div>

              <div className="p-3.5 rounded-lg border border-purple-500/30 bg-purple-950/10 space-y-1.5">
                <span className="text-xs font-semibold text-purple-400">Proposed Evolutionary Rule</span>
                <p className="text-xs font-mono text-purple-200">{prop.proposedRule}</p>
              </div>
            </div>

            {/* Rationale & Evidence */}
            <div className="text-xs text-muted-foreground space-y-1">
              <div><strong className="text-foreground">Empirical Rationale:</strong> {prop.rationale}</div>
              <div className="flex items-center gap-2 pt-1 font-mono text-[11px]">
                <span>Evidence Backing:</span>
                {prop.evidence.map((ev, idx) => (
                  <span key={idx} className="px-1.5 py-0.5 rounded bg-secondary/50 text-foreground">
                    {ev}
                  </span>
                ))}
              </div>
            </div>

            {/* Cryptographic SHA-256 Signature Footer */}
            <div className="flex items-center justify-between text-[11px] text-muted-foreground pt-3 border-t border-border/30 font-mono">
              <div className="flex items-center gap-1.5 truncate max-w-md">
                <Lock className="w-3.5 h-3.5 text-purple-400 flex-shrink-0" />
                <span className="truncate">SHA-256 Hash: {prop.sha256Hash}</span>
              </div>
              {prop.status === 'PENDING_APPROVAL' && (
                <Button variant="primary" size="sm">
                  Cast Governance Vote
                </Button>
              )}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
