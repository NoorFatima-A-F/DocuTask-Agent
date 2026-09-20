import React, { useState } from 'react';
import {
  Compass,
  CheckCircle2,
  RefreshCw,
  Zap,
  HelpCircle
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

interface DiagnosisExplorerProps {
  missionId?: string;
}

export const DiagnosisExplorer: React.FC<DiagnosisExplorerProps> = ({
  missionId = 'inc-9b2f1a',
}) => {
  const [activeDiagnosis] = useState({
    diagnosisId: 'diag-4a1d8e',
    incidentId: missionId,
    primaryCulprit: 'WORKERS',
    errorPattern: 'WORKER_CRASH',
    confidence: 0.965,
    recommendedAction: 'WORKER_RESTART',
    summary: 'Root cause identified in [WORKERS] (WORKER_CRASH) causing downstream degradation in 2 subsystems.',
    causalChain: [
      'Anomaly originated in [WORKERS] characterized by unhandled OCR segfault in thread #4.',
      'Degradation propagated downstream from [WORKERS] to [PLANNER] queue listener.',
      'Cascading failure bounded; autonomous healing isolation engaged for [WORKERS].',
    ],
    evidenceSources: ['EventStore', 'ReplayEngine', 'RuntimeTelemetry', 'TruthLedger'],
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Compass className="w-5 h-5 text-indigo-400" />
            Autonomous Diagnosis & Explainable Root-Cause Explorer
          </h2>
          <p className="text-sm text-slate-400">
            Multi-source causal reasoning, failure propagation topology, and diagnostic confidence proofs for: <code className="text-indigo-300 font-mono text-xs">{activeDiagnosis.incidentId}</code>
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="intelligence" size="md">
            Diagnosis Confidence: {(activeDiagnosis.confidence * 100).toFixed(1)}%
          </Badge>
          <button className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700">
            <RefreshCw className="w-3.5 h-3.5" />
            Re-infer Root Cause
          </button>
        </div>
      </div>

      {/* Summary Card */}
      <Card className="p-5 bg-slate-900 border-slate-800 space-y-4 font-mono">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div>
            <span className="text-xs text-slate-400 block">PRIMARY ROOT CAUSE CULPRIT</span>
            <span className="text-lg font-bold text-rose-400 mt-0.5 block">{activeDiagnosis.primaryCulprit} ({activeDiagnosis.errorPattern})</span>
          </div>
          <div className="text-right">
            <span className="text-xs text-slate-400 block">RECOMMENDED REMEDIATION</span>
            <span className="text-sm font-bold text-emerald-400 flex items-center gap-1 justify-end mt-0.5">
              <Zap className="w-3.5 h-3.5" />
              {activeDiagnosis.recommendedAction}
            </span>
          </div>
        </div>

        <p className="text-xs text-slate-300 leading-relaxed">{activeDiagnosis.summary}</p>

        {/* Evidence Sources */}
        <div className="flex items-center gap-2 pt-2 border-t border-slate-800 text-xs">
          <span className="text-slate-400">Verified Evidence Sources:</span>
          {activeDiagnosis.evidenceSources.map((src, idx) => (
            <Badge key={idx} variant="outline" size="sm">
              <CheckCircle2 className="w-3 h-3 text-emerald-400 mr-1" />
              {src}
            </Badge>
          ))}
        </div>
      </Card>

      {/* Causal Chain Graph */}
      <Card className="p-5 bg-slate-900 border-slate-800 space-y-4 font-mono">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <HelpCircle className="w-4 h-4 text-cyan-400" />
          Explainable Causal Failure Propagation Chain
        </h3>

        <div className="space-y-3">
          {activeDiagnosis.causalChain.map((step, idx) => (
            <div key={idx} className="p-3.5 rounded-lg bg-slate-950 border border-slate-800 flex items-start gap-3">
              <div className="p-1.5 rounded-md bg-indigo-950/60 border border-indigo-500/30 text-indigo-400 text-xs font-bold mt-0.5">
                0{idx + 1}
              </div>
              <div className="space-y-1 text-xs">
                <span className="text-slate-200 font-semibold">{step}</span>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
