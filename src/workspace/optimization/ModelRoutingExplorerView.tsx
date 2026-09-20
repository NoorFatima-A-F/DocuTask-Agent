import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ModelRoutingExplorerView: React.FC = () => {
  const models = [
    {
      id: 'gemini-1.5-flash',
      name: 'Gemini 1.5 Flash',
      expectedAcc: '95.0%',
      expectedCost: '$0.0012',
      expectedLat: '650ms',
      utilityScore: 0.948,
      isWinner: true,
      role: 'Optimal for Current High-Throughput Task',
    },
    {
      id: 'gemini-1.5-pro',
      name: 'Gemini 1.5 Pro',
      expectedAcc: '98.5%',
      expectedCost: '$0.0175',
      expectedLat: '2200ms',
      utilityScore: 0.865,
      isWinner: false,
      role: 'Heavyweight Multimodal & Reasoning',
    },
    {
      id: 'gemini-flash-lite',
      name: 'Gemini Flash Lite',
      expectedAcc: '91.0%',
      expectedCost: '$0.0004',
      expectedLat: '300ms',
      utilityScore: 0.882,
      isWinner: false,
      role: 'Low Cost Pre-Classification',
    },
    {
      id: 'local-ocr-specialist',
      name: 'Local LayoutLM / Tesseract',
      expectedAcc: '88.0%',
      expectedCost: '$0.0000',
      expectedLat: '180ms',
      utilityScore: 0.795,
      isWinner: false,
      role: 'Zero API Cost Local OCR',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">🔀</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Scientific Model Router & Utility Evaluator
              </h2>
              <Badge variant="success" size="sm">
                UTILITY MAXIMIZING ROUTE
              </Badge>
            </div>
            <p className="text-xs text-[#94A3B8] mt-1">
              Model selection is formulated as multi-attribute expected utility maximization under document complexity constraints.
            </p>
          </div>
          <div className="text-right">
            <div className="text-xs font-mono text-[#94A3B8]">Selected Optimal Model</div>
            <div className="text-lg font-mono font-bold text-emerald-400">Gemini 1.5 Flash (U=0.948)</div>
          </div>
        </div>
      </div>

      {/* Model Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {models.map((m) => (
          <Card
            key={m.id}
            className={`p-5 bg-[#0F172A] border transition-all ${
              m.isWinner
                ? 'border-emerald-500/70 shadow-[0_0_20px_rgba(16,185,129,0.15)] ring-1 ring-emerald-500/50'
                : 'border-[#1E293B]'
            }`}
          >
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold text-[#F8FAFC]">{m.name}</span>
                  {m.isWinner && (
                    <Badge variant="success" size="sm">
                      WINNER
                    </Badge>
                  )}
                </div>
                <div className="text-[11px] font-mono text-[#64748B] mt-0.5">{m.role}</div>
              </div>
              <div className="text-right">
                <div className="text-[10px] text-[#94A3B8]">Expected Utility</div>
                <div className="text-base font-mono font-extrabold text-cyan-400">{m.utilityScore.toFixed(3)}</div>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-2 mt-4 pt-3 border-t border-[#1E293B] text-center text-xs font-mono">
              <div className="bg-[#131D35]/50 p-2 rounded-lg">
                <div className="text-[10px] text-[#64748B]">Exp. Accuracy</div>
                <div className="font-bold text-emerald-400">{m.expectedAcc}</div>
              </div>
              <div className="bg-[#131D35]/50 p-2 rounded-lg">
                <div className="text-[10px] text-[#64748B]">Exp. Cost</div>
                <div className="font-bold text-[#F8FAFC]">{m.expectedCost}</div>
              </div>
              <div className="bg-[#131D35]/50 p-2 rounded-lg">
                <div className="text-[10px] text-[#64748B]">Exp. Latency</div>
                <div className="font-bold text-cyan-400">{m.expectedLat}</div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
