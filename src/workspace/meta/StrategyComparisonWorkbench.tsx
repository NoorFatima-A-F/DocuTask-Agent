import React from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Sparkles,
} from 'lucide-react';

interface StrategyProfile {
  id: string;
  name: string;
  type: string;
  latencyMs: number;
  costPerDocUsd: number;
  accuracyFloorPct: number;
  memoryOverheadMb: number;
  paretoScore: number;
  isRecommended: boolean;
}

export const StrategyComparisonWorkbench: React.FC = () => {
  const strategies: StrategyProfile[] = [
    {
      id: 'strat-01',
      name: 'Dynamic Chunk Fan-Out + Schema Caching',
      type: 'AUTONOMOUS_SYNTHESIS',
      latencyMs: 165,
      costPerDocUsd: 0.024,
      accuracyFloorPct: 99.8,
      memoryOverheadMb: 150,
      paretoScore: 0.985,
      isRecommended: true,
    },
    {
      id: 'strat-02',
      name: 'Dynamic Fan-Out Only (No Cache)',
      type: 'PARTIAL_OPTIMIZATION',
      latencyMs: 210,
      costPerDocUsd: 0.034,
      accuracyFloorPct: 99.6,
      memoryOverheadMb: 64,
      paretoScore: 0.912,
      isRecommended: false,
    },
    {
      id: 'strat-03',
      name: 'Greedy Sequential Critical-Path Baseline',
      type: 'LEGACY_BASELINE',
      latencyMs: 380,
      costPerDocUsd: 0.048,
      accuracyFloorPct: 99.2,
      memoryOverheadMb: 32,
      paretoScore: 0.760,
      isRecommended: false,
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Strategy Comparison Workbench</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              PARETO EVALUATION
            </Badge>
            <Badge variant="outline" size="sm">
              AMRS-RSIP Phase 13.9
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Side-by-side Pareto comparison of autonomous strategies against legacy baselines across latency, monetary cost, accuracy floor, and memory footprints.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="intelligence" size="sm">
            <Sparkles className="w-3.5 h-3.5 mr-1.5" />
            Synthesize New Candidate
          </Button>
        </div>
      </div>

      {/* Comparison Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {strategies.map((st) => (
          <Card
            key={st.id}
            className={`p-5 border space-y-4 transition-all flex flex-col justify-between ${
              st.isRecommended
                ? 'border-purple-500/50 bg-purple-950/20 shadow-md'
                : 'border-border/40 bg-secondary/10'
            }`}
          >
            <div className="space-y-3">
              <div className="flex items-start justify-between gap-2">
                <Badge
                  variant={st.isRecommended ? 'intelligence' : 'outline'}
                  size="sm"
                >
                  {st.isRecommended ? '★ Recommended Strategy' : st.type}
                </Badge>
                <span className="text-xs font-mono text-purple-400 font-bold">
                  Score: {(st.paretoScore * 100).toFixed(1)}
                </span>
              </div>

              <h2 className="text-sm font-bold text-foreground">{st.name}</h2>

              {/* Metrics Table */}
              <div className="space-y-2 pt-2 text-xs border-t border-border/30">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Mean Latency:</span>
                  <span className="font-mono font-bold text-foreground">{st.latencyMs}ms</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Compute Cost:</span>
                  <span className="font-mono font-bold text-foreground">${st.costPerDocUsd.toFixed(3)}/doc</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Accuracy Guarantee:</span>
                  <span className="font-mono font-bold text-emerald-400">{st.accuracyFloorPct}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">RAM Overhead:</span>
                  <span className="font-mono font-bold text-muted-foreground">{st.memoryOverheadMb} MB</span>
                </div>
              </div>
            </div>

            <div className="pt-3 border-t border-border/30">
              <Button
                variant={st.isRecommended ? 'primary' : 'outline'}
                size="sm"
                className="w-full"
              >
                {st.isRecommended ? 'Deploy Active Policy' : 'Simulate Replay'}
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
