import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ConsensusAnalyzerView: React.FC = () => {
  const contributions = [
    {
      agent: 'ChiefPlanner',
      department: 'Planning Dept',
      confidence: 0.98,
      recommendation: 'APPROVE',
      riskScore: 0.02,
      weight: 1.2,
      evidenceHashes: ['0x8f2a...c31b', '0x3c7e...b44a'],
      rationale: 'Topological invariant verification satisfied all constraints with zero DAG cycle risk.',
    },
    {
      agent: 'ComplianceGuard',
      department: 'Governance Dept',
      confidence: 0.96,
      recommendation: 'APPROVE',
      riskScore: 0.04,
      weight: 1.1,
      evidenceHashes: ['0x8f2a...c31b'],
      rationale: 'Enterprise policy boundary checked: data retention SLA verified.',
    },
    {
      agent: 'ValidationWorker',
      department: 'QA Dept',
      confidence: 0.92,
      recommendation: 'APPROVE',
      riskScore: 0.08,
      weight: 1.0,
      evidenceHashes: ['0x991a...fe82'],
      rationale: 'Mathematical checksum and Merkle leaf verification passed.',
    },
    {
      agent: 'CostAuditor',
      department: 'Finance Dept',
      confidence: 0.88,
      recommendation: 'APPROVE',
      riskScore: 0.12,
      weight: 0.9,
      evidenceHashes: ['0x8f2a...c31b'],
      rationale: 'Token spend within $0.015 threshold ceiling.',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Consensus Intelligence & Deliberation</h1>
            <Badge variant="intelligence" size="sm">Pillar 7</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Evidence-weighted multi-agent consensus synthesis replacing naive majority voting with mathematically grounded deliberation.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            Agreement Score: 98.4%
          </Badge>
          <Badge variant="outline" size="md">
            Composite Conf: 96.2%
          </Badge>
        </div>
      </div>

      {/* Consensus Verdict Card */}
      <Card className="p-5 border-emerald-500/30 bg-emerald-950/10">
        <div className="flex items-center justify-between border-b border-border/40 pb-3 mb-3">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-muted-foreground">Winning Synthesis:</span>
            <Badge variant="success" size="md">APPROVE WITH FULL ATTESTATION</Badge>
          </div>
          <span className="text-xs font-mono text-emerald-400">Dominant Evidence: 0x8f2a...c31b</span>
        </div>
        <p className="text-xs text-foreground">
          4 independent departments contributed weighted deliberation. 0 conflict edges detected across participating agents.
        </p>
      </Card>

      {/* Agent Contributions List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {contributions.map((c) => (
          <Card key={c.agent} className="p-4 border-border/60">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-xs text-foreground">{c.agent}</span>
                <span className="text-[10px] text-muted-foreground font-mono">[{c.department}]</span>
              </div>
              <Badge variant="success" size="sm">{c.recommendation}</Badge>
            </div>

            <p className="text-xs text-muted-foreground mb-3">{c.rationale}</p>

            <div className="grid grid-cols-3 gap-2 p-2 rounded bg-muted/20 border border-border/40 text-center text-xs">
              <div>
                <div className="text-[10px] text-muted-foreground">Confidence</div>
                <div className="font-mono font-bold text-emerald-400">{(c.confidence * 100).toFixed(1)}%</div>
              </div>
              <div>
                <div className="text-[10px] text-muted-foreground">Risk Score</div>
                <div className="font-mono font-bold text-foreground">{(c.riskScore * 100).toFixed(1)}%</div>
              </div>
              <div>
                <div className="text-[10px] text-muted-foreground">Weight Mult</div>
                <div className="font-mono font-bold text-primary">{c.weight.toFixed(1)}x</div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
