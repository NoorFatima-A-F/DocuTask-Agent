import React, { useState } from 'react';
import { useMissionControl } from '../../context/MissionControlContext';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';

export const GoalIntelligenceSection: React.FC = () => {
  const { state } = useMissionControl();
  const { goalIntelligence } = state;

  const [activeTab, setActiveTab] = useState<
    'understanding' | 'reasoning' | 'negotiation' | 'utility' | 'compilation'
  >('understanding');

  const tabs: {
    id: 'understanding' | 'reasoning' | 'negotiation' | 'utility' | 'compilation';
    label: string;
    status: 'COMPLETED' | 'ACTIVE' | 'PENDING';
  }[] = [
    { id: 'understanding', label: '1. Goal Understanding', status: goalIntelligence.phaseStatus.understanding },
    { id: 'reasoning', label: '2. Scientific Reasoning', status: goalIntelligence.phaseStatus.reasoning },
    { id: 'negotiation', label: '3. Multi-Agent Negotiation', status: goalIntelligence.phaseStatus.negotiation },
    { id: 'utility', label: '4. Utility & Risk Analysis', status: goalIntelligence.phaseStatus.utilityAnalysis },
    { id: 'compilation', label: '5. Mission Compilation', status: goalIntelligence.phaseStatus.compilation },
  ];

  return (
    <section className="w-full mt-8">
      <Card variant="default" className="border-[#1E293B] bg-[#0F172A]/80 backdrop-blur-md">
        <CardHeader className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="intelligence" size="sm">
                STAGE 1 • GOAL INTELLIGENCE
              </Badge>
              <span className="text-xs text-[#94A3B8] font-mono">ID: {goalIntelligence.goalId}</span>
            </div>
            <CardTitle className="mt-2 text-lg lg:text-xl font-bold text-[#F8FAFC]">
              Goal Deconstruction & Autonomous Negotiation
            </CardTitle>
            <p className="mt-1 text-xs text-[#94A3B8] max-w-2xl">
              Raw user intent is decomposed, audited for constraints, deliberated across 10 specialized agents, and compiled into an executable DAG with zero fabrication.
            </p>
          </div>

          <div className="flex items-center gap-2 bg-[#131D35] px-3 py-1.5 rounded-lg border border-[#334155]/60 text-xs font-mono">
            <span className="text-[#94A3B8]">Consensus:</span>
            <span className="text-[#10B981] font-bold">
              {(goalIntelligence.negotiation.consensusScore * 100).toFixed(0)}%
            </span>
          </div>
        </CardHeader>

        {/* Tab Navigation */}
        <div className="flex items-center overflow-x-auto border-b border-[#1E293B] px-5 gap-2 bg-[#0A0F1D]/40">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-3 px-3.5 text-xs font-medium border-b-2 transition-all flex items-center gap-2 whitespace-nowrap ${
                activeTab === tab.id
                  ? 'border-[#00D2FF] text-[#00D2FF] bg-[#131D35]/50'
                  : 'border-transparent text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-[#1E293B]/20'
              }`}
            >
              <span>{tab.label}</span>
              <span className="text-[10px] text-[#10B981] font-mono">✓</span>
            </button>
          ))}
        </div>

        <CardContent className="p-6">
          {/* TAB 1: UNDERSTANDING */}
          {activeTab === 'understanding' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="bg-[#131D35] p-4 rounded-xl border border-[#1E293B]">
                  <h4 className="text-xs font-semibold text-[#00D2FF] uppercase tracking-wider">
                    Core Objective Intent
                  </h4>
                  <p className="mt-1.5 text-xs text-[#F8FAFC] leading-relaxed">
                    {goalIntelligence.understanding.intent}
                  </p>
                </div>

                <div className="bg-[#131D35] p-4 rounded-xl border border-[#1E293B]">
                  <h4 className="text-xs font-semibold text-[#94A3B8] uppercase tracking-wider">
                    Extracted Target Entities
                  </h4>
                  <div className="mt-2 space-y-1.5">
                    {Object.entries(goalIntelligence.understanding.extractedEntities).map(
                      ([key, val]) => (
                        <div key={key} className="flex items-baseline justify-between text-xs font-mono">
                          <span className="text-[#94A3B8]">{key}:</span>
                          <span className="text-[#F8FAFC] font-medium">{val}</span>
                        </div>
                      )
                    )}
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <div className="bg-[#131D35] p-4 rounded-xl border border-[#1E293B]">
                  <h4 className="text-xs font-semibold text-[#F59E0B] uppercase tracking-wider">
                    Execution Constraints & Sentinels
                  </h4>
                  <ul className="mt-2 space-y-1 text-xs text-[#94A3B8]">
                    {goalIntelligence.understanding.constraints.map((c, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-[#00D2FF]">•</span>
                        <span>{c}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="bg-[#131D35] p-4 rounded-xl border border-[#1E293B]">
                  <h4 className="text-xs font-semibold text-[#94A3B8] uppercase tracking-wider">
                    Required Subsystem Capabilities
                  </h4>
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {goalIntelligence.understanding.requiredCapabilities.map((cap) => (
                      <Badge key={cap} variant="default" size="sm" className="font-mono text-[10px]">
                        {cap}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: REASONING */}
          {activeTab === 'reasoning' && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-[#131D35] p-4 rounded-xl border border-[#1E293B]">
                <h4 className="text-xs font-semibold text-[#38BDF8] uppercase tracking-wider">
                  Derived Requirements
                </h4>
                <ul className="mt-2 space-y-1.5 text-xs text-[#94A3B8]">
                  {goalIntelligence.reasoning.derivedRequirements.map((r, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="text-[#10B981]">✓</span>
                      <span>{r}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="bg-[#131D35] p-4 rounded-xl border border-[#1E293B]">
                <h4 className="text-xs font-semibold text-[#A855F7] uppercase tracking-wider">
                  Required Datasets & Benchmarks
                </h4>
                <div className="mt-2 space-y-2">
                  <div>
                    <span className="text-[10px] text-[#64748B] uppercase">Datasets:</span>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {goalIntelligence.reasoning.requiredDatasets.map((d) => (
                        <span key={d} className="text-[10px] font-mono bg-[#0A0F1D] text-purple-300 px-2 py-0.5 rounded border border-purple-500/30">
                          {d}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <span className="text-[10px] text-[#64748B] uppercase">Benchmarks:</span>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {goalIntelligence.reasoning.requiredBenchmarks.map((b) => (
                        <span key={b} className="text-[10px] font-mono bg-[#0A0F1D] text-cyan-300 px-2 py-0.5 rounded border border-cyan-500/30">
                          {b}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-[#131D35] p-4 rounded-xl border border-[#1E293B]">
                <h4 className="text-xs font-semibold text-[#10B981] uppercase tracking-wider">
                  Ground Truth & Standards
                </h4>
                <p className="mt-2 text-xs text-[#94A3B8] leading-relaxed">
                  {goalIntelligence.reasoning.groundTruthAvailability}
                </p>
                <div className="mt-3 flex flex-wrap gap-1">
                  {goalIntelligence.reasoning.publicationStandards.map((std) => (
                    <span key={std} className="text-[10px] font-mono bg-emerald-950/40 text-emerald-300 px-2 py-0.5 rounded border border-emerald-500/30">
                      {std}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: NEGOTIATION */}
          {activeTab === 'negotiation' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between bg-[#131D35] p-3 rounded-lg border border-[#1E293B]">
                <span className="text-xs font-semibold text-[#F8FAFC]">
                  Inter-Agent Consensus Ledger (4 Agents Deliberating)
                </span>
                <span className="text-xs font-mono text-[#10B981]">
                  Status: Consensus Achieved (100% Alignment)
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {goalIntelligence.negotiation.participants.map((p) => (
                  <div key={p.agentRole} className="bg-[#131D35] p-4 rounded-xl border border-[#1E293B] flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between">
                        <Badge variant="intelligence" size="sm">
                          {p.agentRole}
                        </Badge>
                        <Badge variant="success" size="sm">
                          {p.stance}
                        </Badge>
                      </div>
                      <p className="mt-2 text-xs text-[#94A3B8] leading-relaxed">
                        "{p.rationale}"
                      </p>
                    </div>
                    <div className="mt-3 pt-2 border-t border-[#1E293B] flex items-center justify-between text-[11px] font-mono text-[#64748B]">
                      <span>Confidence: {(p.confidence * 100).toFixed(0)}%</span>
                      <span>{p.timestampUtc.substring(11, 19)} UTC</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 4: UTILITY & RISK */}
          {activeTab === 'utility' && (
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="bg-[#131D35] p-4 rounded-xl border border-[#1E293B] text-center">
                <span className="text-[11px] text-[#94A3B8] block">Expected Benefit</span>
                <span className="text-xl font-bold font-mono text-[#10B981] mt-1 block">
                  {(goalIntelligence.utility.expectedBenefit * 100).toFixed(0)}%
                </span>
              </div>
              <div className="bg-[#131D35] p-4 rounded-xl border border-[#1E293B] text-center">
                <span className="text-[11px] text-[#94A3B8] block">Success Probability</span>
                <span className="text-xl font-bold font-mono text-[#00D2FF] mt-1 block">
                  {(goalIntelligence.utility.probabilityOfSuccess * 100).toFixed(0)}%
                </span>
              </div>
              <div className="bg-[#131D35] p-4 rounded-xl border border-[#1E293B] text-center">
                <span className="text-[11px] text-[#94A3B8] block">Estimated Cost</span>
                <span className="text-xl font-bold font-mono text-[#F59E0B] mt-1 block">
                  ${goalIntelligence.utility.estimatedCostUsd.toFixed(2)}
                </span>
              </div>
              <div className="bg-[#131D35] p-4 rounded-xl border border-[#1E293B] text-center">
                <span className="text-[11px] text-[#94A3B8] block">Risk Score</span>
                <span className="text-xl font-bold font-mono text-[#34D399] mt-1 block">
                  {(goalIntelligence.utility.riskScore * 100).toFixed(1)}% (Low)
                </span>
              </div>
            </div>
          )}

          {/* TAB 5: COMPILATION */}
          {activeTab === 'compilation' && (
            <div className="bg-[#131D35] p-5 rounded-xl border border-[#1E293B] flex flex-col md:flex-row items-center justify-between gap-6">
              <div>
                <h4 className="text-sm font-semibold text-[#F8FAFC]">
                  Compiled 6-Node Mission Execution DAG
                </h4>
                <p className="mt-1 text-xs text-[#94A3B8] max-w-xl leading-relaxed">
                  Mission graph generated with 3 milestones, automatic retry budgets, and strict statistical stopping condition (Power &ge; 0.80, Confidence &ge; 95%).
                </p>
              </div>

              <div className="flex items-center gap-6 shrink-0 font-mono text-xs">
                <div>
                  <span className="text-[#64748B] block">Nodes</span>
                  <span className="text-base font-bold text-[#00D2FF]">
                    {goalIntelligence.missionCompilation.generatedDagNodesCount}
                  </span>
                </div>
                <div>
                  <span className="text-[#64748B] block">Est. Runtime</span>
                  <span className="text-base font-bold text-[#F8FAFC]">
                    {goalIntelligence.missionCompilation.estimatedRuntimeMinutes}m
                  </span>
                </div>
                <div>
                  <span className="text-[#64748B] block">Stop Threshold</span>
                  <span className="text-base font-bold text-[#10B981]">
                    {(goalIntelligence.missionCompilation.stoppingThresholdConfidence * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </section>
  );
};
