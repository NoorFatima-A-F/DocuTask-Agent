/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 7: Scenario Simulation Center
 */

import React, { useEffect, useState } from 'react';
import {
  Sparkles,
  RefreshCw,
  Play,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
import { ScenarioBranch } from '../../types/worldModelPlatform';

export const ScenarioSimulationCenter: React.FC = () => {
  const [branches, setBranches] = useState<ScenarioBranch[]>([]);
  const [loading, setLoading] = useState(true);
  const [simulating, setSimulating] = useState(false);
  const [selectedBranch, setSelectedBranch] = useState<ScenarioBranch | null>(null);

  const fetchScenarios = async () => {
    setLoading(true);
    try {
      const res = await WorldModelApiClient.getScenarios();
      setBranches(res.branches || []);
      if (res.branches && res.branches.length > 0 && !selectedBranch) {
        setSelectedBranch(res.branches[0] || null);
      }
    } catch (err) {
      console.error('Error fetching scenarios:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchScenarios();
  }, []);

  const handleRunSim = async () => {
    setSimulating(true);
    try {
      await WorldModelApiClient.simulateScenarios({
        base_snapshot_id: 'snap-01',
        time_horizon_seconds: 86400,
      });
      await fetchScenarios();
    } catch (err) {
      console.error('Error simulating scenarios:', err);
    } finally {
      setSimulating(false);
    }
  };

  const getBranchBadge = (type: string) => {
    switch (type) {
      case 'best_case':
        return <Badge variant="success">Best Case</Badge>;
      case 'worst_case':
        return <Badge variant="error">Worst Case</Badge>;
      case 'black_swan':
        return <Badge variant="warning">Black Swan</Badge>;
      default:
        return <Badge variant="intelligence">Expected Case</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 border border-blue-500/30 rounded-xl p-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-blue-500/10 border border-blue-500/30 rounded-lg text-blue-400">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-white tracking-tight">Scenario Simulation Center</h1>
              <Badge variant="intelligence">Monte Carlo Branches</Badge>
            </div>
            <p className="text-sm text-slate-400">
              Generates stochastic multi-branch futures: Baseline, Best Case, Worst Case, Expected, and Black Swan outlier conditions.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={fetchScenarios} disabled={loading}>
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button variant="intelligence" onClick={handleRunSim} disabled={simulating}>
            <span className="flex items-center gap-2">
              <Play className="w-4 h-4" />
              {simulating ? 'Simulating...' : 'Run Monte Carlo'}
            </span>
          </Button>
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Branches list */}
        <div className="space-y-3">
          <h3 className="text-xs font-semibold uppercase text-slate-400 tracking-wider">
            Simulated Branches ({branches.length})
          </h3>
          <div className="space-y-2.5">
            {branches.map((b) => {
              const isSelected = selectedBranch?.branch_id === b.branch_id;
              return (
                <div
                  key={b.branch_id}
                  onClick={() => setSelectedBranch(b)}
                  className={`p-4 rounded-lg border cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-blue-950/40 border-blue-500/60 shadow-lg'
                      : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-mono text-blue-400">{b.branch_id}</span>
                    {getBranchBadge(b.branch_type)}
                  </div>
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span>Probability: <strong className="text-white">{Math.round((b.probability || 0.6) * 100)}%</strong></span>
                    <span>Divergence: <strong className="text-cyan-400">{b.state_divergence_delta}</strong></span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Selected Branch Inspection */}
        <div className="lg:col-span-2">
          {selectedBranch ? (
            <Card className="bg-slate-900/80 border-slate-800 p-6 space-y-5">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono text-blue-400 bg-blue-950/60 px-2 py-0.5 rounded border border-blue-500/30">
                      {selectedBranch.branch_id}
                    </span>
                    {getBranchBadge(selectedBranch.branch_type)}
                  </div>
                  <h2 className="text-xl font-bold text-white mt-1">
                    {selectedBranch.branch_type.toUpperCase().replace('_', ' ')} SCENARIO TRAJECTORY
                  </h2>
                </div>
                <div className="text-right">
                  <div className="text-xs text-slate-400">Branch Probability</div>
                  <div className="text-2xl font-bold text-blue-400">
                    {Math.round((selectedBranch.probability || 0.65) * 100)}%
                  </div>
                </div>
              </div>

              {/* Critical Events Timeline */}
              <div className="space-y-2">
                <div className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                  Critical Projected Events
                </div>
                <div className="space-y-1.5">
                  {(selectedBranch.critical_events || []).map((evt, idx) => (
                    <div key={idx} className="p-2.5 bg-slate-950/80 rounded border border-slate-800 flex items-center gap-2 text-xs text-slate-200">
                      <span className="text-blue-400 font-bold">•</span>
                      <span>{evt}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Projected State */}
              <div className="space-y-2">
                <div className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                  Projected World State Variables
                </div>
                <pre className="p-3 bg-slate-950/80 rounded border border-slate-800 font-mono text-xs text-cyan-300 whitespace-pre-wrap overflow-x-auto">
                  {JSON.stringify(selectedBranch.projected_state || {}, null, 2)}
                </pre>
              </div>
            </Card>
          ) : (
            <Card className="bg-slate-900/40 border-slate-800 p-12 text-center text-slate-500">
              Select a scenario branch to inspect its projection.
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
