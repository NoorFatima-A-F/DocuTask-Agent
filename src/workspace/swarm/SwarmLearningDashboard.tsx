import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import {
  Sparkles,
} from 'lucide-react';

interface PatternItem {
  id: string;
  name: string;
  type: string;
  roles: string[];
  successRate: number;
  latencyMs: number;
  description: string;
}

export const SwarmLearningDashboard: React.FC = () => {
  const [patterns] = useState<PatternItem[]>([
    {
      id: 'pat-001',
      name: 'Triadic Verification Pipeline',
      type: 'CROSS_VALIDATION_TRIAD',
      roles: ['SPECIALIST', 'VALIDATOR', 'REVIEWER'],
      successRate: 0.998,
      latencyMs: 310.0,
      description: 'Specialist extracts metadata, validator checks cryptographic checksums, reviewer verifies business invariants.',
    },
    {
      id: 'pat-002',
      name: 'Hierarchical Delegation Matrix',
      type: 'HIERARCHICAL_DELEGATION',
      roles: ['EXECUTIVE', 'PLANNER', 'COORDINATOR', 'RESOURCE'],
      successRate: 0.985,
      latencyMs: 450.0,
      description: 'Executive partitions high-level mission into parallel sub-graphs governed by Coordinator under Resource budget constraints.',
    },
    {
      id: 'pat-003',
      name: 'Bargaining-Based Task Allocation',
      type: 'DECOMPOSITION_PIPELINE',
      roles: ['NEGOTIATOR', 'COORDINATOR', 'SPECIALIST'],
      successRate: 0.992,
      latencyMs: 220.0,
      description: 'Auctions high-priority extraction batches to available specialists using SLA & compute cost bargaining.',
    },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Swarm Collective Learning Dashboard</h1>
            <Badge variant="intelligence" size="sm">
              3 STRATEGIES MINED
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Mined collaboration patterns, semantic swarm knowledge graph, emergent multi-agent coordination strategies, and efficiency benchmarks.
          </p>
        </div>
      </div>

      {/* Mined Patterns List */}
      <div className="space-y-4">
        {patterns.map(p => (
          <Card key={p.id} className="p-5 border-border/60 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border/40 pb-3">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-cyan-400" />
                <h3 className="font-bold text-sm">{p.name}</h3>
                <Badge variant="outline" size="sm" className="font-mono">{p.type}</Badge>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="success" size="sm">
                  {(p.successRate * 100).toFixed(1)}% Success Rate
                </Badge>
                <span className="text-xs font-mono text-muted-foreground">{p.latencyMs} ms Avg</span>
              </div>
            </div>

            <p className="text-xs text-muted-foreground leading-relaxed">{p.description}</p>

            <div>
              <span className="text-xs font-semibold text-muted-foreground block mb-2">Required Agent Roles in Triad</span>
              <div className="flex flex-wrap gap-2">
                {p.roles.map(r => (
                  <Badge key={r} variant="outline" size="md" className="font-mono">
                    {r}
                  </Badge>
                ))}
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
