import React, { useState } from 'react';
import { useMissionControl } from '../../context/MissionControlContext';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';

export const DecisionCenterSection: React.FC = () => {
  const { state, approveDecision, rejectDecision, overrideDecision } = useMissionControl();
  const { decisions } = state;
  const [expandedDecisionId, setExpandedDecisionId] = useState<string>(decisions[0]?.id || '');
  const [overrideInput, setOverrideInput] = useState<string>('');
  const [isOverriding, setIsOverriding] = useState<boolean>(false);

  return (
    <section className="w-full mt-8">
      <Card variant="default" className="border-[#1E293B] bg-[#0F172A]/80 backdrop-blur-md">
        <CardHeader className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="intelligence" size="sm">
                STAGE 6 • EXPLAINABILITY
              </Badge>
              <span className="text-xs text-[#94A3B8] font-mono">
                {decisions.length} Autonomous Decisions Audited
              </span>
            </div>
            <CardTitle className="mt-2 text-lg lg:text-xl font-bold text-[#F8FAFC]">
              Explainable Decision Center
            </CardTitle>
            <p className="mt-1 text-xs text-[#94A3B8]">
              No black boxes. Every autonomous decision surfaces its empirical rationale, rejected alternatives, 9-dimension risk vectors, and human override controls.
            </p>
          </div>
        </CardHeader>

        <CardContent className="p-6 space-y-4">
          {decisions.map((dec) => {
            const isExpanded = expandedDecisionId === dec.id;

            return (
              <div
                key={dec.id}
                className="rounded-xl bg-[#131D35] border border-[#1E293B] overflow-hidden transition-all duration-200"
              >
                {/* Decision Bar Summary */}
                <div
                  onClick={() => setExpandedDecisionId(isExpanded ? '' : dec.id)}
                  className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 cursor-pointer hover:bg-[#1E293B]/40 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-xs font-mono font-bold text-[#00D2FF]">
                      [{dec.timestampUtc}]
                    </span>
                    <div>
                      <h4 className="text-sm font-semibold text-[#F8FAFC]">
                        {dec.decisionTitle}
                      </h4>
                      <span className="text-xs font-mono text-[#38BDF8] block mt-0.5">
                        Action: {dec.selectedAction}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 shrink-0">
                    <div className="text-right font-mono text-xs">
                      <span className="text-[#10B981] font-bold">
                        {(dec.confidenceScore * 100).toFixed(1)}%
                      </span>
                      <span className="text-[#64748B] block text-[10px]">
                        {dec.evidenceCount} observations
                      </span>
                    </div>

                    {dec.isHumanOverridden && (
                      <Badge variant="warning" size="sm">
                        OVERRIDDEN
                      </Badge>
                    )}

                    <Button variant="ghost" size="sm" className="text-xs">
                      {isExpanded ? '▲ Hide Explainability' : '▼ Deep Rationale'}
                    </Button>
                  </div>
                </div>

                {/* Expanded Deep Explainability Accordion */}
                {isExpanded && (
                  <div className="p-5 border-t border-[#1E293B] bg-[#0A0F1D]/60 space-y-5">
                    {/* 1. Why? (Reasoning) */}
                    <div>
                      <span className="text-[11px] font-bold uppercase tracking-wider text-[#00D2FF] block">
                        1. Empirical Rationale (Why this action?)
                      </span>
                      <p className="mt-1 text-xs text-[#F8FAFC] leading-relaxed">
                        {dec.reasoning}
                      </p>
                    </div>

                    {/* 2. Rejected Alternatives */}
                    <div>
                      <span className="text-[11px] font-bold uppercase tracking-wider text-[#F59E0B] block">
                        2. Alternatives Evaluated & Rejected
                      </span>
                      <div className="mt-2 grid grid-cols-1 md:grid-cols-2 gap-3">
                        {dec.alternativesConsidered.map((alt) => (
                          <div
                            key={alt.actionName}
                            className="p-3 rounded-lg bg-[#131D35] border border-red-500/20 text-xs"
                          >
                            <div className="flex items-center justify-between font-mono">
                              <span className="font-semibold text-red-400">✗ {alt.actionName}</span>
                              <span className="text-[#64748B]">
                                Score: {(alt.score * 100).toFixed(0)}%
                              </span>
                            </div>
                            <p className="mt-1 text-[11px] text-[#94A3B8]">
                              <strong className="text-[#64748B]">Rejected because:</strong>{' '}
                              {alt.rejectedReason}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* 3. Tradeoffs & Expected Outcome */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                      <div className="p-3 rounded-lg bg-[#131D35] border border-[#1E293B]">
                        <span className="text-[11px] font-bold text-[#94A3B8] uppercase block">
                          Identified Tradeoffs
                        </span>
                        <p className="mt-1 text-xs text-[#F8FAFC]">{dec.tradeoffs}</p>
                      </div>
                      <div className="p-3 rounded-lg bg-[#131D35] border border-[#1E293B]">
                        <span className="text-[11px] font-bold text-[#10B981] uppercase block">
                          Expected Outcome
                        </span>
                        <p className="mt-1 text-xs text-[#F8FAFC]">{dec.expectedOutcome}</p>
                      </div>
                    </div>

                    {/* 4. 9-Dimension Risk Vectors */}
                    <div>
                      <span className="text-[11px] font-bold uppercase tracking-wider text-[#94A3B8] block">
                        4. 9-Dimension Risk Vector Evaluation
                      </span>
                      <div className="mt-2 flex flex-wrap gap-2">
                        {dec.riskVectors.map((r) => (
                          <div
                            key={r.dimension}
                            className="px-2.5 py-1 rounded bg-[#131D35] border border-[#334155] text-[11px] font-mono flex items-center gap-2"
                          >
                            <span className="text-[#94A3B8]">{r.dimension}:</span>
                            <span
                              className={
                                r.severity === 'LOW'
                                  ? 'text-[#10B981]'
                                  : r.severity === 'MEDIUM'
                                  ? 'text-[#F59E0B]'
                                  : 'text-[#EF4444]'
                              }
                            >
                              {(r.score * 100).toFixed(0)}% ({r.severity})
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* 5. Human-in-the-Loop Override / Approval Actions */}
                    <div className="pt-4 border-t border-[#1E293B] flex flex-wrap items-center justify-between gap-3">
                      <div className="flex items-center gap-2">
                        <Button
                          variant="intelligence"
                          size="sm"
                          onClick={() => approveDecision(dec.id)}
                        >
                          ✓ Confirm Decision
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => rejectDecision(dec.id, 'Operator manual rejection')}
                        >
                          ✗ Reject Action
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => setIsOverriding(!isOverriding)}
                        >
                          ⚙ Human Override
                        </Button>
                      </div>

                      <div className="text-[11px] font-mono text-[#64748B]">
                        Est. Cost: ${dec.estimatedCostUsd.toFixed(2)} • Benefit: ${dec.estimatedBenefitUsd.toFixed(0)} • Latency: {dec.estimatedRuntimeMs}ms
                      </div>
                    </div>

                    {/* Inline Override Form */}
                    {isOverriding && (
                      <div className="p-4 rounded-xl bg-[#0F172A] border border-cyan-500/40 mt-3 space-y-3">
                        <span className="text-xs font-semibold text-[#00D2FF]">
                          Override Autonomous Decision with Custom Action:
                        </span>
                        <input
                          type="text"
                          value={overrideInput}
                          onChange={(e) => setOverrideInput(e.target.value)}
                          placeholder="e.g. FORCE_HISTOGRAM_EQUALIZE"
                          className="w-full bg-[#131D35] border border-[#334155] rounded-lg px-3 py-2 text-xs font-mono text-[#F8FAFC] focus:outline-none focus:border-cyan-400"
                        />
                        <div className="flex justify-end gap-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => setIsOverriding(false)}
                          >
                            Cancel
                          </Button>
                          <Button
                            variant="intelligence"
                            size="sm"
                            onClick={() => {
                              if (overrideInput) {
                                overrideDecision(dec.id, overrideInput, 'Operator manual override');
                                setIsOverriding(false);
                              }
                            }}
                          >
                            Apply Override
                          </Button>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </CardContent>
      </Card>
    </section>
  );
};
