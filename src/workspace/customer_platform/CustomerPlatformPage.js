import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { CustomerDashboard, AutomationStudio, WorkflowBuilder, TemplateMarketplace, ConnectorCenter, ApprovalCenter, AnalyticsDashboard, TrustCenter, PerformanceCommandCenter, BusinessValueCommandCenter, EnterpriseReadinessCommandCenter, DemoMode, IndustrySolutions, CaseStudies, } from './index';
export const CustomerPlatformPage = () => {
    const [subView, setSubView] = useState('DEMO_PLAYER');
    const navItems = [
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
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin scrollbar-thumb-gray-800", children: navItems.map((item) => (_jsxs("button", { onClick: () => setSubView(item.id), className: `px-3.5 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-all flex items-center gap-2 ${subView === item.id
                        ? 'bg-gradient-to-r from-[#0066FF] to-[#00D2FF] text-white shadow-lg shadow-[#0066FF]/25 scale-102'
                        : 'bg-[#0F172A] text-[#94A3B8] hover:text-white border border-[#1E293B]'}`, children: [_jsx("span", { children: item.icon }), _jsx("span", { children: item.label })] }, item.id))) }), subView === 'DEMO_PLAYER' && _jsx(DemoMode, {}), subView === 'DASHBOARD' && _jsx(CustomerDashboard, {}), subView === 'READINESS' && _jsx(EnterpriseReadinessCommandCenter, {}), subView === 'BUSINESS_VALUE' && _jsx(BusinessValueCommandCenter, {}), subView === 'PERFORMANCE' && _jsx(PerformanceCommandCenter, {}), subView === 'STUDIO' && _jsx(AutomationStudio, {}), subView === 'WORKFLOW_BUILDER' && _jsx(WorkflowBuilder, {}), subView === 'MARKETPLACE' && _jsx(TemplateMarketplace, {}), subView === 'CONNECTORS' && _jsx(ConnectorCenter, {}), subView === 'APPROVALS' && _jsx(ApprovalCenter, {}), subView === 'ANALYTICS' && _jsx(AnalyticsDashboard, {}), subView === 'TRUST_CENTER' && _jsx(TrustCenter, {}), subView === 'SOLUTIONS' && _jsx(IndustrySolutions, {}), subView === 'CASE_STUDIES' && _jsx(CaseStudies, {})] }));
};
