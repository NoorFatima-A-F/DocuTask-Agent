import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const RuntimeCostIntelligenceView: React.FC = () => {
  const modelBreakdowns = [
    {
      model: 'Gemini 2.5 Flash',
      role: 'High-Throughput Structured Extraction',
      inputTokens: '2,200',
      outputTokens: '650',
      cachedTokens: '1,000 (45%)',
      cost: '$0.00185',
      cacheSavings: '$0.00006',
      energyKwh: '0.00085 kWh',
      co2Grams: '0.32 g',
      pctTotal: '77.0%',
    },
    {
      model: 'Gemini Flash-Lite',
      role: 'Cross-Validation & Invariant Checking',
      inputTokens: '600',
      outputTokens: '150',
      cachedTokens: '400 (66%)',
      cost: '$0.00035',
      cacheSavings: '$0.00002',
      energyKwh: '0.00022 kWh',
      co2Grams: '0.08 g',
      pctTotal: '14.5%',
    },
    {
      model: 'Local LayoutLM / Tesseract',
      role: 'Zero API Token OCR Preprocessing',
      inputTokens: '800',
      outputTokens: '300',
      cachedTokens: '0 (0%)',
      cost: '$0.00020 (Compute)',
      cacheSavings: '$0.00000',
      energyKwh: '0.00033 kWh',
      co2Grams: '0.12 g',
      pctTotal: '8.5%',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">💰</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Runtime Cost & Carbon Energy Intelligence
              </h2>
              <Badge variant="success" size="sm">
                DYNAMIC PARETO GOVERNED
              </Badge>
            </div>
            <p className="text-sm font-mono text-[#94A3B8] mt-1">
              Multi-dimensional cost accounting per tool, model, prompt cache hits, and datacenter energy footprints.
            </p>
          </div>
        </div>
      </div>

      {/* Aggregate KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Total Net Mission Cost</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">$0.00240</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">Budget Ceiling: $0.01000 (24% utilized)</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Prompt Cache Savings</div>
          <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">+$0.00008</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">3.2% net discount from prefix cache</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Total Tokens Consumed</div>
          <div className="text-2xl font-bold font-mono text-indigo-400 mt-1">4,700 tokens</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">Input: 3,600 • Output: 1,100</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Estimated Compute Carbon</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">0.52 g CO₂</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">0.0014 kWh cluster energy</div>
        </Card>
      </div>

      {/* Granular Cost Breakdown Matrix */}
      <Card className="p-6 bg-[#0F172A] border-[#1E293B]">
        <h3 className="text-sm font-bold font-mono text-[#F8FAFC] mb-4">
          Subsystem Token, Financial & Environmental Matrix
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead>
              <tr className="border-b border-[#1E293B] text-[#94A3B8]">
                <th className="pb-3">Model & Role</th>
                <th className="pb-3">Input / Output Tokens</th>
                <th className="pb-3">Cached Tokens</th>
                <th className="pb-3">Net Cost</th>
                <th className="pb-3">Cache Savings</th>
                <th className="pb-3">Carbon (CO₂)</th>
                <th className="pb-3">Share</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E293B]">
              {modelBreakdowns.map((m, idx) => (
                <tr key={idx} className="hover:bg-[#1E293B]/40 transition-colors">
                  <td className="py-3">
                    <div className="font-bold text-[#F8FAFC]">{m.model}</div>
                    <div className="text-[#64748B] text-[11px]">{m.role}</div>
                  </td>
                  <td className="py-3 text-[#E2E8F0]">{m.inputTokens} in / {m.outputTokens} out</td>
                  <td className="py-3 text-cyan-400">{m.cachedTokens}</td>
                  <td className="py-3 text-emerald-400 font-bold">{m.cost}</td>
                  <td className="py-3 text-cyan-400">{m.cacheSavings}</td>
                  <td className="py-3 text-[#94A3B8]">{m.co2Grams}</td>
                  <td className="py-3 text-indigo-400 font-bold">{m.pctTotal}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
