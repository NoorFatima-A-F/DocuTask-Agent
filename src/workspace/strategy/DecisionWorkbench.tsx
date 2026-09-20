import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import {
  Sliders,
} from 'lucide-react';

interface CandidateItem {
  id: string;
  name: string;
  description: string;
  roi: number;
  latencyGain: number;
  govCompliance: number;
  costEfficiency: number;
  riskSafety: number;
}

export const DecisionWorkbench: React.FC = () => {
  const [weights, setWeights] = useState({
    roi: 0.30,
    latency: 0.25,
    governance: 0.20,
    cost: 0.15,
    safety: 0.10,
  });

  const candidates: CandidateItem[] = [
    {
      id: 'cand-opt-caching-triad',
      name: 'Plan Alpha: Speculative Caching + Triadic Strike Teams',
      description: 'Pre-warm tensor cache and cluster workers into specialist triadic teams.',
      roi: 3.8,
      latencyGain: 28.0,
      govCompliance: 0.99,
      costEfficiency: 0.94,
      riskSafety: 0.95,
    },
    {
      id: 'cand-brute-scale',
      name: 'Plan Beta: Brute-Force Worker Over-Provisioning',
      description: 'Spin up 24 additional worker containers without caching.',
      roi: 1.8,
      latencyGain: 24.0,
      govCompliance: 0.95,
      costEfficiency: 0.45,
      riskSafety: 0.88,
    },
    {
      id: 'cand-minimal-tuning',
      name: 'Plan Gamma: Baseline Continuity + Minor Indexing',
      description: 'Maintain current cluster topology with minor SQL index adjustments.',
      roi: 1.2,
      latencyGain: 5.0,
      govCompliance: 0.90,
      costEfficiency: 0.98,
      riskSafety: 0.80,
    },
  ];

  // Calculate dynamic utility score based on tuned weights
  const calculateUtility = (cand: CandidateItem) => {
    const roiNorm = Math.min(cand.roi / 5.0, 1.0);
    const latNorm = Math.min(cand.latencyGain / 35.0, 1.0);
    const govNorm = Math.min(cand.govCompliance, 1.0);
    const costNorm = Math.min(cand.costEfficiency, 1.0);
    const safeNorm = Math.min(cand.riskSafety, 1.0);

    return (
      weights.roi * roiNorm +
      weights.latency * latNorm +
      weights.governance * govNorm +
      weights.cost * costNorm +
      weights.safety * safeNorm
    );
  };

  const rankedCandidates = [...candidates]
    .map((c) => ({ ...c, utility: calculateUtility(c) }))
    .sort((a, b) => b.utility - a.utility);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Sliders className="w-6 h-6 text-indigo-500" />
            Multi-Criteria Decision Analysis (MCDA) Workbench
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Phase 13.11 — Interactive Analytic Hierarchy Process (AHP) weight tuning and multi-objective Pareto candidate ranking.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="intelligence" size="md">
            MCDA Weighted Sum Engine
          </Badge>
        </div>
      </div>

      {/* Criteria Weight Tuners */}
      <Card className="p-5">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider mb-4 flex items-center gap-2">
          <Sliders className="w-4 h-4 text-indigo-500" />
          AHP Criteria Importance Weighting
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 text-xs">
          <div>
            <div className="flex justify-between text-gray-500 mb-1">
              <span>Expected ROI</span>
              <span className="font-mono font-semibold text-indigo-600">{(weights.roi * 100).toFixed(0)}%</span>
            </div>
            <input
              type="range"
              min="0.05"
              max="0.60"
              step="0.05"
              value={weights.roi}
              onChange={(e) => setWeights({ ...weights, roi: parseFloat(e.target.value) })}
              className="w-full accent-indigo-600 cursor-pointer"
            />
          </div>

          <div>
            <div className="flex justify-between text-gray-500 mb-1">
              <span>Latency Gain</span>
              <span className="font-mono font-semibold text-emerald-600">{(weights.latency * 100).toFixed(0)}%</span>
            </div>
            <input
              type="range"
              min="0.05"
              max="0.60"
              step="0.05"
              value={weights.latency}
              onChange={(e) => setWeights({ ...weights, latency: parseFloat(e.target.value) })}
              className="w-full accent-emerald-600 cursor-pointer"
            />
          </div>

          <div>
            <div className="flex justify-between text-gray-500 mb-1">
              <span>Governance</span>
              <span className="font-mono font-semibold text-purple-600">{(weights.governance * 100).toFixed(0)}%</span>
            </div>
            <input
              type="range"
              min="0.05"
              max="0.60"
              step="0.05"
              value={weights.governance}
              onChange={(e) => setWeights({ ...weights, governance: parseFloat(e.target.value) })}
              className="w-full accent-purple-600 cursor-pointer"
            />
          </div>

          <div>
            <div className="flex justify-between text-gray-500 mb-1">
              <span>Cost Efficiency</span>
              <span className="font-mono font-semibold text-amber-600">{(weights.cost * 100).toFixed(0)}%</span>
            </div>
            <input
              type="range"
              min="0.05"
              max="0.60"
              step="0.05"
              value={weights.cost}
              onChange={(e) => setWeights({ ...weights, cost: parseFloat(e.target.value) })}
              className="w-full accent-amber-600 cursor-pointer"
            />
          </div>

          <div>
            <div className="flex justify-between text-gray-500 mb-1">
              <span>Risk & Safety</span>
              <span className="font-mono font-semibold text-sky-600">{(weights.safety * 100).toFixed(0)}%</span>
            </div>
            <input
              type="range"
              min="0.05"
              max="0.60"
              step="0.05"
              value={weights.safety}
              onChange={(e) => setWeights({ ...weights, safety: parseFloat(e.target.value) })}
              className="w-full accent-sky-600 cursor-pointer"
            />
          </div>
        </div>
      </Card>

      {/* Ranked Candidates */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider">
          MCDA Evaluated Strategic Options
        </h3>

        <div className="grid grid-cols-1 gap-4">
          {rankedCandidates.map((cand, idx) => (
            <Card
              key={cand.id}
              className={`p-5 hover:shadow-md transition-shadow ${
                idx === 0
                  ? 'border-l-4 border-l-emerald-500 bg-emerald-50/10 dark:bg-emerald-950/10'
                  : 'border-l-4 border-l-gray-300 dark:border-l-gray-700'
              }`}
            >
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800">
                <div>
                  <div className="flex items-center gap-2">
                    <Badge variant={idx === 0 ? 'success' : 'default'} size="sm">
                      Rank #{idx + 1} {idx === 0 ? '• Dominant' : ''}
                    </Badge>
                    <span className="font-mono text-xs text-gray-400">{cand.id}</span>
                  </div>
                  <h4 className="font-semibold text-gray-900 dark:text-white text-base mt-1">{cand.name}</h4>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{cand.description}</p>
                </div>
                <div className="text-right">
                  <span className="text-xs text-gray-400 block">Computed Utility</span>
                  <span className="text-xl font-bold text-indigo-600 dark:text-indigo-400 font-mono">
                    {cand.utility.toFixed(4)}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mt-4 text-xs">
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">ROI Mult</span>
                  <span className="font-semibold text-gray-800 dark:text-gray-200 font-mono">{cand.roi}x</span>
                </div>
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Latency Reduction</span>
                  <span className="font-semibold text-emerald-600 dark:text-emerald-400 font-mono">+{cand.latencyGain}%</span>
                </div>
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Gov Compliance</span>
                  <span className="font-semibold text-purple-600 dark:text-purple-400 font-mono">{(cand.govCompliance * 100).toFixed(0)}%</span>
                </div>
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Cost Efficiency</span>
                  <span className="font-semibold text-amber-600 dark:text-amber-400 font-mono">{(cand.costEfficiency * 100).toFixed(0)}%</span>
                </div>
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Safety Index</span>
                  <span className="font-semibold text-sky-600 dark:text-sky-400 font-mono">{(cand.riskSafety * 100).toFixed(0)}%</span>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
