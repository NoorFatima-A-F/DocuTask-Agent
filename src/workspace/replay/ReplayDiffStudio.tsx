import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { GitCompare, CheckCircle2, ArrowRight } from 'lucide-react';

export const ReplayDiffStudio: React.FC = () => {
  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-violet-500/20 to-purple-500/20 border border-violet-500/30 rounded-xl text-violet-400">
              <GitCompare className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Replay Diff Studio
                <Badge variant="intelligence" size="sm">Deterministic Comparison</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Compare two missions or replay sessions to visualize structural, behavioral, and confidence differences.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" size="sm">Similarity: 98.5%</Badge>
        </div>
      </div>

      {/* Comparison split cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 font-mono text-xs">
        {/* Mission A */}
        <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-3">
          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
            <span className="font-bold text-cyan-400">Reference: mission_demo_001</span>
            <Badge variant="outline" size="sm">Standard Run</Badge>
          </div>
          <div className="space-y-1.5 text-slate-300">
            <div>Planner Decomposition: <span className="text-white font-bold">3 Tasks</span></div>
            <div>Execution Latency: <span className="text-emerald-400 font-bold">680.0ms</span></div>
            <div>Confidence Score: <span className="text-cyan-400 font-bold">98.42%</span></div>
            <div>Truth Proofs: <span className="text-emerald-400 font-bold">1 Invariant Passed</span></div>
          </div>
        </Card>

        {/* Mission B */}
        <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-3">
          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
            <span className="font-bold text-purple-400">Comparison: mission_resilience_probe_042</span>
            <Badge variant="warning" size="sm">Fault Injected</Badge>
          </div>
          <div className="space-y-1.5 text-slate-300">
            <div>Planner Decomposition: <span className="text-white font-bold">4 Tasks (+1 Recovery)</span></div>
            <div>Execution Latency: <span className="text-amber-400 font-bold">1120.0ms (+440ms)</span></div>
            <div>Confidence Score: <span className="text-cyan-400 font-bold">96.10% (-2.32%)</span></div>
            <div>Truth Proofs: <span className="text-emerald-400 font-bold">1 Invariant Passed</span></div>
          </div>
        </Card>
      </div>

      {/* Diff Delta Analysis */}
      <Card className="p-5 bg-[#0F172A] border-[#1E293B] font-mono text-xs space-y-3">
        <div className="font-bold text-slate-200">Replay Delta Summary:</div>
        <div className="p-3 bg-slate-900/60 rounded border border-slate-800 text-slate-300 space-y-1">
          <div className="text-emerald-400 flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5" /> Both missions satisfied zero-violation SMT balance proofs.
          </div>
          <div className="text-amber-300 flex items-center gap-1.5">
            <ArrowRight className="w-3.5 h-3.5" /> Recovery sub-graph activated on Mission B due to image contrast variance.
          </div>
        </div>
      </Card>
    </div>
  );
};
