import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { GitCommit, ArrowRight } from 'lucide-react';

export const DependencyExplorerView: React.FC = () => {
  const edges = [
    { source: 'node_goal_ingress', target: 'node_split_ocr', type: 'HARD_DEPENDENCY', condition: 'Valid prompt' },
    { source: 'node_split_ocr', target: 'node_ocr_chunk_1', type: 'HARD_DEPENDENCY', condition: 'Page 1-2 rasterized' },
    { source: 'node_split_ocr', target: 'node_ocr_chunk_2', type: 'HARD_DEPENDENCY', condition: 'Page 3-4 rasterized' },
    { source: 'node_ocr_chunk_1', target: 'node_merge_ocr', type: 'DATA_FLOW', condition: 'Text chunk emitted' },
    { source: 'node_ocr_chunk_2', target: 'node_merge_ocr', type: 'DATA_FLOW', condition: 'Table chunk emitted' },
    { source: 'node_merge_ocr', target: 'node_extract_schema', type: 'HARD_DEPENDENCY', condition: 'Merged markdown ready' },
    { source: 'node_extract_schema', target: 'node_validate_invariants', type: 'HARD_DEPENDENCY', condition: 'Fields parsed' },
    { source: 'node_validate_invariants', target: 'node_barrier_governance', type: 'CONDITIONAL', condition: 'Arithmetic invariant passed' },
    { source: 'node_barrier_governance', target: 'node_join_finalize', type: 'BARRIER_SYNC', condition: 'All checks synchronized' },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-indigo-500/20 to-cyan-500/20 border border-indigo-500/30 rounded-xl text-indigo-400">
              <GitCommit className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                DAG Dependency Explorer & Edge Topology
                <Badge variant="success" size="sm">9 Edges</Badge>
              </h1>
              <p className="text-xs text-[#94A3B8] font-mono">
                Typed dependency resolution (Hard, Data Flow, Conditional, Barrier Sync)
              </p>
            </div>
          </div>
        </div>

        <Badge variant="intelligence" size="md">Zero Dependency Cycles</Badge>
      </div>

      {/* Edge List */}
      <div className="space-y-3 font-mono">
        {edges.map((edge, idx) => (
          <Card key={idx} className="p-4 rounded-xl border border-[#1E293B] bg-[#0F172A] flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-3 text-xs">
              <span className="text-[#64748B] w-6">{idx + 1}.</span>
              <span className="font-bold text-cyan-400">{edge.source}</span>
              <ArrowRight className="w-4 h-4 text-[#64748B]" />
              <span className="font-bold text-emerald-400">{edge.target}</span>
            </div>

            <div className="flex items-center gap-4 text-xs">
              <span className="text-[#94A3B8] text-[11px] italic">Condition: {edge.condition}</span>
              <Badge variant={edge.type === 'CONDITIONAL' ? 'warning' : edge.type === 'BARRIER_SYNC' ? 'intelligence' : 'default'} size="sm">
                {edge.type}
              </Badge>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
