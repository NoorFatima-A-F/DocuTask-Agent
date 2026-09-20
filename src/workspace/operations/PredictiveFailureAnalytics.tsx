import React, { useState } from 'react';
import {
  TrendingUp,
  BrainCircuit,
  RefreshCw,
  Cpu,
  DollarSign,
  Layers,
  Sparkles
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

interface PredictiveFailureAnalyticsProps {
  missionId?: string;
}

export const PredictiveFailureAnalytics: React.FC<PredictiveFailureAnalyticsProps> = ({
  missionId = 'cluster-primary-master',
}) => {
  const [predictions] = useState([
    {
      id: 'pred-cap-01',
      type: 'CAPACITY_EXHAUSTION',
      subsystem: 'WORKERS',
      probability: 0.75,
      timeToFailureSec: 140.0,
      severity: 'HIGH',
      recommendation: 'AUTO_SCALE_WORKER_POOL_OR_BURST_LOCAL_OCR',
      icon: <Cpu className="w-4 h-4 text-cyan-400" />,
    },
    {
      id: 'pred-bdg-02',
      type: 'BUDGET_EXHAUSTION',
      subsystem: 'OPTIMIZATION',
      probability: 0.30,
      timeToFailureSec: 620.0,
      severity: 'MEDIUM',
      recommendation: 'SWITCH_TO_QUANTIZED_LOCAL_MODEL_TO_HALT_SPEND',
      icon: <DollarSign className="w-4 h-4 text-emerald-400" />,
    },
    {
      id: 'pred-ret-03',
      type: 'RETRY_STORM',
      subsystem: 'API',
      probability: 0.15,
      timeToFailureSec: 180.0,
      severity: 'LOW',
      recommendation: 'ENGAGE_ADAPTIVE_EXPONENTIAL_BACKOFF_AND_CIRCUIT_BREAKER',
      icon: <TrendingUp className="w-4 h-4 text-amber-400" />,
    },
    {
      id: 'pred-cnf-04',
      type: 'CONFIDENCE_COLLAPSE',
      subsystem: 'PLANNER',
      probability: 0.10,
      timeToFailureSec: 300.0,
      severity: 'LOW',
      recommendation: 'ESCALATE_TO_MULTI_AGENT_CONSENSUS_AND_SMT_SYMBOLIC_VERIFIER',
      icon: <BrainCircuit className="w-4 h-4 text-purple-400" />,
    },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <BrainCircuit className="w-5 h-5 text-indigo-400" />
            Predictive Failure Intelligence & Risk Analytics
          </h2>
          <p className="text-sm text-slate-400">
            Forecasting capacity exhaustion, budget overruns, retry storms, and confidence collapse prior to manifestation for: <code className="text-indigo-300 font-mono text-xs">{missionId}</code>
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="intelligence" size="md">
            Composite Risk: 0.18 (LOW)
          </Badge>
          <button className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700">
            <RefreshCw className="w-3.5 h-3.5" />
            Recalculate Priors
          </button>
        </div>
      </div>

      {/* Predictions Matrix */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono">
        {predictions.map((p) => (
          <Card key={p.id} className="p-5 bg-slate-900 border-slate-800 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                {p.icon}
                <span className="text-xs font-bold text-slate-200">{p.type}</span>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant={p.severity === 'HIGH' ? 'error' : p.severity === 'MEDIUM' ? 'warning' : 'default'} size="sm">
                  {p.severity}
                </Badge>
                <span className="text-xs font-bold text-indigo-400">{(p.probability * 100).toFixed(0)}% Prob</span>
              </div>
            </div>

            <div className="space-y-1">
              <div className="flex justify-between text-xs text-slate-400">
                <span>Estimated Time to Failure:</span>
                <span className="text-amber-400 font-bold">{p.timeToFailureSec} sec</span>
              </div>
              <div className="w-full bg-slate-950 h-1.5 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full ${p.probability > 0.6 ? 'bg-rose-500' : p.probability > 0.3 ? 'bg-amber-500' : 'bg-emerald-500'}`}
                  style={{ width: `${p.probability * 100}%` }}
                />
              </div>
            </div>

            <div className="pt-2 border-t border-slate-800 text-[11px] text-slate-400">
              <span className="text-slate-500 block text-[10px]">PREVENTATIVE ACTION:</span>
              <span className="text-emerald-400 font-bold flex items-center gap-1 mt-0.5">
                <Sparkles className="w-3 h-3" />
                {p.recommendation}
              </span>
            </div>
          </Card>
        ))}
      </div>

      {/* Financial Exposure Risk */}
      <Card className="p-5 bg-slate-900 border-slate-800 space-y-3 font-mono">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <Layers className="w-4 h-4 text-purple-400" />
          Aggregate Risk Exposure & SLA Breach Horizon
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
          <div className="p-3.5 bg-slate-950 rounded-lg border border-slate-800">
            <span className="text-slate-400 block mb-1">Financial Exposure (24h)</span>
            <span className="text-lg font-bold text-emerald-400">$0.00 USD</span>
          </div>
          <div className="p-3.5 bg-slate-950 rounded-lg border border-slate-800">
            <span className="text-slate-400 block mb-1">SLA Breach Probability</span>
            <span className="text-lg font-bold text-cyan-400">0.01%</span>
          </div>
          <div className="p-3.5 bg-slate-950 rounded-lg border border-slate-800">
            <span className="text-slate-400 block mb-1">Preemptive Actions Armed</span>
            <span className="text-lg font-bold text-indigo-400">4 Autonomic Handlers</span>
          </div>
        </div>
      </Card>
    </div>
  );
};
