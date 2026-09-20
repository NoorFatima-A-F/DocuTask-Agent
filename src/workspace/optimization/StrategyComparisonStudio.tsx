import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Layers } from 'lucide-react';

export const StrategyComparisonStudio: React.FC = () => {
  const [selectedObjective, setSelectedObjective] = useState('BALANCED_UTILITY');

  const strategies = [
    {
      id: 'strat-01',
      name: 'Budget Sequential Plan',
      model: 'gemini-1.5-flash',
      ocr: 'TESSERACT_FAST',
      concurrency: 1,
      costUsd: 0.0018,
      latencyMs: 4200,
      confidence: 0.960,
      utility: 0.88,
      isWinner: selectedObjective === 'MINIMIZE_COST',
    },
    {
      id: 'strat-02',
      name: 'High-Throughput Wavefront',
      model: 'gemini-1.5-flash',
      ocr: 'TESSERACT_FAST',
      concurrency: 6,
      costUsd: 0.0032,
      latencyMs: 1850,
      confidence: 0.965,
      utility: 0.945,
      isWinner: selectedObjective === 'BALANCED_UTILITY' || selectedObjective === 'MINIMIZE_LATENCY',
    },
    {
      id: 'strat-03',
      name: 'High-Reasoning Invariant Plan',
      model: 'gemini-1.5-pro',
      ocr: 'DOCUMENT_AI_ADVANCED',
      concurrency: 4,
      costUsd: 0.0120,
      latencyMs: 3100,
      confidence: 0.992,
      utility: 0.91,
      isWinner: selectedObjective === 'MAXIMIZE_CONFIDENCE',
    },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-purple-500/20 to-indigo-500/20 border border-purple-500/30 rounded-xl text-purple-400">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
              Strategy Comparison Studio
              <Badge variant="intelligence" size="sm">Phase 13.6 ARIA-EOP</Badge>
            </h1>
            <p className="text-xs text-[#94A3B8] font-mono">
              Multi-dimensional Pareto frontier comparison across cost, latency, confidence, and resource footprint
            </p>
          </div>
        </div>

        {/* Objective Selector */}
        <select
          value={selectedObjective}
          onChange={(e) => setSelectedObjective(e.target.value)}
          className="bg-[#0F172A] border border-[#334155] rounded-lg px-3 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-purple-500"
        >
          <option value="BALANCED_UTILITY">Objective: Balanced Utility</option>
          <option value="MINIMIZE_COST">Objective: Minimize Cost</option>
          <option value="MINIMIZE_LATENCY">Objective: Minimize Latency</option>
          <option value="MAXIMIZE_CONFIDENCE">Objective: Maximize Confidence</option>
        </select>
      </div>

      {/* Strategy Comparison Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 font-mono">
        {strategies.map((strat) => (
          <Card
            key={strat.id}
            className={`p-5 rounded-2xl border space-y-4 flex flex-col justify-between ${
              strat.isWinner
                ? 'border-indigo-500/60 bg-gradient-to-br from-[#0F172A] to-[#151B38] shadow-[0_0_20px_rgba(99,102,241,0.2)]'
                : 'border-[#1E293B] bg-[#0F172A]'
            }`}
          >
            <div className="space-y-3">
              <div className="flex items-start justify-between gap-2">
                <span className="text-xs text-[#64748B]">{strat.id}</span>
                {strat.isWinner ? (
                  <Badge variant="success" size="sm">WINNING STRATEGY</Badge>
                ) : (
                  <Badge variant="outline" size="sm">Candidate</Badge>
                )}
              </div>

              <div>
                <h3 className="text-sm font-bold text-white">{strat.name}</h3>
                <span className="text-xs text-indigo-400 font-bold block mt-0.5">Utility: {strat.utility}</span>
              </div>

              <div className="space-y-2 text-xs pt-2 border-t border-[#1E293B]">
                <div className="flex justify-between text-[#94A3B8]">
                  <span>Model:</span>
                  <span className="text-white font-bold">{strat.model}</span>
                </div>
                <div className="flex justify-between text-[#94A3B8]">
                  <span>OCR Engine:</span>
                  <span className="text-cyan-400 font-bold">{strat.ocr}</span>
                </div>
                <div className="flex justify-between text-[#94A3B8]">
                  <span>Estimated Cost:</span>
                  <span className="text-emerald-400 font-bold">${strat.costUsd.toFixed(4)}</span>
                </div>
                <div className="flex justify-between text-[#94A3B8]">
                  <span>Latency:</span>
                  <span className="text-amber-400 font-bold">{strat.latencyMs} ms</span>
                </div>
                <div className="flex justify-between text-[#94A3B8]">
                  <span>Confidence:</span>
                  <span className="text-teal-400 font-bold">{(strat.confidence * 100).toFixed(1)}%</span>
                </div>
              </div>
            </div>

            <div className="pt-3 border-t border-[#1E293B] flex items-center justify-between text-xs text-[#64748B]">
              <span>Workers: {strat.concurrency}</span>
              <span className="text-indigo-400 font-bold">Pareto Feasible</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
