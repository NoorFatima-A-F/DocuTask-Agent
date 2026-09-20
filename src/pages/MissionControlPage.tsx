import React from 'react';
import { HeroHeader } from '../components/mission-control/HeroHeader';
import { GoalIntelligenceSection } from '../components/mission-control/GoalIntelligenceSection';
import { LiveCognitionLoop } from '../components/mission-control/LiveCognitionLoop';
import { AgentCollaborationSection } from '../components/mission-control/AgentCollaborationSection';
import { MissionGraphSection } from '../components/mission-control/MissionGraphSection';
import { DecisionCenterSection } from '../components/mission-control/DecisionCenterSection';
import { EvidenceCenterSection } from '../components/mission-control/EvidenceCenterSection';
import { MemoryCenterSection } from '../components/mission-control/MemoryCenterSection';
import { ConfidenceCenterSection } from '../components/mission-control/ConfidenceCenterSection';
import { HumanControlSection } from '../components/mission-control/HumanControlSection';

export const MissionControlPage: React.FC = () => {
  return (
    <main className="min-h-screen bg-[#0A0F1D] text-[#F8FAFC] py-8 px-4 sm:px-6 lg:px-12 max-w-[1600px] mx-auto selection:bg-[#00D2FF]/30 selection:text-white">
      {/* 1. Hero Header & Telemetry */}
      <HeroHeader />

      {/* 2. Goal Intelligence & 6-Phase Deconstruction */}
      <GoalIntelligenceSection />

      {/* 3. Live 11-Stage Cognition Loop (Centerpiece) */}
      <LiveCognitionLoop />

      {/* 4. 10-Agent Collaboration Grid & Thought Stream */}
      <AgentCollaborationSection />

      {/* 5. Mission Dependency Graph (Interactive DAG) */}
      <MissionGraphSection />

      {/* 6. Explainable Decision Center */}
      <DecisionCenterSection />

      {/* 7. Empirical Evidence & SLSA Lineage */}
      <EvidenceCenterSection />

      {/* 8. Long-Term Memory & Retention Decay */}
      <MemoryCenterSection />

      {/* 9. Statistical Confidence & Uncertainty */}
      <ConfidenceCenterSection />

      {/* 10. Human-in-the-Loop Supervisory Cockpit */}
      <HumanControlSection />
    </main>
  );
};
