import React from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  PlusCircle,
  RotateCcw,
  CheckCircle2,
} from 'lucide-react';

interface SelfImprovementCycleItem {
  id: string;
  targetArea: string;
  hypothesis: string;
  gainPct: number;
  status: 'DEPLOYED' | 'GOVERNANCE_PENDING' | 'IN_EXPERIMENT' | 'ROLLED_BACK';
  merkleRoot: string;
  initiatedAt: string;
  completedAt?: string;
}

export const SelfImprovementTimeline: React.FC = () => {
  const cycles: SelfImprovementCycleItem[] = [
    {
      id: 'sic-501',
      targetArea: 'OCR_DAG_PARALLELIZATION',
      hypothesis: 'Parallel chunk fan-out in DAG execution reduces multi-page invoice extraction latency by >= 35%.',
      gainPct: 42.5,
      status: 'DEPLOYED',
      merkleRoot: '7e8f9a0b1c2d3e4f...990a',
      initiatedAt: '2026-09-12 08:30:00 UTC',
      completedAt: '2026-09-12 08:32:15 UTC',
    },
    {
      id: 'sic-502',
      targetArea: 'EMBEDDING_SCHEMA_CACHE',
      hypothesis: 'In-memory zero-copy cache for recurrent invoice templates reduces token compute by >= 20%.',
      gainPct: 22.0,
      status: 'GOVERNANCE_PENDING',
      merkleRoot: '3c4d5e6f7a8b9c0d...112b',
      initiatedAt: '2026-09-12 09:15:00 UTC',
    },
    {
      id: 'sic-503',
      targetArea: 'LOCK_FREE_TELEMETRY_STREAM',
      hypothesis: 'Atomic lock-free ring buffer prevents EventBus queue stalls during high-burst ingestion.',
      gainPct: 15.8,
      status: 'IN_EXPERIMENT',
      merkleRoot: 'a0b1c2d3e4f5a6b7...448c',
      initiatedAt: '2026-09-12 09:40:00 UTC',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Self-Improvement Timeline</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              CLOSED-LOOP ACTIVE
            </Badge>
            <Badge variant="outline" size="sm">
              AMRS-RSIP Phase 13.9
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Chronological audit of recursive self-improvement cycles across observation, reflection, reasoning, experimentation, governance, and deployment.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="intelligence" size="sm">
            <PlusCircle className="w-3.5 h-3.5 mr-1.5" />
            Initiate Self-Improvement Cycle
          </Button>
        </div>
      </div>

      {/* Timeline Stream */}
      <div className="space-y-4">
        {cycles.map((cycle) => (
          <Card key={cycle.id} className="p-5 border-border/40 space-y-3 hover:border-purple-500/30 transition-colors">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold text-foreground">{cycle.targetArea}</span>
                  <Badge
                    variant={
                      cycle.status === 'DEPLOYED'
                        ? 'success'
                        : cycle.status === 'GOVERNANCE_PENDING'
                        ? 'warning'
                        : 'default'
                    }
                    size="sm"
                  >
                    {cycle.status}
                  </Badge>
                </div>
                <div className="text-xs font-medium text-foreground">{cycle.hypothesis}</div>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="success" size="sm">
                  +{cycle.gainPct}% Measured Gain
                </Badge>
              </div>
            </div>

            <div className="flex flex-wrap items-center justify-between text-xs pt-3 border-t border-border/30 text-muted-foreground font-mono">
              <div className="flex items-center gap-4">
                <span>Merkle Checkpoint: {cycle.merkleRoot}</span>
                <span>Initiated: {cycle.initiatedAt}</span>
              </div>
              <div className="flex items-center gap-2 mt-2 sm:mt-0">
                {cycle.status === 'DEPLOYED' && (
                  <Button variant="outline" size="sm">
                    <RotateCcw className="w-3.5 h-3.5 mr-1 text-amber-400" />
                    Rollback Checkpoint
                  </Button>
                )}
                {cycle.status === 'GOVERNANCE_PENDING' && (
                  <Button variant="primary" size="sm">
                    <CheckCircle2 className="w-3.5 h-3.5 mr-1" />
                    Review & Sign
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
