import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { App } from '../../src/App';
import { MissionControlProvider } from '../../src/context/MissionControlContext';
import { HeroHeader } from '../../src/components/mission-control/HeroHeader';
import { LiveCognitionLoop } from '../../src/components/mission-control/LiveCognitionLoop';
import { DecisionCenterSection } from '../../src/components/mission-control/DecisionCenterSection';
import { ConfidenceCenterSection } from '../../src/components/mission-control/ConfidenceCenterSection';
import { HumanControlSection } from '../../src/components/mission-control/HumanControlSection';

import { MissionControlPage } from '../../src/pages/MissionControlPage';

describe('DocuTask Agent — Mission Control Integration Suite', () => {
  it('renders the complete Mission Control page with all 10 core sections', () => {
    render(
      <MissionControlProvider>
        <MissionControlPage />
      </MissionControlProvider>
    );

    // Section 1: Hero Header
    expect(screen.getByText('DocuTask Agent')).toBeDefined();
    expect(
      screen.getByText('An Autonomous AI Coworker for Enterprise Document Operations')
    ).toBeDefined();

    // Section 2: Goal Intelligence
    expect(screen.getByText('Goal Deconstruction & Autonomous Negotiation')).toBeDefined();

    // Section 3: Live Cognition Loop
    expect(
      screen.getByText('Autonomous Cognition & Continuous Improvement Engine')
    ).toBeDefined();

    // Section 4: Multi-Agent Fleet
    expect(screen.getByText('Autonomous Agent Team')).toBeDefined();
    expect(screen.getByText('Cognition Thought Stream')).toBeDefined();

    // Section 5: Mission Dependency Graph
    expect(screen.getByText('Mission Dependency Graph (DAG)')).toBeDefined();

    // Section 6: Decision Center
    expect(screen.getByText('Explainable Decision Center')).toBeDefined();

    // Section 7: Evidence Center
    expect(screen.getByText('Empirical Evidence & SLSA Lineage Ledger')).toBeDefined();

    // Section 8: Memory Center
    expect(screen.getByText('Long-Term Memory & Exponential Retention Decay')).toBeDefined();

    // Section 9: Confidence Center
    expect(
      screen.getByText('Statistical Confidence & Uncertainty Decomposition')
    ).toBeDefined();

    // Section 10: Human Control
    expect(screen.getByText('Human Control & Governance Cockpit')).toBeDefined();
  });

  it('verifies HeroHeader displays live mission telemetry and cryptographic digest', () => {
    render(
      <MissionControlProvider>
        <HeroHeader />
      </MissionControlProvider>
    );

    expect(screen.getByText('mission_autocog_799784')).toBeDefined();
    expect(screen.getByText('97.2%')).toBeDefined();
    expect(screen.getByText('$2.14 / $15.00')).toBeDefined();
    expect(screen.getByText('5fc03ae31fe4...')).toBeDefined();
  });

  it('allows clicking Cognition Loop stages and displaying produced artifacts', () => {
    render(
      <MissionControlProvider>
        <LiveCognitionLoop />
      </MissionControlProvider>
    );

    // Initial selected active stage
    expect(screen.getAllByText('Empirical Reflection').length).toBeGreaterThan(0);

    // Click on "Observation & Gaps" stage
    const observeNode = screen.getByText('Observation & Gaps');
    fireEvent.click(observeNode);

    expect(screen.getByText('Artifacts Produced (2)')).toBeDefined();
    expect(screen.getByText(/scan_histograms.parquet/)).toBeDefined();
  });

  it('expands Decision Explainability and shows 9-dimension risk evaluation', () => {
    render(
      <MissionControlProvider>
        <DecisionCenterSection />
      </MissionControlProvider>
    );

    expect(
      screen.getByText('Approve Adaptive Contrast Optimization Strategy')
    ).toBeDefined();

    // Check that alternatives and risk dimensions are rendered
    expect(screen.getByText(/Global Otsu Binarization/)).toBeDefined();
    expect(screen.getByText(/4. 9-Dimension Risk Vector Evaluation/)).toBeDefined();
    expect(screen.getByText(/ACCURACY:/)).toBeDefined();
  });

  it('renders rigorous statistical power and confidence intervals in ConfidenceCenter', () => {
    render(
      <MissionControlProvider>
        <ConfidenceCenterSection />
      </MissionControlProvider>
    );

    expect(screen.getByText(/p-value: 0.0012/)).toBeDefined();
    expect(screen.getByText(/Sample Count: n=53/)).toBeDefined();
    expect(screen.getByText(/95% Confidence Interval:/)).toBeDefined();
  });

  it('supports pause/resume and zero-fabrication sentinel injection via HumanControl', () => {
    render(
      <MissionControlProvider>
        <HumanControlSection />
      </MissionControlProvider>
    );

    const pauseBtn = screen.getByText('⏸ Pause Mission');
    fireEvent.click(pauseBtn);

    expect(screen.getByText('▶ Resume Autonomous Cognition')).toBeDefined();

    const sentinelBtn = screen.getByText('⚠ Simulate Zero-Fabrication Sentinel');
    fireEvent.click(sentinelBtn);

    expect(screen.getByText(/Supervisory Audit Receipts/)).toBeDefined();
  });
});
