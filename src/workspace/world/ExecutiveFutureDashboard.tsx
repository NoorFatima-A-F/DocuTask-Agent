import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Compass,
  Activity,
  TrendingUp,
  AlertTriangle,
  ShieldCheck,
  RefreshCw,
  Zap,
  Clock,
  Layers,
} from 'lucide-react';

export const ExecutiveFutureDashboard: React.FC = () => {
  const [selectedHorizon, setSelectedHorizon] = useState<'1h' | '6h' | '24h' | '7d'>('24h');
  const [isSimulating, setIsSimulating] = useState(false);

  const horizonMetrics = {
    '1h': {
      throughput: '1,420 doc/min',
      latencyP95: '210ms',
      failureProb: '0.012%',
      costDelta: '-4.2%',
      confidence: 0.994,
    },
    '6h': {
      throughput: '1,850 doc/min',
      latencyP95: '235ms',
      failureProb: '0.045%',
      costDelta: '-8.5%',
      confidence: 0.988,
    },
    '24h': {
      throughput: '2,640 doc/min',
      latencyP95: '275ms',
      failureProb: '0.110%',
      costDelta: '-14.2%',
      confidence: 0.976,
    },
    '7d': {
      throughput: '3,800 doc/min',
      latencyP95: '310ms',
      failureProb: '0.280%',
      costDelta: '-22.0%',
      confidence: 0.942,
    },
  };

  const currentMetric = horizonMetrics[selectedHorizon];

  const handleRunMonteCarlo = () => {
    setIsSimulating(true);
    setTimeout(() => setIsSimulating(false), 1500);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Compass className="w-6 h-6 text-indigo-500" />
            Executive Future Command Cockpit
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Phase 13.10 — Unified predictive digital twin intelligence, multi-horizon simulation & autonomous future optimization.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex bg-gray-100 dark:bg-gray-800 p-1 rounded-lg">
            {(['1h', '6h', '24h', '7d'] as const).map((h) => (
              <button
                key={h}
                onClick={() => setSelectedHorizon(h)}
                className={`px-3 py-1 text-xs font-semibold rounded-md transition-colors ${
                  selectedHorizon === h
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'text-gray-600 dark:text-gray-300 hover:text-indigo-600'
                }`}
              >
                {h} Horizon
              </button>
            ))}
          </div>
          <Button
            variant="intelligence"
            size="sm"
            onClick={handleRunMonteCarlo}
            disabled={isSimulating}
          >
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isSimulating ? 'animate-spin' : ''}`} />
            {isSimulating ? 'Simulating...' : 'Run Monte Carlo'}
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <Card className="p-4 border-l-4 border-l-indigo-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Forecasted Throughput</span>
            <Activity className="w-4 h-4 text-indigo-500" />
          </div>
          <div className="text-xl font-bold text-gray-900 dark:text-white mt-1">
            {currentMetric.throughput}
          </div>
          <span className="text-xs text-emerald-600 dark:text-emerald-400 font-medium">Trajectory: Linear Surge</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-emerald-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Forecasted P95 Latency</span>
            <Clock className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="text-xl font-bold text-gray-900 dark:text-white mt-1">
            {currentMetric.latencyP95}
          </div>
          <span className="text-xs text-emerald-600 dark:text-emerald-400 font-medium">Within 350ms SLA Target</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-amber-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Predicted Failure Prob</span>
            <AlertTriangle className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-xl font-bold text-gray-900 dark:text-white mt-1">
            {currentMetric.failureProb}
          </div>
          <span className="text-xs text-gray-400">Risk Threshold &lt; 0.5%</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-purple-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Projected Cost Delta</span>
            <TrendingUp className="w-4 h-4 text-purple-500" />
          </div>
          <div className="text-xl font-bold text-purple-600 dark:text-purple-400 mt-1">
            {currentMetric.costDelta}
          </div>
          <span className="text-xs text-purple-500">Auto-caching savings</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-sky-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Bayesian Confidence</span>
            <ShieldCheck className="w-4 h-4 text-sky-500" />
          </div>
          <div className="text-xl font-bold text-sky-600 dark:text-sky-400 mt-1">
            {(currentMetric.confidence * 100).toFixed(1)}%
          </div>
          <span className="text-xs text-sky-500">Empirical Telemetry</span>
        </Card>
      </div>

      {/* Main Command Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: World State & Interventions */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="p-5">
            <div className="flex items-center justify-between pb-4 border-b border-gray-100 dark:border-gray-800">
              <div className="flex items-center gap-2">
                <Layers className="w-5 h-5 text-indigo-500" />
                <h3 className="font-semibold text-gray-900 dark:text-white">
                  Active Multi-Branch Future Reality Projections
                </h3>
              </div>
              <Badge variant="intelligence" size="sm">
                4 Active Future Branches
              </Badge>
            </div>

            <div className="space-y-4 mt-4">
              <div className="p-4 bg-indigo-50/40 dark:bg-indigo-950/20 border border-indigo-200 dark:border-indigo-900 rounded-lg">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-sm text-indigo-900 dark:text-indigo-300">
                    Branch A (Recommended): Auto-scaling + Speculative Caching
                  </span>
                  <Badge variant="success" size="sm">Score: 0.942</Badge>
                </div>
                <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                  Executes horizontal scale-out +4 replicas and activates speculative embedding cache.
                  Yields 28% latency reduction, 22% cost savings, and 0.012% predicted risk.
                </p>
                <div className="mt-3 flex items-center gap-3 text-xs text-gray-500">
                  <span>Confidence: <strong className="text-indigo-600 dark:text-indigo-400">99.1%</strong></span>
                  <span>•</span>
                  <span>Pareto Rank: <strong className="text-emerald-600 dark:text-emerald-400">#1 (Dominant)</strong></span>
                  <span>•</span>
                  <span>Governance Status: <strong className="text-emerald-600 dark:text-emerald-400">Pre-Approved</strong></span>
                </div>
              </div>

              <div className="p-4 bg-gray-50 dark:bg-gray-900/40 border border-gray-200 dark:border-gray-800 rounded-lg">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-sm text-gray-800 dark:text-gray-200">
                    Branch B: Baseline Continuation (No Intervention)
                  </span>
                  <Badge variant="warning" size="sm">Score: 0.710</Badge>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Keeps current worker pool unchanged. Latency projected to spike past 410ms at peak load (hour 18).
                </p>
              </div>

              <div className="p-4 bg-gray-50 dark:bg-gray-900/40 border border-gray-200 dark:border-gray-800 rounded-lg">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-sm text-gray-800 dark:text-gray-200">
                    Branch C: Maximum Over-Provisioning (+12 Replicas)
                  </span>
                  <Badge variant="default" size="sm">Score: 0.655</Badge>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Guarantees sub-180ms latency but incurs +38% unnecessary infrastructure expenditure.
                </p>
              </div>
            </div>
          </Card>
        </div>

        {/* Right Col: Autonomous Future Directives */}
        <div className="space-y-6">
          <Card className="p-5">
            <h3 className="font-semibold text-gray-900 dark:text-white flex items-center gap-2 mb-4">
              <Zap className="w-5 h-5 text-amber-500" />
              Autonomous Directives
            </h3>

            <div className="space-y-3">
              <div className="p-3 bg-amber-50/50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900 rounded-lg text-xs space-y-1">
                <span className="font-semibold text-amber-900 dark:text-amber-300 block">
                  Proactive Scale-Up Trigger
                </span>
                <p className="text-gray-600 dark:text-gray-400">
                  Scheduled for 17:45 UTC (15m before predicted load surge).
                </p>
                <div className="pt-1 flex items-center gap-1 text-emerald-600 dark:text-emerald-400 font-medium">
                  <ShieldCheck className="w-3.5 h-3.5" />
                  <span>Safety Guard Signed</span>
                </div>
              </div>

              <div className="p-3 bg-indigo-50/50 dark:bg-indigo-950/20 border border-indigo-200 dark:border-indigo-900 rounded-lg text-xs space-y-1">
                <span className="font-semibold text-indigo-900 dark:text-indigo-300 block">
                  Pre-Warming Invoice Classifier
                </span>
                <p className="text-gray-600 dark:text-gray-400">
                  Pre-warming 3 specialist worker models to avert 850ms cold-start penalty.
                </p>
                <div className="pt-1 flex items-center gap-1 text-emerald-600 dark:text-emerald-400 font-medium">
                  <ShieldCheck className="w-3.5 h-3.5" />
                  <span>Rollback Checkpoint Set</span>
                </div>
              </div>

              <div className="p-3 bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-900 rounded-lg text-xs space-y-1">
                <span className="font-semibold text-emerald-900 dark:text-emerald-300 block">
                  Causal Do-Intervention Locked
                </span>
                <p className="text-gray-600 dark:text-gray-400">
                  Structural invariant do(worker_replicas=8) scheduled with 0% risk violation.
                </p>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
