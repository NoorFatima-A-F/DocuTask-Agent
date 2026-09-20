import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { WorkspaceProvider } from '../../src/workspace/context/WorkspaceContext';
import { MissionControlProvider } from '../../src/context/MissionControlContext';
import { TrustIndicator } from '../../src/components/ui/TrustIndicator';
import { Confetti } from '../../src/components/ui/Confetti';
import { AgentPresenceBadge } from '../../src/components/presence/AgentPresenceBadge';
import { ProgressiveThinkingModal } from '../../src/components/presence/ProgressiveThinkingModal';
import { MissionStoryPanel } from '../../src/workspace/story/MissionStoryPanel';
import { ConfidenceJourneyPanel } from '../../src/workspace/confidence/ConfidenceJourneyPanel';
import { CinematicReplayMovie } from '../../src/workspace/replay/CinematicReplayMovie';
import { CommandPalette } from '../../src/components/ui/CommandPalette';
import { EnterpriseFooter } from '../../src/components/ui/EnterpriseFooter';

describe('DocuTask Agent — AI Coworker Polish & Experience Suite', () => {
  it('renders TrustIndicators with verified empirical status', () => {
    render(<TrustIndicator state="VERIFIED" />);
    expect(screen.getByText('Cryptographically Verified')).toBeDefined();

    render(<TrustIndicator state="EMPIRICAL" />);
    expect(screen.getByText('Empirical Observation')).toBeDefined();

    render(<TrustIndicator state="UNKNOWN" />);
    expect(screen.getByText('Zero-Fabrication Unknown')).toBeDefined();
  });

  it('renders AgentPresenceBadge with live avatar and personality blurb', () => {
    render(
      <AgentPresenceBadge
        role="PLANNER"
        name="Planner Agent"
        status="EXECUTING"
        currentThought="Formulating adaptive DAG"
        confidence={0.96}
      />
    );

    expect(screen.getByText('Planner Agent')).toBeDefined();
    expect(screen.getByText('"Formulating adaptive DAG"')).toBeDefined();
    expect(screen.getByText('96%')).toBeDefined();
  });

  it('renders ProgressiveThinkingModal and displays unfolding intelligence steps', () => {
    render(
      <ProgressiveThinkingModal
        isOpen={true}
        onClose={() => {}}
        targetConfidence={97.2}
      />
    );

    expect(screen.getByText(/PROGRESSIVE COGNITION/i)).toBeDefined();
    expect(screen.getByText(/Understanding Objective & Normalizing Goal Spec/i)).toBeDefined();
  });

  it('renders MissionStoryPanel documentary narrative mode', () => {
    render(<MissionStoryPanel />);

    expect(screen.getByText(/DOCUMENTARY STORYTELLING/i)).toBeDefined();
    expect(screen.getByText(/The Challenge: Degraded Thermal Receipts/i)).toBeDefined();
    expect(screen.getByText(/Memory Recall: Extracting Past Lessons/i)).toBeDefined();
    expect(screen.getByText(/Statistical Certification & Mission Success/i)).toBeDefined();
  });

  it('renders ConfidenceJourneyPanel with milestone delta leaps', () => {
    render(<ConfidenceJourneyPanel />);

    expect(screen.getByText(/CONFIDENCE TRAJECTORY/i)).toBeDefined();
    expect(screen.getByText(/The Confidence Journey \(41% ➔ 97.2%\)/i)).toBeDefined();
    expect(screen.getByText(/\(\+15%\)/i)).toBeDefined();
    expect(screen.getByText(/\(\+18%\)/i)).toBeDefined();
  });

  it('renders CinematicReplayMovie player with speed toggles and scene scrubbing', () => {
    render(
      <WorkspaceProvider>
        <CinematicReplayMovie />
      </WorkspaceProvider>
    );

    expect(screen.getByText(/Cinematic Mission Replay \(Movie Mode\)/i)).toBeDefined();
    expect(screen.getByText('2x')).toBeDefined();

    const speed4Btn = screen.getByText('4x');
    fireEvent.click(speed4Btn);

    const playBtn = screen.getByText('▶ Play Movie');
    fireEvent.click(playBtn);
    expect(screen.getByText('⏸ Pause')).toBeDefined();
  });

  it('supports CommandPalette keyboard actions and search filter', () => {
    render(
      <MissionControlProvider>
        <WorkspaceProvider>
          <CommandPalette isOpen={true} onClose={() => {}} />
        </WorkspaceProvider>
      </MissionControlProvider>
    );

    expect(screen.getByPlaceholderText(/Type a command, navigation, or instruction/i)).toBeDefined();
    expect(screen.getByText(/Start Autonomous Demo/i)).toBeDefined();

    const input = screen.getByPlaceholderText(/Type a command, navigation, or instruction/i);
    fireEvent.change(input, { target: { value: 'memory' } });

    expect(screen.getByText(/Navigate to Causal Memory Graph/i)).toBeDefined();
  });

  it('renders EnterpriseFooter with live latency and SLSA level watermark', () => {
    render(<EnterpriseFooter />);

    expect(screen.getByText(/DocuTask Agent v2.5.0-prod/i)).toBeDefined();
    expect(screen.getByText(/API Latency: 18ms/i)).toBeDefined();
    expect(screen.getByText(/SLSA Level 3\+ Verified/i)).toBeDefined();
  });

  it('renders Confetti celebration without crashing', () => {
    const { container } = render(<Confetti durationMs={500} />);
    expect(container.querySelector('canvas')).toBeDefined();
  });
});
