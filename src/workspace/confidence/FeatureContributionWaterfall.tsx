import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { BarChart3 } from 'lucide-react';

export const FeatureContributionWaterfall: React.FC = () => {
  const waterfallSteps = [
    { step: 1, feature: 'validation_constraint_satisfaction', value: 1.000, weight: '35%', contribution: '+0.3500', runningTotal: '35.0%' },
    { step: 2, feature: 'ocr_mean_confidence', value: 0.992, weight: '20%', contribution: '+0.1984', runningTotal: '54.8%' },
    { step: 3, feature: 'extraction_cross_field_consistency', value: 0.990, weight: '20%', contribution: '+0.1980', runningTotal: '74.6%' },
    { step: 4, feature: 'evidence_hash_integrity', value: 1.000, weight: '15%', contribution: '+0.1500', runningTotal: '89.6%' },
    { step: 5, feature: 'planner_dag_efficiency', value: 0.950, weight: '10%', contribution: '+0.0950', runningTotal: '99.1%' },
    { step: 6, feature: 'temperature_scaling_calibration', value: 1.050, weight: 'CALIB', contribution: '-0.0070', runningTotal: '98.4%' },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-cyan-500/20 to-teal-500/20 border border-cyan-500/30 rounded-xl text-cyan-400">
              <BarChart3 className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Feature Contribution Waterfall & Attribution
                <Badge variant="success" size="sm">Additive SHAP-Equivalent</Badge>
              </h1>
              <p className="text-xs text-[#94A3B8] font-mono">
                Step-by-step breakdown of how raw features and weights accumulate to form final confidence
              </p>
            </div>
          </div>
        </div>

        <Badge variant="intelligence" size="md">Final Score: 98.42%</Badge>
      </div>

      {/* Waterfall Steps */}
      <div className="space-y-3 font-mono">
        {waterfallSteps.map(step => (
          <Card key={step.step} className="p-4 rounded-xl border border-[#1E293B] bg-[#0F172A] flex flex-wrap items-center justify-between gap-4 hover:border-cyan-500/40 transition-all">
            <div className="flex items-center gap-4">
              <div className="w-8 h-8 rounded-lg bg-[#131D35] border border-[#1E293B] flex items-center justify-center text-xs font-bold text-cyan-400">
                0{step.step}
              </div>
              <div>
                <h3 className="text-xs font-bold text-white">{step.feature}</h3>
                <span className="text-[11px] text-[#64748B]">Weight: {step.weight} • Raw Value: {step.value}</span>
              </div>
            </div>

            <div className="flex items-center gap-6 text-xs">
              <div className="text-right">
                <span className="text-[10px] text-[#64748B] block">CONTRIBUTION</span>
                <span className={`font-bold ${step.contribution.startsWith('+') ? 'text-emerald-400' : 'text-amber-400'}`}>
                  {step.contribution}
                </span>
              </div>
              <div className="text-right min-w-[80px]">
                <span className="text-[10px] text-[#64748B] block">RUNNING TOTAL</span>
                <span className="text-cyan-400 font-extrabold">{step.runningTotal}</span>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
