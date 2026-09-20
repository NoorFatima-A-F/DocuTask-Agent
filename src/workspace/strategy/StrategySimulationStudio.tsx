import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  FlaskConical,
  CheckCircle2,
  RefreshCw,
} from 'lucide-react';

interface SimulationItem {
  id: string;
  name: string;
  horizon: string;
  budgetDeltaUsd: number;
  workerDelta: number;
  cacheHitPct: number;
  trafficGrowthPct: number;
  expectedRoi: number;
  expectedP95Ms: number;
  expectedThroughputQps: number;
  riskScore: number;
  actions: string[];
}

export const StrategySimulationStudio: React.FC = () => {
  const [simulations, setSimulations] = useState<SimulationItem[]>([
    {
      id: 'sim-surge-3x-opt',
      name: 'Q4 Year-End 300% Invoicing Peak Surge',
      horizon: 'DAYS_90',
      budgetDeltaUsd: 6000.0,
      workerDelta: 12,
      cacheHitPct: 88.0,
      trafficGrowthPct: 300.0,
      expectedRoi: 4.20,
      expectedP95Ms: 195.0,
      expectedThroughputQps: 3200.0,
      riskScore: 0.065,
      actions: [
        'Deploy +12 pre-warmed worker replicas across AWS us-east-1 and us-west-2.',
        'Activate aggressive 88% speculative tensor caching on corporate schemas.',
        'Enable triadic agent coalitions on balance sheet queue.',
      ],
    },
    {
      id: 'sim-budget-cut-opt',
      name: 'Operational Efficiency & -20% Cost Constraint',
      horizon: 'DAYS_180',
      budgetDeltaUsd: -4000.0,
      workerDelta: -2,
      cacheHitPct: 92.0,
      trafficGrowthPct: 50.0,
      expectedRoi: 3.10,
      expectedP95Ms: 260.0,
      expectedThroughputQps: 1800.0,
      riskScore: 0.120,
      actions: [
        'Maximize lock-free memory ring buffer cache utilization to 92%.',
        'Consolidate idle night-time worker nodes into spot instances.',
      ],
    },
  ]);

  const [isSimulating, setIsSimulating] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);

  const handleRunNewSim = () => {
    setIsSimulating(true);
    setTimeout(() => {
      const newSim: SimulationItem = {
        id: `sim-new-${Date.now().toString().slice(-4)}`,
        name: 'Autonomous Multi-Datacenter Federation (Simulated)',
        horizon: 'DAYS_365',
        budgetDeltaUsd: 12000.0,
        workerDelta: 16,
        cacheHitPct: 94.0,
        trafficGrowthPct: 500.0,
        expectedRoi: 5.10,
        expectedP95Ms: 165.0,
        expectedThroughputQps: 4800.0,
        riskScore: 0.045,
        actions: [
          'Federate EU and US GPU swarms with zero-lock synchronizer.',
          'Pre-warm layout embeddings for all Fortune 500 vendor schemas.',
        ],
      };
      setSimulations((prev) => [newSim, ...prev]);
      setIsSimulating(false);
      setNotice('Strategic Scenario Simulation complete: High-confidence multi-datacenter projection added.');
      setTimeout(() => setNotice(null), 4000);
    }, 1200);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <FlaskConical className="w-6 h-6 text-indigo-500" />
            Strategic Scenario Simulation Studio
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Phase 13.11 — Multi-horizon strategic stress testing, macroeconomic cost modeling, and throughput projection simulations.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="intelligence" size="sm" onClick={handleRunNewSim} disabled={isSimulating}>
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isSimulating ? 'animate-spin' : ''}`} />
            {isSimulating ? 'Simulating Scenario...' : 'Simulate New Scenario'}
          </Button>
        </div>
      </div>

      {notice && (
        <div className="p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-lg text-sm text-emerald-800 dark:text-emerald-300 flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{notice}</span>
        </div>
      )}

      {/* Simulations List */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider">
          Simulated Strategic Scenarios
        </h3>

        <div className="grid grid-cols-1 gap-4">
          {simulations.map((sim) => (
            <Card key={sim.id} className="p-5 border-l-4 border-l-indigo-500 hover:shadow-md transition-shadow">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs text-indigo-600 dark:text-indigo-400 font-semibold">{sim.id}</span>
                    <Badge variant="outline" size="sm">
                      {sim.horizon}
                    </Badge>
                  </div>
                  <h4 className="font-semibold text-gray-900 dark:text-white text-base mt-1">{sim.name}</h4>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <span className="text-xs text-gray-400 block">Expected ROI</span>
                    <span className="text-lg font-bold text-emerald-600 dark:text-emerald-400 font-mono">
                      {sim.expectedRoi}x
                    </span>
                  </div>
                </div>
              </div>

              {/* Projections Matrix */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-4 text-xs">
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Throughput Proj</span>
                  <span className="font-semibold text-gray-900 dark:text-white font-mono">
                    {sim.expectedThroughputQps.toLocaleString()} QPS
                  </span>
                </div>
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">P95 Latency</span>
                  <span className="font-semibold text-indigo-600 dark:text-indigo-400 font-mono">
                    {sim.expectedP95Ms} ms
                  </span>
                </div>
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Traffic Growth</span>
                  <span className="font-semibold text-purple-600 dark:text-purple-400 font-mono">
                    +{sim.trafficGrowthPct}%
                  </span>
                </div>
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Risk Score</span>
                  <span className="font-semibold text-sky-600 dark:text-sky-400 font-mono">
                    {sim.riskScore.toFixed(3)}
                  </span>
                </div>
              </div>

              {/* Recommended Actions */}
              <div className="mt-4 pt-3 border-t border-gray-100 dark:border-gray-800 text-xs">
                <span className="text-gray-400 block mb-1">Recommended Strategic Directives:</span>
                <div className="space-y-1">
                  {sim.actions.map((act, actIdx) => (
                    <div key={actIdx} className="flex items-center gap-1.5 text-gray-700 dark:text-gray-300">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 flex-shrink-0" />
                      <span>{act}</span>
                    </div>
                  ))}
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
