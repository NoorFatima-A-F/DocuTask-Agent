import React, { useState } from 'react';
import { useMissionControl } from '../../context/MissionControlContext';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';
import type { CognitionStageDetails } from '../../types/missionControl';

export const LiveCognitionLoop: React.FC = () => {
  const { state } = useMissionControl();
  const { cognitionLoop, currentCognitionStage } = state;
  const [selectedStage, setSelectedStage] = useState<CognitionStageDetails | null>(
    cognitionLoop.find((s) => s.stage === currentCognitionStage) || cognitionLoop[0] || null
  );

  return (
    <section className="w-full mt-8">
      <Card variant="glassmorphic" className="border-[#00D2FF]/20 shadow-[0_0_35px_rgba(0,102,255,0.15)]">
        <CardHeader className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2">
          <div>
            <div className="flex items-center gap-2">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[#00D2FF]" />
              </span>
              <Badge variant="intelligence" size="sm">
                LIVE COGNITION LOOP
              </Badge>
              <span className="text-xs text-[#00D2FF] font-mono animate-pulse">
                Active Phase: {currentCognitionStage}
              </span>
            </div>

            <CardTitle className="mt-2 text-xl lg:text-2xl font-bold text-[#F8FAFC]">
              Autonomous Cognition & Continuous Improvement Engine
            </CardTitle>
            <p className="mt-1 text-xs text-[#94A3B8]">
              The autonomous employee continuously perceives goals, plans actions, observes evidence, reflects on errors, learns invariants, and updates memory until statistical targets are satisfied.
            </p>
          </div>

          <div className="flex items-center gap-2 bg-[#0A0F1D]/80 px-3.5 py-2 rounded-xl border border-cyan-500/30 text-xs font-mono">
            <span className="text-[#94A3B8]">Loop Status:</span>
            <span className="text-[#00D2FF] font-semibold">Active Deliberation</span>
          </div>
        </CardHeader>

        <CardContent className="p-6">
          {/* Horizontal Step Stepper */}
          <div className="relative flex items-center justify-between overflow-x-auto py-6 px-2 gap-2">
            {cognitionLoop.map((stage, index) => {
              const isCurrent = stage.stage === currentCognitionStage;
              const isCompleted = stage.status === 'COMPLETED';
              const isSelected = selectedStage?.stage === stage.stage;

              return (
                <div key={stage.stage} className="flex items-center flex-1 min-w-[100px] shrink-0">
                  <div
                    onClick={() => setSelectedStage(stage)}
                    className={`relative flex flex-col items-center justify-center p-3 rounded-xl cursor-pointer transition-all duration-300 w-full text-center group ${
                      isSelected
                        ? 'bg-[#1E293B] ring-2 ring-[#00D2FF] shadow-[0_0_15px_rgba(0,210,255,0.3)]'
                        : isCurrent
                        ? 'bg-[#131D35] border border-cyan-400/60 shadow-[0_0_20px_rgba(0,210,255,0.35)] animate-pulse'
                        : isCompleted
                        ? 'bg-[#131D35]/60 border border-emerald-500/30 hover:bg-[#1E293B]/60'
                        : 'bg-[#0A0F1D]/40 border border-[#1E293B]/40 opacity-50 hover:opacity-80'
                    }`}
                  >
                    {/* Circle Indicator */}
                    <div
                      className={`h-7 w-7 rounded-full flex items-center justify-center text-xs font-bold font-mono transition-all ${
                        isCurrent
                          ? 'bg-gradient-to-tr from-[#0066FF] to-[#00D2FF] text-white shadow-[0_0_12px_rgba(0,210,255,0.8)] scale-110'
                          : isCompleted
                          ? 'bg-emerald-500 text-slate-900'
                          : 'bg-[#1E293B] text-[#64748B]'
                      }`}
                    >
                      {isCompleted ? '✓' : index + 1}
                    </div>

                    <span
                      className={`mt-2 text-[11px] font-bold tracking-tight block truncate w-full ${
                        isCurrent
                          ? 'text-[#00D2FF]'
                          : isCompleted
                          ? 'text-[#F8FAFC]'
                          : 'text-[#64748B]'
                      }`}
                    >
                      {stage.label}
                    </span>

                    <span className="text-[10px] font-mono text-[#64748B] block mt-0.5">
                      {stage.status}
                    </span>
                  </div>

                  {index < cognitionLoop.length - 1 && (
                    <div
                      className={`h-0.5 w-4 shrink-0 mx-1 transition-colors ${
                        isCompleted
                          ? 'bg-emerald-500/60'
                          : isCurrent
                          ? 'bg-[#00D2FF]/60'
                          : 'bg-[#1E293B]'
                      }`}
                    />
                  )}
                </div>
              );
            })}
          </div>

          {/* Selected Stage Detail Drawer / Card */}
          {selectedStage && (
            <div className="mt-4 p-5 rounded-xl bg-[#131D35]/80 border border-[#334155] backdrop-blur-md">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#1E293B] pb-3">
                <div className="flex items-center gap-3">
                  <Badge
                    variant={
                      selectedStage.status === 'COMPLETED'
                        ? 'success'
                        : selectedStage.status === 'ACTIVE'
                        ? 'intelligence'
                        : 'default'
                    }
                    size="md"
                    hasDot
                  >
                    {selectedStage.stage}
                  </Badge>
                  <h4 className="text-sm font-bold text-[#F8FAFC]">
                    {selectedStage.label}
                  </h4>
                </div>

                <div className="flex items-center gap-4 text-xs font-mono text-[#94A3B8]">
                  {selectedStage.startedAtUtc && (
                    <span>Started: {selectedStage.startedAtUtc} UTC</span>
                  )}
                  {selectedStage.durationMs && (
                    <span>Duration: {(selectedStage.durationMs / 1000).toFixed(1)}s</span>
                  )}
                  {selectedStage.confidenceScore !== undefined && (
                    <span className="text-[#00D2FF] font-bold">
                      Confidence: {(selectedStage.confidenceScore * 100).toFixed(1)}%
                    </span>
                  )}
                </div>
              </div>

              <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="md:col-span-2 space-y-2">
                  <span className="text-[11px] font-semibold text-[#64748B] uppercase tracking-wider block">
                    Cognitive Phase Summary
                  </span>
                  <p className="text-xs text-[#F8FAFC] leading-relaxed">
                    {selectedStage.summary}
                  </p>
                </div>

                <div className="space-y-2">
                  <span className="text-[11px] font-semibold text-[#64748B] uppercase tracking-wider block">
                    Artifacts Produced ({selectedStage.artifactsProduced.length})
                  </span>
                  {selectedStage.artifactsProduced.length > 0 ? (
                    <div className="flex flex-wrap gap-1.5">
                      {selectedStage.artifactsProduced.map((art) => (
                        <span
                          key={art}
                          className="text-[11px] font-mono bg-[#0A0F1D] text-cyan-300 px-2 py-1 rounded border border-cyan-500/30"
                        >
                          📄 {art}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <span className="text-xs text-[#64748B] italic">No artifacts produced yet</span>
                  )}
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </section>
  );
};
