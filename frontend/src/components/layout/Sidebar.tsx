import React from 'react';
import { UploadCloud, Workflow, CheckSquare, BarChart3 } from 'lucide-react';

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
  activeDocId,
}) => {
  const navItems = [
    {
      id: 'ingestion' as ActiveTab,
      label: 'Ingestion Studio',
      icon: UploadCloud,
      badge: '15MB',
    },
    {
      id: 'pipeline' as ActiveTab,
      label: 'Pipeline Monitor',
      icon: Workflow,
      badge: activeJobId ? 'Active' : undefined,
    },
    {
      id: 'reviewer' as ActiveTab,
      label: 'HITL Reviewer',
      icon: CheckSquare,
      badge: 'Split View',
    },
    {
      id: 'observability' as ActiveTab,
      label: 'DLQ & Telemetry',
      icon: BarChart3,
      badge: 'Live',
    },
  ];

  return (
    <aside className="w-56 border-r border-[#27272a] bg-[#121215] p-2.5 flex flex-col justify-between shrink-0 select-none">
      <div className="space-y-3">
        <div className="px-2 pt-1">
          <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-500 font-semibold">
            Workspaces
          </span>
        </div>

        <nav className="space-y-0.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;

            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full text-left px-2.5 py-2 rounded border text-xs font-medium transition-colors flex items-center justify-between ${
                  isActive
                    ? 'bg-zinc-800 border-zinc-700 text-zinc-100 shadow-sm'
                    : 'bg-transparent border-transparent hover:bg-zinc-800/50 hover:text-zinc-200 text-zinc-400'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-zinc-100' : 'text-zinc-400'}`} />
                  <span>{item.label}</span>
                </div>

                {item.badge && (
                  <span
                    className={`text-[10px] font-mono px-1.5 py-0.2 rounded border ${
                      isActive
                        ? 'bg-zinc-900 text-zinc-300 border-zinc-700'
                        : 'bg-zinc-900/50 text-zinc-500 border-zinc-800'
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

      {/* Operator Metadata Footnote */}
      <div className="p-2.5 rounded border border-zinc-800/80 bg-zinc-900/30 text-[11px] font-mono text-zinc-500 space-y-1">
        <div className="flex items-center justify-between text-zinc-400">
          <span>Target Engine</span>
          <span className="text-zinc-200">Gemini 1.5</span>
        </div>
        <div className="flex items-center justify-between">
          <span>Schema Contract</span>
          <span className="text-zinc-300">Pydantic v2</span>
        </div>
      </div>
    </aside>
  );
};
