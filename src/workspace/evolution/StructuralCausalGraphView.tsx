import React, { useState, useEffect } from 'react';
import {
  Compass,
  Sliders,
  RefreshCw,
  Zap,
} from 'lucide-react';
import { CognitiveEvolutionApiClient } from '../../services/cognitiveEvolutionApiClient';
import { InterventionResultPayload, CausalNodePayload } from '../../types/cognitiveEvolution';

export const StructuralCausalGraphView: React.FC = () => {
  const [nodes, setNodes] = useState<CausalNodePayload[]>([]);
  const [intervention, setIntervention] = useState<InterventionResultPayload | null>(null);
  const [treatmentVal, setTreatmentVal] = useState<number>(8.0);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadCausalModel();
  }, [treatmentVal]);

  const loadCausalModel = async () => {
    setLoading(true);
    try {
      const [nodesRes, intervRes] = await Promise.all([
        CognitiveEvolutionApiClient.getCausalModel(),
        CognitiveEvolutionApiClient.executeDoIntervention(treatmentVal),
      ]);
      setNodes(nodesRes);
      setIntervention(intervRes);
    } catch (e) {
      console.error('Failed to load SCM data:', e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 font-mono">
      {/* Top Banner & Pearl Do-Calculus Controls */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-sm font-bold text-cyan-300 flex items-center gap-2">
              <Compass className="w-4 h-4 text-purple-400" />
              Structural Causal Models & Pearl's Do-Calculus Interventions
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Distinguishes causation from correlation. Evaluates interventional distributions $P(Y \mid do(X = x))$ via graph surgery and backdoor criteria.
            </p>
          </div>

          <button
            onClick={loadCausalModel}
            disabled={loading}
            className="text-slate-400 hover:text-cyan-400 p-1.5 rounded"
            title="Refresh"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>

        {/* Treatment Slider (do(Worker Concurrency = x)) */}
        <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-4 space-y-3">
          <div className="flex items-center justify-between text-xs">
            <span className="text-slate-300 flex items-center gap-2">
              <Sliders className="w-3.5 h-3.5 text-purple-400" />
              Graph Surgery Treatment: <span className="text-purple-300 font-bold">do(Worker Concurrency = {treatmentVal})</span>
            </span>
            <span className="text-cyan-300 font-bold">{treatmentVal} Nodes</span>
          </div>

          <input
            type="range"
            min="1"
            max="16"
            step="1"
            value={treatmentVal}
            onChange={(e) => setTreatmentVal(parseInt(e.target.value))}
            className="w-full accent-purple-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
          />
          <div className="flex justify-between text-[10px] text-slate-500">
            <span>1 Node (Sequential)</span>
            <span>4 Nodes (Observational Default)</span>
            <span>16 Nodes (Massive Parallel)</span>
          </div>
        </div>
      </div>

      {/* Intervention & Average Treatment Effect (ATE) Results Card */}
      {intervention && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h4 className="text-xs uppercase text-slate-300 tracking-wider flex items-center gap-2">
                <Zap className="w-4 h-4 text-cyan-400" />
                Interventional Effect Calculation
              </h4>
              <span className="px-2 py-0.5 rounded text-[10px] bg-purple-950 text-purple-300 border border-purple-800">
                Backdoor Adjusted
              </span>
            </div>

            <div className="grid grid-cols-3 gap-3">
              <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-3 text-center">
                <div className="text-[10px] text-slate-500 uppercase">Observational E[Y]</div>
                <div className="text-lg font-bold text-slate-200 mt-1">
                  {intervention.observational_expectation_e_y.toFixed(0)}ms
                </div>
              </div>

              <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-3 text-center">
                <div className="text-[10px] text-slate-500 uppercase">Interventional E[Y|do(X)]</div>
                <div className="text-lg font-bold text-emerald-400 mt-1">
                  {intervention.interventional_expectation_e_y_do_x.toFixed(0)}ms
                </div>
              </div>

              <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-3 text-center">
                <div className="text-[10px] text-slate-500 uppercase">Causal Effect (ATE)</div>
                <div className="text-lg font-bold text-cyan-300 mt-1">
                  {intervention.causal_effect_ate.toFixed(0)}ms
                </div>
              </div>
            </div>

            <div className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg text-xs text-slate-300">
              <span className="text-slate-500">Causal Explanation: </span>
              {intervention.summary}
            </div>
          </div>

          {/* SCM Structural Nodes List */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3">
            <div className="text-xs uppercase text-slate-300 tracking-wider">SCM Variable Nodes</div>
            <div className="space-y-2">
              {nodes.map((n) => (
                <div key={n.node_id} className="p-2.5 bg-slate-950/70 border border-slate-800 rounded text-xs">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-slate-200">{n.name}</span>
                    <span className="text-[9px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
                      {n.is_treatment ? 'TREATMENT' : n.is_outcome ? 'OUTCOME' : n.is_confounder ? 'CONFOUNDER' : 'MEDIATOR'}
                    </span>
                  </div>
                  <div className="text-[10px] text-slate-500 mt-1">
                    Parents: {n.parents.length > 0 ? n.parents.join(', ') : 'None (Exogenous)'}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
