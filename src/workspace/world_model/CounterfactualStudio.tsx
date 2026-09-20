/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 8: Counterfactual Studio
 */

import React, { useEffect, useState } from 'react';
import {
  Sparkles,
  RefreshCw,
  GitCompare,
  Sliders,
  Zap,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
import { CounterfactualWorld } from '../../types/worldModelPlatform';

export const CounterfactualStudio: React.FC = () => {
  const [simulations, setSimulations] = useState<CounterfactualWorld[]>([]);
  const [loading, setLoading] = useState(true);
  const [queryTarget, setQueryTarget] = useState('P99 Document Extraction Latency');
  const [intervention, setIntervention] = useState('autoscaling_threshold_cpu = 0.6');
  const [simulating, setSimulating] = useState(false);

  const fetchSimulations = async () => {
    setLoading(true);
    try {
      const res = await WorldModelApiClient.getCounterfactuals();
      setSimulations(res.counterfactuals || []);
    } catch (err) {
      console.error('Error fetching counterfactuals:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSimulations();
  }, []);

  const handleSimulate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSimulating(true);
    try {
      await WorldModelApiClient.simulateCounterfactual({
        base_snapshot_id: 'snap-01',
        interventions: { threshold: 0.6 },
        query_target: queryTarget,
        factual_outcome: '2.4 seconds',
      });
      await fetchSimulations();
    } catch (err) {
      console.error('Error running counterfactual:', err);
    } finally {
      setSimulating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 border border-teal-500/30 rounded-xl p-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-teal-500/10 border border-teal-500/30 rounded-lg text-teal-400">
            <GitCompare className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-white tracking-tight">Counterfactual Studio</h1>
              <Badge variant="intelligence">Twin-World Simulation</Badge>
            </div>
            <p className="text-sm text-slate-400">
              Evaluates retrospective and prospective "what-if" branches, computing outcome divergence and causal attribution.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={fetchSimulations} disabled={loading}>
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Past Simulations */}
        <div className="lg:col-span-2 space-y-4">
          <h3 className="text-base font-semibold text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-teal-400" />
            Simulated Twin-World Counterfactuals
          </h3>

          <div className="space-y-4">
            {simulations.map((sim) => (
              <Card key={sim.simulation_id} className="bg-slate-900/60 border-slate-800 p-5 space-y-4 hover:border-teal-500/40 transition-all">
                <div className="flex items-start justify-between">
                  <div>
                    <span className="text-xs font-mono text-teal-400 bg-teal-950/60 px-2 py-0.5 rounded border border-teal-500/30">
                      {sim.simulation_id}
                    </span>
                    <h4 className="text-base font-bold text-white mt-1.5">{sim.query_target}</h4>
                  </div>
                  <Badge variant="success">Divergence: {sim.divergence_score}</Badge>
                </div>

                {/* Factual vs Counterfactual Comparison */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                  <div className="p-3 bg-slate-950/80 rounded border border-slate-800 space-y-1">
                    <span className="text-slate-400 font-semibold uppercase text-[10px]">Factual Outcome (Observed)</span>
                    <div className="text-base font-bold text-slate-200">{String(sim.factual_outcome)}</div>
                  </div>

                  <div className="p-3 bg-teal-950/30 rounded border border-teal-500/30 space-y-1">
                    <span className="text-teal-400 font-semibold uppercase text-[10px]">Counterfactual Outcome (Twin World)</span>
                    <div className="text-base font-bold text-teal-300">{String(sim.counterfactual_outcome)}</div>
                  </div>
                </div>

                <div className="p-3 bg-slate-950/80 rounded border border-slate-800 text-xs">
                  <span className="text-slate-400 block mb-1 font-semibold">Causal Attribution:</span>
                  <span className="text-emerald-300">{sim.causal_attribution}</span>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* What-If Query Form */}
        <Card className="bg-slate-900/60 border-slate-800 p-5 space-y-4">
          <h3 className="text-base font-semibold text-white flex items-center gap-2">
            <Sliders className="w-5 h-5 text-teal-400" />
            Query Counterfactual
          </h3>

          <form onSubmit={handleSimulate} className="space-y-4 text-xs">
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Query Metric / Target</label>
              <input
                type="text"
                required
                value={queryTarget}
                onChange={(e) => setQueryTarget(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-white text-xs"
              />
            </div>

            <div>
              <label className="block text-slate-300 font-semibold mb-1">Intervention Hypothesis</label>
              <input
                type="text"
                required
                value={intervention}
                onChange={(e) => setIntervention(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-white text-xs font-mono"
              />
            </div>

            <Button variant="intelligence" type="submit" disabled={simulating} className="w-full">
              <span className="flex items-center justify-center gap-2">
                <Zap className="w-4 h-4" />
                {simulating ? 'Simulating Twin World...' : 'Simulate Counterfactual'}
              </span>
            </Button>
          </form>
        </Card>
      </div>
    </div>
  );
};
