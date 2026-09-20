import React, { useState, useEffect } from 'react';
import { useWorkspace } from '../../workspace/context/WorkspaceContext';
import { useMissionControl } from '../../context/MissionControlContext';
import type { WorkspaceTabType } from '../../workspace/types/workspace';

export interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onSwitchView?: (view: 'WORKSPACE' | 'MISSION_CONTROL') => void;
  onOpenProgressiveThinking?: () => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({
  isOpen,
  onClose,
  onSwitchView,
  onOpenProgressiveThinking,
}) => {
  const { setActiveTab, startAutonomousDemo, sendUserCommand } = useWorkspace();
  const { state, pauseMission, resumeMission, injectSentinelState } = useMissionControl();
  const [query, setQuery] = useState('');

  const commands: {
    id: string;
    title: string;
    category: string;
    action: () => void;
    shortcut?: string;
  }[] = [
    {
      id: 'cmd_demo',
      title: 'Start Autonomous Demo (One-Click Winning Scenario)',
      category: 'Autonomous Actions',
      shortcut: 'D',
      action: () => {
        onSwitchView?.('WORKSPACE');
        startAutonomousDemo();
      },
    },
    {
      id: 'cmd_progressive',
      title: 'Inspect Progressive Thinking (Intelligence Emergence)',
      category: 'Autonomous Actions',
      action: () => onOpenProgressiveThinking?.(),
    },
    {
      id: 'cmd_pause_resume',
      title: state.isPaused ? 'Resume Mission' : 'Pause Mission',
      category: 'Human Supervision',
      shortcut: 'Space',
      action: () => (state.isPaused ? resumeMission('Operator via Palette') : pauseMission('Operator via Palette')),
    },
    {
      id: 'cmd_sentinel',
      title: 'Simulate Zero-Fabrication Sentinel (DATASET_UNAVAILABLE)',
      category: 'Human Supervision',
      action: () => injectSentinelState(),
    },
    {
      id: 'cmd_nav_conv',
      title: 'Navigate to Conversation (Natural Language Command Center)',
      category: 'Navigation',
      action: () => {
        onSwitchView?.('WORKSPACE');
        setActiveTab('CONVERSATION');
      },
    },
    {
      id: 'cmd_nav_inbox',
      title: 'Navigate to Agent Inbox (Slack-like Channels)',
      category: 'Navigation',
      action: () => {
        onSwitchView?.('WORKSPACE');
        setActiveTab('AGENT_INBOX');
      },
    },
    {
      id: 'cmd_nav_tasks',
      title: 'Navigate to Task Board (Multi-Agent Kanban)',
      category: 'Navigation',
      action: () => {
        onSwitchView?.('WORKSPACE');
        setActiveTab('TASK_BOARD');
      },
    },
    {
      id: 'cmd_nav_memory',
      title: 'Navigate to Causal Memory Graph',
      category: 'Navigation',
      action: () => {
        onSwitchView?.('WORKSPACE');
        setActiveTab('MEMORY_GRAPH');
      },
    },
    {
      id: 'cmd_nav_confidence',
      title: 'Navigate to Confidence Explorer & Trajectory',
      category: 'Navigation',
      action: () => {
        onSwitchView?.('WORKSPACE');
        setActiveTab('CONFIDENCE_EXPLORER');
      },
    },
    {
      id: 'cmd_nav_story',
      title: 'Navigate to Documentary Mission Story',
      category: 'Navigation',
      action: () => {
        onSwitchView?.('WORKSPACE');
        setActiveTab('MISSION_STORY' as WorkspaceTabType);
      },
    },
    {
      id: 'cmd_nav_movie',
      title: 'Navigate to Cinematic Replay Movie Player',
      category: 'Navigation',
      action: () => {
        onSwitchView?.('WORKSPACE');
        setActiveTab('CINEMATIC_REPLAY' as WorkspaceTabType);
      },
    },
    {
      id: 'cmd_nav_mc',
      title: 'Switch to Full Mission Control View (10 Sections)',
      category: 'Navigation',
      action: () => onSwitchView?.('MISSION_CONTROL'),
    },
    {
      id: 'cmd_optimize_invoice',
      title: 'Instruction: "Improve invoice extraction on thermal scans"',
      category: 'Quick Instructions',
      action: () => {
        onSwitchView?.('WORKSPACE');
        setActiveTab('CONVERSATION');
        sendUserCommand('Improve invoice extraction on thermal scans');
      },
    },
  ];

  const filtered = query.trim()
    ? commands.filter(
        (c) =>
          c.title.toLowerCase().includes(query.toLowerCase()) ||
          c.category.toLowerCase().includes(query.toLowerCase())
      )
    : commands;

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    if (isOpen) {
      window.addEventListener('keydown', handleKeyDown);
    }
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-24 p-4 bg-black/80 backdrop-blur-md">
      <div className="w-full max-w-2xl rounded-3xl bg-[#0F172A] border border-cyan-500/40 shadow-[0_0_60px_rgba(0,102,255,0.4)] overflow-hidden">
        {/* Search Input */}
        <div className="p-4 border-b border-[#1E293B] bg-[#131D35]/60 flex items-center gap-3">
          <span className="text-[#00D2FF] text-lg font-mono">⌘</span>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Type a command, navigation, or instruction (e.g. 'demo', 'memory', 'confidence')..."
            autoFocus
            className="w-full bg-transparent text-xs sm:text-sm font-mono text-[#F8FAFC] placeholder-[#64748B] focus:outline-none"
          />
          <span className="text-[10px] font-mono bg-[#0A0F1D] text-[#94A3B8] px-2 py-1 rounded border border-[#334155]">
            ESC to close
          </span>
        </div>

        {/* Results List */}
        <div className="max-h-96 overflow-y-auto p-3 space-y-1">
          {filtered.length > 0 ? (
            filtered.map((cmd) => (
              <button
                key={cmd.id}
                onClick={() => {
                  cmd.action();
                  onClose();
                }}
                className="w-full p-3 rounded-xl text-left hover:bg-[#1E293B] flex items-center justify-between transition-colors group"
              >
                <div>
                  <span className="text-xs font-semibold text-[#F8FAFC] group-hover:text-[#00D2FF] transition-colors block">
                    {cmd.title}
                  </span>
                  <span className="text-[10px] font-mono text-[#64748B] block mt-0.5">
                    {cmd.category}
                  </span>
                </div>

                {cmd.shortcut && (
                  <span className="text-[10px] font-mono bg-[#0A0F1D] text-[#00D2FF] px-2 py-0.5 rounded border border-cyan-500/30">
                    {cmd.shortcut}
                  </span>
                )}
              </button>
            ))
          ) : (
            <div className="p-8 text-center text-xs text-[#64748B]">No matching commands found</div>
          )}
        </div>
      </div>
    </div>
  );
};
