import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const CausalAnalysisView: React.FC = () => {
  const [selectedTreatment, setSelectedTreatment] = useState('gemini-1.5-pro');

  const scmNodes = [
    { id: 'complexity', name: 'Document Complexity (Z)', type: 'EXOGENOUS', desc: 'Layout density, table count, visual noise' },
    { id: 'ocr_noise', name: 'OCR Quality Noise (W)', type: 'EXOGENOUS', desc: 'Base optical character recognition confidence score' },
    { id: 'model_choice', name: 'Planner Model Choice (X)', type: 'INTERVENTION', desc: 'Routing decision: Flash vs Pro vs Flash-Lite' },
    { id: 'retry_count', name: 'Retry Loop Count (R)', type: 'MEDIATOR', desc: 'Validation failures & exponential backoff retries' },
    { id: 'accuracy', name: 'Extraction Accuracy (Y_A)', type: 'OUTCOME', desc: 'Ground truth field-level exact-match score' },
    { id: 'latency_ms', name: 'End-to-End Latency (Y_L)', type: 'OUTCOME', desc: 'Total mission execution duration (ms)' },
    { id: 'cost_usd', name: 'Execution Cost USD (Y_C)', type: 'OUTCOME', desc: 'Total LLM API token monetary expenditure' },
  ];

  const rootCauseAttributions = [
    {
      node: 'OCR Quality Noise (W)',
      share: '35.0%',
      isRoot: true,
      explanation: 'Low OCR confidence (0.68) triggered extensive re-OCR and heuristic repair passes.',
    },
    {
      node: 'Retry Loop Count (R)',
      share: '40.0%',
      isRoot: false,
      explanation: '3 exponential backoff retries amplified cumulative mission latency by +1200ms.',
    },
    {
      node: 'Planner Model Choice (X)',
      share: '25.0%',
      isRoot: false,
      explanation: 'Heavyweight reasoning model choice incurred higher base token processing time.',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">🕸️</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Pearl's Structural Causal Models (SCM) & do()-Calculus
              </h2>
              <Badge variant="success" size="sm">
                BACKDOOR ADJUSTED
              </Badge>
            </div>
            <p className="text-sm font-mono text-[#94A3B8] mt-1">
              Causal DAG structural equation modeling, interventional Average Treatment Effect (ATE), and root-cause attribution.
            </p>
          </div>
        </div>
      </div>

      {/* SCM DAG Node Matrix */}
      <Card className="p-6 bg-[#0F172A] border-[#1E293B]">
        <h3 className="text-sm font-bold font-mono text-[#F8FAFC] mb-4">
          Structural Causal Model DAG Architecture
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
          {scmNodes.map((n) => (
            <div key={n.id} className="p-3 rounded-lg bg-[#020617] border border-[#1E293B]">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold font-mono text-[#F8FAFC]">{n.name}</span>
                <Badge
                  variant={
                    n.type === 'INTERVENTION'
                      ? 'info'
                      : n.type === 'OUTCOME'
                      ? 'success'
                      : n.type === 'MEDIATOR'
                      ? 'warning'
                      : 'default'
                  }
                  size="sm"
                >
                  {n.type}
                </Badge>
              </div>
              <p className="text-[11px] font-mono text-[#94A3B8] mt-2">{n.desc}</p>
            </div>
          ))}
        </div>
      </Card>

      {/* Pearl's do-Calculus Intervention Calculator */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-6 bg-[#0F172A] border-[#1E293B]">
          <h3 className="text-sm font-bold font-mono text-[#F8FAFC] mb-2">
            Interventional do(X = x) Average Treatment Effect
          </h3>
          <p className="text-xs font-mono text-[#94A3B8] mb-4">
            Formula: P(Y | do(X=x)) = ∑_z P(Y | X=x, Z=z) · P(Z=z)
          </p>
          <div className="flex items-center gap-2 mb-4">
            <button
              onClick={() => setSelectedTreatment('gemini-1.5-pro')}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${
                selectedTreatment === 'gemini-1.5-pro'
                  ? 'bg-blue-600 text-white'
                  : 'bg-[#1E293B] text-[#94A3B8]'
              }`}
            >
              do(Model = Gemini 1.5 Pro)
            </button>
            <button
              onClick={() => setSelectedTreatment('gemini-flash-lite')}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${
                selectedTreatment === 'gemini-flash-lite'
                  ? 'bg-blue-600 text-white'
                  : 'bg-[#1E293B] text-[#94A3B8]'
              }`}
            >
              do(Model = Flash-Lite)
            </button>
          </div>

          <div className="p-4 rounded-xl bg-[#020617] border border-[#1E293B] space-y-2 font-mono text-xs">
            <div className="flex justify-between">
              <span className="text-[#94A3B8]">Observational Expectation E[Y|X]:</span>
              <span className="text-[#F8FAFC]">0.9700</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#94A3B8]">Interventional Expectation E[Y|do(X)]:</span>
              <span className="text-cyan-400 font-bold">0.9855</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#94A3B8]">Confounding Bias (Selection Effect):</span>
              <span className="text-amber-400">-0.0155</span>
            </div>
            <div className="flex justify-between pt-2 border-t border-[#1E293B]">
              <span className="text-[#94A3B8]">Average Treatment Effect (ATE):</span>
              <span className="text-emerald-400 font-bold">+0.0355 (+3.55% Acc)</span>
            </div>
          </div>
        </Card>

        {/* Root Cause Attribution */}
        <Card className="p-6 bg-[#0F172A] border-[#1E293B]">
          <h3 className="text-sm font-bold font-mono text-[#F8FAFC] mb-2">
            Causal Root-Cause Attribution Waterfall
          </h3>
          <p className="text-xs font-mono text-[#94A3B8] mb-4">
            Decomposition of +1970ms Latency Spike on Mission MIS-SCAN-1099.
          </p>
          <div className="space-y-3 font-mono text-xs">
            {rootCauseAttributions.map((att, idx) => (
              <div key={idx} className="p-3 rounded-lg bg-[#020617] border border-[#1E293B]">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-[#F8FAFC]">{att.node}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-cyan-400 font-bold">{att.share}</span>
                    {att.isRoot && (
                      <Badge variant="error" size="sm">
                        ROOT CAUSE
                      </Badge>
                    )}
                  </div>
                </div>
                <p className="text-[11px] text-[#94A3B8] mt-1">{att.explanation}</p>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};
