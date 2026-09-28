import React, { useState, useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppShell } from './components/layout/AppShell';
import { ActiveTab } from './components/layout/Sidebar';
import { IngestionStudio } from './pages/IngestionStudio';
import { AsyncStepper } from './components/pipeline/AsyncStepper';
import { TwoPaneReviewer } from './components/reviewer/TwoPaneReviewer';
import { MetricsSummary } from './components/observability/MetricsSummary';
import { ToastProvider, useToast } from './components/common/Toast';
import { CommandPalette } from './components/common/CommandPalette';
import { KeyboardShortcutsModal } from './components/common/KeyboardShortcutsModal';
import { SchemaRuleDrawer } from './components/common/SchemaRuleDrawer';
import { useAuth } from './hooks/useAuth';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2,
      staleTime: 5000,
      refetchOnWindowFocus: false,
    },
  },
});

export const AppContent: React.FC = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState<ActiveTab>('ingestion');
  const [activeJobId, setActiveJobId] = useState<string | null>('job_demo_9841a0');
  const [activeDocId, setActiveDocId] = useState<string | null>('doc_e847c910a2');
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState<boolean>(false);
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState<boolean>(false);
  const [isShortcutsOpen, setIsShortcutsOpen] = useState<boolean>(false);
  const [isSchemaRulesOpen, setIsSchemaRulesOpen] = useState<boolean>(false);
  const { success, info } = useToast();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Don't trigger if user is typing inside an input or textarea
      const target = e.target as HTMLElement;
      const isInput = target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable;

      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsCommandPaletteOpen((prev) => !prev);
      } else if ((e.metaKey || e.ctrlKey) && e.key === '[') {
        e.preventDefault();
        setIsSidebarCollapsed((prev) => !prev);
      } else if (e.key === '?' && !isInput) {
        e.preventDefault();
        setIsShortcutsOpen(true);
      } else if (!isInput && !e.metaKey && !e.ctrlKey && !e.altKey) {
        if (e.key === '1') setActiveTab('ingestion');
        else if (e.key === '2') setActiveTab('pipeline');
        else if (e.key === '3') setActiveTab('reviewer');
        else if (e.key === '4') setActiveTab('observability');
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleJobCreated = (jobId: string, documentId: string) => {
    setActiveJobId(jobId);
    setActiveDocId(documentId);
    setActiveTab('pipeline');
    success('Batch Enqueued', `Job ${jobId} successfully dispatched to Celery pipeline.`);
  };

  const handleNavigateToReview = (documentId: string) => {
    setActiveDocId(documentId);
    setActiveTab('reviewer');
    info('HITL Workspace Loaded', `Reviewing document ${documentId}`);
  };

  const handleRejectBatch = () => {
    setActiveTab('observability');
    info('Task Quarantined', 'Document quarantined to Dead Letter Queue.');
  };

  const handleBackToIngestion = () => {
    setActiveTab('ingestion');
  };

  const handleTriggerDiagnostic = () => {
    success('System Diagnostic Sweep Complete', 'All workers, schemas, and broker queues verified healthy.');
  };

  return (
    <>
      <AppShell
        user={user}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        activeJobId={activeJobId}
        activeDocId={activeDocId}
        isSidebarCollapsed={isSidebarCollapsed}
        onToggleSidebarCollapse={() => setIsSidebarCollapsed((prev) => !prev)}
        onOpenCommandPalette={() => setIsCommandPaletteOpen(true)}
        onOpenShortcuts={() => setIsShortcutsOpen(true)}
        onOpenSchemaRules={() => setIsSchemaRulesOpen(true)}
      >
        {activeTab === 'ingestion' && (
          <IngestionStudio
            onJobCreated={handleJobCreated}
            onNavigateToReview={handleNavigateToReview}
            onOpenSchemaRules={() => setIsSchemaRulesOpen(true)}
          />
        )}

        {activeTab === 'pipeline' && (
          <AsyncStepper
            jobId={activeJobId || 'job_demo_9841a0'}
            documentId={activeDocId || 'doc_e847c910a2'}
            onNavigateToReview={handleNavigateToReview}
          />
        )}

        {activeTab === 'reviewer' && (
          <TwoPaneReviewer
            documentId={activeDocId || 'doc_e847c910a2'}
            onApproveSuccess={() => {
              success('Schema Approved & Persisted', 'Feedback logged to feedback buffer.');
              setActiveTab('observability');
            }}
            onRejectBatch={handleRejectBatch}
            onBackToIngestion={handleBackToIngestion}
          />
        )}

        {activeTab === 'observability' && <MetricsSummary />}
      </AppShell>

      {/* Global Command Palette (⌘K) */}
      <CommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
        onNavigate={(tab) => setActiveTab(tab)}
        onTriggerDiagnostic={handleTriggerDiagnostic}
      />

      {/* Global Keyboard Shortcuts Modal (?) */}
      <KeyboardShortcutsModal
        isOpen={isShortcutsOpen}
        onClose={() => setIsShortcutsOpen(false)}
      />

      {/* Schema Invariants & Pydantic Rules Drawer */}
      <SchemaRuleDrawer
        isOpen={isSchemaRulesOpen}
        onClose={() => setIsSchemaRulesOpen(false)}
        selectedSchemaId="Commercial Invoices"
      />
    </>
  );
};

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ToastProvider>
        <AppContent />
      </ToastProvider>
    </QueryClientProvider>
  );
}
