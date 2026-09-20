import React, { useState, useEffect } from 'react';
import type { DecisionGraph, DecisionRecord } from '../../types/esmrReplay';
import { EsmrReplayApiClient } from '../../services/esmrReplayApiClient';

interface DecisionGraphViewProps {
  missionId: string;
}

export const DecisionGraphView: React.FC<DecisionGraphViewProps> = ({ missionId }) => {
  const [graph, setGraph] = useState<DecisionGraph | null>(null);
  const [decisions, setDecisions] = useState<DecisionRecord[]>([]);
  const [selectedDecision, setSelectedDecision] = useState<DecisionRecord | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    Promise.all([
      EsmrReplayApiClient.getDecisionGraph(missionId),
      EsmrReplayApiClient.getDecisions(missionId),
    ])
      .then(([g, d]) => {
        setGraph(g);
        setDecisions(d);
        if (d.length > 0 && d[0]) setSelectedDecision(d[0]);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [missionId]);

  if (loading || !graph) {
    return (
      <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl text-slate-400 animate-pulse">
        Reconstructing Autonomous Decision Provenance DAG...
      </div>
    );
  }

  return (
    <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 shadow-2xl space-y-6 text-slate-100">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <span>🧠</span> Decision Provenance & Explainability Graph
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Proven Decisions: <span className="font-mono text-cyan-400">{graph.nodes.length}</span> | Coverage:{' '}
            <span className="font-mono text-emerald-400">{graph.coverage_percentage.toFixed(1)}%</span>
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-3 py-1 text-xs font-mono bg-purple-950/70 border border-purple-500/40 text-purple-300 rounded-lg">
            ZERO HALLUCINATION COGNITIVE LOG
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Nodes List */}
        <div className="space-y-3">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono">
            Decision Lineage Nodes
          </h4>
          <div className="space-y-2 max-h-[450px] overflow-y-auto pr-1">
            {decisions.map((dec) => (
              <div
                key={dec.decision_id}
                onClick={() => setSelectedDecision(dec)}
                className={`p-3 rounded-lg border cursor-pointer transition-all ${
                  selectedDecision?.decision_id === dec.decision_id
                    ? 'bg-cyan-950/60 border-cyan-500 text-white shadow-lg'
                    : 'bg-slate-900/80 border-slate-800 hover:border-slate-700 text-slate-300'
                }`}
              >
                <div className="flex items-center justify-between text-xs font-mono">
                  <span className="font-semibold text-cyan-400">{dec.decision_id}</span>
                  <span className="text-emerald-400 font-bold">{(dec.confidence * 100).toFixed(0)}% Conf</span>
                </div>
                <div className="text-sm font-semibold mt-1 text-slate-100">{dec.selected_strategy}</div>
                <div className="text-xs text-slate-400 mt-1 line-clamp-2">{dec.why}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Selected Decision Deep-Dive */}
        <div className="lg:col-span-2 space-y-4 bg-slate-900/60 border border-slate-800 p-5 rounded-xl">
          {selectedDecision ? (
            <>
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div>
                  <span className="text-xs font-mono text-cyan-400">Gen {selectedDecision.planner_generation} Strategy Decision</span>
                  <h4 className="text-base font-bold text-white mt-0.5">{selectedDecision.selected_strategy}</h4>
                </div>
                <div className="text-right">
                  <span className="text-xs font-mono text-slate-400">Total Utility</span>
                  <div className="text-lg font-bold text-emerald-400 font-mono">
                    {selectedDecision.utility_breakdown.total_utility.toFixed(4)}
                  </div>
                </div>
              </div>

              {/* 4 Pillars of Explainability */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                {/* WHY */}
                <div className="bg-slate-950/80 border border-slate-800 p-3.5 rounded-lg space-y-1">
                  <span className="font-bold text-cyan-400 uppercase tracking-wider font-mono">1. Why (Rationale)</span>
                  <p className="text-slate-300 leading-relaxed">{selectedDecision.why}</p>
                </div>

                {/* WHAT */}
                <div className="bg-slate-950/80 border border-slate-800 p-3.5 rounded-lg space-y-1">
                  <span className="font-bold text-emerald-400 uppercase tracking-wider font-mono">2. What (Action Executed)</span>
                  <p className="text-slate-300 leading-relaxed">{selectedDecision.what}</p>
                </div>

                {/* BASED ON */}
                <div className="bg-slate-950/80 border border-slate-800 p-3.5 rounded-lg space-y-1">
                  <span className="font-bold text-purple-400 uppercase tracking-wider font-mono">3. Based On (Evidence)</span>
                  <pre className="text-[11px] text-slate-300 font-mono overflow-x-auto">
                    {JSON.stringify(selectedDecision.based_on, null, 2)}
                  </pre>
                </div>

                {/* WHY NOT OTHERS */}
                <div className="bg-slate-950/80 border border-slate-800 p-3.5 rounded-lg space-y-1">
                  <span className="font-bold text-amber-400 uppercase tracking-wider font-mono">4. Why Not Others (Counterfactuals)</span>
                  <div className="space-y-1 text-slate-300">
                    {Object.entries(selectedDecision.why_not_others).map(([alt, reason]) => (
                      <div key={alt} className="border-b border-slate-800/80 pb-1">
                        <span className="text-amber-300 font-semibold">{alt}:</span> {reason}
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Multi-Objective Utility Breakdown */}
              <div className="bg-slate-950 border border-slate-800 p-4 rounded-lg space-y-2">
                <span className="text-xs font-bold text-slate-400 uppercase font-mono">Pareto Utility Breakdown</span>
                <div className="grid grid-cols-4 gap-2 text-center">
                  <div className="bg-slate-900 p-2 rounded border border-slate-800">
                    <span className="text-[10px] text-slate-400 block font-mono">Accuracy</span>
                    <span className="text-xs font-bold text-cyan-400 font-mono">
                      {(selectedDecision.utility_breakdown.accuracy * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="bg-slate-900 p-2 rounded border border-slate-800">
                    <span className="text-[10px] text-slate-400 block font-mono">Latency</span>
                    <span className="text-xs font-bold text-emerald-400 font-mono">
                      {(selectedDecision.utility_breakdown.latency_score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="bg-slate-900 p-2 rounded border border-slate-800">
                    <span className="text-[10px] text-slate-400 block font-mono">Cost</span>
                    <span className="text-xs font-bold text-amber-400 font-mono">
                      {(selectedDecision.utility_breakdown.cost_score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="bg-slate-900 p-2 rounded border border-slate-800">
                    <span className="text-[10px] text-slate-400 block font-mono">Safety</span>
                    <span className="text-xs font-bold text-purple-400 font-mono">
                      {(selectedDecision.utility_breakdown.safety_score * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>

              {/* Provenance Hash */}
              <div className="text-[11px] font-mono text-slate-400 flex items-center justify-between bg-slate-950 p-2.5 rounded border border-slate-800">
                <span>Provenance SHA-256:</span>
                <span className="text-cyan-400">{selectedDecision.sha256_provenance_hash}</span>
              </div>
            </>
          ) : (
            <div className="text-center py-12 text-slate-500">Select a decision node to view provenance breakdown.</div>
          )}
        </div>
      </div>
    </div>
  );
};
