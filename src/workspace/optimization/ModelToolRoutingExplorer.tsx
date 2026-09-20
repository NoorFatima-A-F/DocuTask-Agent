import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { GitBranch, CheckCircle2 } from 'lucide-react';

export const ModelToolRoutingExplorer: React.FC = () => {
  const routes = [
    {
      taskId: 'task-extract-invoice-01',
      type: 'MODEL_ROUTING',
      target: 'gemini-1.5-flash',
      confidence: 0.965,
      cost: '$0.0021',
      rationale: 'Standard invoice density processed efficiently with low token latency on Gemini 1.5 Flash.',
    },
    {
      taskId: 'task-ocr-scanned-02',
      type: 'OCR_ROUTING',
      target: 'TESSERACT_FAST',
      confidence: 0.985,
      cost: '$0.0004',
      rationale: 'High-contrast clean digital document routed to local high-speed Tesseract OCR cluster.',
    },
    {
      taskId: 'task-verify-financial-totals-03',
      type: 'VALIDATION_ROUTING',
      target: 'SMT_SYMBOLIC_PROVER',
      confidence: 0.999,
      cost: '$0.0010',
      rationale: 'Financial balance table requires mathematical Z3 SMT constraint solving for zero schema drift.',
    },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 rounded-xl text-indigo-400">
            <GitBranch className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
              Model & Tool Routing Explorer
              <Badge variant="intelligence" size="sm">Phase 13.6 ARIA-EOP</Badge>
            </h1>
            <p className="text-xs text-[#94A3B8] font-mono">
              Policy-driven contextual routing across LLM reasoning tiers, OCR engines, and mathematical validation depth
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">Policy Governed Routing</Badge>
        </div>
      </div>

      {/* Routing Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 font-mono">
        {routes.map((r, idx) => (
          <Card key={idx} className="p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] space-y-4 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-start justify-between gap-2">
                <Badge variant="intelligence" size="sm">{r.type}</Badge>
                <span className="text-xs text-emerald-400 font-bold">{(r.confidence * 100).toFixed(1)}% Conf</span>
              </div>

              <div>
                <span className="text-[11px] text-[#64748B] block">TASK: {r.taskId}</span>
                <h3 className="text-sm font-bold text-white mt-1">{r.target}</h3>
              </div>

              <p className="text-xs text-[#94A3B8] leading-relaxed">{r.rationale}</p>
            </div>

            <div className="pt-3 border-t border-[#1E293B] flex items-center justify-between text-xs">
              <span className="text-cyan-400 font-bold">Cost: {r.cost}</span>
              <span className="text-emerald-400 flex items-center gap-1 font-bold">
                <CheckCircle2 className="w-3.5 h-3.5" /> Optimal
              </span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
