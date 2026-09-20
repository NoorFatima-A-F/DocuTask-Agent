import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { DollarSign } from 'lucide-react';

export const EconomicIntelligenceCenter: React.FC = () => {
  const economicData = {
    totalCostUsd: 0.0032,
    modelCostUsd: 0.0018,
    ocrCostUsd: 0.0008,
    computeCostUsd: 0.0005,
    storageCostUsd: 0.0001,
    grossBusinessValueUsd: 16.50,
    netValueGeneratedUsd: 16.4968,
    roiRatio: 51.5,
    costPerConfidencePoint: 0.000033,
    costPerMinuteSaved: 0.0016,
    energyJoules: 14.2,
  };

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 rounded-xl text-emerald-400">
            <DollarSign className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
              Economic Intelligence Center
              <Badge variant="intelligence" size="sm">Phase 13.6 ARIA-EOP</Badge>
            </h1>
            <p className="text-xs text-[#94A3B8] font-mono">
              Deterministic cost models, token economics, business value generation, and enterprise ROI calculations
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">ROI Multiple: {economicData.roiRatio}x</Badge>
        </div>
      </div>

      {/* Top Economic KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 font-mono">
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B] rounded-xl">
          <span className="text-[11px] text-[#64748B] block">Execution Cost</span>
          <span className="text-2xl font-bold text-cyan-400 mt-1 block">${economicData.totalCostUsd.toFixed(4)}</span>
        </Card>
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B] rounded-xl">
          <span className="text-[11px] text-[#64748B] block">Gross Business Value</span>
          <span className="text-2xl font-bold text-emerald-400 mt-1 block">${economicData.grossBusinessValueUsd.toFixed(2)}</span>
        </Card>
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B] rounded-xl">
          <span className="text-[11px] text-[#64748B] block">Net Value Generated</span>
          <span className="text-2xl font-bold text-indigo-400 mt-1 block">${economicData.netValueGeneratedUsd.toFixed(2)}</span>
        </Card>
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B] rounded-xl">
          <span className="text-[11px] text-[#64748B] block">Energy Consumed</span>
          <span className="text-2xl font-bold text-amber-400 mt-1 block">{economicData.energyJoules} J</span>
        </Card>
      </div>

      {/* Detailed Cost Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 font-mono">
        <Card className="p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] space-y-4">
          <span className="text-xs font-bold text-white block">Unit Cost Decomposition</span>
          <div className="space-y-2.5 text-xs">
            <div className="flex justify-between text-[#94A3B8] pb-1 border-b border-[#1E293B]">
              <span>LLM Token Inference</span>
              <span className="text-cyan-400 font-bold">${economicData.modelCostUsd.toFixed(4)} USD</span>
            </div>
            <div className="flex justify-between text-[#94A3B8] pb-1 border-b border-[#1E293B]">
              <span>OCR Pipeline Execution</span>
              <span className="text-indigo-400 font-bold">${economicData.ocrCostUsd.toFixed(4)} USD</span>
            </div>
            <div className="flex justify-between text-[#94A3B8] pb-1 border-b border-[#1E293B]">
              <span>Worker Node Compute</span>
              <span className="text-purple-400 font-bold">${economicData.computeCostUsd.toFixed(4)} USD</span>
            </div>
            <div className="flex justify-between text-[#94A3B8] pb-1 border-b border-[#1E293B]">
              <span>Cache & Ephemeral Storage</span>
              <span className="text-emerald-400 font-bold">${economicData.storageCostUsd.toFixed(4)} USD</span>
            </div>
          </div>
        </Card>

        {/* Marginal Value & Efficiency Multiple */}
        <Card className="p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] space-y-4">
          <span className="text-xs font-bold text-white block">Efficiency & Value Metrics</span>
          <div className="space-y-2.5 text-xs">
            <div className="flex justify-between text-[#94A3B8] pb-1 border-b border-[#1E293B]">
              <span>Cost per Confidence Point</span>
              <span className="text-emerald-400 font-bold">${economicData.costPerConfidencePoint.toFixed(6)}</span>
            </div>
            <div className="flex justify-between text-[#94A3B8] pb-1 border-b border-[#1E293B]">
              <span>Cost per Minute Saved</span>
              <span className="text-cyan-400 font-bold">${economicData.costPerMinuteSaved.toFixed(4)}</span>
            </div>
            <div className="flex justify-between text-[#94A3B8] pb-1 border-b border-[#1E293B]">
              <span>Manual Review Saved (Est.)</span>
              <span className="text-indigo-400 font-bold">$4.50 USD</span>
            </div>
            <div className="flex justify-between text-[#94A3B8] pb-1 border-b border-[#1E293B]">
              <span>Downstream Error Risk Avoided</span>
              <span className="text-teal-400 font-bold">$12.00 USD</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
