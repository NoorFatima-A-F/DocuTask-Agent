import React, { useState } from 'react';
import { useWorkspace } from '../context/WorkspaceContext';
import { CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const HumanFeedbackPanel: React.FC = () => {
  const {
    feedbackItems,
    convertFeedbackToMemory,
    convertFeedbackToBenchmark,
    convertFeedbackToRule,
    addFeedbackItem,
  } = useWorkspace();

  const [newDocId, setNewDocId] = useState('INVOICE_SCAN_Q3_09.pdf');
  const [newField, setNewField] = useState('VendorIBAN');
  const [extractedVal, setExtractedVal] = useState('DE89370400440532013000');
  const [correctedVal, setCorrectedVal] = useState('DE89370400440532013088');

  const handleManualFeedback = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newField || !correctedVal) return;
    addFeedbackItem({
      documentId: newDocId,
      fieldName: newField,
      extractedValue: extractedVal,
      correctedValue: correctedVal,
      confidenceWas: 0.78,
    });
  };

  return (
    <div className="w-full flex flex-col h-[700px] rounded-2xl bg-[#0F172A]/90 border border-[#1E293B] shadow-2xl overflow-hidden">
      <CardHeader className="flex flex-row items-center justify-between py-4 px-6 border-b border-[#1E293B] bg-[#131D35]/50">
        <div>
          <div className="flex items-center gap-2">
            <Badge variant="intelligence" size="sm">
              HUMAN + AI FEEDBACK LOOP
            </Badge>
            <span className="text-xs text-[#94A3B8] font-mono">
              Active Knowledge Distillation
            </span>
          </div>
          <CardTitle className="mt-1 text-base font-bold text-[#F8FAFC]">
            Interactive Correction & Ground Truth Learning
          </CardTitle>
        </div>

        <div className="text-xs font-mono text-[#10B981] bg-[#0A0F1D] px-3 py-1.5 rounded-lg border border-emerald-500/30">
          Reinforcement Rate: 100%
        </div>
      </CardHeader>

      <CardContent className="flex-1 overflow-y-auto p-6 space-y-6">
        {/* Quick Correction Input Tool */}
        <form
          onSubmit={handleManualFeedback}
          className="p-5 rounded-xl bg-[#131D35] border border-cyan-500/30 space-y-4"
        >
          <span className="text-xs font-bold text-[#00D2FF] uppercase tracking-wider block font-mono">
            + Flag Field for Autonomous Learning:
          </span>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
            <div>
              <label className="text-[10px] text-[#64748B] uppercase font-mono block mb-1">
                Document Name
              </label>
              <input
                type="text"
                value={newDocId}
                onChange={(e) => setNewDocId(e.target.value)}
                className="w-full bg-[#0A0F1D] border border-[#334155] rounded-lg px-3 py-2 text-xs font-mono text-[#F8FAFC]"
              />
            </div>
            <div>
              <label className="text-[10px] text-[#64748B] uppercase font-mono block mb-1">
                Target Field
              </label>
              <input
                type="text"
                value={newField}
                onChange={(e) => setNewField(e.target.value)}
                className="w-full bg-[#0A0F1D] border border-[#334155] rounded-lg px-3 py-2 text-xs font-mono text-[#F8FAFC]"
              />
            </div>
            <div>
              <label className="text-[10px] text-[#64748B] uppercase font-mono block mb-1">
                Extracted Value
              </label>
              <input
                type="text"
                value={extractedVal}
                onChange={(e) => setExtractedVal(e.target.value)}
                className="w-full bg-[#0A0F1D] border border-red-500/30 text-red-300 rounded-lg px-3 py-2 text-xs font-mono"
              />
            </div>
            <div>
              <label className="text-[10px] text-[#64748B] uppercase font-mono block mb-1">
                Human Corrected Value
              </label>
              <input
                type="text"
                value={correctedVal}
                onChange={(e) => setCorrectedVal(e.target.value)}
                className="w-full bg-[#0A0F1D] border border-emerald-500/40 text-emerald-300 rounded-lg px-3 py-2 text-xs font-mono"
              />
            </div>
          </div>

          <div className="flex justify-end">
            <Button type="submit" variant="intelligence" size="sm">
              Submit Correction for Distillation ➔
            </Button>
          </div>
        </form>

        {/* Existing Feedback Items */}
        <div className="space-y-4">
          <span className="text-xs font-bold text-[#64748B] uppercase tracking-wider block font-mono">
            Pending & Applied Human Feedback Ledger:
          </span>

          {feedbackItems.map((fb) => (
            <div
              key={fb.id}
              className="p-5 rounded-xl bg-[#131D35] border border-[#1E293B] space-y-4"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#1E293B] pb-3">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold font-mono text-[#F8FAFC]">
                    {fb.documentId}
                  </span>
                  <Badge variant="default" size="sm" className="font-mono">
                    {fb.fieldName}
                  </Badge>
                </div>

                <div className="flex items-center gap-2 text-xs font-mono text-[#64748B]">
                  <span>Prior Conf: {(fb.confidenceWas * 100).toFixed(0)}%</span>
                  <span>• {fb.submittedAtUtc} UTC</span>
                </div>
              </div>

              {/* Extraction vs Correction comparison */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
                <div className="p-3 rounded-lg bg-red-950/20 border border-red-500/30">
                  <span className="text-[#64748B] block text-[10px] uppercase">AI Extracted:</span>
                  <span className="text-red-400 font-bold mt-0.5 block">{fb.extractedValue}</span>
                </div>
                <div className="p-3 rounded-lg bg-emerald-950/20 border border-emerald-500/30">
                  <span className="text-[#64748B] block text-[10px] uppercase">
                    Human Correction:
                  </span>
                  <span className="text-emerald-400 font-bold mt-0.5 block">
                    {fb.correctedValue}
                  </span>
                </div>
              </div>

              {/* Distillation Action Buttons */}
              {fb.status === 'PENDING_REVIEW' ? (
                <div className="p-4 rounded-xl bg-[#0A0F1D] border border-cyan-500/30 space-y-3">
                  <span className="text-xs font-semibold text-[#00D2FF]">
                    How should the autonomous employee distill this correction?
                  </span>
                  <div className="flex flex-wrap gap-2">
                    <Button
                      variant="intelligence"
                      size="sm"
                      onClick={() => convertFeedbackToMemory(fb.id)}
                    >
                      🧠 Store as Long-Term Memory (R=0.98)
                    </Button>
                    <Button
                      variant="secondary"
                      size="sm"
                      onClick={() => convertFeedbackToBenchmark(fb.id)}
                    >
                      📊 Add to Gold Benchmark Suite
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => convertFeedbackToRule(fb.id)}
                    >
                      🔒 Lock as Governance Policy Rule
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="p-3 rounded-lg bg-[#0A0F1D] border border-emerald-500/30 flex items-center justify-between text-xs font-mono">
                  <span className="text-[#10B981]">✓ {fb.appliedLessonSummary}</span>
                  <Badge variant="success" size="sm">
                    {fb.status}
                  </Badge>
                </div>
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </div>
  );
};
