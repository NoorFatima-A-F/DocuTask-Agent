import React, { useState, useEffect } from 'react';
import { Layers, Network, Cpu, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { knowledgeApiClient } from '../../services/knowledgeApiClient';
import { GraphNode, GraphEdge } from '../../types/knowledge';

export const KnowledgeGraphExplorer: React.FC = () => {
  const [graphData, setGraphData] = useState<{ nodes: GraphNode[]; edges: GraphEdge[]; total_nodes: number; total_edges: number } | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);

  const loadGraph = async () => {
    setLoading(true);
    try {
      const data = await knowledgeApiClient.getGraphOverview();
      setGraphData(data);
      if (data.nodes.length > 0 && !selectedNode) {
        setSelectedNode(data.nodes[0] || null);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadGraph();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Network className="w-7 h-7 text-cyan-400" />
            Enterprise Knowledge Graph & Ontology
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Visual organizational ontology connecting employees, departments, AI agents, systems, and policies.
          </p>
        </div>
        <Button variant="outline" onClick={loadGraph}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh Graph
          </span>
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Graph Entities List */}
        <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-4">
          <h2 className="text-base font-semibold text-slate-200 flex items-center gap-2">
            <Layers className="w-4 h-4 text-cyan-400" />
            Ontology Nodes ({graphData?.total_nodes || 0})
          </h2>
          <div className="space-y-2 max-h-[460px] overflow-y-auto">
            {graphData?.nodes.map((node) => (
              <div
                key={node.id}
                onClick={() => setSelectedNode(node)}
                className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                  selectedNode?.id === node.id
                    ? 'bg-cyan-950/40 border-cyan-500/50'
                    : 'bg-slate-800/40 border-slate-700/50 hover:border-slate-600'
                }`}
              >
                <div className="flex justify-between items-center mb-1">
                  <Badge variant="outline" className="text-cyan-400 border-cyan-500/30 text-[10px]">
                    {node.entity_type}
                  </Badge>
                  <span className="text-[10px] text-slate-500">Confidence: 100%</span>
                </div>
                <p className="text-sm font-medium text-slate-200">{node.name}</p>
              </div>
            ))}
          </div>
        </Card>

        {/* Node Inspection & Relational Links */}
        <Card className="p-5 bg-slate-900/60 border-slate-800 lg:col-span-2 space-y-5">
          <div>
            <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2 mb-1">
              <Cpu className="w-5 h-5 text-indigo-400" />
              Entity Traversal & Impact Analysis
            </h2>
            <p className="text-xs text-slate-400">
              Selected node: <span className="text-cyan-400 font-semibold">{selectedNode?.name || 'None'}</span>
            </p>
          </div>

          {selectedNode && (
            <div className="p-4 rounded-lg bg-slate-800/60 border border-slate-700 space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-xs text-slate-400 uppercase font-semibold">Node ID</span>
                <span className="font-mono text-xs text-slate-300">{selectedNode.id}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-slate-400 uppercase font-semibold">Entity Type</span>
                <Badge variant="info">{selectedNode.entity_type}</Badge>
              </div>
            </div>
          )}

          <div>
            <h3 className="text-sm font-semibold text-slate-200 mb-3">Relational Graph Connections</h3>
            <div className="space-y-2">
              {graphData?.edges.map((edge) => {
                const src = graphData.nodes.find(n => n.id === edge.source_node_id);
                const tgt = graphData.nodes.find(n => n.id === edge.target_node_id);
                return (
                  <div key={edge.id} className="p-3 bg-slate-800/40 rounded border border-slate-700/60 flex items-center justify-between text-xs">
                    <span className="font-medium text-slate-200">{src?.name || edge.source_node_id}</span>
                    <span className="px-2 py-1 bg-cyan-950/60 text-cyan-300 rounded font-mono">
                      --({edge.relation_type})--&gt;
                    </span>
                    <span className="font-medium text-slate-200">{tgt?.name || edge.target_node_id}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
