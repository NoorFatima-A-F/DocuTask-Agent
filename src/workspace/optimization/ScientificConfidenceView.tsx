import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ScientificConfidenceView: React.FC = () => {
  const confidenceData = {
    posteriorProb: 0.9842,
    rawProb: 0.9615,
    ci95: { lower: 0.962, upper: 0.998 },
    calibrationMethod: 'Platt Logistic Sigmoid (A=-4.2, B=2.1)',
    uncertainty: {
      total: 0.124,
      aleatoric: 0.082,
      epistemic: 0.042,
      entropy: 0.098,
      infoGain: 0.038,
    },
    evidenceFactors: [
      { source: 'Schema Invariant Validator', score: 1.0, reliability: 0.99, weight: 0.99, lr: 99.0 },
      { source: 'Dual OCR Ensemble Consensus', score: 0.96, reliability: 0.92, weight: 0.883, lr: 23.0 },
      { source: 'Cross-Agent Verification Council', score: 0.97, reliability: 0.94, weight: 0.912, lr: 31.3 },
      { source: 'Episodic Memory Grounding', score: 0.88, reliability: 0.88, weight: 0.774, lr: 7.33 },
    ],
  };

  return (
    <div className="space-y-6">
      {/* Overview Card */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">🎯</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Scientific Confidence & Evidence Fusion Lab
              </h2>
              <Badge variant="intelligence" size="sm">
                BAYESIAN POSTERIOR
              </Badge>
            </div>
            <p className="text-xs text-[#94A3B8] mt-1">
              Confidence is not a single heuristic number. Decomposed into Bayesian posterior, exact Wilson confidence intervals, and uncertainty types.
            </p>
          </div>
          <div className="flex items-center gap-6">
            <div className="text-right">
              <div className="text-xs font-mono text-[#94A3B8]">Calibrated Posterior</div>
              <div className="text-2xl font-mono font-extrabold text-emerald-400">
                {(confidenceData.posteriorProb * 100).toFixed(2)}%
              </div>
            </div>
            <div className="text-right border-l border-[#1E293B] pl-6">
              <div className="text-xs font-mono text-[#94A3B8]">95% Confidence Interval</div>
              <div className="text-sm font-mono text-cyan-400 font-bold">
                [{(confidenceData.ci95.lower * 100).toFixed(1)}%, {(confidenceData.ci95.upper * 100).toFixed(1)}%]
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Grid of details */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Uncertainty Decomposition */}
        <Card className="p-5 bg-[#0F172A] border border-[#1E293B] space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold font-mono text-[#F8FAFC] flex items-center gap-2">
              <span>🔮</span> Uncertainty Decomposition
            </h3>
            <Badge variant="outline" size="sm">
              Shannon Entropy
            </Badge>
          </div>

          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-[#94A3B8]">Aleatoric Uncertainty (Data Noise)</span>
                <span className="font-mono text-cyan-400 font-bold">{confidenceData.uncertainty.aleatoric}</span>
              </div>
              <div className="w-full bg-[#131D35] h-2 rounded-full overflow-hidden">
                <div
                  className="bg-cyan-400 h-2 rounded-full"
                  style={{ width: `${confidenceData.uncertainty.aleatoric * 100}%` }}
                />
              </div>
              <p className="text-[10px] text-[#64748B] mt-1">Intrinsic visual degradation, blur, table overlap</p>
            </div>

            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-[#94A3B8]">Epistemic Uncertainty (Model Ignorance)</span>
                <span className="font-mono text-amber-400 font-bold">{confidenceData.uncertainty.epistemic}</span>
              </div>
              <div className="w-full bg-[#131D35] h-2 rounded-full overflow-hidden">
                <div
                  className="bg-amber-400 h-2 rounded-full"
                  style={{ width: `${confidenceData.uncertainty.epistemic * 100}%` }}
                />
              </div>
              <p className="text-[10px] text-[#64748B] mt-1">Novel taxonomy structure / out-of-domain sample</p>
            </div>

            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-[#94A3B8]">Shannon Binary Entropy H(p)</span>
                <span className="font-mono text-[#F8FAFC]">{confidenceData.uncertainty.entropy}</span>
              </div>
            </div>
          </div>
        </Card>

        {/* Evidence Weighting Table */}
        <Card className="p-5 bg-[#0F172A] border border-[#1E293B] lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold font-mono text-[#F8FAFC] flex items-center gap-2">
              <span>⚖️</span> Evidentiary Factor Likelihood Fusion
            </h3>
            <Badge variant="success" size="sm">
              Bayesian Log-Odds
            </Badge>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs font-mono">
              <thead>
                <tr className="border-b border-[#1E293B] text-[#64748B]">
                  <th className="pb-2">Evidence Signal</th>
                  <th className="pb-2">Raw Score</th>
                  <th className="pb-2">Reliability</th>
                  <th className="pb-2">Effective Weight</th>
                  <th className="pb-2">Bayes Likelihood Ratio (LR)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1E293B]/60">
                {confidenceData.evidenceFactors.map((f) => (
                  <tr key={f.source} className="hover:bg-[#131D35]/50">
                    <td className="py-2.5 font-sans font-semibold text-[#F8FAFC]">{f.source}</td>
                    <td className="py-2.5 text-cyan-400">{f.score.toFixed(2)}</td>
                    <td className="py-2.5 text-[#94A3B8]">{(f.reliability * 100).toFixed(0)}%</td>
                    <td className="py-2.5 text-[#F8FAFC]">{f.weight.toFixed(3)}</td>
                    <td className="py-2.5 text-emerald-400 font-bold">{f.lr.toFixed(2)}x</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </div>
  );
};
