import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { ShieldAlert, ArrowRight, Search, CheckCircle2 } from 'lucide-react';

export const ReplayForensicsCenter: React.FC = () => {
  const findings = [
    {
      id: 'F-001',
      category: 'RECOVERY_TRIGGER',
      severity: 'WARNING',
      event: 'worker.step.retry',
      description: 'OCR scan contrast below threshold on page 2. Activated contrast auto-normalization recovery sub-graph.',
      causalChain: ['evt_004 (worker.started)', 'evt_005 (quality.checked)', 'evt_006 (worker.step.retry)'],
      remedy: 'Contrast equalization succeeded; nominal extraction continued.',
    },
    {
      id: 'F-002',
      category: 'CONFIDENCE_DRIFT',
      severity: 'INFO',
      event: 'confidence.evaluated',
      description: 'Epistemic uncertainty decreased by 0.014 following invariant verification satisfaction.',
      causalChain: ['evt_007 (confidence.evaluated)', 'evt_008 (truth.invariant.checked)'],
      remedy: 'Posterior belief updated to 98.42%.',
    },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-amber-500/20 to-red-500/20 border border-amber-500/30 rounded-xl text-amber-400">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Replay Forensics & Root-Cause Center
                <Badge variant="warning" size="sm">Automated Causal Backtracking</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Post-mortem causal analysis, failure chain reconstruction, and anomaly attribution across mission lifecycles.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" size="sm">0 Invariant Violations</Badge>
        </div>
      </div>

      {/* Forensic Findings List */}
      <div className="space-y-4 font-mono text-xs">
        {findings.map((f) => (
          <Card key={f.id} className="p-5 bg-[#0F172A] border-[#1E293B] space-y-3">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <span className="font-bold text-amber-400">{f.id}</span>
                <span className="font-bold text-white text-sm">{f.category}</span>
                <Badge variant="warning" size="sm">{f.severity}</Badge>
              </div>
              <Badge variant="outline" size="sm">{f.event}</Badge>
            </div>

            <p className="text-slate-300 text-xs">{f.description}</p>

            {/* Causal chain */}
            <div className="p-3 bg-slate-900/60 rounded-lg border border-slate-800 space-y-1.5">
              <div className="text-[11px] font-bold text-slate-400 flex items-center gap-1.5">
                <Search className="w-3.5 h-3.5 text-cyan-400" /> Causal Dependency Chain:
              </div>
              <div className="flex flex-wrap items-center gap-2 text-slate-300">
                {f.causalChain.map((step, idx) => (
                  <React.Fragment key={idx}>
                    <span className="bg-slate-800 px-2 py-0.5 rounded text-cyan-300">{step}</span>
                    {idx < f.causalChain.length - 1 && <ArrowRight className="w-3 h-3 text-slate-500" />}
                  </React.Fragment>
                ))}
              </div>
            </div>

            <div className="flex items-center gap-2 text-emerald-400 text-[11px]">
              <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
              <span>Attribution: {f.remedy}</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
