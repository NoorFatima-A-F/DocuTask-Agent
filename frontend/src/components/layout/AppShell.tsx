import React from 'react';
import { Navbar } from './Navbar';
import { Sidebar, ActiveTab } from './Sidebar';
import { UserProfile } from '../../api/auth';

interface AppShellProps {
  user: UserProfile | null;
  activeTab: ActiveTab;
  setActiveTab: (tab: ActiveTab) => void;
  activeJobId?: string | null;
  activeDocId?: string | null;
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({
  user,
  activeTab,
  setActiveTab,
  activeJobId,
  activeDocId,
  children,
}) => {
  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 flex flex-col font-sans antialiased selection:bg-indigo-500/30 selection:text-indigo-200">
      <Navbar user={user} activeTab={activeTab} />
      <div className="flex-1 flex overflow-hidden">
        <Sidebar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          activeJobId={activeJobId}
          activeDocId={activeDocId}
        />
        <main className="flex-1 overflow-y-auto bg-slate-950/40 p-6 flex flex-col">
          {children}
        </main>
      </div>
    </div>
  );
};
