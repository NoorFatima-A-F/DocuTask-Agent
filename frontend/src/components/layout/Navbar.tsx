import React from 'react';
import { Terminal, ExternalLink, Activity, Database, AlertCircle, Search, ShieldCheck } from 'lucide-react';
import { UserProfile } from '../../api/auth';
import { useSystemHealth } from '../../hooks/useSystemHealth';

interface NavbarProps {
  user: UserProfile | null;
  activeTab: string;
  onOpenCommandPalette?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onOpenCommandPalette }) => {
  const { data: health } = useSystemHealth();
  const isOnline = health?.isOnline ?? true;

  return (
    <div className="sticky top-0 z-30 select-none shrink-0">
      {/* Offline Warning Banner with aria-live */}
      {!isOnline && (
        <div
          role="alert"
          aria-live="polite"
          className="bg-rose-950 border-b border-rose-800/80 px-4 py-1.5 flex items-center justify-between text-xs font-mono text-rose-200"
        >
          <div className="flex items-center gap-2">
            <AlertCircle className="w-3.5 h-3.5 text-rose-400" />
            <span>Backend API unreachable. Ensure Uvicorn is running on port 8000 (<code className="text-white bg-rose-900/60 px-1 py-0.5 rounded">py -3.14 -m uvicorn app.main:app --port 8000</code>).</span>
          </div>
          <span className="text-[10px] text-rose-300 font-semibold uppercase tracking-wider">OFFLINE • AUTO-RETRYING</span>
        </div>
      )}

      {/* Main Header Bar */}
      <header className="h-11 border-b border-[#27272a] bg-[#121215] px-4 flex items-center justify-between">
        {/* Brand & Version Badge */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div className="w-5 h-5 rounded bg-zinc-100 flex items-center justify-center text-zinc-950 font-bold text-xs font-mono">
              D
            </div>
            <span className="font-semibold text-sm text-zinc-100 tracking-tight">DocuTask</span>
            <span className="font-mono text-[11px] text-zinc-400 bg-zinc-900 border border-zinc-800 px-1.5 py-0.2 rounded">
              v1.0.0
            </span>
          </div>

          {/* Quick Command Palette Button */}
          {onOpenCommandPalette && (
            <button
              onClick={onOpenCommandPalette}
              className="hidden lg:flex items-center gap-2 px-2.5 py-1 rounded bg-zinc-900/80 hover:bg-zinc-800 border border-zinc-800 text-xs font-mono text-zinc-400 hover:text-zinc-200 transition-colors ml-2"
              title="Search workspaces and commands (Cmd+K / Ctrl+K)"
            >
              <Search className="w-3 h-3 text-zinc-400" />
              <span>Spotlight...</span>
              <kbd className="px-1 rounded bg-zinc-950 border border-zinc-800 text-[10px] text-zinc-400">
                ⌘K
              </kbd>
            </button>
          )}
        </div>

        {/* Center Live Probes (Synchronized Single Source of Truth) */}
        <div className="hidden md:flex items-center gap-4 text-xs font-mono text-zinc-400">
          <div className="flex items-center gap-1.5" title="FastAPI Core Application Status">
            <span className={`w-2 h-2 rounded-full ${isOnline ? 'bg-emerald-400' : 'bg-rose-500 animate-pulse'}`} />
            <span className="text-zinc-300">FastAPI</span>
            <span className={isOnline ? 'text-emerald-400 font-medium' : 'text-rose-400 font-medium'}>
              {isOnline ? 'ONLINE' : 'OFFLINE'}
            </span>
          </div>

          <div className="h-3 w-px bg-zinc-800" />

          <div className="flex items-center gap-1.5" title="Celery Redis Message Broker Status">
            <Database className="w-3.5 h-3.5 text-zinc-400" />
            <span className="text-zinc-300">Redis:</span>
            <span className={isOnline ? 'text-emerald-400 font-medium' : 'text-rose-400 font-medium'}>
              {isOnline ? 'READY' : 'DISCONNECTED'}
            </span>
          </div>

          <div className="h-3 w-px bg-zinc-800" />

          <div className="flex items-center gap-1.5" title="Active Celery Worker Containers">
            <Activity className="w-3.5 h-3.5 text-zinc-400" />
            <span className="text-zinc-300">Active Workers:</span>
            <span className="text-zinc-100 font-semibold tabular-nums">{isOnline ? health?.activeWorkers ?? 1 : 0}</span>
          </div>

          <div className="h-3 w-px bg-zinc-800" />

          <div className="flex items-center gap-1.5" title="Current Ingestion Queue Backlog">
            <span className="text-zinc-400">Queue Depth:</span>
            <span className="text-zinc-100 font-semibold tabular-nums">{isOnline ? health?.queueDepth ?? 0 : 0}</span>
          </div>
        </div>

        {/* Right Controls */}
        <div className="flex items-center gap-3">
          <a
            href="/api/v1/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 text-xs font-mono text-zinc-300 hover:text-zinc-100 px-2.5 py-1 rounded border border-zinc-800 hover:border-zinc-700 bg-zinc-900/60 transition-colors"
            title="Open OpenAPI Swagger UI"
          >
            <Terminal className="w-3.5 h-3.5 text-zinc-400" />
            <span className="hidden sm:inline">OpenAPI Docs</span>
            <ExternalLink className="w-3 h-3 opacity-60" />
          </a>

          <div className="flex items-center gap-2 pl-2 border-l border-zinc-800">
            <div className="w-6 h-6 rounded bg-zinc-800 border border-zinc-700 flex items-center justify-center font-mono text-[11px] font-bold text-zinc-300">
              OP
            </div>
            <span className="text-xs font-medium text-zinc-300 hidden lg:inline">
              lead.operator
            </span>
          </div>
        </div>
      </header>
    </div>
  );
};
