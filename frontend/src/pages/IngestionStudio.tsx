import React, { useState } from 'react';
import { IngestionDock, IngestionQueueRow } from '../components/ingestion/IngestionDock';
import { DocumentPreviewPanel } from '../components/ingestion/DocumentPreviewPanel';
import { LiveStreamTable } from '../components/ingestion/LiveStreamTable';
import { useDocumentUpload } from '../hooks/useDocumentUpload';

interface IngestionStudioProps {
  onJobCreated?: (jobId: string, documentId: string) => void;
  onNavigateToReview?: (documentId: string) => void;
}

const INITIAL_QUEUE: IngestionQueueRow[] = [
  {
    taskId: 'task_e847c91a',
    documentId: 'doc_e847c910a2',
    filename: 'INV-2026-8894.pdf',
    schemaType: 'InvoiceTaxonomy.v2',
    priority: 'P0',
    confidence: 94.2,
    latencyMs: 640,
    status: 'Tax Discrepancy',
    reviewReason: 'Calculated tax variance (68% vs 85% expected)',
    timestamp: '1 min ago',
  },
  {
    taskId: 'task_b921fa02',
    documentId: 'doc_b921fa0281',
    filename: 'Cloudflare_Subscription_Q3.pdf',
    schemaType: 'InvoiceTaxonomy.v2',
    priority: 'P1',
    confidence: 98.5,
    latencyMs: 412,
    status: 'Completed',
    timestamp: '8 mins ago',
  },
  {
    taskId: 'task_3821a99f',
    documentId: 'doc_3821a99fa4',
    filename: 'Uber_Business_Receipt_98.png',
    schemaType: 'CommercialReceipt.v1',
    priority: 'P2',
    confidence: 72.4,
    latencyMs: 380,
    status: 'Needs Review',
    reviewReason: 'Model confidence below 75% threshold',
    timestamp: '22 mins ago',
  },
  {
    taskId: 'task_1120aa44',
    documentId: 'doc_1120aa44bc',
    filename: 'Master_Services_Agmt_v4.pdf',
    schemaType: 'EnterpriseContract.v1',
    priority: 'P0',
    confidence: 91.2,
    latencyMs: 820,
    status: 'Completed',
    timestamp: '1 hour ago',
  },
];

export const IngestionStudio: React.FC<IngestionStudioProps> = ({
  onJobCreated,
  onNavigateToReview,
}) => {
  const [tasks, setTasks] = useState<IngestionQueueRow[]>(INITIAL_QUEUE);
  const [selectedTask, setSelectedTask] = useState<IngestionQueueRow | null>(null);

  const { isUploading: isSubmitting, uploadProgress, uploadAndProcess } = useDocumentUpload(
    (jobId, documentId) => {
      const newTask: IngestionQueueRow = {
        taskId: `task_${jobId.substring(0, 8)}`,
        documentId: documentId,
        filename: 'staged_document.pdf',
        schemaType: 'InvoiceTaxonomy.v2',
        priority: 'P0',
        confidence: 94.2,
        latencyMs: 640,
        status: 'Tax Discrepancy',
        reviewReason: 'Calculated tax variance (68% vs 85% expected)',
        timestamp: 'Just now',
      };
      setTasks((prev) => [newTask, ...prev]);
      setSelectedTask(newTask);
      if (onJobCreated) onJobCreated(jobId, documentId);
    }
  );

  const handleDispatch = async (file: File, schemaType: string, priority: 'P0' | 'P1' | 'P2') => {
    await uploadAndProcess(file);
  };

  const handleInspectTask = (task: IngestionQueueRow) => {
    setSelectedTask(task);
  };

  return (
    <div className="mx-auto flex w-full max-w-[1680px] flex-col gap-6">
      {/* Workspace Dual-Pane Grid */}
      <div className="grid grid-cols-1 items-stretch gap-6 lg:grid-cols-12">
        <div className="lg:col-span-5 xl:col-span-4">
          <IngestionDock
            isSubmitting={isSubmitting}
            uploadProgress={uploadProgress}
            onDispatch={handleDispatch}
          />
        </div>
        <div className="lg:col-span-7 xl:col-span-8">
          <DocumentPreviewPanel
            selectedTask={selectedTask}
            onClearSelection={() => setSelectedTask(null)}
            onNavigateToReview={onNavigateToReview}
          />
        </div>
      </div>

      {/* Real-time Task Stream Table */}
      <div className="w-full">
        <LiveStreamTable
          tasks={tasks}
          selectedTaskId={selectedTask?.taskId}
          onInspectTask={handleInspectTask}
        />
      </div>
    </div>
  );
};
