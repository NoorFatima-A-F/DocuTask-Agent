import React from 'react';
import { UploadCloud, Workflow, CheckSquare, BarChart3, ShieldCheck, Cpu } from 'lucide-react';

export type ActiveTab = 'ingestion' | 'pipeline' | 'reviewer' | 'observability';

interface SidebarProps {
  activeTab: ActiveTab;
  setActiveTab: (tab: ActiveTab) => void;
  activeJobId?: string | null;
  activeDocId?: string | null;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  setActiveTab,
  activeJobId,
}) => {
  const navItems = [
    {
      id: 'ingestion' as ActiveTab,
      label: 'Ingestion Studio',
      icon: UploadCloud,
      badge: undefined,
    },
    {
      id: 'pipeline' as ActiveTab,
      label: 'Pipeline Monitor',
      icon: Workflow,
      badge: activeJobId ? 'Active' : undefined,
      badgeColor: 'bg-emerald-950/60 text-emerald-400 border-emerald-800/60',
    },
    {
      id: 'reviewer' as ActiveTab,
      label: 'HITL Reviewer',
      icon: CheckSquare,
      badge: '2 Pending',
      badgeColor: 'bg-amber-950/60 text-amber-400 border-amber-800/60',
    },
    {
      id: 'observability' as ActiveTab,
      label: 'DLQ & Telemetry',
      icon: BarChart3,
      badge: 'Healthy',
      badgeColor: 'bg-emerald-950/60 text-emerald-400 border-emerald-800/60',
    },
  ];

  return (
    <aside
      aria-label="Workspaces navigation"
      className="w-64 shrink-0 border-r border-zinc-800 bg-[#121215] p-3 flex flex-col justify-between h-full select-none z-20"
    >
      <div className="space-y-4">
        {/* Brand Header */}
        <div className="flex items-center gap-2.5 px-2 py-1.5 border-b border-zinc-800/80">
          <div className="w-6 h-6 rounded bg-indigo-600 flex items-center justify-center text-white font-bold text-xs font-mono shadow-sm">
            D
          </div>
          <div className="flex flex-col">
            <div className="flex items-center gap-1.5">
              <span className="font-semibold text-sm text-zinc-100 tracking-tight">DocuTask</span>
              <span className="font-mono text-[10px] text-zinc-400 bg-zinc-900 border border-zinc-800 px-1 py-0.2 rounded">
                v1.0.0
              </span>
            </div>
            <span className="text-[10px] text-zinc-400 font-mono">Document Intelligence</span>
          </div>
        </div>

        {/* Workspace Navigation Header & List */}
        <div className="space-y-1">
          <div className="px-2 pb-1">
            <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-400 font-semibold">
              Workspaces
            </span>
          </div>

          <nav role="navigation" className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;

              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full text-left px-3 py-2 rounded-lg border text-xs font-medium transition-all flex items-center justify-between cursor-pointer focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none ${
                    isActive
                      ? 'bg-zinc-800/90 border-zinc-700 text-zinc-100 shadow-sm'
                      : 'bg-transparent border-transparent hover:bg-zinc-800/40 hover:text-zinc-200 text-zinc-400'
                  }`}
                >
                  <div className="flex items-center gap-2.5">
                    <Icon className={`w-4 h-4 ${isActive ? 'text-indigo-400' : 'text-zinc-400'}`} />
                    <span>{item.label}</span>
                  </div>

                  {item.badge && (
                    <span
                      className={`text-[10px] font-mono px-1.5 py-0.5 rounded border ${
                        item.badgeColor || (isActive ? 'bg-zinc-900 text-zinc-200 border-zinc-700' : 'bg-zinc-900/50 text-zinc-400 border-zinc-800')
                      }`}
                    >
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Operator Metadata Footnote (WCAG AA compliant contrast) */}
      <div className="p-3 rounded-lg border border-zinc-800 bg-zinc-950/60 text-[11px] font-mono text-zinc-400 space-y-1.5">
        <div className="flex items-center justify-between">
          <span className="text-zinc-400 flex items-center gap-1.5">
            <Cpu className="w-3.5 h-3.5 text-zinc-400" />
            <span>LLM Engine</span>
          </span>
          <span className="text-zinc-200 font-medium">Multimodal v1.5</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-zinc-400 flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>Schema Rules</span>
          </span>
          <span className="text-emerald-400 font-medium">Validated</span>
        </div>
      </div>
    </aside>
  );
};
