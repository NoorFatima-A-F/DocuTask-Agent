import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { HelpCircle, Percent } from 'lucide-react';

interface IntervalItem {
  dimension: string;
  mean: number;
  ci95Low: number;
  ci95High: number;
  ci99Low: number;
  ci99High: number;
  aleatoric: number;
  epistemic: number;
}

const intervals: IntervalItem[] = [
  {
    dimension: 'Overall Mission Confidence',
    mean: 98.42,
    ci95Low: 96.97,
    ci95High: 99.87,
    ci99Low: 96.25,
    ci99High: 99.98,
    aleatoric: 0.008,
    epistemic: 0.006,
  },
  {
    dimension: 'OCR Quality',
    mean: 99.20,
    ci95Low: 98.40,
    ci95High: 100.00,
    ci99Low: 97.90,
    ci99High: 100.00,
    aleatoric: 0.005,
    epistemic: 0.003,
  },
  {
    dimension: 'Schema Extraction',
    mean: 98.00,
    ci95Low: 96.80,
    ci95High: 99.20,
    ci99Low: 96.10,
    ci99High: 99.70,
    aleatoric: 0.009,
    epistemic: 0.004,
  },
  {
    dimension: 'Invariant Validation',
    mean: 99.90,
    ci95Low: 99.80,
    ci95High: 100.00,
    ci99Low: 99.70,
    ci99High: 100.00,
    aleatoric: 0.001,
    epistemic: 0.000,
  },
  {
    dimension: 'Planner Efficiency',
    mean: 95.00,
    ci95Low: 92.90,
    ci95High: 97.10,
    ci99Low: 91.80,
    ci99High: 98.20,
    aleatoric: 0.015,
    epistemic: 0.006,
  },
];

export const UncertaintyIntervalViewer: React.FC = () => {
  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-violet-500/20 to-purple-500/20 border border-violet-500/30 rounded-xl text-violet-400">
              <Percent className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Uncertainty Intervals & Variance Decomposition
                <Badge variant="intelligence" size="sm">Aleatoric vs Epistemic</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Rigorous statistical confidence intervals (95% & 99%) and uncertainty variance decomposition.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" size="sm">Bounds Narrow & Stable</Badge>
        </div>
      </div>

      {/* Uncertainty Decomposition Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card className="p-5 bg-[#0F172A] border-[#1E293B]">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-mono font-bold text-violet-400">Aleatoric Uncertainty (Data / Noise)</span>
            <Badge variant="outline" size="sm">0.008 Total</Badge>
          </div>
          <p className="text-xs text-slate-400">
            Irreducible noise present in environment observations, tool responses, and document scans.
          </p>
        </Card>

        <Card className="p-5 bg-[#0F172A] border-[#1E293B]">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-mono font-bold text-indigo-400">Epistemic Uncertainty (Model / Knowledge)</span>
            <Badge variant="success" size="sm">0.006 Total (Low)</Badge>
          </div>
          <p className="text-xs text-slate-400">
            Reducible uncertainty due to lack of training/calibration data or missing runtime context.
          </p>
        </Card>
      </div>

      {/* Table of intervals */}
      <Card className="p-5 bg-[#0F172A] border-[#1E293B]">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-bold font-mono text-slate-200">Dimension Confidence Intervals</h2>
          <span className="text-xs text-slate-500 font-mono flex items-center gap-1">
            <HelpCircle className="w-3.5 h-3.5" /> Normal Gaussian Projection
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-[#1E293B]/60 text-slate-400 border-b border-[#1E293B]">
              <tr>
                <th className="p-3">Dimension</th>
                <th className="p-3">Mean (&mu;)</th>
                <th className="p-3">95% CI Range</th>
                <th className="p-3">99% CI Range</th>
                <th className="p-3">Aleatoric</th>
                <th className="p-3">Epistemic</th>
                <th className="p-3">Total Width</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E293B]/40">
              {intervals.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-800/30 transition-colors">
                  <td className="p-3 font-semibold text-slate-100">{item.dimension}</td>
                  <td className="p-3 text-cyan-400 font-bold">{item.mean.toFixed(2)}%</td>
                  <td className="p-3 text-emerald-400">
                    [{item.ci95Low.toFixed(2)}%, {item.ci95High.toFixed(2)}%]
                  </td>
                  <td className="p-3 text-indigo-300">
                    [{item.ci99Low.toFixed(2)}%, {item.ci99High.toFixed(2)}%]
                  </td>
                  <td className="p-3 text-slate-400">{item.aleatoric.toFixed(4)}</td>
                  <td className="p-3 text-slate-400">{item.epistemic.toFixed(4)}</td>
                  <td className="p-3 text-slate-200">
                    ±{((item.ci95High - item.mean)).toFixed(2)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
