import React, { useState } from 'react';
import {
  GitFork,
  Sliders,
  Clock,
  DollarSign,
  Award,
  Play,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';
import { ModelRouteDecision } from '../../types/aiOperations';

export const ModelRoutingCenter: React.FC = () => {
  const [weightQuality, setWeightQuality] = useState(0.5);
  const [weightLatency, setWeightLatency] = useState(0.3);
  const [weightCost, setWeightCost] = useState(0.2);
  const [promptTokens, setPromptTokens] = useState(1500);
  const [completionTokens, setCompletionTokens] = useState(500);
  const [decision, setDecision] = useState<ModelRouteDecision | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSimulateRoute = async () => {
    try {
      setLoading(true);
      const res = await AIOperationsApiClient.routeModel({
        task_id: 'task_sim_01',
        estimated_prompt_tokens: promptTokens,
        estimated_completion_tokens: completionTokens,
        weight_quality: weightQuality,
        weight_latency: weightLatency,
        weight_cost: weightCost,
      });
      setDecision(res);
    } catch (err) {
      console.error('Failed to simulate model routing:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-blue-500/10 rounded-xl border border-blue-500/20">
            <GitFork className="w-6 h-6 text-blue-400" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Multi-Objective Pareto Model Routing</h1>
            <p className="text-xs text-slate-400">Dynamically routes tasks across model tiers balancing Quality, Latency, and Cost</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Controls & Sliders (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <Card className="p-5 bg-slate-900/50 border-slate-800 space-y-4">
            <h2 className="text-sm font-semibold text-white flex items-center gap-2">
              <Sliders className="w-4 h-4 text-blue-400" /> Multi-Objective Weights
            </h2>

            {/* Quality Slider */}
            <div className="space-y-1.5">
              <div className="flex justify-between text-xs">
                <span className="text-slate-300">Quality Weight</span>
                <span className="font-semibold text-indigo-400">{(weightQuality * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={weightQuality}
                onChange={(e) => setWeightQuality(parseFloat(e.target.value))}
                className="w-full accent-indigo-500"
              />
            </div>

            {/* Latency Slider */}
            <div className="space-y-1.5">
              <div className="flex justify-between text-xs">
                <span className="text-slate-300">Latency Weight</span>
                <span className="font-semibold text-cyan-400">{(weightLatency * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={weightLatency}
                onChange={(e) => setWeightLatency(parseFloat(e.target.value))}
                className="w-full accent-cyan-500"
              />
            </div>

            {/* Cost Slider */}
            <div className="space-y-1.5">
              <div className="flex justify-between text-xs">
                <span className="text-slate-300">Cost Savings Weight</span>
                <span className="font-semibold text-emerald-400">{(weightCost * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={weightCost}
                onChange={(e) => setWeightCost(parseFloat(e.target.value))}
                className="w-full accent-emerald-500"
              />
            </div>

            {/* Token Inputs */}
            <div className="grid grid-cols-2 gap-3 pt-2 border-t border-slate-800">
              <div>
                <label className="text-xs text-slate-400 block mb-1">Prompt Tokens</label>
                <input
                  type="number"
                  value={promptTokens}
                  onChange={(e) => setPromptTokens(parseInt(e.target.value) || 0)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white"
                />
              </div>
              <div>
                <label className="text-xs text-slate-400 block mb-1">Completion Tokens</label>
                <input
                  type="number"
                  value={completionTokens}
                  onChange={(e) => setCompletionTokens(parseInt(e.target.value) || 0)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white"
                />
              </div>
            </div>

            <Button variant="intelligence" className="w-full" onClick={handleSimulateRoute} disabled={loading}>
              <span className="flex items-center justify-center gap-2">
                <Play className="w-4 h-4" />
                {loading ? 'Evaluating Pareto Frontier...' : 'Evaluate Optimal Route'}
              </span>
            </Button>
          </Card>
        </div>

        {/* Route Decision & Frontier Result (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          {decision ? (
            <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-5">
              <div className="flex items-start justify-between border-b border-slate-800 pb-4">
                <div>
                  <Badge variant="intelligence" className="mb-1">Optimal Pareto Match</Badge>
                  <h2 className="text-2xl font-bold text-white tracking-tight">{decision.selected_model}</h2>
                  <p className="text-xs text-slate-400 mt-0.5">Tier: {decision.selected_tier}</p>
                </div>
                <div className="text-right">
                  <span className="text-2xl font-bold text-indigo-400">{decision.pareto_score}</span>
                  <p className="text-[11px] text-slate-400">Pareto Utility Score</p>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div className="p-3 bg-slate-950/60 rounded-xl border border-slate-800/60">
                  <span className="text-xs text-slate-400 flex items-center gap-1"><Award className="w-3.5 h-3.5 text-indigo-400" /> Est. Quality</span>
                  <p className="text-lg font-bold text-white mt-1">{(decision.estimated_quality_score * 100).toFixed(0)}%</p>
                </div>
                <div className="p-3 bg-slate-950/60 rounded-xl border border-slate-800/60">
                  <span className="text-xs text-slate-400 flex items-center gap-1"><Clock className="w-3.5 h-3.5 text-cyan-400" /> Est. Latency</span>
                  <p className="text-lg font-bold text-white mt-1">{decision.estimated_latency_ms} ms</p>
                </div>
                <div className="p-3 bg-slate-950/60 rounded-xl border border-slate-800/60">
                  <span className="text-xs text-slate-400 flex items-center gap-1"><DollarSign className="w-3.5 h-3.5 text-emerald-400" /> Est. Cost</span>
                  <p className="text-lg font-bold text-white mt-1">${decision.estimated_cost_usd}</p>
                </div>
              </div>

              {/* Fallback Chain */}
              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800/80">
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Automated Fallback Chain</h4>
                <div className="flex flex-wrap items-center gap-2">
                  <Badge variant="success">Primary: {decision.selected_model}</Badge>
                  {decision.fallback_models.map((fb, idx) => (
                    <Badge key={fb} variant="outline">Fallback {idx + 1}: {fb}</Badge>
                  ))}
                </div>
              </div>
            </Card>
          ) : (
            <Card className="p-8 text-center text-slate-400 bg-slate-900/40 border-slate-800">
              <GitFork className="w-8 h-8 text-slate-600 mx-auto mb-2" />
              <p>Configure task weights and click 'Evaluate Optimal Route' to simulate model selection.</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
