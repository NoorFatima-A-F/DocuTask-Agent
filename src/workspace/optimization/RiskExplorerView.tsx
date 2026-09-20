import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const RiskExplorerView: React.FC = () => {
  const failureProbabilities = [
    { name: 'P(timeout)', value: 0.018, threshold: 0.05, status: 'LOW' },
    { name: 'P(validation failure)', value: 0.012, threshold: 0.04, status: 'LOW' },
    { name: 'P(OCR degradation)', value: 0.035, threshold: 0.10, status: 'LOW' },
    { name: 'P(retry requirement)', value: 0.024, threshold: 0.08, status: 'LOW' },
    { name: 'P(memory mismatch)', value: 0.015, threshold: 0.05, status: 'LOW' },
    { name: 'P(worker failure)', value: 0.008, threshold: 0.03, status: 'MINIMAL' },
  ];

  const mitigations = [
    {
      id: 'MIT-01',
      target: 'P(OCR degradation)',
      action: 'Auto-enable dual-engine ensemble (PyTesseract + Vision Transformer)',
      reduction: '-65% Risk',
      cost: '+$0.005',
    },
    {
      id: 'MIT-02',
      target: 'P(timeout)',
      action: 'Speculative sub-task branch parallelization with fast Flash fallback',
      reduction: '-70% Risk',
      cost: '-$0.002',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">⚠️</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Scientific Risk Engine & Hazard Modeler
              </h2>
              <Badge variant="success" size="sm">
                JOINT HAZARD: 2.0%
              </Badge>
            </div>
            <p className="text-xs text-[#94A3B8] mt-1">
              Replaces qualitative labels with explicit marginal failure probabilities: $P(timeout)$, $P(validation)$, $P(retry)$.
            </p>
          </div>
          <div className="text-right">
            <div className="text-xs font-mono text-[#94A3B8]">Overall Failure Probability</div>
            <div className="text-2xl font-mono font-extrabold text-emerald-400">1.98%</div>
          </div>
        </div>
      </div>

      {/* Probabilities Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {failureProbabilities.map((p) => (
          <Card key={p.name} className="p-4 bg-[#0F172A] border border-[#1E293B] space-y-2">
            <div className="flex justify-between items-center text-xs font-mono">
              <span className="text-cyan-400 font-bold">{p.name}</span>
              <Badge variant="outline" size="sm">
                {p.status}
              </Badge>
            </div>
            <div className="flex justify-between items-baseline pt-1">
              <span className="text-xl font-mono font-bold text-[#F8FAFC]">{(p.value * 100).toFixed(2)}%</span>
              <span className="text-[11px] font-mono text-[#64748B]">Cap: {(p.threshold * 100).toFixed(1)}%</span>
            </div>
            <div className="w-full bg-[#131D35] h-1.5 rounded-full overflow-hidden">
              <div
                className="bg-emerald-400 h-1.5 rounded-full"
                style={{ width: `${(p.value / p.threshold) * 100}%` }}
              />
            </div>
          </Card>
        ))}
      </div>

      {/* Prescriptive Mitigations */}
      <Card className="p-5 bg-[#0F172A] border border-[#1E293B] space-y-3">
        <h3 className="text-sm font-bold font-mono text-[#F8FAFC] flex items-center gap-2">
          <span>🩹</span> Prescriptive Dynamic Risk Mitigations
        </h3>
        <div className="space-y-2">
          {mitigations.map((m) => (
            <div
              key={m.id}
              className="p-3 rounded-xl bg-[#131D35]/50 border border-[#1E293B] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs font-mono"
            >
              <div className="flex items-center gap-3">
                <Badge variant="outline" size="sm">
                  {m.id}
                </Badge>
                <div>
                  <div className="text-cyan-400 font-bold">{m.target}</div>
                  <div className="text-[#94A3B8] font-sans text-[11px]">{m.action}</div>
                </div>
              </div>
              <div className="flex items-center gap-3 text-right shrink-0">
                <span className="text-emerald-400 font-bold">{m.reduction}</span>
                <span className="text-[#64748B]">{m.cost}</span>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
