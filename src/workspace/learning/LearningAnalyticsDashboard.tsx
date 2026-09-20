import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { BarChart3, TrendingUp } from 'lucide-react';

export const LearningAnalyticsDashboard: React.FC = () => {
  const metrics = {
    learningEfficiency: '+42.5%',
    reflectionsCount: 48,
    minedRulesCount: 112,
    governanceApprovalRate: '94.2%',
    averagePosteriorGain: '+8.4%',
    driftRate: '0.0%',
  };

  const learningCycles = [
    { cycle: 'Cycle 1 (Initial Baseline)', throughput: '10.2 tasks/s', latency: '3.8s', conf: '91.2%' },
    { cycle: 'Cycle 2 (Wavefront OCR)', throughput: '13.6 tasks/s', latency: '2.9s', conf: '94.8%' },
    { cycle: 'Cycle 3 (SMT Invariance)', throughput: '14.8 tasks/s', latency: '2.4s', conf: '98.5%' },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-indigo-500/20 to-cyan-500/20 border border-indigo-500/30 rounded-xl text-indigo-400">
            <BarChart3 className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
              Autonomous Learning & KPI Analytics
              <Badge variant="intelligence" size="sm">Phase 13.5</Badge>
            </h1>
            <p className="text-xs text-[#94A3B8] font-mono">
              Empirical velocity metrics, governance approval trends, and self-improving performance progression
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">Continuous Optimization Active</Badge>
        </div>
      </div>

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 font-mono">
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B] rounded-xl">
          <span className="text-[11px] text-[#64748B] block">Learning Speedup</span>
          <span className="text-2xl font-bold text-cyan-400 mt-1 block">{metrics.learningEfficiency}</span>
        </Card>
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B] rounded-xl">
          <span className="text-[11px] text-[#64748B] block">Total Reflections</span>
          <span className="text-2xl font-bold text-white mt-1 block">{metrics.reflectionsCount}</span>
        </Card>
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B] rounded-xl">
          <span className="text-[11px] text-[#64748B] block">Mined Rules</span>
          <span className="text-2xl font-bold text-indigo-400 mt-1 block">{metrics.minedRulesCount}</span>
        </Card>
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B] rounded-xl">
          <span className="text-[11px] text-[#64748B] block">Gov Approval Rate</span>
          <span className="text-2xl font-bold text-emerald-400 mt-1 block">{metrics.governanceApprovalRate}</span>
        </Card>
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B] rounded-xl">
          <span className="text-[11px] text-[#64748B] block">Posterior Gain</span>
          <span className="text-2xl font-bold text-purple-400 mt-1 block">{metrics.averagePosteriorGain}</span>
        </Card>
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B] rounded-xl">
          <span className="text-[11px] text-[#64748B] block">Uncalibrated Drift</span>
          <span className="text-2xl font-bold text-teal-400 mt-1 block">{metrics.driftRate}</span>
        </Card>
      </div>

      {/* Evolutionary Progression Table */}
      <Card className="p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] font-mono space-y-4">
        <div className="flex items-center justify-between border-b border-[#1E293B] pb-3">
          <span className="text-xs font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-emerald-400" />
            Empirical Self-Improvement Progression Across Cycles
          </span>
          <Badge variant="outline" size="sm">Monotonically Improving</Badge>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-[#1E293B] text-[#64748B]">
                <th className="pb-2">EVOLUTION CYCLE</th>
                <th className="pb-2">THROUGHPUT</th>
                <th className="pb-2">LATENCY</th>
                <th className="pb-2">CONFIDENCE</th>
                <th className="pb-2">STATUS</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E293B]/50">
              {learningCycles.map((c, idx) => (
                <tr key={idx} className="hover:bg-[#0B1120]/40">
                  <td className="py-3 font-bold text-white">{c.cycle}</td>
                  <td className="py-3 text-cyan-400 font-bold">{c.throughput}</td>
                  <td className="py-3 text-indigo-400 font-bold">{c.latency}</td>
                  <td className="py-3 text-emerald-400 font-bold">{c.conf}</td>
                  <td className="py-3">
                    <Badge variant="success" size="sm">PROMOTED</Badge>
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
