import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Grid } from 'lucide-react';

export const ConfidenceDimensionMatrix: React.FC = () => {
  const dimensions = [
    { name: 'OCR Confidence', score: '99.2%', uncertainty: '±0.8%', formula: 'WeightedEnsemble v1.3', weight: '20%', signals: 4520, status: 'VERIFIED' },
    { name: 'Schema Extraction', score: '98.0%', uncertainty: '±1.2%', formula: 'WeightedEnsemble v1.3', weight: '20%', signals: 24, status: 'VERIFIED' },
    { name: 'Invariant Validation', score: '99.9%', uncertainty: '±0.1%', formula: 'Deterministic Invariant', weight: '35%', signals: 12, status: 'VERIFIED' },
    { name: 'Planner Efficiency', score: '95.0%', uncertainty: '±2.1%', formula: 'CPM Ratio Metric', weight: '10%', signals: 9, status: 'VERIFIED' },
    { name: 'Execution DAG', score: '98.5%', uncertainty: '±1.0%', formula: 'Wavefront Latency Bound', weight: '5%', signals: 9, status: 'VERIFIED' },
    { name: 'Worker Reliability', score: '98.8%', uncertainty: '±0.9%', formula: 'Historical Beta Fit', weight: '5%', signals: 6, status: 'VERIFIED' },
    { name: 'Memory Graph', score: '97.5%', uncertainty: '±1.5%', formula: 'Cosine Similarity Decay', weight: '2%', signals: 3, status: 'VERIFIED' },
    { name: 'Evidence Integrity', score: '100.0%', uncertainty: '±0.0%', formula: 'Merkle Hash Verification', weight: '15%', signals: 12, status: 'VERIFIED' },
    { name: 'Recovery Readiness', score: '99.0%', uncertainty: '±0.5%', formula: 'Fallback Route Availability', weight: '3%', signals: 2, status: 'VERIFIED' },
    { name: 'Reflection Feedback', score: '96.2%', uncertainty: '±1.8%', formula: 'Rule Acceptance Rate', weight: '2%', signals: 4, status: 'VERIFIED' },
    { name: 'Governance SLA', score: '100.0%', uncertainty: '±0.0%', formula: 'SLA Boundary Check', weight: '5%', signals: 1, status: 'VERIFIED' },
    { name: 'Mission Synthesis', score: '98.4%', uncertainty: '±1.4%', formula: 'Bayesian Joint Posterior', weight: '100%', signals: 50, status: 'VERIFIED' },
    { name: 'Platform Aggregate', score: '98.42%', uncertainty: '±1.45%', formula: 'Ensemble Meta-Model', weight: 'GLOBAL', signals: 1420, status: 'VERIFIED' },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 rounded-xl text-indigo-400">
              <Grid className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                13-Dimension Confidence Matrix
                <Badge variant="success" size="sm">Independent Dimensions</Badge>
              </h1>
              <p className="text-xs text-[#94A3B8] font-mono">
                Independent formulas, version controls, weights, and evidence backings per dimension
              </p>
            </div>
          </div>
        </div>

        <Badge variant="intelligence" size="md">Multi-Dimensional Certainty</Badge>
      </div>

      {/* Table */}
      <Card className="rounded-2xl border border-[#1E293B] bg-[#0F172A] overflow-hidden font-mono text-xs">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-[#1E293B] bg-[#131D35]/50 text-[#64748B] text-[10px] uppercase tracking-wider">
                <th className="p-3.5">Dimension</th>
                <th className="p-3.5">Score</th>
                <th className="p-3.5">Uncertainty</th>
                <th className="p-3.5">Formula Model</th>
                <th className="p-3.5">Policy Weight</th>
                <th className="p-3.5">Evidence Count</th>
                <th className="p-3.5">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E293B]">
              {dimensions.map(d => (
                <tr key={d.name} className="hover:bg-[#131D35]/40 transition-colors">
                  <td className="p-3.5 font-bold text-white">{d.name}</td>
                  <td className="p-3.5 font-bold text-cyan-400">{d.score}</td>
                  <td className="p-3.5 text-[#94A3B8]">{d.uncertainty}</td>
                  <td className="p-3.5 text-indigo-300">{d.formula}</td>
                  <td className="p-3.5 text-purple-400 font-semibold">{d.weight}</td>
                  <td className="p-3.5 text-white">{d.signals} signals</td>
                  <td className="p-3.5">
                    <Badge variant="success" size="sm">{d.status}</Badge>
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
