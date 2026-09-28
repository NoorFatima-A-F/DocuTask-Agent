import React, { useState, useEffect, useRef } from 'react';
import { Search, UploadCloud, Workflow, CheckSquare, BarChart3, Terminal, Shield } from 'lucide-react';
import { ActiveTab } from '../layout/Sidebar';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  onNavigate: (tab: ActiveTab) => void;
  onTriggerDiagnostic?: () => void;
}

export const CommandPalette: React.FC<CommandPaletteProps> = ({
  isOpen,
  onClose,
  onNavigate,
  onTriggerDiagnostic,
}) => {
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  const actions = [
    {
      id: 'ingestion',
      title: 'Go to Ingestion Studio',
      subtitle: 'Upload and stage documents for OCR taxonomy extraction',
      icon: UploadCloud,
      action: () => { onNavigate('ingestion'); onClose(); },
    },
    {
      id: 'pipeline',
      title: 'Go to Pipeline Monitor',
      subtitle: 'Inspect live asynchronous DAG stage milestones and latency',
      icon: Workflow,
      action: () => { onNavigate('pipeline'); onClose(); },
    },
    {
      id: 'reviewer',
      title: 'Go to HITL Reviewer',
      subtitle: 'Human-in-the-loop two-pane PDF bounding box editor',
      icon: CheckSquare,
      action: () => { onNavigate('reviewer'); onClose(); },
    },
    {
      id: 'observability',
      title: 'Go to DLQ & Telemetry Hub',
      subtitle: 'Examine worker load, latency percentiles, and DLQ quarantine',
      icon: BarChart3,
      action: () => { onNavigate('observability'); onClose(); },
    },
    {
      id: 'openapi',
      title: 'Open OpenAPI / Swagger Docs',
      subtitle: 'Interactive REST API specification at /api/v1/docs',
      icon: Terminal,
      action: () => { window.open('/api/v1/docs', '_blank'); onClose(); },
    },
    {
      id: 'diagnostic',
      title: 'Run Pipeline Diagnostic Sweep',
      subtitle: 'Verify worker heartbeat, Redis broker, and OCR engine readiness',
      icon: Shield,
      action: () => { if (onTriggerDiagnostic) onTriggerDiagnostic(); onClose(); },
    },
  ];

  const filtered = actions.filter(
    (a) =>
      a.title.toLowerCase().includes(query.toLowerCase()) ||
      a.subtitle.toLowerCase().includes(query.toLowerCase())
  );

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
      setQuery('');
      setSelectedIndex(0);
    }
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isOpen) return;
      if (e.key === 'Escape') {
        onClose();
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedIndex((prev) => (prev + 1) % (filtered.length || 1));
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedIndex((prev) => (prev - 1 + filtered.length) % (filtered.length || 1));
      } else if (e.key === 'Enter' && filtered[selectedIndex]) {
        e.preventDefault();
        filtered[selectedIndex].action();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, filtered, selectedIndex, onClose]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label="Command Palette"
      className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-start justify-center pt-20 p-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-xl bg-[#121215] border border-zinc-700/80 rounded-xl shadow-2xl overflow-hidden flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Search Input */}
        <div className="flex items-center gap-3 px-4 py-3 border-b border-zinc-800">
          <Search className="w-4 h-4 text-zinc-400 shrink-0" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setSelectedIndex(0);
            }}
            placeholder="Type a command or jump to workspace (e.g. HITL, DLQ)..."
            className="w-full bg-transparent text-sm text-zinc-100 placeholder-zinc-500 focus:outline-none font-mono"
          />
          <kbd className="hidden sm:inline-block px-1.5 py-0.5 rounded bg-zinc-900 border border-zinc-800 text-[10px] font-mono text-zinc-400">
            ESC
          </kbd>
        </div>

        {/* Results List */}
        <div className="max-h-80 overflow-y-auto p-2 space-y-1">
          {filtered.length === 0 ? (
            <div className="py-8 text-center text-xs font-mono text-zinc-500">
              No matching commands found.
            </div>
          ) : (
            filtered.map((item, idx) => {
              const Icon = item.icon;
              const isSelected = idx === selectedIndex;
              return (
                <button
                  key={item.id}
                  onClick={item.action}
                  className={`w-full text-left px-3 py-2.5 rounded-lg flex items-center gap-3 transition-colors ${
                    isSelected
                      ? 'bg-zinc-800 text-zinc-100'
                      : 'text-zinc-400 hover:bg-zinc-800/50 hover:text-zinc-200'
                  }`}
                >
                  <div className={`p-1.5 rounded-md ${isSelected ? 'bg-zinc-700 text-white' : 'bg-zinc-900 text-zinc-400'}`}>
                    <Icon className="w-4 h-4" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs font-semibold font-mono text-zinc-200">{item.title}</div>
                    <div className="text-[11px] text-zinc-400 truncate">{item.subtitle}</div>
                  </div>
                </button>
              );
            })
          )}
        </div>

        {/* Footer Shortcut Hints */}
        <div className="px-4 py-2 bg-[#0d0d10] border-t border-zinc-800 flex items-center justify-between text-[11px] font-mono text-zinc-500">
          <div className="flex items-center gap-2">
            <span>Navigate: <kbd className="text-zinc-400">↑</kbd> <kbd className="text-zinc-400">↓</kbd></span>
            <span>•</span>
            <span>Select: <kbd className="text-zinc-400">↵</kbd></span>
          </div>
          <span>DocuTask Spotlight</span>
        </div>
      </div>
    </div>
  );
};
