import { useState } from 'react';
import { IngestionDock } from '../components/ingestion/IngestionDock';
import { DocumentPreviewPanel } from '../components/ingestion/DocumentPreviewPanel';
import { LiveStreamTable } from '../components/ingestion/LiveStreamTable';

export interface IngestionTask {
  id: string;
  documentName: string;
  schema: string;
  schemaBadge: string;
  priority: 'P0' | 'P1' | 'P2';
  confidence: number;
  latencyMs: number;
  status: 'Completed' | 'Tax Discrepancy' | 'Needs Review';
  statusDetails?: string;
  timestamp: string;
  extractedFields?: Array<{ field: string; value: string; confidence: number; isAnomaly?: boolean }>;
}

const INITIAL_TASKS: IngestionTask[] = [
  {
    id: 'task_e847c91a',
    documentName: 'INV-2026-8894.pdf',
    schema: 'Commercial Invoices',
    schemaBadge: 'v2.1',
    priority: 'P0',
    confidence: 94.2,
    latencyMs: 640,
    status: 'Tax Discrepancy',
    statusDetails: 'Calculated tax variance (68% vs 85% expected)',
    timestamp: 'Just now',
    extractedFields: [
      { field: 'Invoice ID', value: 'INV-2026-8894', confidence: 99.8 },
      { field: 'Vendor Name', value: 'Apex Global Logistics LLC', confidence: 98.4 },
      { field: 'Tax Rate', value: '68% (Discrepant)', confidence: 91.2, isAnomaly: true },
      { field: 'Total Amount', value: '$14,820.00 USD', confidence: 99.1 }
    ]
  },
  {
    id: 'task_b921fa02',
    documentName: 'Cloudflare_Subscription_Q3.pdf',
    schema: 'Commercial Invoices',
    schemaBadge: 'v2.1',
    priority: 'P1',
    confidence: 98.5,
    latencyMs: 412,
    status: 'Completed',
    timestamp: '2m ago',
    extractedFields: [
      { field: 'Invoice ID', value: 'CF-99120-Q3', confidence: 99.9 },
      { field: 'Vendor Name', value: 'Cloudflare, Inc.', confidence: 99.5 },
      { field: 'Total Amount', value: '$2,400.00 USD', confidence: 98.9 }
    ]
  },
  {
    id: 'task_3821a99f',
    documentName: 'Uber_Business_Receipt_98.png',
    schema: 'Point-of-Sale Receipts',
    schemaBadge: 'v1.0',
    priority: 'P2',
    confidence: 72.4,
    latencyMs: 380,
    status: 'Needs Review',
    statusDetails: 'Model confidence below 75% threshold',
    timestamp: '5m ago',
    extractedFields: [
      { field: 'Merchant', value: 'Uber Technologies Inc', confidence: 84.1 },
      { field: 'Trip Fare', value: '$42.50', confidence: 71.0, isAnomaly: true },
      { field: 'Tip Amount', value: '$5.00', confidence: 68.2, isAnomaly: true }
    ]
  },
  {
    id: 'task_1120aa44',
    documentName: 'Master_Services_Agmt_v4.pdf',
    schema: 'Enterprise Contracts & MSAs',
    schemaBadge: 'v1.4',
    priority: 'P0',
    confidence: 91.2,
    latencyMs: 820,
    status: 'Completed',
    timestamp: '8m ago',
    extractedFields: [
      { field: 'Contract Type', value: 'Master Services Agreement', confidence: 95.0 },
      { field: 'Effective Date', value: '2026-10-01', confidence: 92.4 },
      { field: 'Governing Law', value: 'State of Delaware', confidence: 88.5 }
    ]
  }
];

export interface IngestionStudioProps {
  onJobCreated?: (jobId: string, documentId: string) => void;
  onNavigateToReview?: (documentId: string) => void;
}

export function IngestionStudio({ onJobCreated, onNavigateToReview }: IngestionStudioProps) {
  const [tasks, setTasks] = useState<IngestionTask[]>(INITIAL_TASKS);
  const [selectedTask, setSelectedTask] = useState<IngestionTask | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleDispatch = (payload: { file: File; schema: string; priority: 'P0' | 'P1' | 'P2' }) => {
    setIsSubmitting(true);
    setTimeout(() => {
      const newTaskId = `task_${Math.random().toString(16).slice(2, 10)}`;
      const newDocId = `doc_${Math.random().toString(16).slice(2, 10)}`;
      const newTask: IngestionTask = {
        id: newTaskId,
        documentName: payload.file.name,
        schema: payload.schema,
        schemaBadge: 'v2.1',
        priority: payload.priority,
        confidence: 96.4,
        latencyMs: 480,
        status: 'Completed',
        timestamp: 'Just now',
        extractedFields: [
          { field: 'Document Title', value: payload.file.name.replace(/\.[^/.]+$/, ''), confidence: 97.2 },
          { field: 'Extraction Engine', value: 'Multimodal v1.5', confidence: 99.0 }
        ]
      };
      setTasks((prev) => [newTask, ...prev]);
      setSelectedTask(newTask);
      setIsSubmitting(false);
      if (onJobCreated) onJobCreated(newTaskId, newDocId);
    }, 750);
  };

  return (
    <div className="w-full max-w-[1680px] mx-auto p-4 sm:p-6 flex flex-col gap-6 overflow-x-hidden">
      {/* Dual-Pane Viewport Section */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
        <div className="lg:col-span-5 xl:col-span-4 flex flex-col">
          <IngestionDock isSubmitting={isSubmitting} onDispatch={handleDispatch} />
        </div>
        <div className="lg:col-span-7 xl:col-span-8 flex flex-col">
          <DocumentPreviewPanel
            selectedTask={selectedTask}
            onClose={() => setSelectedTask(null)}
            onNavigateToReview={onNavigateToReview}
          />
        </div>
      </div>

      {/* Real-time Ingestion Stream Table */}
      <div className="w-full">
        <LiveStreamTable
          tasks={tasks}
          selectedTaskId={selectedTask?.id}
          onSelectTask={(task) => setSelectedTask(task)}
        />
      </div>
    </div>
  );
}
