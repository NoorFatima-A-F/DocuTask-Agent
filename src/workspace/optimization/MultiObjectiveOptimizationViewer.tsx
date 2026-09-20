import React, { useState } from 'react';
import {
  Sliders,
  Scale,
  TrendingUp,
  CheckCircle2,
  RefreshCw,
  Award,
  Layers,
  BarChart3,
  Target
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

interface MultiObjectiveOptimizationViewerProps {
  missionId?: string;
}

interface ObjectiveWeight {
  id: string;
  name: string;
  description: string;
  weight: number;
  unit: string;
  color: string;
  icon: React.ReactNode;
}

interface ParetoCandidate {
  id: string;
  name: string;
  cost: number;
  latencyMs: number;
  confidence: number;
  throughputRps: number;
  compositeScore: number;
  isParetoOptimal: boolean;
  selected: boolean;
}

export const MultiObjectiveOptimizationViewer: React.FC<MultiObjectiveOptimizationViewerProps> = ({
  missionId = 'mission-current',
}) => {
  const [weights, setWeights] = useState<ObjectiveWeight[]>([
    { id: 'cost', name: 'Monetary Cost', description: 'Minimize API tokens, compute, and OCR costs', weight: 0.25, unit: 'USD', color: 'emerald', icon: <Scale className="w-4 h-4 text-emerald-400" /> },
    { id: 'latency', name: 'Turnaround Latency', description: 'Minimize time-to-first-extraction and completion latency', weight: 0.25, unit: 'ms', color: 'amber', icon: <TrendingUp className="w-4 h-4 text-amber-400" /> },
    { id: 'confidence', name: 'Extraction Confidence', description: 'Maximize scientific confidence and zero-fabrication guarantees', weight: 0.40, unit: '%', color: 'indigo', icon: <Target className="w-4 h-4 text-indigo-400" /> },
    { id: 'throughput', name: 'Concurrency / Throughput', description: 'Maximize parallel document ingestion volume', weight: 0.10, unit: 'doc/s', color: 'purple', icon: <BarChart3 className="w-4 h-4 text-purple-400" /> },
  ]);

  const [candidates] = useState<ParetoCandidate[]>([
    { id: 'cand-1', name: 'Ultra-Fast Flash-Lite OCR', cost: 0.008, latencyMs: 380, confidence: 0.885, throughputRps: 120, compositeScore: 0.74, isParetoOptimal: true, selected: false },
    { id: 'cand-2', name: 'Balanced Hybrid Cloud (Recommended)', cost: 0.034, latencyMs: 950, confidence: 0.962, throughputRps: 45, compositeScore: 0.91, isParetoOptimal: true, selected: true },
    { id: 'cand-3', name: 'High-Precision Ensemble Pro', cost: 0.125, latencyMs: 2400, confidence: 0.994, throughputRps: 12, compositeScore: 0.86, isParetoOptimal: true, selected: false },
    { id: 'cand-4', name: 'Suboptimal Legacy Single-Pass', cost: 0.082, latencyMs: 2100, confidence: 0.912, throughputRps: 15, compositeScore: 0.62, isParetoOptimal: false, selected: false },
    { id: 'cand-5', name: 'Aggressive Quantized Local', cost: 0.003, latencyMs: 620, confidence: 0.830, throughputRps: 80, compositeScore: 0.69, isParetoOptimal: true, selected: false },
  ]);

  const [selectedCandidateId, setSelectedCandidateId] = useState<string>('cand-2');

  const updateWeight = (id: string, newWeight: number) => {
    setWeights(prev => {
      const updated = prev.map(w => w.id === id ? { ...w, weight: Math.max(0, Math.min(1, newWeight)) } : w);
      const total = updated.reduce((sum, w) => sum + w.weight, 0);
      if (total === 0) return updated;
      return updated.map(w => ({ ...w, weight: parseFloat((w.weight / total).toFixed(3)) }));
    });
  };

  const selectedCandidate: ParetoCandidate = candidates.find(c => c.id === selectedCandidateId) ?? candidates[0]!;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Sliders className="w-5 h-5 text-indigo-400" />
            Multi-Objective Optimization & Pareto Frontier Studio
          </h2>
          <p className="text-sm text-slate-400">
            Scalarized multi-objective trade-off solver across cost, latency, confidence, and throughput for mission: <code className="text-indigo-300 font-mono text-xs">{missionId}</code>
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="intelligence" size="md">
            Pareto Dimension: 4D Convex Hull
          </Badge>
          <button className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700">
            <RefreshCw className="w-3.5 h-3.5" />
            Re-solve Frontier
          </button>
        </div>
      </div>

      {/* Objective Weight Tuning Sliders */}
      <Card className="p-5 bg-slate-900 border-slate-800">
        <h3 className="text-sm font-semibold text-slate-200 mb-3 flex items-center gap-2">
          <Scale className="w-4 h-4 text-indigo-400" />
          Interactive Scalarization Weight Vector (Normalized Sum = 1.0)
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {weights.map(obj => (
            <div key={obj.id} className="p-3.5 rounded-lg bg-slate-950 border border-slate-800">
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center gap-2">
                  {obj.icon}
                  <span className="text-xs font-semibold text-slate-200">{obj.name}</span>
                </div>
                <span className="text-xs font-mono font-bold text-indigo-400">
                  {(obj.weight * 100).toFixed(1)}%
                </span>
              </div>
              <p className="text-[11px] text-slate-400 mb-2 leading-tight">{obj.description}</p>
              <input
                type="range"
                min="0"
                max="100"
                value={Math.round(obj.weight * 100)}
                onChange={(e) => updateWeight(obj.id, parseFloat(e.target.value) / 100)}
                className="w-full accent-indigo-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg appearance-none"
              />
            </div>
          ))}
        </div>
      </Card>

      {/* Candidate Solutions on Pareto Frontier */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <Card className="p-5 bg-slate-900 border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
                <Layers className="w-4 h-4 text-purple-400" />
                Pareto Non-Dominated Solutions Matrix
              </h3>
              <span className="text-xs text-slate-400">{candidates.filter(c => c.isParetoOptimal).length} Non-Dominated Fronts</span>
            </div>

            <div className="space-y-2.5">
              {candidates.map(cand => {
                const isSelected = cand.id === selectedCandidateId;
                return (
                  <div
                    key={cand.id}
                    onClick={() => setSelectedCandidateId(cand.id)}
                    className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                      isSelected
                        ? 'bg-indigo-950/40 border-indigo-500/50 shadow-lg shadow-indigo-950/30'
                        : cand.isParetoOptimal
                        ? 'bg-slate-950/60 border-slate-800 hover:border-slate-700'
                        : 'bg-slate-950/30 border-slate-800/50 opacity-60'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        {cand.isParetoOptimal ? (
                          <Award className="w-4 h-4 text-amber-400" />
                        ) : (
                          <div className="w-4 h-4 rounded-full border border-slate-600 flex items-center justify-center text-[9px] text-slate-500">✕</div>
                        )}
                        <span className="text-xs font-semibold text-slate-200">{cand.name}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        {cand.isParetoOptimal ? (
                          <Badge variant="success" size="sm">Pareto Optimal</Badge>
                        ) : (
                          <Badge variant="default" size="sm">Dominated</Badge>
                        )}
                        <span className="text-xs font-mono font-bold text-indigo-400">
                          Score: {(cand.compositeScore * 100).toFixed(0)}
                        </span>
                      </div>
                    </div>

                    <div className="grid grid-cols-4 gap-2 pt-2 border-t border-slate-800/80 text-[11px] font-mono">
                      <div>
                        <span className="text-slate-500 block text-[10px]">Cost:</span>
                        <span className="text-emerald-400 font-semibold">${cand.cost.toFixed(3)}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[10px]">Latency:</span>
                        <span className="text-amber-400 font-semibold">{cand.latencyMs}ms</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[10px]">Confidence:</span>
                        <span className="text-indigo-400 font-semibold">{(cand.confidence * 100).toFixed(1)}%</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[10px]">Throughput:</span>
                        <span className="text-purple-400 font-semibold">{cand.throughputRps} rps</span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </Card>
        </div>

        {/* Selected Candidate Deep Dive */}
        <div>
          <Card className="p-5 bg-slate-900 border-slate-800 space-y-4">
            <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              Solution Envelope Details
            </h3>

            <div className="p-3.5 rounded-lg bg-slate-950 border border-slate-800 space-y-3">
              <div>
                <span className="text-xs text-slate-400 block mb-0.5">Configuration</span>
                <span className="text-sm font-bold text-slate-100">{selectedCandidate.name}</span>
              </div>
              <div className="space-y-2">
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-slate-400">Confidence Guarantee</span>
                    <span className="text-indigo-400 font-mono font-semibold">{(selectedCandidate.confidence * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                    <div className="bg-indigo-500 h-full rounded-full" style={{ width: `${selectedCandidate.confidence * 100}%` }} />
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-slate-400">Relative Latency</span>
                    <span className="text-amber-400 font-mono font-semibold">{selectedCandidate.latencyMs} ms</span>
                  </div>
                  <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                    <div className="bg-amber-500 h-full rounded-full" style={{ width: `${Math.min(100, (selectedCandidate.latencyMs / 2500) * 100)}%` }} />
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-slate-400">Financial Spend</span>
                    <span className="text-emerald-400 font-mono font-semibold">${selectedCandidate.cost.toFixed(3)}</span>
                  </div>
                  <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                    <div className="bg-emerald-500 h-full rounded-full" style={{ width: `${Math.min(100, (selectedCandidate.cost / 0.15) * 100)}%` }} />
                  </div>
                </div>
              </div>
            </div>

            <button className="w-full py-2 px-3 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg shadow-lg shadow-indigo-600/20 transition-all flex items-center justify-center gap-1.5">
              <CheckCircle2 className="w-4 h-4" />
              Commit Selected Frontier Directive
            </button>
          </Card>
        </div>
      </div>
    </div>
  );
};
