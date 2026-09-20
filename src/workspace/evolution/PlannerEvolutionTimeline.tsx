import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  TrendingUp,
  CheckCircle2,
  RefreshCw,
  Trophy,
} from 'lucide-react';
import { CognitiveEvolutionApiClient } from '../../services/cognitiveEvolutionApiClient';
import { PlannerGenerationPayload, EvolutionCycleReportPayload } from '../../types/cognitiveEvolution';

export const PlannerEvolutionTimeline: React.FC = () => {
  const [generations, setGenerations] = useState<PlannerGenerationPayload[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [evolving, setEvolving] = useState<boolean>(false);
  const [evolutionReport, setEvolutionReport] = useState<EvolutionCycleReportPayload | null>(null);

  useEffect(() => {
    loadGenerations();
  }, []);

  const loadGenerations = async () => {
    setLoading(true);
    try {
      const data = await CognitiveEvolutionApiClient.listPlannerGenerations();
      setGenerations(data);
    } catch (e) {
      console.error('Failed to load planner generations:', e);
    } finally {
      setLoading(false);
    }
  };

  const handleTriggerEvolution = async () => {
    setEvolving(true);
    try {
      const report = await CognitiveEvolutionApiClient.evolvePlanner('Sub-optimal token allocation in high-noise scans');
      setEvolutionReport(report);
      await loadGenerations();
    } catch (e) {
      console.error('Planner self-evolution failed:', e);
    } finally {
      setEvolving(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner & Self-Evolution Trigger */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-sm font-bold font-mono text-cyan-300 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-cyan-400" />
              Planner Self-Evolution & Continuous Rewriting Engine
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Closed-loop evolutionary self-rewriting: Weakness Detection &rarr; Chromosome Mutation &rarr; 1,000 Trial Digital Twin Simulation &rarr; Canary Promotion.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleTriggerEvolution}
              disabled={evolving}
              className="flex items-center gap-2 px-3 py-1.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white rounded-lg text-xs font-mono font-bold shadow-lg shadow-purple-950/40 transition-all disabled:opacity-50"
            >
              <Sparkles className={`w-3.5 h-3.5 ${evolving ? 'animate-spin' : ''}`} />
              Evolve Next Planner Generation
            </button>

            <button
              onClick={loadGenerations}
              disabled={loading}
              className="text-slate-400 hover:text-cyan-400 p-1.5 rounded"
              title="Refresh generations"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </div>

        {evolutionReport && (
          <div className="p-4 bg-purple-950/40 border border-purple-800/60 rounded-lg space-y-2 font-mono text-xs">
            <div className="flex items-center justify-between text-purple-300 font-bold">
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                Evolution Cycle Success: {evolutionReport.previous_version} &rarr; {evolutionReport.candidate_version}
              </span>
              <span className="text-emerald-400 font-bold">+{evolutionReport.utility_gain_pct}% Pareto Gain</span>
            </div>
            <p className="text-slate-300 text-[11px]">{evolutionReport.rationale}</p>
          </div>
        )}
      </div>

      {/* Planner Generations Genealogy Timeline */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h4 className="text-xs font-mono uppercase tracking-wider text-slate-400">
            Immutable Planner Generation Genealogy ({generations.length} Versions)
          </h4>
          <span className="text-[10px] font-mono text-slate-500">
            Cryptographically Sealed Merkle Lineage
          </span>
        </div>

        <div className="space-y-3">
          {generations.map((gen, idx) => {
            const isProduction = gen.is_promoted_production;
            return (
              <div
                key={gen.generation_id || idx}
                className={`p-5 rounded-xl border font-mono transition-all ${
                  isProduction
                    ? 'bg-slate-900/90 border-cyan-500/60 shadow-lg shadow-cyan-950/20'
                    : 'bg-slate-950/70 border-slate-800/80'
                }`}
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 text-cyan-300 flex items-center justify-center font-bold text-sm">
                      {gen.version_tag}
                    </div>
                    <div>
                      <div className="text-sm font-bold text-slate-100 flex items-center gap-2">
                        <span>Generation {idx + 1}</span>
                        {isProduction && (
                          <span className="px-2 py-0.5 rounded text-[10px] bg-cyan-950 text-cyan-300 border border-cyan-800 flex items-center gap-1">
                            <Trophy className="w-3 h-3 text-amber-400" />
                            ACTIVE PRODUCTION
                          </span>
                        )}
                      </div>
                      <div className="text-[10px] text-slate-500 mt-0.5">
                        Parent: {gen.parent_version || 'None (Genesis)'} &bull; Sealed:{' '}
                        <span className="text-purple-400">{gen.cryptographic_seal_hash.slice(0, 16)}...</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-4 text-right">
                    <div>
                      <div className="text-[10px] text-slate-500 uppercase">Benchmark Utility</div>
                      <div className="text-base font-bold text-emerald-400">{gen.benchmark_utility.toFixed(4)}</div>
                    </div>
                    <div>
                      <div className="text-[10px] text-slate-500 uppercase">Brier Error (↓)</div>
                      <div className="text-base font-bold text-purple-300">{gen.brier_score.toFixed(3)}</div>
                    </div>
                  </div>
                </div>

                {/* Parameters Matrix */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-3 text-xs">
                  <div className="bg-slate-950/60 border border-slate-800/60 rounded p-2 text-center">
                    <span className="text-[10px] text-slate-500 uppercase">Weight Acc</span>
                    <div className="font-bold text-slate-200 mt-0.5">{gen.parameters.weight_accuracy || 0.5}</div>
                  </div>
                  <div className="bg-slate-950/60 border border-slate-800/60 rounded p-2 text-center">
                    <span className="text-[10px] text-slate-500 uppercase">Weight Cost</span>
                    <div className="font-bold text-slate-200 mt-0.5">{gen.parameters.weight_cost || 0.3}</div>
                  </div>
                  <div className="bg-slate-950/60 border border-slate-800/60 rounded p-2 text-center">
                    <span className="text-[10px] text-slate-500 uppercase">Beam Width</span>
                    <div className="font-bold text-cyan-300 mt-0.5">{gen.parameters.beam_width || 8}</div>
                  </div>
                  <div className="bg-slate-950/60 border border-slate-800/60 rounded p-2 text-center">
                    <span className="text-[10px] text-slate-500 uppercase">Sim. Trials</span>
                    <div className="font-bold text-amber-300 mt-0.5">{gen.simulated_trials_count}</div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
