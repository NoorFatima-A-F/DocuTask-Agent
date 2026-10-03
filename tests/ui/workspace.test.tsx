import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { App } from '../../src/App';
import { WorkspaceProvider } from '../../src/workspace/context/WorkspaceContext';
import { ConversationPanel } from '../../src/workspace/conversation/ConversationPanel';
import { AgentInboxPanel } from '../../src/workspace/agent-inbox/AgentInboxPanel';
import { HumanFeedbackPanel } from '../../src/workspace/feedback/HumanFeedbackPanel';
import { MissionReplayPlayer } from '../../src/workspace/replay/MissionReplayPlayer';
import { MemoryGraphPanel } from '../../src/workspace/memory-graph/MemoryGraphPanel';
import { ConfidenceExplorerPanel } from '../../src/workspace/confidence/ConfidenceExplorerPanel';

describe('DocuTask Agent — AI Coworker Workspace Integration Suite', () => {
  it('renders the top-level Workspace tabs and view mode switcher', () => {
    render(<App />);

    expect(screen.getAllByText('DocuTask Agent').length).toBeGreaterThan(0);
    expect(screen.getByText('👥 AI Coworker Workspace')).toBeDefined();
    expect(screen.getByText('🛰️ Mission Control')).toBeDefined();

    // Verify Workspace Tabs
    expect(screen.getByText('Conversation')).toBeDefined();
    expect(screen.getByText('Agent Inbox')).toBeDefined();
    expect(screen.getByText('Task Board')).toBeDefined();
    expect(screen.getByText('Feedback Loop')).toBeDefined();
    expect(screen.getByText('Time Machine Replay')).toBeDefined();
  });

  it('allows natural language command submission in ConversationPanel', () => {
    render(
      <WorkspaceProvider>
        <ConversationPanel />
      </WorkspaceProvider>
    );

    const textarea = screen.getByPlaceholderText(/Type natural language instruction/i);
    fireEvent.change(textarea, { target: { value: 'Explain why confidence changed' } });

    const submitBtn = screen.getByText(/Dispatch Instruction/i);
    fireEvent.click(submitBtn);

    expect(screen.getByText('Explain why confidence changed')).toBeDefined();
  });

  it('verifies Agent Inbox channel selection and direct message sending', () => {
    render(
      <WorkspaceProvider>
        <AgentInboxPanel />
      </WorkspaceProvider>
    );

    expect(screen.getAllByText('Planner Agent').length).toBeGreaterThan(0);
    expect(screen.getByText('Evidence Agent')).toBeDefined();

    // Click on Evidence Agent channel
    const evidenceChannel = screen.getByText('Evidence Agent');
    fireEvent.click(evidenceChannel);

    const input = screen.getByPlaceholderText(/Send instructions directly to/i);
    fireEvent.change(input, { target: { value: 'Verify patch #42 checksum' } });

    const form = input.closest('form');
    if (form) {
      fireEvent.submit(form);
    }

    expect(screen.getByText('Verify patch #42 checksum')).toBeDefined();
  });

  it('supports human feedback distillation into long-term memory', () => {
    render(
      <WorkspaceProvider>
        <HumanFeedbackPanel />
      </WorkspaceProvider>
    );

    expect(screen.getByText(/Interactive Correction & Ground Truth Learning/i)).toBeDefined();
    expect(screen.getByText('INV_THERMAL_984.pdf')).toBeDefined();
  });

  it('supports Time Machine Replay stepping and scrubbing', () => {
    render(
      <WorkspaceProvider>
        <MissionReplayPlayer />
      </WorkspaceProvider>
    );

    expect(screen.getByText(/Deterministic Mission Replay & Execution Scrubber/i)).toBeDefined();

    const stepBackwardBtn = screen.getByText('⏮ Step Backward');
    fireEvent.click(stepBackwardBtn);

    expect(screen.getByText(/Time Machine Replay/i)).toBeDefined();
  });

  it('renders Memory Causal Graph and Confidence Decomposition', () => {
    render(
      <WorkspaceProvider>
        <MemoryGraphPanel />
      </WorkspaceProvider>
    );

    expect(screen.getByText(/Causal Memory & Experience Graph/i)).toBeDefined();
    expect(screen.getByText(/Thermal Invoice Scans/i)).toBeDefined();

    render(
      <WorkspaceProvider>
        <ConfidenceExplorerPanel />
      </WorkspaceProvider>
    );

    expect(screen.getByText(/Mathematical Confidence & Evidence Contribution/i)).toBeDefined();
    expect(screen.getByText(/OCR Core Engine & Adaptive Preprocessor/i)).toBeDefined();
  });
});
