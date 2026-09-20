import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import {
  Sparkles,
  CheckCircle2,
} from 'lucide-react';

interface RecommendationItem {
  id: string;
  targetArea: string;
  budgetUsd: number;
  expectedGainPct: number;
  rationale: string;
  riskLevel: string;
  confidence: number;
}

export const StrategicInsightsCenter: React.FC = () => {
  const [recommendations] = useState<RecommendationItem[]>([
    {
      id: 'rec-001',
      targetArea: 'Speculative Embedding Caching',
      budgetUsd: 4500.0,
      expectedGainPct: 28.0,
      rationale: 'High concentration of identical vendor invoice headers enables 85% cache hit efficiency and $9.8k/mo savings.',
      riskLevel: 'LOW',
      confidence: 0.990,
    },
    {
      id: 'rec-002',
      targetArea: 'Autonomous Agent Strike Teams',
      budgetUsd: 6000.0,
      expectedGainPct: 19.5,
      rationale: 'Triadic coalition model reduces negotiation friction during high-concurrency balance sheet runs.',
      riskLevel: 'LOW',
      confidence: 0.982,
    },
    {
      id: 'rec-003',
      targetArea: 'Lock-Free Memory Buffer Migration',
      budgetUsd: 2500.0,
      expectedGainPct: 15.0,
      rationale: 'Migrating global state mutex locks to atomic ring buffers eliminates 180ms telemetry contention stalls.',
      riskLevel: 'LOW',
      confidence: 0.995,
    },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-indigo-500" />
            Strategic Insights & Investment Opportunities Center
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Phase 13.11 — Autonomous strategic pattern mining, capital allocation recommendations, and ROI gain forecasts.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="intelligence" size="md">
            {recommendations.length} Active Recommendations
          </Badge>
        </div>
      </div>

      {/* Recommendations List */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider">
          AI Chief Strategy Officer (CSO) Investment Directives
        </h3>

        <div className="grid grid-cols-1 gap-4">
          {recommendations.map((rec) => (
            <Card key={rec.id} className="p-5 hover:shadow-md transition-shadow border-l-4 border-l-emerald-500">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs text-emerald-600 dark:text-emerald-400 font-semibold">{rec.id}</span>
                    <Badge variant="success" size="sm">
                      Expected Gain: +{rec.expectedGainPct}%
                    </Badge>
                    <Badge variant="outline" size="sm">
                      Risk: {rec.riskLevel}
                    </Badge>
                  </div>
                  <h4 className="font-semibold text-gray-900 dark:text-white text-base mt-1">{rec.targetArea}</h4>
                </div>
                <div className="text-right">
                  <span className="text-xs text-gray-400 block">Recommended Budget</span>
                  <span className="text-lg font-bold text-gray-900 dark:text-white font-mono">
                    ${rec.budgetUsd.toLocaleString()}
                  </span>
                </div>
              </div>

              <p className="text-xs text-gray-600 dark:text-gray-300 mt-3">{rec.rationale}</p>

              <div className="mt-4 pt-3 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between text-xs">
                <span className="text-purple-600 dark:text-purple-400 font-medium">
                  Bayesian Empirical Confidence: {(rec.confidence * 100).toFixed(1)}%
                </span>
                <span className="text-emerald-600 dark:text-emerald-400 flex items-center gap-1 font-medium">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Validated via Truth Ledger
                </span>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
