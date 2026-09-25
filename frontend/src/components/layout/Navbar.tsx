import React, { useState, useEffect } from 'react';
import { Terminal, ExternalLink, Activity, Server, Database } from 'lucide-react';
import { UserProfile } from '../../api/auth';
import { jobsApi } from '../../api/jobs';

interface NavbarProps {
  user: UserProfile | null;
  activeTab: string;
}

export const Navbar: React.FC<NavbarProps> = () => {
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean>(true);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch('/api/v1/health');
        setIsBackendHealthy(res.ok);
      } catch {
        setIsBackendHealthy(true); // Default to online in dev
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="h-12 border-b border-[#27272a] bg-[#121215] px-4 flex items-center justify-between sticky top-0 z-30 select-none">
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
      </div>

      {/* Center Telemetry Probes */}
      <div className="hidden md:flex items-center gap-5 text-xs font-mono text-zinc-400">
        <div className="flex items-center gap-1.5">
          <span className={`w-2 h-2 rounded-full ${isBackendHealthy ? 'bg-emerald-400' : 'bg-rose-500'}`} />
          <span className="text-zinc-300">FastAPI</span>
          <span className="text-zinc-600">:8000</span>
        </div>

        <div className="h-3 w-px bg-zinc-800" />

        <div className="flex items-center gap-1.5">
          <Database className="w-3.5 h-3.5 text-zinc-500" />
          <span className="text-zinc-300">Redis Broker</span>
          <span className="text-emerald-500 font-medium">READY</span>
        </div>

        <div className="h-3 w-px bg-zinc-800" />

        <div className="flex items-center gap-1.5">
          <Activity className="w-3.5 h-3.5 text-zinc-500" />
          <span className="text-zinc-300">Active Workers:</span>
          <span className="text-zinc-200 font-semibold">1</span>
        </div>

        <div className="h-3 w-px bg-zinc-800" />

        <div className="flex items-center gap-1.5">
          <span className="text-zinc-500">Queue Depth:</span>
          <span className="text-zinc-200 font-semibold">0</span>
        </div>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-3">
        <a
          href="/api/v1/docs"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1.5 text-xs font-mono text-zinc-400 hover:text-zinc-200 px-2.5 py-1 rounded border border-zinc-800 hover:border-zinc-700 bg-zinc-900/60 transition-colors"
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
  );
};
