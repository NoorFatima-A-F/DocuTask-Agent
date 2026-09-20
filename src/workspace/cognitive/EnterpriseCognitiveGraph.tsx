import React, { useState, useEffect } from 'react';
import { Network, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { cognitiveApiClient } from '../../services/cognitiveApiClient';
import { CognitiveNode, CognitiveEdge } from '../../types/cognitive';

export const EnterpriseCognitiveGraph: React.FC = () => {
  const [graph, setGraph] = useState<{ nodes: CognitiveNode[]; edges: CognitiveEdge[] } | null>(null);

  const loadData = async () => {
    const data = await cognitiveApiClient.getCognitiveGraph();
    setGraph(data);
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Network className="w-7 h-7 text-cyan-400" />
            Enterprise Cognitive Reasoning Graph
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Visual multi-hop causal reasoning connecting KPIs, Business Goals, Agents, Risks, and Hypotheses.
          </p>
        </div>
        <Button variant="outline" onClick={loadData}>
          <span className="flex items-center gap-2">
            <RefreshCw className="w-4 h-4" />
            Refresh Graph
          </span>
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-3">
          <h2 className="text-base font-semibold text-slate-200">Cognitive Reasoning Nodes ({graph?.nodes.length || 0})</h2>
          <div className="space-y-2 max-h-[460px] overflow-y-auto">
            {graph?.nodes.map((n) => (
              <div key={n.id} className="p-3 rounded-lg bg-slate-800/40 border border-slate-700/60 space-y-1">
                <div className="flex justify-between items-center">
                  <Badge variant="outline" className="text-cyan-400 border-cyan-500/30 text-[10px]">
                    {n.node_type}
                  </Badge>
                  <span className="text-[10px] text-slate-500 font-mono">{n.id}</span>
                </div>
                <p className="text-sm font-medium text-slate-200">{n.name}</p>
              </div>
            ))}
          </div>
        </Card>

        <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-3">
          <h2 className="text-base font-semibold text-slate-200">Causal Relational Edges ({graph?.edges.length || 0})</h2>
          <div className="space-y-2 max-h-[460px] overflow-y-auto">
            {graph?.edges.map((e) => {
              const src = graph.nodes.find(n => n.id === e.source_node_id);
              const tgt = graph.nodes.find(n => n.id === e.target_node_id);
              return (
                <div key={e.id} className="p-3 rounded-lg bg-slate-800/40 border border-slate-700/60 text-xs flex items-center justify-between">
                  <span className="font-medium text-slate-200">{src?.name || e.source_node_id}</span>
                  <span className="px-2 py-1 bg-indigo-950/60 text-indigo-300 rounded font-mono">
                    --({e.relation})--&gt;
                  </span>
                  <span className="font-medium text-slate-200">{tgt?.name || e.target_node_id}</span>
                </div>
              );
            })}
          </div>
        </Card>
      </div>
    </div>
  );
};
