import React, { useState } from 'react';
import {
  LineChart,
  BrainCircuit,
  TrendingUp,
  Cpu,
  RefreshCw,
  Sparkles,
  Zap,
  Layers
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

interface PredictionAnalyticsDashboardProps {
  missionId?: string;
}

interface QuantileDistribution {
  p50: number;
  p90: number;
  p95: number;
  p99: number;
  unit: string;
}

export const PredictionAnalyticsDashboard: React.FC<PredictionAnalyticsDashboardProps> = ({
  missionId = 'mission-current',
}) => {
  const [selectedTaskType, setSelectedTaskType] = useState<string>('INVOICE_TABLE_EXTRACTION');

  const [latencyQuantiles] = useState<QuantileDistribution>({
    p50: 820,
    p90: 1240,
    p95: 1560,
    p99: 2100,
    unit: 'ms',
  });

  const [tokenQuantiles] = useState<QuantileDistribution>({
    p50: 1850,
    p90: 2900,
    p95: 3400,
    p99: 4800,
    unit: 'tokens',
  });

  const [costQuantiles] = useState<QuantileDistribution>({
    p50: 0.024,
    p90: 0.048,
    p95: 0.062,
    p99: 0.098,
    unit: 'USD',
  });

  const taskHistograms = [
    { name: 'Gemini 1.5 Flash + Tesseract', avgLatency: 640, avgTokens: 1400, confidenceMean: 0.942, p99Risk: 'LOW' },
    { name: 'Gemini 1.5 Pro + Azure OCR', avgLatency: 1850, avgTokens: 3800, confidenceMean: 0.988, p99Risk: 'MEDIUM' },
    { name: 'Claude 3.5 Sonnet + Textract', avgLatency: 2200, avgTokens: 4200, confidenceMean: 0.991, p99Risk: 'HIGH' },
    { name: 'Local Quantized LLaVA + EasyOCR', avgLatency: 480, avgTokens: 900, confidenceMean: 0.880, p99Risk: 'LOW' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <LineChart className="w-5 h-5 text-indigo-400" />
            Probabilistic Resource & Latency Prediction Analytics
          </h2>
          <p className="text-sm text-slate-400">
            Bayesian prior and parametric quantile forecasting (p50, p90, p95, p99) for mission: <code className="text-indigo-300 font-mono text-xs">{missionId}</code>
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="intelligence" size="md">
            Model: Kalman + Empirical Bayes
          </Badge>
          <button className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700">
            <RefreshCw className="w-3.5 h-3.5" />
            Recalibrate Priors
          </button>
        </div>
      </div>

      {/* Task Filter Selector */}
      <div className="flex items-center gap-2">
        <span className="text-xs text-slate-400 font-medium">Task Class:</span>
        {['INVOICE_TABLE_EXTRACTION', 'RECEIPT_NER', 'CONTRACT_CLAUSE_ANALYSIS', 'PATENT_SEARCH'].map(t => (
          <button
            key={t}
            onClick={() => setSelectedTaskType(t)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              selectedTaskType === t
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'bg-slate-900 text-slate-400 border border-slate-800 hover:border-slate-700 hover:text-slate-200'
            }`}
          >
            {t.replace(/_/g, ' ')}
          </button>
        ))}
      </div>

      {/* Quantile Distributions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Latency Quantiles */}
        <Card className="p-5 bg-slate-900 border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-amber-400" />
              Turnaround Latency Forecast
            </span>
            <Badge variant="warning" size="sm">ms</Badge>
          </div>

          <div className="space-y-2.5">
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400 font-mono">p50 (Median):</span>
              <span className="text-slate-200 font-bold font-mono">{latencyQuantiles.p50} ms</span>
            </div>
            <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
              <div className="bg-amber-400 h-full rounded-full" style={{ width: '40%' }} />
            </div>

            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400 font-mono">p90:</span>
              <span className="text-amber-400 font-bold font-mono">{latencyQuantiles.p90} ms</span>
            </div>
            <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
              <div className="bg-amber-500 h-full rounded-full" style={{ width: '60%' }} />
            </div>

            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400 font-mono">p95:</span>
              <span className="text-orange-400 font-bold font-mono">{latencyQuantiles.p95} ms</span>
            </div>
            <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
              <div className="bg-orange-500 h-full rounded-full" style={{ width: '75%' }} />
            </div>

            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400 font-mono">p99 (Tail):</span>
              <span className="text-rose-400 font-bold font-mono">{latencyQuantiles.p99} ms</span>
            </div>
            <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
              <div className="bg-rose-500 h-full rounded-full" style={{ width: '100%' }} />
            </div>
          </div>
        </Card>

        {/* Token Spend Forecast */}
        <Card className="p-5 bg-slate-900 border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-indigo-400" />
              Token Consumption Forecast
            </span>
            <Badge variant="intelligence" size="sm">tokens</Badge>
          </div>

          <div className="space-y-2.5">
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400 font-mono">p50 (Median):</span>
              <span className="text-slate-200 font-bold font-mono">{tokenQuantiles.p50} tok</span>
            </div>
            <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
              <div className="bg-indigo-400 h-full rounded-full" style={{ width: '38%' }} />
            </div>

            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400 font-mono">p90:</span>
              <span className="text-indigo-400 font-bold font-mono">{tokenQuantiles.p90} tok</span>
            </div>
            <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
              <div className="bg-indigo-500 h-full rounded-full" style={{ width: '60%' }} />
            </div>

            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400 font-mono">p95:</span>
              <span className="text-purple-400 font-bold font-mono">{tokenQuantiles.p95} tok</span>
            </div>
            <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
              <div className="bg-purple-500 h-full rounded-full" style={{ width: '70%' }} />
            </div>

            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400 font-mono">p99 (Tail):</span>
              <span className="text-rose-400 font-bold font-mono">{tokenQuantiles.p99} tok</span>
            </div>
            <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
              <div className="bg-rose-500 h-full rounded-full" style={{ width: '100%' }} />
            </div>
          </div>
        </Card>

        {/* Cost Forecast */}
        <Card className="p-5 bg-slate-900 border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-emerald-400" />
              Dollar Cost Per Document
            </span>
            <Badge variant="success" size="sm">USD</Badge>
          </div>

          <div className="space-y-2.5">
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400 font-mono">p50 (Median):</span>
              <span className="text-emerald-400 font-bold font-mono">${costQuantiles.p50.toFixed(3)}</span>
            </div>
            <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
              <div className="bg-emerald-400 h-full rounded-full" style={{ width: '25%' }} />
            </div>

            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400 font-mono">p90:</span>
              <span className="text-emerald-400 font-bold font-mono">${costQuantiles.p90.toFixed(3)}</span>
            </div>
            <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
              <div className="bg-emerald-500 h-full rounded-full" style={{ width: '48%' }} />
            </div>

            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400 font-mono">p95:</span>
              <span className="text-amber-400 font-bold font-mono">${costQuantiles.p95.toFixed(3)}</span>
            </div>
            <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
              <div className="bg-amber-500 h-full rounded-full" style={{ width: '63%' }} />
            </div>

            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400 font-mono">p99 (Tail):</span>
              <span className="text-rose-400 font-bold font-mono">${costQuantiles.p99.toFixed(3)}</span>
            </div>
            <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden">
              <div className="bg-rose-500 h-full rounded-full" style={{ width: '100%' }} />
            </div>
          </div>
        </Card>
      </div>

      {/* Model Stack Empirical Performance Profiles */}
      <Card className="p-5 bg-slate-900 border-slate-800">
        <h3 className="text-sm font-semibold text-slate-200 mb-4 flex items-center gap-2">
          <BrainCircuit className="w-4 h-4 text-purple-400" />
          Predictive Pipeline Engine Benchmark Profiles
        </h3>

        <div className="space-y-3">
          {taskHistograms.map((th, idx) => (
            <div key={idx} className="p-3.5 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-indigo-400">
                  <Zap className="w-4 h-4" />
                </div>
                <div>
                  <span className="text-xs font-bold text-slate-200 block">{th.name}</span>
                  <div className="flex items-center gap-3 text-[11px] text-slate-400 font-mono mt-0.5">
                    <span>Avg Latency: <strong className="text-amber-400">{th.avgLatency}ms</strong></span>
                    <span>Tokens: <strong className="text-indigo-300">{th.avgTokens}</strong></span>
                    <span>Confidence: <strong className="text-emerald-400">{(th.confidenceMean * 100).toFixed(1)}%</strong></span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <Badge variant={th.p99Risk === 'LOW' ? 'success' : th.p99Risk === 'MEDIUM' ? 'warning' : 'error'} size="sm">
                  {th.p99Risk} P99 Risk
                </Badge>
                <button className="px-2.5 py-1 text-[11px] font-medium bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 flex items-center gap-1">
                  <Layers className="w-3 h-3" />
                  Details
                </button>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
