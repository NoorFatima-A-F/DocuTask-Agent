import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const OutcomeVerificationView: React.FC = () => {
  const [selectedFilter, setSelectedFilter] = useState<'ALL' | 'SLA_BREACH' | 'VERIFIED'>('ALL');

  const outcomes = [
    {
      id: 'OUT-2026-901',
      missionId: 'MIS-INV-8821',
      task: 'Structured Invoice Extraction',
      model: 'Gemini 2.5 Flash',
      predictedAcc: 0.965,
      observedAcc: 0.972,
      predictedLat: 480,
      observedLat: 462,
      predictedCost: 0.0018,
      observedCost: 0.00175,
      slaTargetMs: 1000,
      isSlaOk: true,
      timestamp: '1 min ago',
      status: 'VERIFIED',
    },
    {
      id: 'OUT-2026-902',
      missionId: 'MIS-TABLE-4412',
      task: 'Multi-Page Financial Table Extraction',
      model: 'Gemini 1.5 Pro',
      predictedAcc: 0.985,
      observedAcc: 0.988,
      predictedLat: 1850,
      observedLat: 1920,
      predictedCost: 0.0125,
      observedCost: 0.0131,
      slaTargetMs: 2500,
      isSlaOk: true,
      timestamp: '3 mins ago',
      status: 'VERIFIED',
    },
    {
      id: 'OUT-2026-903',
      missionId: 'MIS-SCAN-1099',
      task: 'Degraded Receipt OCR & Normalization',
      model: 'Gemini 2.5 Flash',
      predictedAcc: 0.920,
      observedAcc: 0.895,
      predictedLat: 550,
      observedLat: 1150,
      predictedCost: 0.0018,
      observedCost: 0.0036,
      slaTargetMs: 1000,
      isSlaOk: false,
      timestamp: '8 mins ago',
      status: 'SLA_BREACH',
    },
    {
      id: 'OUT-2026-904',
      missionId: 'MIS-KYC-0034',
      task: 'Identity Document Verification',
      model: 'Gemini Flash-Lite',
      predictedAcc: 0.940,
      observedAcc: 0.945,
      predictedLat: 220,
      observedLat: 210,
      predictedCost: 0.0004,
      observedCost: 0.00038,
      slaTargetMs: 800,
      isSlaOk: true,
      timestamp: '12 mins ago',
      status: 'VERIFIED',
    },
  ];

  const filteredOutcomes = outcomes.filter((o) => {
    if (selectedFilter === 'ALL') return true;
    return o.status === selectedFilter;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">🎯</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Empirical Outcome Verification Engine
              </h2>
              <Badge variant="success" size="sm">
                ONLINE PAIRING ACTIVE
              </Badge>
            </div>
            <p className="text-sm font-mono text-[#94A3B8] mt-1">
              Deterministic comparison of pre-execution planner predictions against post-execution ground-truth telemetry.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setSelectedFilter('ALL')}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${
                selectedFilter === 'ALL'
                  ? 'bg-blue-600 text-white'
                  : 'bg-[#1E293B] text-[#94A3B8] hover:bg-[#334155]'
              }`}
            >
              All Runs ({outcomes.length})
            </button>
            <button
              onClick={() => setSelectedFilter('SLA_BREACH')}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${
                selectedFilter === 'SLA_BREACH'
                  ? 'bg-rose-600 text-white'
                  : 'bg-[#1E293B] text-[#94A3B8] hover:bg-[#334155]'
              }`}
            >
              SLA Breaches (1)
            </button>
          </div>
        </div>
      </div>

      {/* Aggregate KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Overall SLA Compliance</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">97.8%</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">Target: ≥ 95.0%</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Mean Accuracy Error (MAE)</div>
          <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">0.0142</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">1.4% average residual</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Mean Latency Error</div>
          <div className="text-2xl font-bold font-mono text-indigo-400 mt-1">38.4 ms</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">Within ±50ms band</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Cost Drift Tracking</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">-$0.00004</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">Slight empirical surplus</div>
        </Card>
      </div>

      {/* Outcome Comparison Table */}
      <Card className="p-6 bg-[#0F172A] border-[#1E293B]">
        <h3 className="text-sm font-bold font-mono text-[#F8FAFC] mb-4">
          Recent Ground-Truth Verification Records
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead>
              <tr className="border-b border-[#1E293B] text-[#94A3B8]">
                <th className="pb-3">Mission & Task</th>
                <th className="pb-3">Model</th>
                <th className="pb-3">Predicted vs Observed Acc</th>
                <th className="pb-3">Predicted vs Observed Latency</th>
                <th className="pb-3">Predicted vs Observed Cost</th>
                <th className="pb-3">SLA Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E293B]">
              {filteredOutcomes.map((o) => {
                const accDiff = (o.observedAcc - o.predictedAcc) * 100;
                const latDiff = o.observedLat - o.predictedLat;
                return (
                  <tr key={o.id} className="hover:bg-[#1E293B]/40 transition-colors">
                    <td className="py-3">
                      <div className="font-bold text-[#F8FAFC]">{o.missionId}</div>
                      <div className="text-[#64748B] text-[11px]">{o.task}</div>
                    </td>
                    <td className="py-3 text-[#E2E8F0]">{o.model}</td>
                    <td className="py-3">
                      <div className="text-[#F8FAFC]">
                        {(o.predictedAcc * 100).toFixed(1)}% → {(o.observedAcc * 100).toFixed(1)}%
                      </div>
                      <div className={`text-[11px] ${accDiff >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                        {accDiff >= 0 ? `+${accDiff.toFixed(1)}%` : `${accDiff.toFixed(1)}%`}
                      </div>
                    </td>
                    <td className="py-3">
                      <div className="text-[#F8FAFC]">
                        {o.predictedLat}ms → {o.observedLat}ms
                      </div>
                      <div className={`text-[11px] ${latDiff <= 0 ? 'text-emerald-400' : 'text-amber-400'}`}>
                        {latDiff >= 0 ? `+${latDiff}ms` : `${latDiff}ms`}
                      </div>
                    </td>
                    <td className="py-3">
                      <div className="text-[#F8FAFC]">
                        ${o.predictedCost.toFixed(4)} → ${o.observedCost.toFixed(4)}
                      </div>
                    </td>
                    <td className="py-3">
                      <Badge variant={o.isSlaOk ? 'success' : 'error'} size="sm">
                        {o.isSlaOk ? 'COMPLIANT' : 'BREACH'}
                      </Badge>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
