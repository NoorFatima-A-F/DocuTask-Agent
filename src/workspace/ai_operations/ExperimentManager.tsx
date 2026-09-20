import React, { useState, useEffect } from 'react';
import {
  TestTube2,
  Play,
  Clock,
  TrendingUp,
  RefreshCw,
  Award,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';
import { ExperimentRecord } from '../../types/aiOperations';

export const ExperimentManager: React.FC = () => {
  const [experiments, setExperiments] = useState<ExperimentRecord[]>([]);
  const [selectedExp, setSelectedExp] = useState<ExperimentRecord | null>(null);
  const [loading, setLoading] = useState(true);
  const [runningNew, setRunningNew] = useState(false);

  const loadExperiments = async () => {
    try {
      setLoading(true);
      const data = await AIOperationsApiClient.getExperiments();
      setExperiments(data);
      if (data.length > 0 && !selectedExp) {
        setSelectedExp(data[0] || null);
      }
    } catch (err) {
      console.error('Failed to load experiments:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadExperiments();
  }, []);

  const handleLaunchExperiment = async () => {
    try {
      setRunningNew(true);
      const res = await AIOperationsApiClient.runExperiment({
        name: 'Manual Canary Test Run',
        agent_id: 'agent_chief_architect',
        control_version: 'v1.0.0',
        candidate_version: 'v1.1.0',
        sample_size: 100,
      });
      setSelectedExp(res);
      await loadExperiments();
    } catch (err) {
      console.error('Failed to run experiment:', err);
    } finally {
      setRunningNew(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-cyan-500/10 rounded-xl border border-cyan-500/20">
            <TestTube2 className="w-6 h-6 text-cyan-400" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">A/B Canary Experiment Manager</h1>
            <p className="text-xs text-slate-400">Statistical hypothesis testing (Welch's t-test, Cohen's d) for prompt & model deployments</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={loadExperiments} disabled={loading}>
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button variant="intelligence" onClick={handleLaunchExperiment} disabled={runningNew}>
            <span className="flex items-center gap-2">
              <Play className={`w-4 h-4 ${runningNew ? 'animate-spin' : ''}`} />
              {runningNew ? 'Running Canary...' : 'Launch Canary A/B Run'}
            </span>
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Experiment List (4 cols) */}
        <div className="lg:col-span-4 space-y-3">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-1">Canary Experiment Runs</h2>
          <div className="space-y-2 max-h-[600px] overflow-y-auto pr-1">
            {experiments.map((exp) => (
              <Card
                key={exp.experiment_id}
                className={`p-3.5 cursor-pointer transition-all border ${
                  selectedExp?.experiment_id === exp.experiment_id
                    ? 'bg-cyan-950/30 border-cyan-500/50 shadow-md shadow-cyan-950/20'
                    : 'bg-slate-900/40 border-slate-800/80 hover:bg-slate-800/40'
                }`}
                onClick={() => setSelectedExp(exp)}
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-white text-xs">{exp.agent_id}</span>
                  <Badge variant={exp.statistically_significant ? 'success' : 'outline'}>
                    {exp.statistically_significant ? 'Stat Sig (p<0.05)' : 'Inconclusive'}
                  </Badge>
                </div>
                <h3 className="font-medium text-slate-200 text-xs mt-1 line-clamp-1">{exp.name}</h3>
                <div className="flex items-center justify-between mt-2.5 text-[11px] text-slate-400 border-t border-slate-800/60 pt-2">
                  <span>{(exp.control_success_rate * 100).toFixed(0)}% → {(exp.candidate_success_rate * 100).toFixed(0)}%</span>
                  <span>n={exp.sample_size}</span>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Selected Experiment Details (8 cols) */}
        <div className="lg:col-span-8 space-y-4">
          {selectedExp ? (
            <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-5">
              <div className="flex items-start justify-between border-b border-slate-800 pb-4">
                <div>
                  <div className="flex items-center gap-2">
                    <Badge variant="intelligence">{selectedExp.agent_id}</Badge>
                    <h2 className="text-lg font-bold text-white">{selectedExp.name}</h2>
                  </div>
                  <p className="text-xs text-slate-400 font-mono mt-0.5">
                    Experiment ID: {selectedExp.experiment_id} • Status: {selectedExp.status}
                  </p>
                </div>
                <Badge variant={selectedExp.statistically_significant ? 'success' : 'warning'}>
                  {selectedExp.statistically_significant ? 'Statistically Validated' : 'Not Significant'}
                </Badge>
              </div>

              {/* Statistical Rigor Indicators */}
              <div className="grid grid-cols-3 gap-3">
                <div className="p-3 bg-slate-950/60 rounded-xl border border-slate-800/60">
                  <span className="text-xs text-slate-400 flex items-center gap-1"><Award className="w-3.5 h-3.5 text-cyan-400" /> p-Value (Welch's t)</span>
                  <p className="text-lg font-bold text-cyan-300 mt-1">{selectedExp.p_value}</p>
                </div>
                <div className="p-3 bg-slate-950/60 rounded-xl border border-slate-800/60">
                  <span className="text-xs text-slate-400 flex items-center gap-1"><TrendingUp className="w-3.5 h-3.5 text-indigo-400" /> Cohen's d Effect Size</span>
                  <p className="text-lg font-bold text-indigo-300 mt-1">{selectedExp.effect_size_cohen_d}</p>
                </div>
                <div className="p-3 bg-slate-950/60 rounded-xl border border-slate-800/60">
                  <span className="text-xs text-slate-400 flex items-center gap-1"><Clock className="w-3.5 h-3.5 text-amber-400" /> Sample Trials</span>
                  <p className="text-lg font-bold text-white mt-1">{selectedExp.sample_size}</p>
                </div>
              </div>

              {/* Control vs Candidate Comparison */}
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800/80">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-semibold text-slate-400">Control ({selectedExp.control_version})</span>
                    <Badge variant="outline">Baseline</Badge>
                  </div>
                  <div className="text-2xl font-bold text-white">{(selectedExp.control_success_rate * 100).toFixed(1)}%</div>
                  <p className="text-xs text-slate-400 mt-1">Avg Latency: {selectedExp.control_avg_latency_ms} ms</p>
                  <p className="text-xs text-slate-500">Avg Cost: ${selectedExp.control_avg_cost_usd}</p>
                </div>

                <div className="p-4 bg-slate-950/60 rounded-xl border border-cyan-500/40">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-semibold text-cyan-300">Candidate ({selectedExp.candidate_version})</span>
                    <Badge variant="success">Candidate</Badge>
                  </div>
                  <div className="text-2xl font-bold text-cyan-400">{(selectedExp.candidate_success_rate * 100).toFixed(1)}%</div>
                  <p className="text-xs text-slate-300 mt-1">Avg Latency: {selectedExp.candidate_avg_latency_ms} ms</p>
                  <p className="text-xs text-slate-400">Avg Cost: ${selectedExp.candidate_avg_cost_usd}</p>
                </div>
              </div>
            </Card>
          ) : (
            <Card className="p-8 text-center text-slate-400 bg-slate-900/40 border-slate-800">
              <TestTube2 className="w-8 h-8 text-slate-600 mx-auto mb-2" />
              <p>Select a canary experiment run to inspect statistical significance metrics.</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
