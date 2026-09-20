import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Compass, Sliders } from 'lucide-react';

export const OptimizationDecisionExplorer: React.FC = () => {
  const optimizationDecision = {
    optimizationId: 'opt_8f1a029c',
    missionId: 'mission-001',
    objective: 'BALANCED_UTILITY',
    winningStrategy: 'High-Throughput Wavefront Strategy',
    utilityScore: 0.945,
    expectedSavings: '34.5%',
    expectedSpeedup: '28.2%',
    confidenceTarget: '96.5%',
    rationale: 'Pareto-optimal solution balancing latency (1850ms) and cost ($0.0032) while guaranteeing >96% confidence floor.',
    directives: {
      concurrencyPoolSize: 6,
      batchChunkSize: 4,
      baseRetryDelayMs: 250,
      modelTarget: 'gemini-1.5-flash',
      ocrTarget: 'TESSERACT_FAST',
      validationDepth: 'SMT_SYMBOLIC',
    },
  };

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-indigo-500/20 to-cyan-500/20 border border-indigo-500/30 rounded-xl text-indigo-400">
            <Compass className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
              Optimization Decision Explorer
              <Badge variant="intelligence" size="sm">Phase 13.6 ARIA-EOP</Badge>
            </h1>
            <p className="text-xs text-[#94A3B8] font-mono">
              Explainable decision engine showing why winning strategy was selected over candidate alternatives
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">Utility: {optimizationDecision.utilityScore}</Badge>
        </div>
      </div>

      {/* Decision Summary Card */}
      <Card className="p-6 rounded-2xl border border-indigo-500/40 bg-gradient-to-br from-[#0F172A] to-[#161D38] font-mono space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-4">
          <div>
            <span className="text-xs text-[#64748B] block">SELECTED OPTIMAL STRATEGY</span>
            <div className="flex items-baseline gap-3 mt-1">
              <span className="text-2xl font-bold text-white tracking-tight">{optimizationDecision.winningStrategy}</span>
              <Badge variant="success" size="sm">Pareto Dominant</Badge>
            </div>
          </div>
          <div className="text-right text-xs text-[#94A3B8]">
            <div>Objective: <span className="text-cyan-400">{optimizationDecision.objective}</span></div>
            <div>Optimization ID: <span className="text-white">{optimizationDecision.optimizationId}</span></div>
          </div>
        </div>

        <p className="text-xs text-[#94A3B8] leading-relaxed">{optimizationDecision.rationale}</p>

        {/* Gains Grid */}
        <div className="grid grid-cols-3 gap-4 pt-2">
          <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl">
            <span className="text-[10px] text-[#64748B] block">Cost Savings</span>
            <span className="text-lg font-bold text-cyan-400 block">{optimizationDecision.expectedSavings}</span>
          </div>
          <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl">
            <span className="text-[10px] text-[#64748B] block">Throughput Speedup</span>
            <span className="text-lg font-bold text-indigo-400 block">{optimizationDecision.expectedSpeedup}</span>
          </div>
          <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl">
            <span className="text-[10px] text-[#64748B] block">Confidence Target</span>
            <span className="text-lg font-bold text-emerald-400 block">{optimizationDecision.confidenceTarget}</span>
          </div>
        </div>
      </Card>

      {/* Generated Runtime Directives */}
      <Card className="p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] font-mono space-y-4">
        <div className="flex items-center justify-between border-b border-[#1E293B] pb-3">
          <span className="text-xs font-bold text-white flex items-center gap-1.5">
            <Sliders className="w-4 h-4 text-cyan-400" />
            Generated Execution Directives
          </span>
          <Badge variant="outline" size="sm">Ready for Execution Engine</Badge>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
          <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl">
            <span className="text-[10px] text-[#64748B] block">Concurrency Pool</span>
            <span className="text-white font-bold">{optimizationDecision.directives.concurrencyPoolSize} Workers</span>
          </div>
          <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl">
            <span className="text-[10px] text-[#64748B] block">Batch Chunk Size</span>
            <span className="text-white font-bold">{optimizationDecision.directives.batchChunkSize} Pages</span>
          </div>
          <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl">
            <span className="text-[10px] text-[#64748B] block">Model Target</span>
            <span className="text-cyan-400 font-bold">{optimizationDecision.directives.modelTarget}</span>
          </div>
          <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl">
            <span className="text-[10px] text-[#64748B] block">OCR Engine Target</span>
            <span className="text-indigo-400 font-bold">{optimizationDecision.directives.ocrTarget}</span>
          </div>
          <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl">
            <span className="text-[10px] text-[#64748B] block">Validation Depth</span>
            <span className="text-emerald-400 font-bold">{optimizationDecision.directives.validationDepth}</span>
          </div>
          <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl">
            <span className="text-[10px] text-[#64748B] block">Retry Delay (Jitter)</span>
            <span className="text-purple-400 font-bold">{optimizationDecision.directives.baseRetryDelayMs} ms</span>
          </div>
        </div>
      </Card>
    </div>
  );
};
