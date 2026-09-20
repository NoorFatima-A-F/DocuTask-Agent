import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Calendar,
} from 'lucide-react';

interface TemporalNodeItem {
  id: string;
  label: string;
  type: string;
  validFrom: string;
  validTo?: string;
  isProjected: boolean;
  properties: Record<string, any>;
}

export const TemporalKnowledgeGraph: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'ALL' | 'HISTORICAL' | 'PROJECTED'>('ALL');

  const nodes: TemporalNodeItem[] = [
    {
      id: 'tnode-01',
      label: 'Legacy Sequential APDLE DAG (T-24h)',
      type: 'MISSION_STATE',
      validFrom: '2026-09-11 00:00 UTC',
      validTo: '2026-09-12 00:00 UTC',
      isProjected: false,
      properties: { mean_latency_ms: 380.0, errors: 0 },
    },
    {
      id: 'tnode-02',
      label: 'Dynamic Fan-Out DAG + Cache (Present)',
      type: 'MISSION_STATE',
      validFrom: '2026-09-12 00:00 UTC',
      isProjected: false,
      properties: { mean_latency_ms: 180.0, cache_hit_rate: 0.82 },
    },
    {
      id: 'tnode-03',
      label: 'Projected Autonomous Strike Swarm (T+48h)',
      type: 'PREDICTED_FUTURE',
      validFrom: '2026-09-14 00:00 UTC',
      isProjected: true,
      properties: { predicted_latency_ms: 95.0, confidence: 0.985 },
    },
  ];

  const filteredNodes = nodes.filter((n) => {
    if (activeTab === 'HISTORICAL') return !n.isProjected;
    if (activeTab === 'PROJECTED') return n.isProjected;
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Temporal Knowledge Graph</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              4D TEMPORAL REASONING
            </Badge>
            <Badge variant="outline" size="sm">
              AWM-PSDTIP Phase 13.10
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Time-aware graph linking historical state transitions, evolutionary trajectories, and projected future execution branches.
          </p>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 border-b border-border/40 pb-2">
        {(['ALL', 'HISTORICAL', 'PROJECTED'] as const).map((t) => (
          <Button
            key={t}
            variant={activeTab === t ? 'primary' : 'ghost'}
            size="sm"
            onClick={() => setActiveTab(t)}
          >
            {t}
          </Button>
        ))}
      </div>

      {/* Temporal Stream */}
      <div className="space-y-4">
        {filteredNodes.map((n) => (
          <Card
            key={n.id}
            className={`p-5 border transition-all ${
              n.isProjected
                ? 'border-purple-500/50 bg-purple-950/20 shadow-sm'
                : 'border-border/40 bg-secondary/10'
            }`}
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold text-foreground">{n.id}</span>
                  <Badge variant={n.isProjected ? 'intelligence' : 'outline'} size="sm">
                    {n.type}
                  </Badge>
                  {n.isProjected && <Badge variant="success" size="sm">Projected Future</Badge>}
                </div>
                <h3 className="text-sm font-semibold text-foreground">{n.label}</h3>
              </div>
              <div className="text-xs font-mono text-muted-foreground flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5" />
                <span>Valid: {n.validFrom} {n.validTo ? `→ ${n.validTo}` : '(Current)'}</span>
              </div>
            </div>

            {/* Properties Matrix */}
            <div className="p-3 rounded bg-secondary/20 border border-border/30 text-xs font-mono text-muted-foreground grid grid-cols-1 sm:grid-cols-3 gap-2 mt-3">
              {Object.entries(n.properties).map(([k, v], idx) => (
                <div key={idx} className="truncate">
                  <span className="text-foreground">{k}:</span> {String(v)}
                </div>
              ))}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
