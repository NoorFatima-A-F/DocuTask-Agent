import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import {
  ArrowRight,
} from 'lucide-react';

interface TrustEdge {
  source: string;
  target: string;
  trustScore: number;
  totalCollaborations: number;
  status: 'OPTIMAL' | 'DEGRADED' | 'EVALUATING';
}

export const TrustNetworkExplorer: React.FC = () => {
  const [edges] = useState<TrustEdge[]>([
    { source: 'agent-exec-01', target: 'agent-plan-01', trustScore: 0.995, totalCollaborations: 142, status: 'OPTIMAL' },
    { source: 'agent-plan-01', target: 'agent-coord-01', trustScore: 0.985, totalCollaborations: 310, status: 'OPTIMAL' },
    { source: 'agent-coord-01', target: 'agent-spec-ocr', trustScore: 0.978, totalCollaborations: 480, status: 'OPTIMAL' },
    { source: 'agent-spec-ocr', target: 'agent-val-sec', trustScore: 0.992, totalCollaborations: 760, status: 'OPTIMAL' },
    { source: 'agent-val-sec', target: 'agent-res-opt', trustScore: 0.965, totalCollaborations: 390, status: 'OPTIMAL' },
    { source: 'agent-res-opt', target: 'agent-coord-01', trustScore: 0.980, totalCollaborations: 240, status: 'OPTIMAL' },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Trust Network Explorer</h1>
            <Badge variant="success" size="sm">
              6 TRUST CHANNELS ACTIVE
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Pairwise trust graph edges between collaborating agents, adaptive Bayesian trust scoring, and historical synergy.
          </p>
        </div>
      </div>

      {/* Network Edges Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {edges.map(e => (
          <Card key={`${e.source}-${e.target}`} className="p-4 border-border/60 space-y-3">
            <div className="flex items-center justify-between">
              <Badge variant="outline" size="sm" className="font-mono">
                {e.totalCollaborations} Interactions
              </Badge>
              <Badge variant="success" size="sm">{e.status}</Badge>
            </div>

            <div className="flex items-center justify-between p-3 rounded bg-muted/20 border border-border/30 text-xs font-mono">
              <span className="font-bold text-foreground">{e.source}</span>
              <ArrowRight className="w-3.5 h-3.5 text-primary" />
              <span className="font-bold text-foreground">{e.target}</span>
            </div>

            <div>
              <div className="flex items-center justify-between text-xs mb-1.5 font-mono">
                <span className="text-muted-foreground">Pairwise Trust Score</span>
                <span className="font-bold text-emerald-400">{(e.trustScore * 100).toFixed(1)}%</span>
              </div>
              <div className="w-full bg-background h-2 rounded-full overflow-hidden">
                <div className="bg-emerald-400 h-full rounded-full" style={{ width: `${e.trustScore * 100}%` }} />
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
