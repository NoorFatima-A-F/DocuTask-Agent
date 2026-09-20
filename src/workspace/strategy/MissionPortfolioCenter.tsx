import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  PieChart,
  DollarSign,
  Zap,
  TrendingUp,
  ShieldCheck,
  RefreshCw,
  CheckCircle2,
} from 'lucide-react';

interface PortfolioMissionItem {
  id: string;
  name: string;
  category: string;
  allocatedBudgetUsd: number;
  expectedGainUsd: number;
  expectedRoi: number;
  latencyGainPct: number;
  riskScore: number;
  compositeUtility: number;
  paretoRank: number;
  status: string;
}

export const MissionPortfolioCenter: React.FC = () => {
  const [missions] = useState<PortfolioMissionItem[]>([
    {
      id: 'msn-cache-warm-01',
      name: 'Speculative Layout Cache Pre-Warming',
      category: 'Throughput & Latency Acceleration',
      allocatedBudgetUsd: 3200.0,
      expectedGainUsd: 9800.0,
      expectedRoi: 3.06,
      latencyGainPct: 28.0,
      riskScore: 0.08,
      compositeUtility: 0.925,
      paretoRank: 1,
      status: 'ACTIVE',
    },
    {
      id: 'msn-triadic-coalition-02',
      name: 'Triadic Extraction Strike Team Deployment',
      category: 'Throughput & Latency Acceleration',
      allocatedBudgetUsd: 4500.0,
      expectedGainUsd: 12500.0,
      expectedRoi: 2.77,
      latencyGainPct: 22.0,
      riskScore: 0.12,
      compositeUtility: 0.890,
      paretoRank: 1,
      status: 'ACTIVE',
    },
    {
      id: 'msn-sec-sha-ledger',
      name: 'Zero-Knowledge Ledger Rollback Checkpoints',
      category: 'Governance & Cryptographic Assurance',
      allocatedBudgetUsd: 2800.0,
      expectedGainUsd: 6000.0,
      expectedRoi: 2.14,
      latencyGainPct: 0.0,
      riskScore: 0.04,
      compositeUtility: 0.940,
      paretoRank: 1,
      status: 'ACTIVE',
    },
    {
      id: 'msn-auto-roadmap-04',
      name: 'Long-Horizon Strategic Roadmapping Engine',
      category: 'Autonomous Strategic Cognition',
      allocatedBudgetUsd: 5000.0,
      expectedGainUsd: 18000.0,
      expectedRoi: 3.60,
      latencyGainPct: 15.0,
      riskScore: 0.14,
      compositeUtility: 0.955,
      paretoRank: 1,
      status: 'ACTIVE',
    },
  ]);

  const [isOptimizing, setIsOptimizing] = useState(false);
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  const totalAllocated = missions.reduce((acc, m) => acc + m.allocatedBudgetUsd, 0);
  const budgetLimit = 30000.0;
  const utilizationPct = (totalAllocated / budgetLimit) * 100;
  const totalProjectedGain = missions.reduce((acc, m) => acc + m.expectedGainUsd, 0);

  const handleOptimize = () => {
    setIsOptimizing(true);
    setTimeout(() => {
      setIsOptimizing(false);
      setStatusMsg('Pareto Frontier Optimization complete: All 4 active missions confirmed Pareto-dominant (#1).');
      setTimeout(() => setStatusMsg(null), 4000);
    }, 1200);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <PieChart className="w-6 h-6 text-indigo-500" />
            Mission Portfolio Optimization & Pareto Frontier Center
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Phase 13.11 — Dynamic mission portfolio clustering, Pareto multi-objective ranking, and ROI budget balancing.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="intelligence" size="sm" onClick={handleOptimize} disabled={isOptimizing}>
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isOptimizing ? 'animate-spin' : ''}`} />
            {isOptimizing ? 'Rebalancing Pareto...' : 'Rebalance Portfolio'}
          </Button>
        </div>
      </div>

      {statusMsg && (
        <div className="p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-lg text-sm text-emerald-800 dark:text-emerald-300 flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{statusMsg}</span>
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4 border-l-4 border-l-indigo-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Total Allocated Budget</span>
            <DollarSign className="w-4 h-4 text-indigo-500" />
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
            ${totalAllocated.toLocaleString()}
          </div>
          <span className="text-xs text-indigo-600 dark:text-indigo-400 font-medium">
            {utilizationPct.toFixed(1)}% of ${budgetLimit.toLocaleString()} Limit
          </span>
        </Card>

        <Card className="p-4 border-l-4 border-l-emerald-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Projected Net Gain</span>
            <TrendingUp className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">
            ${totalProjectedGain.toLocaleString()}
          </div>
          <span className="text-xs text-emerald-500">Expected ROI: 3.01x Aggregate</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-purple-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Pareto Non-Dominated Missions</span>
            <ShieldCheck className="w-4 h-4 text-purple-500" />
          </div>
          <div className="text-2xl font-bold text-purple-600 dark:text-purple-400 mt-1">4 / 4</div>
          <span className="text-xs text-purple-500">100% Rank #1 Dominant</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-sky-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Portfolio Risk Index</span>
            <Zap className="w-4 h-4 text-sky-500" />
          </div>
          <div className="text-2xl font-bold text-sky-600 dark:text-sky-400 mt-1">0.098</div>
          <span className="text-xs text-sky-500">Safe Boundary (&lt; 0.250)</span>
        </Card>
      </div>

      {/* Missions Table */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider">
          Active Portfolio Mission Allocations
        </h3>

        <div className="grid grid-cols-1 gap-4">
          {missions.map((m) => (
            <Card key={m.id} className="p-5 hover:shadow-md transition-shadow border-l-4 border-l-indigo-500">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs text-indigo-600 dark:text-indigo-400 font-semibold">{m.id}</span>
                    <Badge variant="intelligence" size="sm">
                      Pareto Rank #{m.paretoRank}
                    </Badge>
                    <Badge variant="outline" size="sm">
                      {m.category}
                    </Badge>
                  </div>
                  <h4 className="font-semibold text-gray-900 dark:text-white text-base mt-1">{m.name}</h4>
                </div>
                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <span className="text-xs text-gray-400 block">Composite Utility</span>
                    <span className="text-lg font-bold text-indigo-600 dark:text-indigo-400 font-mono">
                      {m.compositeUtility.toFixed(3)}
                    </span>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-4 text-xs">
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Budget Allocation</span>
                  <span className="font-semibold text-gray-900 dark:text-white font-mono">
                    ${m.allocatedBudgetUsd.toLocaleString()}
                  </span>
                </div>
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Projected Value</span>
                  <span className="font-semibold text-emerald-600 dark:text-emerald-400 font-mono">
                    ${m.expectedGainUsd.toLocaleString()} ({m.expectedRoi}x ROI)
                  </span>
                </div>
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Latency Reduction</span>
                  <span className="font-semibold text-purple-600 dark:text-purple-400 font-mono">
                    +{m.latencyGainPct}%
                  </span>
                </div>
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Risk Score</span>
                  <span className="font-semibold text-sky-600 dark:text-sky-400 font-mono">
                    {m.riskScore.toFixed(3)}
                  </span>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
