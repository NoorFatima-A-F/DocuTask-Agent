import React, { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppShell } from './components/layout/AppShell';
import { ActiveTab } from './components/layout/Sidebar';
import { DragDropZone } from './components/ingestion/DragDropZone';
import { AsyncStepper } from './components/pipeline/AsyncStepper';
import { TwoPaneReviewer } from './components/reviewer/TwoPaneReviewer';
import { MetricsSummary } from './components/observability/MetricsSummary';
import { useAuth } from './hooks/useAuth';

// Initialize React Query client with resilient defaults
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

  const handleJobCreated = (jobId: string, documentId: string) => {
    setActiveJobId(jobId);
    setActiveDocId(documentId);
    setActiveTab('pipeline');
  };

  const handleNavigateToReview = (documentId: string) => {
    setActiveDocId(documentId);
    setActiveTab('reviewer');
  };

  return (
    <AppShell
      user={user}
      activeTab={activeTab}
      setActiveTab={setActiveTab}
      activeJobId={activeJobId}
      activeDocId={activeDocId}
    >
      {activeTab === 'ingestion' && (
        <DragDropZone onJobCreated={handleJobCreated} />
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
          onApproveSuccess={() => setActiveTab('observability')}
        />
      )}

      {activeTab === 'observability' && <MetricsSummary />}
    </AppShell>
  );
};

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
}
