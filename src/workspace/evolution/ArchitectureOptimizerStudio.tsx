import React, { useState, useEffect } from 'react';
import {
  Sliders,
  RefreshCw,
  Sparkles,
  Calculator,
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
import { OptimizationCandidatePayload } from '../../types/evolutionPlatform';

export const ArchitectureOptimizerStudio: React.FC = () => {
  const [candidates, setCandidates] = useState<OptimizationCandidatePayload[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [generating, setGenerating] = useState<boolean>(false);

  // Optimizer tuning parameters
  const [targetSubsystem, setTargetSubsystem] = useState<string>('llm_cognition');
  const [objective, setObjective] = useState<string>('TOKEN_EFFICIENCY');
  const [riskTolerance, setRiskTolerance] = useState<number>(0.15);

  useEffect(() => {
    loadCandidates();
  }, []);

  const loadCandidates = async () => {
    setLoading(true);
    try {
      const data = await EvolutionPlatformApiClient.listOptimizationCandidates();
      setCandidates(data);
    } catch (err) {
      console.error('Failed to load optimization candidates:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const newCand = await EvolutionPlatformApiClient.generateCandidate({
        target_subsystem: targetSubsystem,
        objective: objective,
        custom_risk_tolerance: riskTolerance,
      });
      setCandidates((prev) => [newCand, ...prev]);
    } catch (err) {
      console.error('Candidate generation failed:', err);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-amber-500/10 border border-amber-500/20 rounded-xl">
            <Sliders className="w-6 h-6 text-amber-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-slate-100">Multi-Objective Pareto Optimizer Studio</h1>
              <Badge variant="intelligence" size="sm">Bayesian & Genetic Search</Badge>
            </div>
            <p className="text-sm text-slate-400 mt-0.5">
              Simultaneously optimizes latency, token economy, and accuracy with mathematical proofs and Pareto ranking.
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            onClick={loadCandidates}
            disabled={loading}
          >
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button
            variant="intelligence"
            onClick={handleGenerate}
            disabled={generating}
          >
            <span className="flex items-center gap-2">
              <Sparkles className={`w-4 h-4 ${generating ? 'animate-spin' : ''}`} />
              {generating ? 'Optimizing Frontier...' : 'Generate Pareto Candidate'}
            </span>
          </Button>
        </div>
      </div>

      {/* Control Tuning Panel */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-sm font-semibold text-slate-200">Hyperparameter & Subsystem Target Configuration</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div>
            <label className="text-xs font-medium text-slate-400 block mb-1">Target Subsystem</label>
            <select
              value={targetSubsystem}
              onChange={(e) => setTargetSubsystem(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-amber-500"
            >
              <option value="llm_cognition">LLM Cognition Layer</option>
              <option value="memory_layer">Episodic Vector Memory</option>
              <option value="swarm_orchestrator">Swarm Coordination Ring</option>
              <option value="governance_sentinel">Governance & Sentinel</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-medium text-slate-400 block mb-1">Primary Optimization Objective</label>
            <select
              value={objective}
              onChange={(e) => setObjective(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-amber-500"
            >
              <option value="TOKEN_EFFICIENCY">Token Efficiency (Min Context Waste)</option>
              <option value="LATENCY_REDUCTION">Latency Reduction (Lock-Free SIMD)</option>
              <option value="ACCURACY_MAXIMIZATION">Accuracy Maximization</option>
              <option value="COST_MINIMIZATION">Cost Minimization</option>
              <option value="SAFETY_COMPLIANCE">Safety & Guardrail Compliance</option>
            </select>
          </div>

          <div>
            <div className="flex items-center justify-between text-xs font-medium text-slate-400 mb-1">
              <span>Risk Tolerance Threshold</span>
              <span className="font-mono text-amber-400">{(riskTolerance * 100).toFixed(0)}%</span>
            </div>
            <input
              type="range"
              min="0.05"
              max="0.40"
              step="0.01"
              value={riskTolerance}
              onChange={(e) => setRiskTolerance(parseFloat(e.target.value))}
              className="w-full accent-amber-400 cursor-pointer mt-2"
            />
            <div className="flex justify-between text-[10px] text-slate-500 font-mono mt-1">
              <span>Strict Zero-Risk (5%)</span>
              <span>Aggressive (40%)</span>
            </div>
          </div>
        </div>
      </div>

      {/* Candidate Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {candidates.map((c) => (
          <div
            key={c.candidate_id}
            className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4 hover:border-slate-700 transition-all flex flex-col justify-between"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-slate-300">{c.candidate_id}</span>
                <Badge variant={c.pareto_rank === 1 ? 'intelligence' : 'outline'} size="sm">
                  Pareto Rank #{c.pareto_rank}
                </Badge>
              </div>
              <div className="text-sm font-semibold text-slate-100">{c.target_subsystem}</div>
              <div className="text-xs text-amber-400 font-mono">Objective: {c.objective}</div>
            </div>

            {/* Proof text */}
            <div className="p-3 bg-slate-950/80 border border-slate-800/80 rounded-lg text-xs text-slate-400 font-mono space-y-1">
              <div className="flex items-center gap-1.5 text-slate-300 font-bold">
                <Calculator className="w-3.5 h-3.5 text-amber-400" />
                <span>Mathematical Proof</span>
              </div>
              <p className="line-clamp-3 text-[11px] text-slate-400">{c.mathematical_proof}</p>
            </div>

            {/* Metrics footer */}
            <div className="pt-3 border-t border-slate-800/80 grid grid-cols-3 gap-2 text-center text-xs font-mono">
              <div className="bg-slate-950/60 p-2 rounded">
                <div className="text-slate-500 text-[10px]">GAIN</div>
                <div className="text-emerald-400 font-semibold">+{c.expected_gain_pct.toFixed(1)}%</div>
              </div>
              <div className="bg-slate-950/60 p-2 rounded">
                <div className="text-slate-500 text-[10px]">FITNESS</div>
                <div className="text-indigo-300 font-semibold">{(c.fitness_score * 100).toFixed(1)}%</div>
              </div>
              <div className="bg-slate-950/60 p-2 rounded">
                <div className="text-slate-500 text-[10px]">RISK</div>
                <div className="text-amber-300 font-semibold">{(c.estimated_risk * 100).toFixed(1)}%</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
