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
    <div className="min-h-screen w-full max-w-full overflow-x-hidden bg-zinc-950 text-zinc-100 flex flex-col font-sans antialiased selection:bg-zinc-800 selection:text-zinc-100">
      <Navbar user={user} activeTab={activeTab} onOpenCommandPalette={onOpenCommandPalette} />
      <div className="flex-1 flex flex-col lg:flex-row min-h-0 w-full max-w-full">
        <Sidebar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          activeJobId={activeJobId}
          activeDocId={activeDocId}
        />
        <main role="main" className="flex-1 min-h-0 min-w-0 w-full max-w-full bg-zinc-950 p-4 lg:p-6 flex flex-col overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
};
