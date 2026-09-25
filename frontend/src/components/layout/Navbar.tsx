import React from 'react';
import {
  FileText,
  Activity,
  ShieldCheck,
  Terminal,
  ExternalLink,
} from 'lucide-react';
import { UserProfile } from '../../api/auth';

interface NavbarProps {
  user: UserProfile | null;
  activeTab: string;
}

export const Navbar: React.FC<NavbarProps> = ({ user }) => {
  return (
    <header className="h-14 border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md px-4 flex items-center justify-between sticky top-0 z-30">
      {/* Brand & Platform Identity */}
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-cyan-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
          <FileText className="w-4 h-4 text-white" />
        </div>
        <div className="flex flex-col">
          <div className="flex items-center gap-2">
            <span className="font-bold text-sm text-slate-100 tracking-tight">DocuTask Agent</span>
            <span className="text-[10px] font-mono font-semibold px-1.5 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/30">
              v1.0.0-PROD
            </span>
          </div>
          <span className="text-[11px] text-slate-400 hidden sm:inline">
            Enterprise Multimodal Document Intelligence & HITL Platform
          </span>
        </div>
      </div>

      {/* Center Engine Telemetry Indicator */}
      <div className="hidden md:flex items-center gap-4 text-xs font-mono text-slate-400">
        <div className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-slate-300">FastAPI Gateway</span>
          <span className="text-slate-600">:8000</span>
        </div>
        <div className="h-3 w-px bg-slate-800" />
        <div className="flex items-center gap-1.5">
          <Activity className="w-3.5 h-3.5 text-indigo-400" />
          <span>Celery & Redis</span>
          <span className="text-emerald-400 font-semibold">ONLINE</span>
        </div>
        <div className="h-3 w-px bg-slate-800" />
        <div className="flex items-center gap-1.5">
          <ShieldCheck className="w-3.5 h-3.5 text-cyan-400" />
          <span>Gemini 1.5</span>
          <span className="text-emerald-400 font-semibold">ACTIVE</span>
        </div>
      </div>

      {/* Right Controls & User Session */}
      <div className="flex items-center gap-3">
        <a
          href="/api/v1/docs"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1.5 text-xs font-mono text-slate-400 hover:text-slate-200 px-2.5 py-1.5 rounded-md border border-slate-800 hover:border-slate-700 bg-slate-900/60 transition-colors"
          title="Open Swagger OpenAPI Documentation"
        >
          <Terminal className="w-3.5 h-3.5 text-indigo-400" />
          <span className="hidden sm:inline">OpenAPI Docs</span>
          <ExternalLink className="w-3 h-3 opacity-60" />
        </a>

        {/* User Pill */}
        <div className="flex items-center gap-2 pl-2 border-l border-slate-800">
          <div className="w-7 h-7 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center font-mono text-xs font-bold text-slate-300">
            {user?.username?.substring(0, 2).toUpperCase() || 'OP'}
          </div>
          <div className="hidden lg:flex flex-col">
            <span className="text-xs font-medium text-slate-200 leading-none">
              {user?.username || 'lead.operator'}
            </span>
            <span className="text-[10px] text-emerald-400 font-mono">HITL Lead</span>
          </div>
        </div>
      </div>
    </header>
  );
};
