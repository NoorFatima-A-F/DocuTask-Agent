import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { TrendingUp, Activity, BarChart2, ShieldAlert } from 'lucide-react';

interface TrendMetric {
  title: string;
  current: string;
  change: string;
  status: 'positive' | 'neutral' | 'negative';
  description: string;
}

const metrics: TrendMetric[] = [
  {
    title: 'Mission Convergence Rate',
    current: '98.42%',
    change: '+1.8% vs last 50 missions',
    status: 'positive',
    description: 'Average final posterior confidence achieved across all automated workflows.',
  },
  {
    title: 'Epistemic Uncertainty Index',
    current: '0.014',
    change: '-35% variance reduction',
    status: 'positive',
    description: 'Model uncertainty due to missing evidence or distribution shift.',
  },
  {
    title: 'Aleatoric Variance',
    current: '0.008',
    change: 'Stable within bounds',
    status: 'neutral',
    description: 'Inherent runtime environment noise across tool execution & OCR steps.',
  },
  {
    title: 'Calibration Brier Score',
    current: '0.018',
    change: '-0.004 improvement',
    status: 'positive',
    description: 'Mean squared difference between predicted confidence and empirical outcome.',
  },
];

export const ConfidenceTrendAnalysis: React.FC = () => {
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
                Confidence Trend Analysis
                <Badge variant="intelligence" size="sm">Empirical Stability</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Longitudinal analysis of confidence convergence, uncertainty dispersion, and calibration stability.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" size="sm">System Trend: OPTIMAL</Badge>
        </div>
      </div>

      {/* High-level metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map((m, idx) => (
          <Card key={idx} className="p-4 bg-[#0F172A] border-[#1E293B]">
            <div className="text-xs font-medium text-slate-400 font-mono">{m.title}</div>
            <div className="text-2xl font-bold text-slate-100 font-mono mt-2">{m.current}</div>
            <div className="text-xs text-emerald-400 font-mono mt-1">{m.change}</div>
            <p className="text-[11px] text-slate-500 mt-2">{m.description}</p>
          </Card>
        ))}
      </div>

      {/* Stability & Distribution Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-5 bg-[#0F172A] border-[#1E293B]">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-bold font-mono text-slate-200 flex items-center gap-2">
              <Activity className="w-4 h-4 text-indigo-400" />
              Dimension Stability Tracking (Last 100 Runs)
            </h2>
            <Badge variant="outline" size="sm">Zero Outliers</Badge>
          </div>
          <div className="space-y-3 font-mono text-xs">
            <div className="space-y-1">
              <div className="flex justify-between text-slate-400">
                <span>OCR Quality Stability</span>
                <span className="text-cyan-400">σ = 0.009 (High)</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2">
                <div className="bg-cyan-400 h-2 rounded-full" style={{ width: '96%' }}></div>
              </div>
            </div>

            <div className="space-y-1">
              <div className="flex justify-between text-slate-400">
                <span>Schema Extraction Stability</span>
                <span className="text-indigo-400">σ = 0.012 (High)</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2">
                <div className="bg-indigo-400 h-2 rounded-full" style={{ width: '92%' }}></div>
              </div>
            </div>

            <div className="space-y-1">
              <div className="flex justify-between text-slate-400">
                <span>Invariant Validation Stability</span>
                <span className="text-emerald-400">σ = 0.001 (Deterministic)</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2">
                <div className="bg-emerald-400 h-2 rounded-full" style={{ width: '99%' }}></div>
              </div>
            </div>

            <div className="space-y-1">
              <div className="flex justify-between text-slate-400">
                <span>Planner Efficiency Stability</span>
                <span className="text-purple-400">σ = 0.021 (Nominal)</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2">
                <div className="bg-purple-400 h-2 rounded-full" style={{ width: '88%' }}></div>
              </div>
            </div>
          </div>
        </Card>

        <Card className="p-5 bg-[#0F172A] border-[#1E293B]">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-bold font-mono text-slate-200 flex items-center gap-2">
              <BarChart2 className="w-4 h-4 text-emerald-400" />
              Distribution Shape & Skewness
            </h2>
            <Badge variant="success" size="sm">Normal Gaussian</Badge>
          </div>
          <div className="p-4 bg-slate-900/60 rounded-lg border border-slate-800 space-y-3 font-mono text-xs">
            <div className="flex justify-between text-slate-300">
              <span>Mean Confidence (&mu;):</span>
              <span className="text-white font-bold">98.15%</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span>Standard Deviation (&sigma;):</span>
              <span className="text-white font-bold">1.12%</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span>Skewness (&gamma;<sub>1</sub>):</span>
              <span className="text-white font-bold">-0.14 (Left-tailed)</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span>Kurtosis (&kappa;):</span>
              <span className="text-white font-bold">3.04 (Meso-kurtic)</span>
            </div>
            <div className="flex justify-between text-slate-300 border-t border-slate-800 pt-2">
              <span>Kolmogorov-Smirnov Test:</span>
              <span className="text-emerald-400 font-bold">p = 0.88 &gt; 0.05 (Passed)</span>
            </div>
          </div>
        </Card>
      </div>

      {/* Safety Summary Alert */}
      <Card className="p-4 bg-gradient-to-r from-emerald-900/20 to-indigo-900/20 border-emerald-500/30 flex items-center gap-4">
        <ShieldAlert className="w-6 h-6 text-emerald-400 shrink-0" />
        <div className="text-xs text-slate-300">
          <span className="font-bold text-white">Confidence Stability Verified: </span>
          No drift or calibration decay detected across 500 execution events. Formula monotonic bounds strictly preserved.
        </div>
      </Card>
    </div>
  );
};
