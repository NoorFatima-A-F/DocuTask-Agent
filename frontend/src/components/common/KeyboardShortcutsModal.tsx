import React, { useEffect } from 'react';
import { X, Command } from 'lucide-react';

interface KeyboardShortcutsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const KeyboardShortcutsModal: React.FC<KeyboardShortcutsModalProps> = ({ isOpen, onClose }) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isOpen) return;
      if (e.key === 'Escape') {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const shortcutGroups = [
    {
      title: 'Global Navigation',
      items: [
        { keys: ['⌘', 'K'], label: 'Open Command Palette (Spotlight)' },
        { keys: ['⌘', '['], label: 'Toggle Sidebar Collapse' },
        { keys: ['?'], label: 'Open Keyboard Shortcuts' },
        { keys: ['Esc'], label: 'Close Active Modal / Drawer' },
      ],
    },
    {
      title: 'Workspace Switching',
      items: [
        { keys: ['1'], label: 'Jump to Ingestion Studio' },
        { keys: ['2'], label: 'Jump to Pipeline Monitor' },
        { keys: ['3'], label: 'Jump to HITL Reviewer' },
        { keys: ['4'], label: 'Jump to DLQ & Telemetry' },
      ],
    },
    {
      title: 'HITL Reviewer & Verification',
      items: [
        { keys: ['⌘', 'S'], label: 'Approve & Persist Active Document' },
        { keys: ['⌘', 'D'], label: 'Toggle Side-by-Side Diff Mode' },
        { keys: ['⌘', 'Z'], label: 'Reset Field to OCR Ground Truth' },
      ],
    },
  ];

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label="Keyboard Shortcuts"
      className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-lg bg-[#121215] border border-zinc-700/80 rounded-xl shadow-2xl overflow-hidden flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between px-5 py-3.5 border-b border-zinc-800 bg-zinc-950/60">
          <div className="flex items-center gap-2">
            <Command className="w-4 h-4 text-indigo-400" />
            <h3 className="text-xs font-semibold text-zinc-100 uppercase tracking-wider font-mono">
              Platform Keyboard Shortcuts
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 transition-colors cursor-pointer"
            aria-label="Close shortcuts modal"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-5 space-y-5 max-h-[70vh] overflow-y-auto">
          {shortcutGroups.map((group) => (
            <div key={group.title} className="space-y-2">
              <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-400 font-semibold block">
                {group.title}
              </span>
              <div className="space-y-1.5">
                {group.items.map((item, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between py-1.5 px-2.5 rounded bg-zinc-950/50 border border-zinc-800/80 text-xs font-mono"
                  >
                    <span className="text-zinc-300 font-sans text-xs">{item.label}</span>
                    <div className="flex items-center gap-1">
                      {item.keys.map((k, ki) => (
                        <kbd
                          key={ki}
                          className="px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-700 text-zinc-200 text-[11px] font-mono shadow-sm"
                        >
                          {k}
                        </kbd>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="px-5 py-2.5 bg-zinc-950/80 border-t border-zinc-800 text-[11px] font-mono text-zinc-400 flex items-center justify-between">
          <span>Press <kbd className="px-1 py-0.5 rounded bg-zinc-900 border border-zinc-800 text-zinc-300">Esc</kbd> to dismiss</span>
          <span>DocuTask v1.0.0</span>
        </div>
      </div>
    </div>
  );
};
