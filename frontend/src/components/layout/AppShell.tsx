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
  onOpenCommandPalette?: () => void;
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({
  user,
  activeTab,
  setActiveTab,
  activeJobId,
  activeDocId,
  onOpenCommandPalette,
  children,
}) => {
  return (
    <div className="min-h-screen lg:h-screen w-screen lg:overflow-hidden bg-[#09090b] text-zinc-100 flex flex-col font-sans antialiased selection:bg-zinc-800 selection:text-zinc-100">
      <Navbar user={user} activeTab={activeTab} onOpenCommandPalette={onOpenCommandPalette} />
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden min-h-0">
        <Sidebar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          activeJobId={activeJobId}
          activeDocId={activeDocId}
        />
        <main role="main" className="flex-1 h-full overflow-y-auto lg:overflow-hidden bg-[#09090b] p-3.5 flex flex-col min-h-0 min-w-0">
          {children}
        </main>
      </div>
    </div>
  );
};
