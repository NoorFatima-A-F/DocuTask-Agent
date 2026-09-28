import React, { useState, useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppShell } from './components/layout/AppShell';
import { ActiveTab } from './components/layout/Sidebar';
import { DragDropZone } from './components/ingestion/DragDropZone';
import { AsyncStepper } from './components/pipeline/AsyncStepper';
import { TwoPaneReviewer } from './components/reviewer/TwoPaneReviewer';
import { MetricsSummary } from './components/observability/MetricsSummary';
import { ToastProvider, useToast } from './components/common/Toast';
import { CommandPalette } from './components/common/CommandPalette';
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
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState<boolean>(false);
  const { success, info } = useToast();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsCommandPaletteOpen((prev) => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleJobCreated = (jobId: string, documentId: string) => {
    setActiveJobId(jobId);
    setActiveDocId(documentId);
    setActiveTab('pipeline');
    success('Document Enqueued', `Job ${jobId} successfully dispatched to pipeline.`);
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
        onOpenCommandPalette={() => setIsCommandPaletteOpen(true)}
      >
        {activeTab === 'ingestion' && (
          <DragDropZone
            onJobCreated={handleJobCreated}
            onNavigateToReview={handleNavigateToReview}
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

      <CommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
        onNavigate={(tab) => setActiveTab(tab)}
        onTriggerDiagnostic={handleTriggerDiagnostic}
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
