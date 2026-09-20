import React from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Sparkles,
} from 'lucide-react';

interface ScenarioComparisonItem {
  id: string;
  name: string;
  mode: string;
  latencyMs: number;
  costUsd: number;
  riskScore: number;
  throughputQps: number;
  paretoOptimality: number;
  isOptimal: boolean;
}

export const ScenarioComparisonWorkbench: React.FC = () => {
  const scenarios: ScenarioComparisonItem[] = [
    {
      id: 'scen-opt-01',
      name: 'Dynamic Fan-Out + Speculative Caching',
      mode: 'AUTONOMOUS_OPTIMAL',
      latencyMs: 95.0,
      costUsd: 0.0276,
      riskScore: 0.05,
      throughputQps: 168.4,
      paretoOptimality: 0.985,
      isOptimal: true,
    },
    {
      id: 'scen-opt-02',
      name: 'Dynamic Fan-Out (No Cache)',
      mode: 'PARTIAL_CONCURRENCY',
      latencyMs: 145.0,
      costUsd: 0.0380,
      riskScore: 0.12,
      throughputQps: 110.3,
      paretoOptimality: 0.912,
      isOptimal: false,
    },
    {
      id: 'scen-opt-03',
      name: 'Sequential Greedy Execution Baseline',
      mode: 'LEGACY_BASELINE',
      latencyMs: 380.0,
      costUsd: 0.0480,
      riskScore: 0.28,
      throughputQps: 42.1,
      paretoOptimality: 0.740,
      isOptimal: false,
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Scenario Comparison Workbench</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              PARETO EVALUATION
            </Badge>
            <Badge variant="outline" size="sm">
              AWM-PSDTIP Phase 13.10
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Side-by-side Pareto scenario comparison across predicted latency, monetary compute cost, risk index, and throughput capacity.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="intelligence" size="sm">
            <Sparkles className="w-3.5 h-3.5 mr-1.5" />
            Synthesize New Scenario
          </Button>
        </div>
      </div>

      {/* Comparison Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {scenarios.map((scen) => (
          <Card
            key={scen.id}
            className={`p-5 border space-y-4 transition-all flex flex-col justify-between ${
              scen.isOptimal
                ? 'border-purple-500/50 bg-purple-950/20 shadow-md'
                : 'border-border/40 bg-secondary/10'
            }`}
          >
            <div className="space-y-3">
              <div className="flex items-start justify-between gap-2">
                <Badge variant={scen.isOptimal ? 'intelligence' : 'outline'} size="sm">
                  {scen.isOptimal ? '★ Pareto Optimal' : scen.mode}
                </Badge>
                <span className="text-xs font-mono text-purple-400 font-bold">
                  Score: {(scen.paretoOptimality * 100).toFixed(1)}
                </span>
              </div>

              <h2 className="text-sm font-bold text-foreground">{scen.name}</h2>

              {/* Metrics Table */}
              <div className="space-y-2 pt-2 text-xs border-t border-border/30">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Predicted Latency:</span>
                  <span className="font-mono font-bold text-foreground">{scen.latencyMs}ms</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Compute Cost:</span>
                  <span className="font-mono font-bold text-foreground">${scen.costUsd.toFixed(4)}/doc</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Throughput:</span>
                  <span className="font-mono font-bold text-emerald-400">{scen.throughputQps} QPS</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Risk Exposure:</span>
                  <span className="font-mono font-bold text-muted-foreground">{(scen.riskScore * 100).toFixed(1)}%</span>
                </div>
              </div>
            </div>

            <div className="pt-3 border-t border-border/30">
              <Button
                variant={scen.isOptimal ? 'primary' : 'outline'}
                size="sm"
                className="w-full"
              >
                {scen.isOptimal ? 'Authorize For Production' : 'Simulate Monte Carlo'}
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
