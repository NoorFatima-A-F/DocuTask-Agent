import React from 'react';
import { Badge } from '../../components/ui/Badge';

export const AnalyticsDashboard: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-[#0F172A] to-[#1E293B] border border-[#334155]/60 shadow-xl">
        <div>
          <Badge variant="intelligence" size="sm">EXECUTIVE BUSINESS INTELLIGENCE</Badge>
          <h1 className="text-2xl font-black text-white mt-1">ROI & Operational Impact Dashboard</h1>
          <p className="text-sm text-[#94A3B8]">
            Quantifiable labor savings, unit cost economics, and straight-through processing benchmarks.
          </p>
        </div>
        <div className="text-right">
          <span className="text-xs text-[#94A3B8] block">Audited Payback Period</span>
          <span className="text-xl font-black text-emerald-400 font-mono">1.4 Months (4.2x ROI)</span>
        </div>
      </div>

      {/* Financial ROI Overview Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 rounded-2xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xl space-y-3">
          <span className="text-xs text-[#94A3B8] uppercase font-mono">Manual Baseline Cost</span>
          <div className="text-3xl font-black text-rose-400 font-mono">$2,450,000 / yr</div>
          <p className="text-xs text-[#94A3B8] leading-relaxed">
            Based on 22 full-time analysts processing 125,000 annual documents at $35.00/doc.
          </p>
        </div>

        <div className="p-6 rounded-2xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xl space-y-3">
          <span className="text-xs text-[#94A3B8] uppercase font-mono">Autonomous AI Cost</span>
          <div className="text-3xl font-black text-cyan-400 font-mono">$170,000 / yr</div>
          <p className="text-xs text-[#94A3B8] leading-relaxed">
            Blended LLM token usage, OCR compute, and infrastructure at $0.025/doc.
          </p>
        </div>

        <div className="p-6 rounded-2xl bg-[#0F172A]/80 border border-emerald-500/40 bg-gradient-to-br from-emerald-950/20 to-transparent shadow-xl space-y-3">
          <span className="text-xs text-emerald-400 uppercase font-mono">Net Annual Value Liberated</span>
          <div className="text-3xl font-black text-emerald-400 font-mono">$2,280,000 / yr</div>
          <p className="text-xs text-[#CBD5E1] leading-relaxed">
            92.8% net cost reduction and 57,500 human hours redirected to high-value strategy.
          </p>
        </div>
      </div>

      {/* Operational Performance Breakdown */}
      <div className="p-6 rounded-2xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xl space-y-4">
        <h2 className="text-base font-bold text-white">Operational SLA & Throughput Metrics</h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
          <div className="p-4 rounded-xl bg-[#0A0F1D] border border-[#1E293B]">
            <span className="text-xs text-[#94A3B8] block mb-1">P95 Latency</span>
            <span className="text-xl font-bold text-white font-mono">285 ms</span>
          </div>
          <div className="p-4 rounded-xl bg-[#0A0F1D] border border-[#1E293B]">
            <span className="text-xs text-[#94A3B8] block mb-1">Extraction Accuracy</span>
            <span className="text-xl font-bold text-emerald-400 font-mono">99.1%</span>
          </div>
          <div className="p-4 rounded-xl bg-[#0A0F1D] border border-[#1E293B]">
            <span className="text-xs text-[#94A3B8] block mb-1">System Availability</span>
            <span className="text-xl font-bold text-cyan-400 font-mono">99.99%</span>
          </div>
          <div className="p-4 rounded-xl bg-[#0A0F1D] border border-[#1E293B]">
            <span className="text-xs text-[#94A3B8] block mb-1">MTTR (Recovery)</span>
            <span className="text-xl font-bold text-purple-400 font-mono">2.2 sec</span>
          </div>
        </div>
      </div>
    </div>
  );
};
