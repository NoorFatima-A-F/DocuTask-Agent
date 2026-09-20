import React, { useState, useEffect } from 'react';
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

export const AppContent: React.FC = () => {
  const [viewMode, setViewMode] = useState<'WORKSPACE' | 'MISSION_CONTROL' | 'CUSTOMER_PLATFORM'>('CUSTOMER_PLATFORM');
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);
  const [isProgressiveThinkingOpen, setIsProgressiveThinkingOpen] = useState(false);

  const { isConnected, selectedEventForInspector, setSelectedEventForInspector } = useRuntimeTelemetry();

  // Global Keyboard Shortcuts (Ctrl+K, Space, D)
  useEffect(() => {
    const handleGlobalKeyDown = (e: KeyboardEvent) => {
      // Don't intercept when user is typing in an input/textarea
      const targetTag = (e.target as HTMLElement)?.tagName?.toLowerCase();
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

  return (
    <div className="min-h-screen bg-[#0A0F1D] text-[#F8FAFC]">
      {/* Global Top Navbar */}
      <nav className="sticky top-0 z-40 bg-[#0F172A]/90 backdrop-blur-xl border-b border-[#1E293B] px-6 py-3.5 flex items-center justify-between shadow-lg">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-lg bg-gradient-to-tr from-[#0066FF] to-[#00D2FF] flex items-center justify-center font-bold text-white shadow-[0_0_12px_rgba(0,210,255,0.6)]">
            DT
          </div>
          <div>
            <span className="font-extrabold text-sm tracking-tight text-[#F8FAFC]">
              DocuTask Agent
            </span>
            <span className="hidden sm:inline text-xs text-[#94A3B8] ml-2 font-mono">
              Autonomous AI Coworker
            </span>
          </div>
          <Badge variant="intelligence" size="sm" hasDot isPulsing={isConnected}>
            {isConnected ? 'LIVE RUNTIME' : 'ONLINE'}
          </Badge>
        </div>

        {/* View Mode Switcher & Quick Command Trigger */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-[#0A0F1D] p-1 rounded-xl border border-[#1E293B]">
            <Button
              variant={viewMode === 'CUSTOMER_PLATFORM' ? 'intelligence' : 'ghost'}
              size="sm"
              onClick={() => setViewMode('CUSTOMER_PLATFORM')}
              className="text-xs font-mono"
            >
              🏢 Enterprise Customer Portal
            </Button>
            <Button
              variant={viewMode === 'WORKSPACE' ? 'intelligence' : 'ghost'}
              size="sm"
              onClick={() => setViewMode('WORKSPACE')}
              className="text-xs font-mono"
            >
              👥 AI Coworker Workspace
            </Button>
            <Button
              variant={viewMode === 'MISSION_CONTROL' ? 'intelligence' : 'ghost'}
              size="sm"
              onClick={() => setViewMode('MISSION_CONTROL')}
              className="text-xs font-mono"
            >
              🛰️ Mission Control
            </Button>
          </div>

          <button
            onClick={() => setIsCommandPaletteOpen(true)}
            className="hidden sm:flex items-center gap-1.5 bg-[#131D35] px-3 py-1.5 rounded-xl border border-[#334155] hover:border-cyan-400 text-xs font-mono text-[#F8FAFC] transition-colors"
          >
            <span className="text-[#00D2FF]">⌘K</span>
            <span className="text-[#94A3B8]">Palette</span>
          </button>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="py-8 px-4 sm:px-6 lg:px-12 max-w-[1600px] mx-auto">
        {viewMode === 'CUSTOMER_PLATFORM' ? (
          <CustomerPlatformPage />
        ) : viewMode === 'WORKSPACE' ? (
          <WorkspacePage />
        ) : (
          <MissionControlPage />
        )}
      </main>

      {/* Global Enterprise Footer */}
      <div className="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-12">
        <EnterpriseFooter onOpenCommandPalette={() => setIsCommandPaletteOpen(true)} />
      </div>

      {/* Global Modals */}
      <CommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
        onSwitchView={(v) => setViewMode(v)}
        onOpenProgressiveThinking={() => setIsProgressiveThinkingOpen(true)}
      />

      <ProgressiveThinkingModal
        isOpen={isProgressiveThinkingOpen}
        onClose={() => setIsProgressiveThinkingOpen(false)}
        targetConfidence={97.2}
      />

      {/* Temporal / OpenTelemetry Event Inspector Modal */}
      <EventInspectorModal
        event={selectedEventForInspector}
        onClose={() => setSelectedEventForInspector(null)}
      />
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <RuntimeTelemetryProvider>
      <MissionControlProvider>
        <WorkspaceProvider>
          <AppContent />
        </WorkspaceProvider>
      </MissionControlProvider>
    </RuntimeTelemetryProvider>
  );
};

export default App;
