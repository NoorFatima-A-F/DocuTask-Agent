import React, { useState } from 'react';
import {
  CustomerDashboard,
  AutomationStudio,
  WorkflowBuilder,
  TemplateMarketplace,
  ConnectorCenter,
  ApprovalCenter,
  AnalyticsDashboard,
  TrustCenter,
  PerformanceCommandCenter,
  BusinessValueCommandCenter,
  EnterpriseReadinessCommandCenter,
  DemoMode,
  IndustrySolutions,
  CaseStudies,
} from './index';

type CustomerSubView =
  | 'DEMO_PLAYER'
  | 'DASHBOARD'
  | 'READINESS'
  | 'BUSINESS_VALUE'
  | 'PERFORMANCE'
  | 'STUDIO'
  | 'WORKFLOW_BUILDER'
  | 'MARKETPLACE'
  | 'CONNECTORS'
  | 'APPROVALS'
  | 'ANALYTICS'
  | 'TRUST_CENTER'
  | 'SOLUTIONS'
  | 'CASE_STUDIES';

export const CustomerPlatformPage: React.FC = () => {
  const [subView, setSubView] = useState<CustomerSubView>('DEMO_PLAYER');

  const navItems: { id: CustomerSubView; label: string; icon: string }[] = [
    { id: 'DEMO_PLAYER', label: '1-Click Live Demo', icon: '▶' },
    { id: 'DASHBOARD', label: 'Customer Dashboard', icon: '📊' },
    { id: 'READINESS', label: 'Master Readiness & Audit', icon: '🎖️' },
    { id: 'BUSINESS_VALUE', label: 'Business Value & ROI', icon: '💎' },
    { id: 'PERFORMANCE', label: 'Performance & SRE', icon: '⚡' },
    { id: 'STUDIO', label: 'Automation Studio', icon: '🛠️' },
    { id: 'WORKFLOW_BUILDER', label: 'Visual Workflow Builder', icon: '🔀' },
    { id: 'MARKETPLACE', label: 'Template Marketplace', icon: '🏪' },
    { id: 'CONNECTORS', label: 'Connector Center', icon: '🔌' },
    { id: 'APPROVALS', label: 'Approval & HITL Center', icon: '👤' },
    { id: 'ANALYTICS', label: 'Executive ROI Analytics', icon: '📈' },
    { id: 'TRUST_CENTER', label: 'AI Trust & Governance', icon: '🛡️' },
    { id: 'SOLUTIONS', label: 'Industry Solutions', icon: '🏢' },
    { id: 'CASE_STUDIES', label: 'Case Studies & Scripts', icon: '📜' },
  ];

  return (
    <div className="space-y-6">
      {/* Sub-Navigation Bar */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin scrollbar-thumb-gray-800">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setSubView(item.id)}
            className={`px-3.5 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-all flex items-center gap-2 ${
              subView === item.id
                ? 'bg-gradient-to-r from-[#0066FF] to-[#00D2FF] text-white shadow-lg shadow-[#0066FF]/25 scale-102'
                : 'bg-[#0F172A] text-[#94A3B8] hover:text-white border border-[#1E293B]'
            }`}
          >
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </div>

      {/* Render SubView */}
      {subView === 'DEMO_PLAYER' && <DemoMode />}
      {subView === 'DASHBOARD' && <CustomerDashboard />}
      {subView === 'READINESS' && <EnterpriseReadinessCommandCenter />}
      {subView === 'BUSINESS_VALUE' && <BusinessValueCommandCenter />}
      {subView === 'PERFORMANCE' && <PerformanceCommandCenter />}
      {subView === 'STUDIO' && <AutomationStudio />}
      {subView === 'WORKFLOW_BUILDER' && <WorkflowBuilder />}
      {subView === 'MARKETPLACE' && <TemplateMarketplace />}
      {subView === 'CONNECTORS' && <ConnectorCenter />}
      {subView === 'APPROVALS' && <ApprovalCenter />}
      {subView === 'ANALYTICS' && <AnalyticsDashboard />}
      {subView === 'TRUST_CENTER' && <TrustCenter />}
      {subView === 'SOLUTIONS' && <IndustrySolutions />}
      {subView === 'CASE_STUDIES' && <CaseStudies />}
    </div>
  );
};
