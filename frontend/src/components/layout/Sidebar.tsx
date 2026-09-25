import React from 'react';
import {
  UploadCloud,
  Workflow,
  CheckSquare,
  BarChart3,
  Layers,
  Sparkles,
} from 'lucide-react';

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
      label: 'Ingestion Hub',
      path: '/upload',
      icon: UploadCloud,
      badge: 'Defensive',
      description: 'Magic byte sniff & 15MB guard',
    },
    {
      id: 'pipeline' as ActiveTab,
      label: 'Pipeline Monitor',
      path: activeJobId ? `/jobs/${activeJobId.substring(0, 8)}` : '/jobs',
      icon: Workflow,
      badge: activeJobId ? 'Active' : undefined,
      badgeColor: 'text-cyan-400 bg-cyan-500/10 border-cyan-500/30',
      description: 'Asynchronous 5-milestone state machine',
    },
    {
      id: 'reviewer' as ActiveTab,
      label: 'HITL Reviewer',
      path: activeDocId ? `/documents/${activeDocId.substring(0, 8)}/review` : '/reviewer',
      icon: CheckSquare,
      badge: 'Two-Pane',
      badgeColor: 'text-amber-400 bg-amber-500/10 border-amber-500/30',
      description: 'Confidence-gated schema & bounding box',
    },
    {
      id: 'observability' as ActiveTab,
      label: 'Observability & DLQ',
      path: '/dashboard',
      icon: BarChart3,
      badge: 'Real-Time',
      badgeColor: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30',
      description: 'KPIs, dead letter queue & replay',
    },
  ];

  return (
    <aside className="w-64 border-r border-slate-800/80 bg-slate-950/60 p-3 flex flex-col justify-between shrink-0">
      <div className="space-y-4">
        <div className="px-3 pt-2">
          <span className="text-[11px] font-mono uppercase tracking-wider text-slate-400 font-semibold flex items-center gap-1.5">
            <Layers className="w-3 h-3 text-indigo-400" />
            Core Workspaces
          </span>
        </div>

        <nav className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;

            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full text-left p-2.5 rounded-lg border transition-all flex flex-col gap-1 ${
                  isActive
                    ? 'bg-slate-900 border-indigo-500/40 shadow-sm shadow-indigo-500/10'
                    : 'bg-transparent border-transparent hover:bg-slate-900/50 hover:border-slate-800 text-slate-400'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <Icon
                      className={`w-4 h-4 ${
                        isActive ? 'text-indigo-400' : 'text-slate-400'
                      }`}
                    />
                    <span
                      className={`text-xs font-semibold ${
                        isActive ? 'text-slate-100' : 'text-slate-300'
                      }`}
                    >
                      {item.label}
                    </span>
                  </div>

                  {item.badge && (
                    <span
                      className={`text-[10px] font-mono px-1.5 py-0.2 rounded border ${
                        item.badgeColor ||
                        'text-indigo-400 bg-indigo-500/10 border-indigo-500/30'
                      }`}
                    >
                      {item.badge}
                    </span>
                  )}
                </div>

                <div className="flex items-center justify-between text-[10px] font-mono text-slate-400 pl-6.5">
                  <span className="truncate">{item.description}</span>
                </div>
              </button>
            );
          })}
        </nav>
      </div>

      {/* System Status Footnote */}
      <div className="p-3 rounded-lg border border-slate-800/80 bg-slate-900/40 space-y-2">
        <div className="flex items-center justify-between text-[11px]">
          <span className="text-slate-400 font-mono flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-amber-400" />
            Distillation
          </span>
          <span className="font-mono text-emerald-400 text-[10px] bg-emerald-500/10 px-1.5 py-0.5 rounded border border-emerald-500/30">
            Active
          </span>
        </div>
        <p className="text-[10px] text-slate-400 leading-relaxed">
          Human corrections are dispatched directly to <code className="text-indigo-300">/api/v1/runtime/feedback</code> for continuous policy distillation.
        </p>
      </div>
    </aside>
  );
};
