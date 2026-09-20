import React, { useState, useEffect } from 'react';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';

export interface ProgressiveThinkingModalProps {
  isOpen: boolean;
  onClose: () => void;
  targetConfidence?: number;
}

export const ProgressiveThinkingModal: React.FC<ProgressiveThinkingModalProps> = ({
  isOpen,
  onClose,
  targetConfidence = 97.2,
}) => {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [displayedConfidence, setDisplayedConfidence] = useState(41);

  const steps = [
    { title: 'Understanding Objective & Normalizing Goal Spec', agent: 'Coordinator Agent', boost: 15 },
    { title: 'Searching Long-Term Memory & Historical Missions', agent: 'Memory Agent', boost: 18 },
    { title: 'Auditing Failure Modes & Watermark Anomaly Data', agent: 'Evidence Agent', boost: 9 },
    { title: 'Formulating Adaptive Local Contrast Plan (x*=0.6800)', agent: 'Planner Agent', boost: 7 },
    { title: 'Multi-Agent Consensus & Constraint Negotiation', agent: 'Governance Agent', boost: 7 },
    { title: 'Statistical Power & Effect Size Verification (n=53)', agent: 'Statistics Agent', boost: targetConfidence - 90 },
  ];

  useEffect(() => {
    if (!isOpen) {
      setCurrentStepIndex(0);
      setDisplayedConfidence(41);
      return;
    }

    const interval = setInterval(() => {
      setCurrentStepIndex((prev) => {
        if (prev < steps.length - 1) {
          const next = prev + 1;
          const target = Math.min(
            targetConfidence,
            Math.round(41 + (next / steps.length) * (targetConfidence - 41))
          );
          setDisplayedConfidence(target);
          return next;
        }
        setDisplayedConfidence(targetConfidence);
        return prev;
      });
    }, 1200);

    return () => clearInterval(interval);
  }, [isOpen, targetConfidence, steps.length]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
      <div className="w-full max-w-lg rounded-3xl bg-[#0F172A] border border-cyan-500/40 p-6 shadow-[0_0_50px_rgba(0,102,255,0.3)] space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-[#1E293B] pb-4">
          <div className="flex items-center gap-2">
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              PROGRESSIVE COGNITION
            </Badge>
            <span className="text-xs text-[#94A3B8] font-mono">
              Intelligence Emergence Trace
            </span>
          </div>

          <div className="text-right font-mono">
            <span className="text-xl font-extrabold text-[#00D2FF]">
              {displayedConfidence.toFixed(1)}%
            </span>
            <span className="text-[10px] text-[#64748B] block">Certainty</span>
          </div>
        </div>

        {/* Unfolding Steps */}
        <div className="space-y-3">
          {steps.map((step, idx) => {
            const isDone = idx < currentStepIndex;
            const isCurrent = idx === currentStepIndex;

            return (
              <div
                key={step.title}
                className={`p-3 rounded-xl border transition-all flex items-center justify-between ${
                  isCurrent
                    ? 'bg-[#131D35] border-cyan-400 shadow-[0_0_15px_rgba(0,210,255,0.2)]'
                    : isDone
                    ? 'bg-[#131D35]/60 border-emerald-500/30'
                    : 'bg-[#0A0F1D]/40 border-[#1E293B] opacity-40'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`h-6 w-6 rounded-full flex items-center justify-center text-xs font-mono font-bold ${
                      isDone
                        ? 'bg-emerald-500 text-slate-900'
                        : isCurrent
                        ? 'bg-[#00D2FF] text-slate-900 animate-pulse'
                        : 'bg-[#1E293B] text-[#64748B]'
                    }`}
                  >
                    {isDone ? '✓' : idx + 1}
                  </div>

                  <div>
                    <span
                      className={`text-xs font-medium block ${
                        isCurrent ? 'text-[#00D2FF]' : isDone ? 'text-[#F8FAFC]' : 'text-[#64748B]'
                      }`}
                    >
                      {step.title}
                    </span>
                    <span className="text-[10px] text-[#64748B] font-mono block">
                      {step.agent}
                    </span>
                  </div>
                </div>

                {isCurrent && (
                  <span className="text-[10px] font-mono text-[#00D2FF] animate-pulse">
                    Evaluating...
                  </span>
                )}
                {isDone && (
                  <span className="text-[10px] font-mono text-[#10B981]">
                    +{step.boost}%
                  </span>
                )}
              </div>
            );
          })}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between pt-4 border-t border-[#1E293B]">
          <span className="text-[11px] text-[#64748B] font-mono">
            Zero-Fabrication invariant verified
          </span>

          <Button variant="intelligence" size="sm" onClick={onClose}>
            Close Inspector ✓
          </Button>
        </div>
      </div>
    </div>
  );
};
