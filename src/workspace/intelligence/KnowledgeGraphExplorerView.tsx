import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const KnowledgeGraphExplorerView: React.FC = () => {
  const nodes = [
    { id: 'msn_1001', type: 'MISSION', label: 'Invoice Mission #1001' },
    { id: 'ent_invoice', type: 'ENTITY', label: 'Invoice Schema v2' },
    { id: 'strat_fast', type: 'STRATEGY', label: 'Fast-Track Fan-Out Strategy' },
    { id: 'pol_gdpr', type: 'POLICY', label: 'EU Data Boundary Policy' },
    { id: 'ev_001', type: 'EVIDENCE', label: 'Merkle Root 0x8f2a...c31b' },
    { id: 'out_json', type: 'OUTCOME', label: 'Verified Document JSON' },
  ];

  const edges = [
    { from: 'msn_1001', to: 'ent_invoice', rel: 'PROCESSES_SCHEMA', evidence: '0x8f2a...c31b' },
    { from: 'msn_1001', to: 'strat_fast', rel: 'APPLIES_STRATEGY', evidence: '0x8f2a...c31b' },
    { from: 'strat_fast', to: 'pol_gdpr', rel: 'GOVERNED_BY', evidence: '0x8f2a...c31b' },
    { from: 'msn_1001', to: 'ev_001', rel: 'SUPPORTED_BY_EVIDENCE', evidence: '0x8f2a...c31b' },
    { from: 'ev_001', to: 'out_json', rel: 'PRODUCED_OUTCOME', evidence: '0x8f2a...c31b' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Adaptive Knowledge Graph</h1>
            <Badge variant="intelligence" size="sm">Pillar 6</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Evidence-linked knowledge graph connecting Missions &rarr; Entities &rarr; Strategies &rarr; Policies &rarr; Evidence &rarr; Outcomes.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            Nodes: {nodes.length} | Edges: {edges.length}
          </Badge>
        </div>
      </div>

      {/* Graph Visualizer Cards */}
      <Card className="p-5 border-border/60">
        <h3 className="text-sm font-semibold text-foreground mb-3">Knowledge Graph Active Topology</h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-6">
          {nodes.map((n) => (
            <div key={n.id} className="p-3 rounded-lg border border-border/40 bg-muted/10">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs text-primary font-semibold">{n.id}</span>
                <Badge variant={n.type === 'EVIDENCE' ? 'success' : n.type === 'STRATEGY' ? 'intelligence' : 'outline'} size="sm">
                  {n.type}
                </Badge>
              </div>
              <div className="text-xs font-medium text-foreground mt-1">{n.label}</div>
            </div>
          ))}
        </div>

        <h3 className="text-sm font-semibold text-foreground mb-3">Cryptographically Linked Graph Relationships</h3>
        <div className="space-y-2">
          {edges.map((e, idx) => (
            <div key={idx} className="p-2.5 rounded border border-border/40 bg-muted/5 flex items-center justify-between text-xs">
              <div className="flex items-center gap-2">
                <span className="font-mono font-semibold text-foreground">{e.from}</span>
                <span className="text-primary font-mono">&rarr; [{e.rel}] &rarr;</span>
                <span className="font-mono font-semibold text-foreground">{e.to}</span>
              </div>
              <div className="text-[11px] font-mono text-muted-foreground">
                Proof Hash: <span className="text-emerald-400">{e.evidence}</span>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
