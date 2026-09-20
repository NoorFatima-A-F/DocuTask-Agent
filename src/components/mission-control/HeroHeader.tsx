import React from 'react';
import { useMissionControl } from '../../context/MissionControlContext';
import { Badge } from '../ui/Badge';
import { StatusIndicator } from '../ui/StatusIndicator';
import { Button } from '../ui/Button';

export const HeroHeader: React.FC = () => {
  const { state, toggleLiveSimulation } = useMissionControl();
  const { mission, confidenceData, isPaused } = state;

  const formatElapsed = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}m ${secs < 10 ? '0' : ''}${secs}s`;
  };

  return (
    <header className="relative w-full rounded-2xl bg-[#0F172A]/90 border border-[#1E293B] shadow-2xl p-6 lg:p-8 backdrop-blur-xl overflow-hidden">
      {/* Ambient Neural Glow Background */}
      <div className="absolute -top-24 -right-24 w-96 h-96 bg-gradient-to-br from-blue-600/15 to-cyan-400/10 rounded-full blur-3xl pointer-events-none" />

      {/* Top Banner */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 relative z-10">
        <div>
          <div className="flex items-center gap-3">
            <Badge variant="intelligence" size="md" hasDot isPulsing>
              AUTONOMOUS RUNTIME
            </Badge>
            <span className="text-xs font-mono text-[#94A3B8]">
              v2.5-enterprise • SLSA L3+
            </span>
          </div>

          <h1 className="mt-3 text-2xl lg:text-4xl font-extrabold text-[#F8FAFC] tracking-tight">
            DocuTask Agent
          </h1>
          <p className="mt-1 text-base lg:text-lg font-medium text-[#38BDF8]">
            An Autonomous AI Coworker for Enterprise Document Operations
          </p>
          <p className="mt-2 text-xs lg:text-sm text-[#94A3B8] max-w-3xl leading-relaxed">
            AI that understands document-processing goals, plans workflows, executes tools, validates
            results, learns from experience, and improves until statistical confidence targets are met.
          </p>
        </div>

        {/* Live Status & Quick Action Badge */}
        <div className="flex flex-col items-start lg:items-end gap-3 shrink-0">
          <div className="flex items-center gap-2 bg-[#131D35] px-3.5 py-2 rounded-xl border border-[#334155]/60 shadow-inner">
            <StatusIndicator
              status={isPaused ? 'waiting' : 'executing'}
              label={isPaused ? 'Mission Paused' : 'Autonomous Cognition Active'}
              sublabel={`Heartbeat: ${new Date().toISOString().substring(11, 19)} UTC`}
              showPulse={!isPaused}
            />
          </div>

          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleLiveSimulation}
              className="text-xs font-mono"
            >
              {state.isSimulatingLive ? '● Live Stream ON' : '○ Live Stream PAUSED'}
            </Button>
          </div>
        </div>
      </div>

      {/* Mission Key Telemetry Bar */}
      <div className="mt-8 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 pt-6 border-t border-[#1E293B]/80 relative z-10">
        {/* Mission ID & Type */}
        <div className="bg-[#131D35]/60 p-3 rounded-lg border border-[#1E293B]">
          <span className="text-[11px] font-medium text-[#64748B] block">Current Mission</span>
          <span className="text-xs font-bold font-mono text-[#F8FAFC] block truncate mt-0.5">
            {mission.missionId}
          </span>
          <span className="text-[10px] text-[#38BDF8] font-mono block mt-0.5">
            {mission.missionType}
          </span>
        </div>

        {/* Mission State */}
        <div className="bg-[#131D35]/60 p-3 rounded-lg border border-[#1E293B]">
          <span className="text-[11px] font-medium text-[#64748B] block">Mission State</span>
          <div className="mt-1">
            <Badge
              variant={
                mission.currentState === 'ACTIVE'
                  ? 'success'
                  : mission.currentState === 'PAUSED'
                  ? 'warning'
                  : 'default'
              }
              size="sm"
              hasDot
            >
              {mission.currentState}
            </Badge>
          </div>
        </div>

        {/* Elapsed Time */}
        <div className="bg-[#131D35]/60 p-3 rounded-lg border border-[#1E293B]">
          <span className="text-[11px] font-medium text-[#64748B] block">Elapsed Time</span>
          <span className="text-sm font-semibold font-mono text-[#F8FAFC] block mt-0.5">
            {formatElapsed(mission.elapsedSeconds)}
          </span>
          <span className="text-[10px] text-[#64748B] block">Started: {mission.startedAtUtc.substring(11, 19)}</span>
        </div>

        {/* Confidence Score */}
        <div className="bg-[#131D35]/60 p-3 rounded-lg border border-cyan-500/20">
          <span className="text-[11px] font-medium text-cyan-400 block">Statistical Confidence</span>
          <span className="text-sm font-bold font-mono text-[#00D2FF] block mt-0.5">
            {(confidenceData.currentConfidence * 100).toFixed(1)}%
          </span>
          <span className="text-[10px] text-[#64748B] font-mono block">
            Target: {(confidenceData.targetConfidence * 100).toFixed(0)}% (n={confidenceData.sampleSize})
          </span>
        </div>

        {/* Compute & Financial Budget */}
        <div className="bg-[#131D35]/60 p-3 rounded-lg border border-[#1E293B]">
          <span className="text-[11px] font-medium text-[#64748B] block">Budget Burn</span>
          <span className="text-xs font-semibold font-mono text-[#F8FAFC] block mt-0.5">
            ${mission.budgetConsumedUsd.toFixed(2)} / ${mission.budgetAllocatedUsd.toFixed(2)}
          </span>
          <span className="text-[10px] text-[#64748B] font-mono block">
            {mission.hardwareHoursUsed.toFixed(2)} hrs hardware
          </span>
        </div>

        {/* Cryptographic Proof SHA-256 */}
        <div className="bg-[#131D35]/60 p-3 rounded-lg border border-[#1E293B]">
          <span className="text-[11px] font-medium text-[#64748B] block">Canonical Digest</span>
          <span
            className="text-[11px] font-mono text-[#A855F7] block truncate mt-0.5 cursor-pointer hover:underline"
            title={mission.canonicalDigestSha256}
          >
            {mission.canonicalDigestSha256.substring(0, 12)}...
          </span>
          <span className="text-[10px] text-[#10B981] font-mono block">✓ SHA-256 Verified</span>
        </div>
      </div>
    </header>
  );
};
