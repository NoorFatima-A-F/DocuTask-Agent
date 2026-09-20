/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 5: Causal Analysis Workbench
 */

import React, { useEffect, useState } from 'react';
import {
  GitBranch,
  RefreshCw,
  Zap,
  CheckCircle2,
  Sliders,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
import { CausalGraph } from '../../types/worldModelPlatform';

export const CausalAnalysisWorkbench: React.FC = () => {
  const [graph, setGraph] = useState<CausalGraph | null>(null);
  const [loading, setLoading] = useState(true);
  const [targetNode, setTargetNode] = useState('k8s_replicas_count');
  const [interventionVal, setInterventionVal] = useState('6');
  const [simulating, setSimulating] = useState(false);
  const [interventionResult, setInterventionResult] = useState<any>(null);

  const fetchCausal = async () => {
    setLoading(true);
    try {
      const res = await WorldModelApiClient.getCausalGraph();
      setGraph(res.graph || null);
    } catch (err) {
      console.error('Error fetching causal graph:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCausal();
  }, []);

  const handleSimulateIntervention = async (e: React.FormEvent) => {
    e.preventDefault();
    setSimulating(true);
    try {
      const res = await WorldModelApiClient.executeCausalIntervention({
        target_node: targetNode,
        interventions: { [targetNode]: parseFloat(interventionVal) || interventionVal },
      });
      setInterventionResult(res.causal_effect || res.intervention || res);
    } catch (err) {
      console.error('Error executing causal intervention:', err);
    } finally {
      setSimulating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 border border-amber-500/30 rounded-xl p-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-amber-500/10 border border-amber-500/30 rounded-lg text-amber-400">
            <GitBranch className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-white tracking-tight">Causal Analysis Workbench</h1>
              <Badge variant="intelligence">Pearl's do-calculus</Badge>
            </div>
            <p className="text-sm text-slate-400">
              Structural Causal Models (SCM), DAG edge discovery, confounder adjustments, and synthetic interventional simulations.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={fetchCausal} disabled={loading}>
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Active Causal DAG */}
        <Card className="bg-slate-900/60 border-slate-800 p-5 lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-semibold text-white flex items-center gap-2">
              <GitBranch className="w-5 h-5 text-amber-400" />
              Active Structural Causal DAG & Path Coefficients
            </h3>
            <Badge variant="intelligence">{graph?.edges?.length || 2} Causal Paths</Badge>
          </div>

          <div className="space-y-3">
            {(graph?.edges || []).map((edge, idx) => (
              <div
                key={idx}
                className="p-4 bg-slate-950/80 rounded-lg border border-slate-800 space-y-2 hover:border-amber-500/40 transition-all"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-amber-400 font-mono font-semibold text-sm">{edge.source_id}</span>
                    <span className="text-slate-500 font-bold">―(do)→</span>
                    <span className="text-cyan-400 font-mono font-semibold text-sm">{edge.target_id}</span>
                  </div>
                  <Badge variant="warning">Weight: {edge.weight}</Badge>
                </div>

                <div className="flex items-center justify-between text-xs text-slate-400 pt-1">
                  <div>Strength: <strong className="text-slate-200 capitalize">{edge.strength}</strong></div>
                  <div>Mechanism: <span className="text-slate-300 font-mono text-[11px]">{edge.mechanism || 'Direct path'}</span></div>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Interventional do(X=x) Simulator */}
        <Card className="bg-slate-900/60 border-slate-800 p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-semibold text-white flex items-center gap-2">
              <Sliders className="w-5 h-5 text-cyan-400" />
              Interventional do(X) Simulator
            </h3>
          </div>

          <form onSubmit={handleSimulateIntervention} className="space-y-4 text-xs">
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Target Action Variable</label>
              <input
                type="text"
                value={targetNode}
                onChange={(e) => setTargetNode(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-white font-mono text-xs focus:outline-none focus:border-amber-500"
              />
            </div>

            <div>
              <label className="block text-slate-300 font-semibold mb-1">Forced Intervention Value</label>
              <input
                type="text"
                value={interventionVal}
                onChange={(e) => setInterventionVal(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-white font-mono text-xs focus:outline-none focus:border-amber-500"
              />
            </div>

            <Button variant="intelligence" type="submit" disabled={simulating} className="w-full">
              <span className="flex items-center justify-center gap-2">
                <Zap className="w-4 h-4" />
                {simulating ? 'Computing do(X)...' : 'Simulate Intervention'}
              </span>
            </Button>
          </form>

          {interventionResult && (
            <div className="p-3 bg-amber-950/40 border border-amber-500/40 rounded-lg space-y-2 text-xs text-amber-200 animate-in fade-in">
              <div className="font-semibold text-amber-300 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-amber-400" />
                Causal Effect Estimated
              </div>
              <pre className="p-2 bg-slate-950/80 rounded font-mono text-[11px] text-slate-200 whitespace-pre-wrap overflow-x-auto">
                {JSON.stringify(interventionResult, null, 2)}
              </pre>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};
