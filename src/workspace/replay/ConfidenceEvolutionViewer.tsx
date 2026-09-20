import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { TrendingUp, Target } from 'lucide-react';

export const ConfidenceEvolutionViewer: React.FC = () => {
  const steps = [
    { frame: 0, score: 50.0, unc: 20.0, formula: 'Prior Init', trigger: 'mission.started' },
    { frame: 2, score: 75.0, unc: 12.0, formula: 'WeightedEnsemble (v1.3.0)', trigger: 'planner.dag' },
    { frame: 5, score: 94.2, unc: 4.5, formula: 'WeightedEnsemble (v1.3.0)', trigger: 'worker.completed' },
    { frame: 8, score: 98.42, unc: 1.45, formula: 'WeightedEnsemble (v1.3.0)', trigger: 'truth.merkle' },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-purple-500/20 to-pink-500/20 border border-purple-500/30 rounded-xl text-purple-400">
              <TrendingUp className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Confidence Evolution Viewer
                <Badge variant="intelligence" size="sm">Scientific Lineage Replay</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Frame-by-frame confidence score, uncertainty intervals, and formula version progression.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" size="sm">Converged: 98.42%</Badge>
        </div>
      </div>

      {/* Evolution Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 font-mono">
        {steps.map((s) => (
          <Card key={s.frame} className="p-4 bg-[#0F172A] border-[#1E293B] space-y-2">
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>Frame #{s.frame}</span>
              <Badge variant="outline" size="sm">{s.trigger}</Badge>
            </div>
            <div className="text-2xl font-bold text-white mt-1">{s.score.toFixed(2)}%</div>
            <div className="text-[11px] text-slate-400">Uncertainty: &plusmn;{s.unc.toFixed(2)}%</div>
            <div className="text-[10px] text-cyan-400 truncate pt-2 border-t border-slate-800">{s.formula}</div>
          </Card>
        ))}
      </div>

      {/* Uncertainty & Lineage info */}
      <Card className="p-5 bg-[#0F172A] border-[#1E293B] font-mono text-xs space-y-3">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2">
          <span className="font-bold text-slate-200 flex items-center gap-2">
            <Target className="w-4 h-4 text-cyan-400" />
            Calibration & Invariance Confirmation
          </span>
          <Badge variant="success" size="sm">Monotonic Bounds Maintained</Badge>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-slate-300">
          <div>Expected Calibration Error: <span className="text-emerald-400 font-bold">0.014 (Optimal)</span></div>
          <div>Brier Score: <span className="text-cyan-400 font-bold">0.018</span></div>
          <div>Cryptographic Seal: <span className="text-amber-400 font-bold">sha256:7fa189c4...</span></div>
        </div>
      </Card>
    </div>
  );
};
