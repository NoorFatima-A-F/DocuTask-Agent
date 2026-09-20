import React from 'react';
import { useMissionControl } from '../../context/MissionControlContext';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { ProgressRing } from '../ui/ProgressRing';

export const ConfidenceCenterSection: React.FC = () => {
  const { state } = useMissionControl();
  const { confidenceData } = state;

  return (
    <section className="w-full mt-8">
      <Card variant="glassmorphic" className="border-cyan-500/30 bg-[#0F172A]/90 shadow-[0_0_30px_rgba(0,102,255,0.15)]">
        <CardHeader className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="intelligence" size="sm">
                STAGE 9 • STATISTICAL CERTAINTY
              </Badge>
              <span className="text-xs text-[#00D2FF] font-mono">
                Power = {confidenceData.statisticalPower.toFixed(2)} (Target &ge; 0.80)
              </span>
            </div>
            <CardTitle className="mt-2 text-xl font-bold text-[#F8FAFC]">
              Statistical Confidence & Uncertainty Decomposition
            </CardTitle>
            <p className="mt-1 text-xs text-[#94A3B8]">
              Decisions are backed by rigorous statistical power formulas (n &ge; 2((z_&alpha; + z_&beta;)/ES)&sup2;) rather than arbitrary heuristics.
            </p>
          </div>

          <div className="flex items-center gap-2 bg-[#131D35] px-4 py-2 rounded-xl border border-cyan-500/40 font-mono text-xs">
            <span className="text-[#94A3B8]">Stopping Criterion:</span>
            <span className="text-[#10B981] font-bold">EXCEEDED (97.2% &ge; 95.0%)</span>
          </div>
        </CardHeader>

        <CardContent className="p-6">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
            {/* LEFT: Large Gauge & Key Intervals (5 cols) */}
            <div className="lg:col-span-5 flex flex-col items-center justify-center p-6 rounded-2xl bg-[#131D35]/80 border border-[#1E293B] text-center">
              <ProgressRing
                value={confidenceData.currentConfidence * 100}
                size={140}
                strokeWidth={10}
                variant="intelligence"
              >
                <div className="flex flex-col items-center">
                  <span className="text-2xl font-black font-mono text-[#00D2FF]">
                    {(confidenceData.currentConfidence * 100).toFixed(1)}%
                  </span>
                  <span className="text-[10px] text-[#94A3B8] font-mono">
                    ±{(confidenceData.marginOfError * 100).toFixed(1)}% MoE
                  </span>
                </div>
              </ProgressRing>

              <span className="mt-4 text-xs font-semibold text-[#F8FAFC]">
                95% Confidence Interval: [{confidenceData.confidenceInterval[0].toFixed(3)}, {confidenceData.confidenceInterval[1].toFixed(3)}]
              </span>
              <span className="text-[11px] font-mono text-[#10B981] mt-1">
                p-value: {confidenceData.pValue} • Sample Count: n={confidenceData.sampleSize}
              </span>
            </div>

            {/* RIGHT: Why Confidence Changed & Uncertainty Sources (7 cols) */}
            <div className="lg:col-span-7 space-y-4">
              <div className="p-4 rounded-xl bg-[#131D35] border border-[#1E293B]">
                <span className="text-[11px] font-bold uppercase tracking-wider text-[#00D2FF] block">
                  Why Confidence Changed
                </span>
                <p className="mt-1.5 text-xs text-[#F8FAFC] leading-relaxed">
                  {confidenceData.whyConfidenceChanged}
                </p>
              </div>

              <div className="p-4 rounded-xl bg-[#131D35] border border-[#1E293B]">
                <span className="text-[11px] font-bold uppercase tracking-wider text-[#94A3B8] block">
                  Uncertainty Sources & Active Mitigations
                </span>
                <div className="mt-2 space-y-2">
                  {confidenceData.uncertaintySources.map((unc, i) => (
                    <div
                      key={i}
                      className="flex items-center justify-between text-xs p-2 rounded bg-[#0A0F1D] border border-[#1E293B]"
                    >
                      <span className="text-[#F8FAFC]">{unc.source}</span>
                      <span className="text-[11px] font-mono text-cyan-300">
                        {unc.mitigationStatus} (-{unc.impactPercentage}%)
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </section>
  );
};
