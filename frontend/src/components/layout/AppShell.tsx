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
    <div className="flex h-screen w-full overflow-hidden bg-zinc-950 text-zinc-100 font-sans antialiased selection:bg-zinc-800 selection:text-zinc-100">
      {/* Persistent Left Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        activeJobId={activeJobId}
        activeDocId={activeDocId}
      />

      {/* Right Column: Top Navbar & Scrollable Primary Workspace */}
      <div className="flex flex-1 flex-col overflow-hidden min-w-0 h-screen">
        <Navbar user={user} activeTab={activeTab} onOpenCommandPalette={onOpenCommandPalette} />
        <main
          role="main"
          className="flex-1 overflow-y-auto w-full max-w-full bg-zinc-950 p-4 lg:p-6 flex flex-col min-h-0"
        >
          {children}
        </main>
      </div>
    </div>
  );
};
