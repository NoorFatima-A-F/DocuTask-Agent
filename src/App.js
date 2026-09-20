import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { RuntimeTelemetryProvider, useRuntimeTelemetry } from './context/RuntimeTelemetryContext';
import { MissionControlProvider } from './context/MissionControlContext';
import { WorkspaceProvider } from './workspace/context/WorkspaceContext';
import { MissionControlPage } from './pages/MissionControlPage';
import { WorkspacePage } from './workspace/WorkspacePage';
import { Button } from './components/ui/Button';
import { Badge } from './components/ui/Badge';
import { CommandPalette } from './components/ui/CommandPalette';
import { ProgressiveThinkingModal } from './components/presence/ProgressiveThinkingModal';
import { EventInspectorModal } from './components/telemetry/EventInspectorModal';
import { EnterpriseFooter } from './components/ui/EnterpriseFooter';
import { CustomerPlatformPage } from './workspace/customer_platform/CustomerPlatformPage';
export const AppContent = () => {
    const [viewMode, setViewMode] = useState('CUSTOMER_PLATFORM');
    const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);
    const [isProgressiveThinkingOpen, setIsProgressiveThinkingOpen] = useState(false);
    const { isConnected, selectedEventForInspector, setSelectedEventForInspector } = useRuntimeTelemetry();
    // Global Keyboard Shortcuts (Ctrl+K, Space, D)
    useEffect(() => {
        const handleGlobalKeyDown = (e) => {
            // Don't intercept when user is typing in an input/textarea
            const targetTag = e.target?.tagName?.toLowerCase();
            if (targetTag === 'input' || targetTag === 'textarea') {
                if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                    e.preventDefault();
                    setIsCommandPaletteOpen((prev) => !prev);
                }
                return;
            }
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                setIsCommandPaletteOpen((prev) => !prev);
            }
        };
        window.addEventListener('keydown', handleGlobalKeyDown);
        return () => window.removeEventListener('keydown', handleGlobalKeyDown);
    }, []);
    return (_jsxs("div", { className: "min-h-screen bg-[#0A0F1D] text-[#F8FAFC]", children: [_jsxs("nav", { className: "sticky top-0 z-40 bg-[#0F172A]/90 backdrop-blur-xl border-b border-[#1E293B] px-6 py-3.5 flex items-center justify-between shadow-lg", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "h-8 w-8 rounded-lg bg-gradient-to-tr from-[#0066FF] to-[#00D2FF] flex items-center justify-center font-bold text-white shadow-[0_0_12px_rgba(0,210,255,0.6)]", children: "DT" }), _jsxs("div", { children: [_jsx("span", { className: "font-extrabold text-sm tracking-tight text-[#F8FAFC]", children: "DocuTask Agent" }), _jsx("span", { className: "hidden sm:inline text-xs text-[#94A3B8] ml-2 font-mono", children: "Autonomous AI Coworker" })] }), _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: isConnected, children: isConnected ? 'LIVE RUNTIME' : 'ONLINE' })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsxs("div", { className: "flex items-center gap-2 bg-[#0A0F1D] p-1 rounded-xl border border-[#1E293B]", children: [_jsx(Button, { variant: viewMode === 'CUSTOMER_PLATFORM' ? 'intelligence' : 'ghost', size: "sm", onClick: () => setViewMode('CUSTOMER_PLATFORM'), className: "text-xs font-mono", children: "\uD83C\uDFE2 Enterprise Customer Portal" }), _jsx(Button, { variant: viewMode === 'WORKSPACE' ? 'intelligence' : 'ghost', size: "sm", onClick: () => setViewMode('WORKSPACE'), className: "text-xs font-mono", children: "\uD83D\uDC65 AI Coworker Workspace" }), _jsx(Button, { variant: viewMode === 'MISSION_CONTROL' ? 'intelligence' : 'ghost', size: "sm", onClick: () => setViewMode('MISSION_CONTROL'), className: "text-xs font-mono", children: "\uD83D\uDEF0\uFE0F Mission Control" })] }), _jsxs("button", { onClick: () => setIsCommandPaletteOpen(true), className: "hidden sm:flex items-center gap-1.5 bg-[#131D35] px-3 py-1.5 rounded-xl border border-[#334155] hover:border-cyan-400 text-xs font-mono text-[#F8FAFC] transition-colors", children: [_jsx("span", { className: "text-[#00D2FF]", children: "\u2318K" }), _jsx("span", { className: "text-[#94A3B8]", children: "Palette" })] })] })] }), _jsx("main", { className: "py-8 px-4 sm:px-6 lg:px-12 max-w-[1600px] mx-auto", children: viewMode === 'CUSTOMER_PLATFORM' ? (_jsx(CustomerPlatformPage, {})) : viewMode === 'WORKSPACE' ? (_jsx(WorkspacePage, {})) : (_jsx(MissionControlPage, {})) }), _jsx("div", { className: "max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-12", children: _jsx(EnterpriseFooter, { onOpenCommandPalette: () => setIsCommandPaletteOpen(true) }) }), _jsx(CommandPalette, { isOpen: isCommandPaletteOpen, onClose: () => setIsCommandPaletteOpen(false), onSwitchView: (v) => setViewMode(v), onOpenProgressiveThinking: () => setIsProgressiveThinkingOpen(true) }), _jsx(ProgressiveThinkingModal, { isOpen: isProgressiveThinkingOpen, onClose: () => setIsProgressiveThinkingOpen(false), targetConfidence: 97.2 }), _jsx(EventInspectorModal, { event: selectedEventForInspector, onClose: () => setSelectedEventForInspector(null) })] }));
};
export const App = () => {
    return (_jsx(RuntimeTelemetryProvider, { children: _jsx(MissionControlProvider, { children: _jsx(WorkspaceProvider, { children: _jsx(AppContent, {}) }) }) }));
};
export default App;
