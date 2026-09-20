import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  RefreshCw,
} from 'lucide-react';

interface EvidenceNodeItem {
  id: string;
  type: 'SUBSYSTEM' | 'METRIC_ANOMALY' | 'MISSION' | 'FAILURE_PATTERN';
  label: string;
  details: string;
  connections: number;
}

interface EvidenceEdgeItem {
  source: string;
  target: string;
  relationship: string;
  weight: number;
}

export const StrategicKnowledgeGraph: React.FC = () => {
  const [selectedNodeId, setSelectedNodeId] = useState<string>('obs-node-1');

  const nodes: EvidenceNodeItem[] = [
    {
      id: 'obs-node-1',
      type: 'SUBSYSTEM',
      label: 'APDLE Live DAG Scheduler',
      details: 'Current greedy critical-path heuristic scheduler operating at 180ms baseline.',
      connections: 3,
    },
    {
      id: 'obs-node-2',
      type: 'METRIC_ANOMALY',
      label: 'OCR Burst Serialization',
      details: 'Queue depth spiked to 14 tasks during 50-page PDF ingestion (+128% latency).',
      connections: 2,
    },
    {
      id: 'obs-node-3',
      type: 'SUBSYSTEM',
      label: 'Ed25519 Validator Strike Team',
      details: 'Triadic consensus verification engine with 100% mathematical zero-fabrication ratio.',
      connections: 2,
    },
    {
      id: 'obs-node-4',
      type: 'FAILURE_PATTERN',
      label: 'Repeated Cold Embedding Overhead',
      details: 'Redundant token embedding calls for recurrent corporate balance sheet templates.',
      connections: 1,
    },
  ];

  const edges: EvidenceEdgeItem[] = [
    { source: 'OCR Burst Serialization', target: 'APDLE Live DAG Scheduler', relationship: 'CONSTRAINED_BY', weight: 0.88 },
    { source: 'APDLE Live DAG Scheduler', target: 'Ed25519 Validator Strike Team', relationship: 'CORRELATES_WITH', weight: 0.96 },
    { source: 'Repeated Cold Embedding Overhead', target: 'APDLE Live DAG Scheduler', relationship: 'CAUSED_BY', weight: 0.74 },
  ];

  const selectedNode = nodes.find((n) => n.id === selectedNodeId) ?? nodes[0]!;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Strategic Knowledge Graph</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              CROSS-MISSION GRAPH ONLINE
            </Badge>
            <Badge variant="outline" size="sm">
              AMRS-RSIP Phase 13.9
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Queryable Strategic Evidence Graph connecting operational incidents, bottlenecks, failure patterns, and verifiable causal links.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <RefreshCw className="w-3.5 h-3.5 mr-1.5" />
            Re-index Graph
          </Button>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Nodes List */}
        <div className="lg:col-span-5 space-y-3">
          <h2 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            Evidence Nodes ({nodes.length})
          </h2>
          {nodes.map((n) => (
            <Card
              key={n.id}
              onClick={() => setSelectedNodeId(n.id)}
              className={`p-4 cursor-pointer transition-all border ${
                selectedNodeId === n.id
                  ? 'border-purple-500/60 bg-purple-950/30 shadow-sm'
                  : 'border-border/40 bg-secondary/10 hover:bg-secondary/20'
              }`}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="space-y-1">
                  <Badge
                    variant={
                      n.type === 'METRIC_ANOMALY'
                        ? 'warning'
                        : n.type === 'FAILURE_PATTERN'
                        ? 'error'
                        : 'intelligence'
                    }
                    size="sm"
                  >
                    {n.type.replace('_', ' ')}
                  </Badge>
                  <h3 className="text-sm font-semibold text-foreground">{n.label}</h3>
                </div>
                <span className="text-xs font-mono text-muted-foreground">{n.connections} Edges</span>
              </div>
              <p className="text-xs text-muted-foreground mt-2">{n.details}</p>
            </Card>
          ))}
        </div>

        {/* Node Inspection & Causal Link Matrix */}
        <div className="lg:col-span-7 space-y-4">
          <Card className="p-5 border-border/40 space-y-4">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-xs font-mono font-bold text-purple-400">NODE INSPECTION</span>
                <h3 className="text-lg font-bold text-foreground mt-0.5">{selectedNode.label}</h3>
              </div>
              <Badge variant="outline" size="sm">
                Type: {selectedNode.type}
              </Badge>
            </div>

            <p className="text-xs text-muted-foreground leading-relaxed">{selectedNode.details}</p>

            {/* Causal Edges */}
            <div className="space-y-2 pt-2">
              <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                Cryptographic Causal Edges
              </span>
              <div className="space-y-2">
                {edges.map((e, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between p-3 rounded-lg border border-purple-500/20 bg-purple-950/10 text-xs font-mono"
                  >
                    <div className="flex items-center gap-2 truncate max-w-sm">
                      <span className="text-foreground">{e.source}</span>
                      <span className="text-purple-400 font-bold">-[ {e.relationship} ]-&gt;</span>
                      <span className="text-foreground">{e.target}</span>
                    </div>
                    <Badge variant="success" size="sm">
                      Weight: {e.weight}
                    </Badge>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
