import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
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
export const MissionControlPage = () => {
    return (_jsxs("main", { className: "min-h-screen bg-[#0A0F1D] text-[#F8FAFC] py-8 px-4 sm:px-6 lg:px-12 max-w-[1600px] mx-auto selection:bg-[#00D2FF]/30 selection:text-white", children: [_jsx(HeroHeader, {}), _jsx(GoalIntelligenceSection, {}), _jsx(LiveCognitionLoop, {}), _jsx(AgentCollaborationSection, {}), _jsx(MissionGraphSection, {}), _jsx(DecisionCenterSection, {}), _jsx(EvidenceCenterSection, {}), _jsx(MemoryCenterSection, {}), _jsx(ConfidenceCenterSection, {}), _jsx(HumanControlSection, {})] }));
};
