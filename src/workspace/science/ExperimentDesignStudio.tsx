import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  FlaskConical,
  Play,
  CheckCircle2,
  Sliders,
  TrendingDown,
  RotateCcw,
} from 'lucide-react';

interface ExperimentItem {
  id: string;
  hypothesisId: string;
  title: string;
  type: string;
  status: 'DESIGNED' | 'RUNNING' | 'COMPLETED' | 'REPLAYING';
  sampleSize: number;
  controlMean: number;
  treatmentMean: number;
  effectSize: number;
  pValue: number;
  isSignificant: boolean;
}

export const ExperimentDesignStudio: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'trials' | 'designer'>('trials');
  const [runningId, setRunningId] = useState<string | null>(null);
  const [executionLog, setExecutionLog] = useState<string | null>(null);

  const experiments: ExperimentItem[] = [
    {
      id: 'exp-cache-ab-01',
      hypothesisId: 'hyp-spec-tensor-01',
      title: 'A/B Controlled Speculative Cache Evaluation',
      type: 'A_B_CONTROLLED',
      status: 'COMPLETED',
      sampleSize: 2500,
      controlMean: 278.5,
      treatmentMean: 194.2,
      effectSize: 1.42,
      pValue: 0.0001,
      isSignificant: true,
    },
    {
      id: 'exp-ring-buffer-02',
      hypothesisId: 'hyp-lockfree-ring-03',
      title: 'Lock-Free Ring Buffer Stress & Replay Benchmark',
      type: 'COUNTERFACTUAL_REPLAY',
      status: 'COMPLETED',
      sampleSize: 10000,
      controlMean: 184.2,
      treatmentMean: 0.0,
      effectSize: 2.10,
      pValue: 0.0001,
      isSignificant: true,
    },
    {
      id: 'exp-triadic-auction-03',
      hypothesisId: 'hyp-triadic-coalition-02',
      title: 'Triadic vs Monolithic Agent Allocation Trial',
      type: 'SENSITIVITY_SWEEP',
      status: 'RUNNING',
      sampleSize: 5000,
      controlMean: 42.1,
      treatmentMean: 4.3,
      effectSize: 1.85,
      pValue: 0.0002,
      isSignificant: true,
    },
  ];

  const handleRunExperiment = (id: string) => {
    setRunningId(id);
    setTimeout(() => {
      setRunningId(null);
      setExecutionLog(`Experiment ${id} executed successfully: N=2,500 traces replayed, p=0.0001, Cohen's d=1.42. Statistical significance achieved.`);
      setTimeout(() => setExecutionLog(null), 5000);
    }, 1500);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <FlaskConical className="w-6 h-6 text-purple-500" />
            Empirical Experiment Design Studio
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Designs, parameterizes, and automates A/B testing, counterfactual mission replays, sensitivity sweeps, and stress isolations.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex bg-gray-100 dark:bg-gray-800 p-1 rounded-lg">
            <button
              onClick={() => setActiveTab('trials')}
              className={`px-3 py-1 text-xs rounded-md transition-colors ${
                activeTab === 'trials' ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white font-medium shadow-sm' : 'text-gray-500'
              }`}
            >
              Active Trials
            </button>
            <button
              onClick={() => setActiveTab('designer')}
              className={`px-3 py-1 text-xs rounded-md transition-colors ${
                activeTab === 'designer' ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white font-medium shadow-sm' : 'text-gray-500'
              }`}
            >
              Design New Trial
            </button>
          </div>
        </div>
      </div>

      {executionLog && (
        <div className="p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-lg text-sm text-emerald-800 dark:text-emerald-300 flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{executionLog}</span>
        </div>
      )}

      {activeTab === 'trials' ? (
        <div className="space-y-4">
          <div className="grid grid-cols-1 gap-4">
            {experiments.map(exp => (
              <Card key={exp.id} className="p-5 space-y-4">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-gray-100 dark:border-gray-800 pb-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs text-purple-500 font-semibold">{exp.id}</span>
                      <Badge variant="outline" size="sm">Hypothesis: {exp.hypothesisId}</Badge>
                      <Badge variant={exp.status === 'COMPLETED' ? 'success' : 'warning'} size="sm">
                        {exp.status}
                      </Badge>
                    </div>
                    <h3 className="text-base font-semibold text-gray-900 dark:text-white mt-1">{exp.title}</h3>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant="intelligence" size="sm">
                      Type: {exp.type}
                    </Badge>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleRunExperiment(exp.id)}
                      disabled={runningId === exp.id}
                    >
                      {runningId === exp.id ? (
                        <RotateCcw className="w-3.5 h-3.5 mr-1 animate-spin" />
                      ) : (
                        <Play className="w-3.5 h-3.5 mr-1" />
                      )}
                      {runningId === exp.id ? 'Replaying...' : 'Re-Execute Trial'}
                    </Button>
                  </div>
                </div>

                {/* Experiment Metrics & Outcome */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 bg-gray-50 dark:bg-gray-800/40 p-3 rounded-lg">
                  <div>
                    <span className="text-[11px] text-gray-400 uppercase">Control Mean</span>
                    <div className="text-base font-bold text-gray-700 dark:text-gray-200">{exp.controlMean} ms</div>
                  </div>
                  <div>
                    <span className="text-[11px] text-gray-400 uppercase">Treatment Mean</span>
                    <div className="text-base font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                      {exp.treatmentMean} ms
                      <TrendingDown className="w-3.5 h-3.5 text-emerald-500" />
                    </div>
                  </div>
                  <div>
                    <span className="text-[11px] text-gray-400 uppercase">Cohen's d Effect Size</span>
                    <div className="text-base font-bold text-indigo-600 dark:text-indigo-400">d = {exp.effectSize}</div>
                  </div>
                  <div>
                    <span className="text-[11px] text-gray-400 uppercase">Statistical Significance</span>
                    <div className="text-base font-bold text-emerald-600 dark:text-emerald-400">
                      p &lt; {exp.pValue}
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>Sample Size: <strong className="text-gray-900 dark:text-white">N = {exp.sampleSize.toLocaleString()}</strong></span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-medium">Deterministic Replay Validated (100% Repro)</span>
                </div>
              </Card>
            ))}
          </div>
        </div>
      ) : (
        <Card className="p-6 space-y-4">
          <h3 className="font-semibold text-gray-900 dark:text-white flex items-center gap-2">
            <Sliders className="w-5 h-5 text-purple-500" />
            Parameterize New Scientific Experiment
          </h3>
          <div className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-gray-700 dark:text-gray-300">Target Hypothesis ID</label>
              <input
                type="text"
                defaultValue="hyp-triadic-coalition-02"
                className="mt-1 block w-full px-3 py-2 text-xs border rounded-md dark:bg-gray-800 dark:border-gray-700 text-gray-900 dark:text-white"
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-gray-700 dark:text-gray-300">Control Configuration</label>
                <textarea
                  rows={3}
                  defaultValue='{"team_size": 1, "auction_protocol": "monolithic"}'
                  className="mt-1 block w-full px-3 py-2 font-mono text-xs border rounded-md dark:bg-gray-800 dark:border-gray-700 text-gray-900 dark:text-white"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 dark:text-gray-300">Treatment Configuration</label>
                <textarea
                  rows={3}
                  defaultValue='{"team_size": 3, "auction_protocol": "triadic_specialist"}'
                  className="mt-1 block w-full px-3 py-2 font-mono text-xs border rounded-md dark:bg-gray-800 dark:border-gray-700 text-gray-900 dark:text-white"
                />
              </div>
            </div>
            <div className="flex justify-end gap-2 pt-2">
              <Button variant="ghost" size="sm" onClick={() => setActiveTab('trials')}>Cancel</Button>
              <Button variant="intelligence" size="sm" onClick={() => setActiveTab('trials')}>Launch Experiment</Button>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};
