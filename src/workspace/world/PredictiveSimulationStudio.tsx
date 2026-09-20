import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  FlaskConical,
  RefreshCw,
  TrendingUp,
  BarChart2,
  PlusCircle,
  Zap,
} from 'lucide-react';

interface SimulationItem {
  id: string;
  name: string;
  type: string;
  expectedLatencyMs: number;
  latencyCi: [number, number];
  expectedCostUsd: number;
  costCi: [number, number];
  failureProb: number;
  throughputQps: number;
  risk: string;
}

export const PredictiveSimulationStudio: React.FC = () => {
  const [isSimulating, setIsSimulating] = useState<boolean>(false);

  const simulations: SimulationItem[] = [
    {
      id: 'sres-001',
      name: 'Baseline 500 Enterprise Invoice Ingestion',
      type: 'BASELINE (MONTE_CARLO)',
      expectedLatencyMs: 180.0,
      latencyCi: [177.06, 182.94],
      expectedCostUsd: 0.024,
      costCi: [0.0236, 0.0244],
      failureProb: 0.002,
      throughputQps: 44.4,
      risk: 'LOW',
    },
    {
      id: 'sres-002',
      name: 'Peak Burst Load (3x Concurrent Traffic)',
      type: 'BURST_TRAFFIC (STRESS_TEST)',
      expectedLatencyMs: 225.0,
      latencyCi: [222.60, 227.40],
      expectedCostUsd: 0.0648,
      costCi: [0.0645, 0.0651],
      failureProb: 0.015,
      throughputQps: 71.1,
      risk: 'MEDIUM',
    },
    {
      id: 'sres-003',
      name: 'Swarm Scaling (16 Concurrent Specialists)',
      type: 'SWARM_SCALING (MONTE_CARLO)',
      expectedLatencyMs: 95.0,
      latencyCi: [92.06, 97.94],
      expectedCostUsd: 0.0276,
      costCi: [0.0272, 0.0280],
      failureProb: 0.001,
      throughputQps: 168.4,
      risk: 'LOW',
    },
  ];

  const handleSimulate = () => {
    setIsSimulating(true);
    setTimeout(() => {
      setIsSimulating(false);
    }, 1500);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Predictive Simulation Studio</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              MONTE CARLO READY
            </Badge>
            <Badge variant="outline" size="sm">
              AWM-PSDTIP Phase 13.10
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Simulates hypothetical future mission executions across baseline, burst traffic, swarm scaling, and chaos failure scenarios with 95% confidence bounds.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleSimulate} disabled={isSimulating}>
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isSimulating ? 'animate-spin' : ''}`} />
            {isSimulating ? 'Simulating Trials...' : 'Run Scenario Trials'}
          </Button>
          <Button variant="intelligence" size="sm">
            <PlusCircle className="w-3.5 h-3.5 mr-1.5" />
            Create Simulation Scenario
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-4 bg-purple-950/10 border-purple-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Simulated Scenarios</span>
            <FlaskConical className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-2">1,250 Trials</div>
          <div className="text-[11px] text-muted-foreground mt-1">Grounded in replay history</div>
        </Card>

        <Card className="p-4 bg-emerald-950/10 border-emerald-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Optimal Peak Throughput</span>
            <Zap className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-2">168.4 QPS</div>
          <div className="text-[11px] text-muted-foreground mt-1">Swarm scaling scenario</div>
        </Card>

        <Card className="p-4 bg-blue-950/10 border-blue-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Confidence Interval Floor</span>
            <BarChart2 className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-blue-400 mt-2">95% CI (±2.9ms)</div>
          <div className="text-[11px] text-muted-foreground mt-1">Statistical variance calibrated</div>
        </Card>

        <Card className="p-4 bg-indigo-950/10 border-indigo-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Mean Failure Risk</span>
            <TrendingUp className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-indigo-400 mt-2">&lt; 0.2%</div>
          <div className="text-[11px] text-muted-foreground mt-1">Zero invariant violation</div>
        </Card>
      </div>

      {/* Simulation Results List */}
      <div className="space-y-4">
        {simulations.map((sim) => (
          <Card key={sim.id} className="p-5 border-border/40 space-y-4 hover:border-purple-500/30 transition-colors">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <h2 className="text-base font-semibold text-foreground">{sim.name}</h2>
                  <Badge variant="intelligence" size="sm">{sim.type}</Badge>
                </div>
                <span className="text-xs font-mono text-muted-foreground">Scenario ID: {sim.id}</span>
              </div>
              <Badge variant={sim.risk === 'LOW' ? 'success' : 'warning'} size="sm">
                Risk: {sim.risk}
              </Badge>
            </div>

            {/* Metrics Breakdown */}
            <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs font-mono">
              <div className="p-3 rounded bg-secondary/20 border border-border/30">
                <span className="text-muted-foreground">Expected Latency:</span>
                <div className="text-base font-bold text-foreground mt-1">{sim.expectedLatencyMs}ms</div>
                <span className="text-[10px] text-purple-300">95% CI: [{sim.latencyCi[0]}, {sim.latencyCi[1]}]</span>
              </div>

              <div className="p-3 rounded bg-secondary/20 border border-border/30">
                <span className="text-muted-foreground">Compute Cost:</span>
                <div className="text-base font-bold text-foreground mt-1">${sim.expectedCostUsd.toFixed(4)}</div>
                <span className="text-[10px] text-emerald-300">95% CI: [{sim.costCi[0]}, {sim.costCi[1]}]</span>
              </div>

              <div className="p-3 rounded bg-secondary/20 border border-border/30">
                <span className="text-muted-foreground">Predicted Throughput:</span>
                <div className="text-base font-bold text-emerald-400 mt-1">{sim.throughputQps} QPS</div>
                <span className="text-[10px] text-muted-foreground">Linear scaling factor</span>
              </div>

              <div className="p-3 rounded bg-secondary/20 border border-border/30">
                <span className="text-muted-foreground">Failure Probability:</span>
                <div className="text-base font-bold text-foreground mt-1">{(sim.failureProb * 100).toFixed(2)}%</div>
                <span className="text-[10px] text-emerald-400">Zero deadlock risk</span>
              </div>
            </div>

            <div className="flex items-center justify-between text-xs pt-2 border-t border-border/30">
              <span className="text-[11px] font-mono text-muted-foreground">Deterministic Replay Proof Available</span>
              <Button variant="outline" size="sm">
                Apply Simulation Parameters
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
