import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  GitBranch,
  RefreshCw,
  Plus,
  Minus,
} from 'lucide-react';
import { ApdlePlannerApiClient } from '../../services/apdlePlannerApiClient';
import { GraphMutationRecordPayload } from '../../types/apdlePlanner';

export const GraphMutationTimeline: React.FC = () => {
  const [mutations, setMutations] = useState<GraphMutationRecordPayload[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadMutations();
  }, []);

  const loadMutations = async () => {
    setLoading(true);
    try {
      const data = await ApdlePlannerApiClient.getMutations('default_mission');
      setMutations(data);
    } catch (e) {
      console.error('Failed to load mutations:', e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 font-mono">
      {/* Header Banner */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-sm font-bold text-cyan-300 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-purple-400" />
              Runtime Graph Mutation & Replanning History
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Audit log of in-flight structural DAG alterations. Inspects injected recovery pipelines and topology diffs.
            </p>
          </div>

          <button
            onClick={loadMutations}
            disabled={loading}
            className="text-slate-400 hover:text-cyan-400 p-1.5 rounded"
            title="Refresh"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>

        {/* Mutation Stream */}
        {mutations.length === 0 ? (
          <div className="p-8 text-center text-slate-500 text-xs bg-slate-950/60 rounded-lg">
            No runtime mutations applied yet. The DAG is currently executing on its nominal synthesis plan.
          </div>
        ) : (
          <div className="space-y-3">
            {mutations.map((m, idx) => (
              <div
                key={m.mutation_id || idx}
                className="p-4 bg-slate-950/80 border border-purple-800/60 rounded-xl space-y-2 text-xs"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-purple-300 flex items-center gap-2">
                    <GitBranch className="w-3.5 h-3.5" />
                    Mutation {m.mutation_type}
                  </span>
                  <span className="text-[10px] text-slate-500">{m.mutation_id}</span>
                </div>

                <div className="text-slate-300 text-[11px]">{m.trigger_reason}</div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 border-t border-slate-800/80 text-[10px]">
                  <div className="flex items-center gap-1 text-emerald-400">
                    <Plus className="w-3 h-3" /> {m.nodes_added_count} Nodes Added
                  </div>
                  <div className="flex items-center gap-1 text-slate-400">
                    <Minus className="w-3 h-3" /> {m.nodes_removed_count} Nodes Removed
                  </div>
                  <div className="flex items-center gap-1 text-cyan-300">
                    +{m.edges_added_count} Edges Rewired
                  </div>
                  <div className="text-right text-slate-500">
                    {new Date(m.timestamp * 1000).toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
