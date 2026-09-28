import React, { useState, useRef, ChangeEvent, DragEvent } from 'react';
import {
  UploadCloud,
  FileCheck,
  ArrowRight,
  Eye,
  RefreshCw,
  Loader2,
  AlertTriangle,
  CheckCircle2,
  X,
  FileText,
  Search,
  SlidersHorizontal,
  ExternalLink,
} from 'lucide-react';
import { validateDocumentFile } from '../../utils/fileValidation';
import { DocumentValidationResult } from '../../types/document';
import { useDocumentUpload } from '../../hooks/useDocumentUpload';
import { StatusBadge } from '../layout/StatusBadge';

export const SCHEMA_CONFIG: Record<string, { label: string; badge: string; description: string }> = {
  'InvoiceTaxonomy.v2': {
    label: 'Commercial Invoices',
    badge: 'v2.1',
    description: 'Extracts line items, VAT/tax breakdowns, and vendor details',
  },
  'CommercialReceipt.v1': {
    label: 'Point-of-Sale Receipts',
    badge: 'v1.0',
    description: 'Itemized totals, tip calculation, and payment tokens',
  },
  'EnterpriseContract.v1': {
    label: 'Enterprise Contracts & MSAs',
    badge: 'v1.4',
    description: 'Indemnity clauses, effective dates, and governing law',
  },
  'IdentityCredential.v1': {
    label: 'Identity & Passports',
    badge: 'v1.2',
    description: 'MRZ validation, biometric fields, and expiration dates',
  },
};

interface DragDropZoneProps {
  onJobCreated: (jobId: string, documentId: string) => void;
  onNavigateToReview: (documentId: string) => void;
}

export interface IngestionQueueRow {
  taskId: string;
  documentId: string;
  filename: string;
  schemaType: string;
  priority: 'P0' | 'P1' | 'P2';
  confidence: number;
  latencyMs: number;
  status: 'COMPLETED' | 'TAX_ANOMALY' | 'LOW_CONFIDENCE' | 'PROCESSING';
  reviewReason?: string;
  timestamp: string;
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
    status: 'TAX_ANOMALY',
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
    status: 'COMPLETED',
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
    status: 'LOW_CONFIDENCE',
    reviewReason: 'Model confidence (72.4%) below 75% threshold',
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
    status: 'COMPLETED',
    timestamp: '1 hour ago',
  },
];

export const DragDropZone: React.FC<DragDropZoneProps> = ({
  onJobCreated,
  onNavigateToReview,
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [schemaType, setSchemaType] = useState<string>('InvoiceTaxonomy.v2');
  const [priority, setPriority] = useState<string>('P0');
  const [validationResult, setValidationResult] = useState<DocumentValidationResult | null>(null);
  const [queue, setQueue] = useState<IngestionQueueRow[]>(INITIAL_QUEUE);
  const [isDragging, setIsDragging] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [isLive, setIsLive] = useState(true);
  const [selectedTaskPreview, setSelectedTaskPreview] = useState<IngestionQueueRow | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const { isUploading: isSubmitting, uploadProgress, uploadAndProcess } = useDocumentUpload(
    (jobId, documentId) => {
      const newRow: IngestionQueueRow = {
        taskId: `task_${jobId.substring(0, 8)}`,
        documentId: documentId,
        filename: selectedFile?.name || 'document.pdf',
        schemaType,
        priority: priority as 'P0' | 'P1' | 'P2',
        confidence: 94.2,
        latencyMs: 640,
        status: 'TAX_ANOMALY',
        reviewReason: 'Calculated tax variance (68% vs 85% expected)',
        timestamp: 'Just now',
      };
      setQueue((prev) => [newRow, ...prev]);
      setSelectedTaskPreview(newRow);
      onJobCreated(jobId, documentId);
    }
  );

  const handleFile = async (file: File) => {
    setSelectedFile(file);
    const result = await validateDocumentFile(file);
    setValidationResult(result);
  };

  const handleClearFile = (e: React.MouseEvent) => {
    e.stopPropagation();
    setSelectedFile(null);
    setValidationResult(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleDispatch = async () => {
    if (!selectedFile || (validationResult !== null && !validationResult.isValid)) return;
    await uploadAndProcess(selectedFile);
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = async (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      await handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleInputChange = async (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      await handleFile(e.target.files[0]);
    }
  };

  const filteredQueue = queue.filter((row) => {
    const matchesSearch =
      row.taskId.toLowerCase().includes(searchQuery.toLowerCase()) ||
      row.filename.toLowerCase().includes(searchQuery.toLowerCase()) ||
      row.schemaType.toLowerCase().includes(searchQuery.toLowerCase());

    if (!matchesSearch) return false;

    if (statusFilter === 'ALL') return true;
    if (statusFilter === 'ANOMALIES') return row.status !== 'COMPLETED';
    if (statusFilter === 'COMPLETED') return row.status === 'COMPLETED';
    return true;
  });

  return (
    <div className="w-full max-w-full space-y-6">
      {/* ========================================================================= */}
      {/* OBJECTIVE 1 & 4: SPLIT-PANE WORKSPACE (Ingestion Dock + Document Inspector) */}
      {/* ========================================================================= */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 w-full max-w-full">
        {/* --- LEFT COLUMN: Ingestion Dock (5 cols) --- */}
        <div className="lg:col-span-5 flex flex-col justify-between rounded-xl border border-zinc-800 bg-zinc-900/60 p-5 shadow-sm space-y-4">
          <div className="space-y-4">
            {/* Dock Header */}
            <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
              <div className="flex items-center gap-2">
                <UploadCloud className="h-4 w-4 text-indigo-400" />
                <h2 className="text-xs font-semibold uppercase tracking-wider text-zinc-200">
                  Ingestion Dock
                </h2>
              </div>
              <span className="rounded bg-zinc-800/80 px-2 py-0.5 text-[10px] font-mono font-medium text-zinc-400 border border-zinc-700/60">
                Max 15MB Payload
              </span>
            </div>

            {/* Dropzone Component */}
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleInputChange}
              accept=".pdf,.png,.jpg,.jpeg,.tiff,.tif"
              className="sr-only"
            />

            {!selectedFile ? (
              <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                role="button"
                tabIndex={0}
                aria-label="Click to upload or drag and drop document"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    fileInputRef.current?.click();
                  }
                }}
                className={`relative flex flex-col items-center justify-center rounded-xl border-2 border-dashed p-6 text-center transition-all cursor-pointer focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none ${
                  isDragging
                    ? 'border-indigo-500 bg-indigo-500/5'
                    : 'border-zinc-800 bg-zinc-900/30 hover:border-zinc-700 hover:bg-zinc-900/60'
                }`}
              >
                <UploadCloud className="h-9 w-9 text-zinc-400 mb-2 stroke-[1.5]" />
                <p className="text-sm font-medium text-zinc-200">
                  <span className="text-indigo-400 hover:underline">Click to upload</span> or drag and drop
                </p>
                <p className="mt-1 text-xs text-zinc-400">PDF, PNG, TIFF, or JPEG (Max 15MB)</p>
              </div>
            ) : (
              <div className="p-3.5 rounded-xl border border-zinc-700/80 bg-zinc-900/80 flex items-center justify-between gap-3">
                <div className="flex items-center gap-3 min-w-0 flex-1">
                  <div className="w-9 h-9 rounded-lg bg-zinc-800 border border-zinc-700 flex items-center justify-center shrink-0">
                    <FileText className="w-5 h-5 text-indigo-400" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="text-xs font-semibold text-zinc-100 truncate" title={selectedFile.name}>
                      {selectedFile.name}
                    </div>
                    <div className="flex items-center gap-2 text-[11px] font-mono text-zinc-400 mt-0.5">
                      <span>{(selectedFile.size / (1024 * 1024)).toFixed(2)} MB</span>
                      <span>•</span>
                      <span className="text-emerald-400 font-medium">
                        {validationResult?.detectedMimeType || 'Binary Validated'}
                      </span>
                    </div>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={handleClearFile}
                  className="p-1.5 rounded-md text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 transition-colors focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none"
                  aria-label="Remove staged document"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            )}

            {/* Validation Error Notice */}
            {validationResult && !validationResult.isValid && (
              <div className="p-3 rounded-lg border border-rose-800/50 bg-rose-950/30 text-rose-300 text-xs font-mono flex items-start gap-2.5">
                <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                <div className="space-y-0.5 flex-1 min-w-0">
                  <span className="font-semibold block text-rose-200">Magic Header Validation Failed</span>
                  <p className="text-[11px] leading-tight text-rose-300">{validationResult.error}</p>
                </div>
              </div>
            )}

            {/* Objective 3: Document Taxonomy Dropdown with SCHEMA_CONFIG */}
            <div className="space-y-1.5">
              <label htmlFor="schema-select" className="text-xs font-medium text-zinc-300 flex items-center justify-between">
                <span>Document Schema Taxonomy</span>
                <span className="text-[10px] font-mono text-zinc-400">
                  {SCHEMA_CONFIG[schemaType]?.badge || 'v2.1'}
                </span>
              </label>
              <select
                id="schema-select"
                value={schemaType}
                onChange={(e) => setSchemaType(e.target.value)}
                className="w-full bg-zinc-900 border border-zinc-700/80 rounded-lg px-3 py-2 text-xs text-zinc-200 font-medium focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none"
              >
                {Object.entries(SCHEMA_CONFIG).map(([key, config]) => (
                  <option key={key} value={key} className="bg-zinc-900 text-zinc-200 py-1">
                    {config.label} ({config.badge})
                  </option>
                ))}
              </select>
              <p className="text-[11px] text-zinc-400">
                {SCHEMA_CONFIG[schemaType]?.description}
              </p>
            </div>

            {/* Objective 2: Accessible Queue Priority Button Group */}
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-zinc-300 block">Queue Priority Policy</label>
              <div role="radiogroup" aria-label="Queue Priority" className="grid grid-cols-3 gap-2">
                {[
                  { id: 'P0', label: 'P0 — Critical', desc: 'Realtime SLA (<1s)' },
                  { id: 'P1', label: 'P1 — High', desc: 'Standard Queue' },
                  { id: 'P2', label: 'P2 — Batch', desc: 'Background Idle' },
                ].map((p) => {
                  const isActive = priority === p.id;
                  return (
                    <button
                      key={p.id}
                      type="button"
                      role="radio"
                      aria-checked={isActive}
                      onClick={() => setPriority(p.id)}
                      className={`flex flex-col items-center justify-center rounded-lg border px-3 py-2 transition-all focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none ${
                        isActive
                          ? 'border-indigo-500/80 bg-indigo-500/10 text-indigo-300 ring-1 ring-indigo-500/50 shadow-sm'
                          : 'border-zinc-800 bg-zinc-900/60 text-zinc-300 hover:border-zinc-700 hover:bg-zinc-800/60 hover:text-white'
                      }`}
                    >
                      <span className="text-xs font-semibold">{p.id}</span>
                      <span className="text-[10px] text-zinc-400">{p.desc}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Dispatch Ingestion CTA */}
          <div className="pt-2">
            <button
              type="button"
              disabled={!selectedFile || isSubmitting || (validationResult !== null && !validationResult.isValid)}
              onClick={handleDispatch}
              className="flex w-full items-center justify-center gap-2 rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition-all hover:bg-indigo-500 disabled:cursor-not-allowed disabled:bg-zinc-800 disabled:text-zinc-500 focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Routing to Pipeline ({uploadProgress}%)...</span>
                </>
              ) : (
                <>
                  <span>Dispatch Ingestion</span>
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </button>
          </div>
        </div>

        {/* --- RIGHT COLUMN: Document Preview / Extraction Inspector (7 cols) --- */}
        <div className="lg:col-span-7 flex flex-col h-full min-h-[420px]">
          {selectedTaskPreview ? (
            <div className="flex h-full flex-col justify-between rounded-xl border border-zinc-800 bg-zinc-900/60 p-5 shadow-sm space-y-4">
              <div className="space-y-4">
                <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
                  <div className="flex items-center gap-2">
                    <FileCheck className="h-4 w-4 text-emerald-400" />
                    <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-200">
                      Task Inspector Preview
                    </h3>
                  </div>
                  <span className="font-mono text-xs text-zinc-400">{selectedTaskPreview.taskId}</span>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="rounded-lg border border-zinc-800 bg-zinc-900/80 p-3">
                    <span className="text-[10px] uppercase font-mono text-zinc-400 block">File Name</span>
                    <span className="text-xs font-semibold text-zinc-100 truncate block mt-0.5" title={selectedTaskPreview.filename}>
                      {selectedTaskPreview.filename}
                    </span>
                  </div>
                  <div className="rounded-lg border border-zinc-800 bg-zinc-900/80 p-3">
                    <span className="text-[10px] uppercase font-mono text-zinc-400 block">Schema</span>
                    <span className="text-xs font-semibold text-zinc-100 block mt-0.5">
                      {SCHEMA_CONFIG[selectedTaskPreview.schemaType]?.label || selectedTaskPreview.schemaType}
                    </span>
                  </div>
                  <div className="rounded-lg border border-zinc-800 bg-zinc-900/80 p-3">
                    <span className="text-[10px] uppercase font-mono text-zinc-400 block">Confidence</span>
                    <span className="text-xs font-bold font-mono text-emerald-400 block mt-0.5 tabular-nums">
                      {selectedTaskPreview.confidence.toFixed(1)}%
                    </span>
                  </div>
                  <div className="rounded-lg border border-zinc-800 bg-zinc-900/80 p-3">
                    <span className="text-[10px] uppercase font-mono text-zinc-400 block">Latency</span>
                    <span className="text-xs font-bold font-mono text-zinc-300 block mt-0.5 tabular-nums">
                      {selectedTaskPreview.latencyMs}ms
                    </span>
                  </div>
                </div>

                <div className="rounded-lg border border-zinc-800 bg-zinc-950 p-4 space-y-2">
                  <span className="text-xs font-semibold text-zinc-300 block">Reasoning & Extraction Telemetry</span>
                  <StatusBadge status={selectedTaskPreview.status} reason={selectedTaskPreview.reviewReason} />
                </div>
              </div>

              <div className="pt-4 flex items-center justify-between border-t border-zinc-800">
                <button
                  type="button"
                  onClick={() => setSelectedTaskPreview(null)}
                  className="px-3 py-1.5 rounded-lg border border-zinc-800 bg-zinc-900 text-xs text-zinc-400 hover:text-zinc-200 transition-colors focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none"
                >
                  Clear Selection
                </button>
                <button
                  type="button"
                  onClick={() => onNavigateToReview(selectedTaskPreview.documentId)}
                  className="inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-xs font-semibold text-white hover:bg-indigo-500 transition-colors focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none shadow-sm"
                >
                  <Eye className="h-3.5 w-3.5" />
                  <span>Open in HITL Reviewer Canvas</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="flex h-full min-h-[420px] flex-col items-center justify-center rounded-xl border border-dashed border-zinc-800 bg-zinc-900/20 p-8 text-center">
              <div className="rounded-full bg-zinc-800/60 p-4 text-zinc-400 mb-3">
                <Search className="h-8 w-8 stroke-[1.5]" />
              </div>
              <h3 className="text-sm font-semibold text-zinc-200">No Document Selected</h3>
              <p className="mt-1 max-w-xs text-xs text-zinc-400">
                Drop a document on the left or select an ingested task from the stream below to preview OCR bounding boxes and field extractions.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* ========================================================================= */}
      {/* OBJECTIVE 3 & 5: LIVE INGESTION STREAM TABLE & TOOLBAR */}
      {/* ========================================================================= */}
      <div className="w-full max-w-full rounded-xl border border-zinc-800 bg-zinc-900/60 overflow-hidden shadow-sm">
        {/* Stream Controls Toolbar */}
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-zinc-800 px-4 py-3 bg-zinc-900/50">
          {/* Header Title with Live WebSocket Status */}
          <div className="flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <h2 className="text-sm font-semibold tracking-wide uppercase text-zinc-200">Live Ingestion Stream</h2>
            <span className="rounded bg-zinc-800/80 px-1.5 py-0.5 text-[10px] font-medium text-zinc-400 border border-zinc-700/60">
              WebSocket Connected
            </span>
          </div>

          {/* Search, Filter & Live Toggle Controls */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-900 px-2.5 py-1.5 focus-within:border-zinc-700">
              <Search className="h-3.5 w-3.5 text-zinc-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search task ID or document..."
                className="w-44 bg-transparent text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none"
              />
            </div>

            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="rounded-lg border border-zinc-800 bg-zinc-900 px-2.5 py-1.5 text-xs text-zinc-300 font-medium focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none"
            >
              <option value="ALL">All Statuses</option>
              <option value="ANOMALIES">Anomalies &amp; Review</option>
              <option value="COMPLETED">Completed</option>
            </select>

            <button
              type="button"
              onClick={() => setIsLive((prev) => !prev)}
              className="flex items-center gap-1.5 rounded-lg border border-zinc-800 bg-zinc-900 px-2.5 py-1.5 text-xs text-zinc-300 hover:bg-zinc-800 transition-colors focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${isLive ? 'text-emerald-400 animate-spin-slow' : 'text-zinc-500'}`} />
              <span>{isLive ? 'Streaming Live' : 'Paused'}</span>
            </button>
          </div>
        </div>

        {/* Data Table wrapped in constrained scroll container */}
        <div className="w-full overflow-x-auto rounded-b-lg border-t border-zinc-800/80">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-zinc-800 bg-zinc-900/80 text-[11px] font-mono uppercase tracking-wider text-zinc-400">
              <tr>
                <th scope="col" className="py-3 px-4 font-semibold">Task ID</th>
                <th scope="col" className="py-3 px-4 font-semibold">Document / Schema</th>
                <th scope="col" className="py-3 px-3 font-semibold text-center">Priority</th>
                <th scope="col" className="py-3 px-4 font-semibold">Confidence</th>
                <th scope="col" className="py-3 px-3 font-semibold text-right">Latency</th>
                <th scope="col" className="py-3 px-4 font-semibold">Status &amp; Verification</th>
                <th scope="col" className="py-3 px-4 font-semibold text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800/60 text-zinc-300 text-xs">
              {filteredQueue.map((row) => (
                <tr
                  key={row.taskId}
                  onClick={() => setSelectedTaskPreview(row)}
                  className="hover:bg-zinc-800/40 cursor-pointer transition-colors"
                >
                  {/* Task ID */}
                  <td className="py-3.5 px-4 font-mono font-semibold text-zinc-200">
                    {row.taskId}
                  </td>

                  {/* Document & Human-readable schema */}
                  <td className="py-3.5 px-4">
                    <div className="flex flex-col">
                      <span className="font-medium text-zinc-100">{row.filename}</span>
                      <span className="text-[11px] text-zinc-400">
                        {SCHEMA_CONFIG[row.schemaType]?.label || row.schemaType}
                      </span>
                    </div>
                  </td>

                  {/* Priority badge */}
                  <td className="py-3.5 px-3 text-center">
                    <span className="rounded bg-zinc-800 px-2 py-0.5 text-[11px] font-mono font-medium text-zinc-300 border border-zinc-700/60">
                      {row.priority}
                    </span>
                  </td>

                  {/* Objective 5: Confidence with percentage and visual mini-bar */}
                  <td className="py-3.5 px-4">
                    <div className="flex items-center gap-2.5">
                      <span className="font-mono text-xs tabular-nums text-zinc-200 font-medium">
                        {row.confidence.toFixed(1)}%
                      </span>
                      <div className="h-1.5 w-14 rounded-full bg-zinc-800 overflow-hidden shrink-0">
                        <div
                          className={`h-full ${
                            row.confidence >= 90
                              ? 'bg-emerald-500'
                              : row.confidence >= 75
                              ? 'bg-amber-500'
                              : 'bg-rose-500'
                          }`}
                          style={{ width: `${Math.min(100, Math.max(0, row.confidence))}%` }}
                        />
                      </div>
                    </div>
                  </td>

                  {/* Latency with monospace tabular nums and no space */}
                  <td className="py-3.5 px-3 text-right font-mono tabular-nums text-zinc-300 font-medium">
                    {row.latencyMs}ms
                  </td>

                  {/* Status & Reason */}
                  <td className="py-3.5 px-4">
                    <StatusBadge status={row.status} reason={row.reviewReason} />
                  </td>

                  {/* Polished Inspect Button */}
                  <td className="py-3.5 px-4 text-right">
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        onNavigateToReview(row.documentId);
                      }}
                      className="inline-flex items-center gap-1.5 rounded-md border border-zinc-700/60 bg-zinc-800/60 px-2.5 py-1 text-xs font-medium text-zinc-200 transition-colors hover:border-zinc-600 hover:bg-zinc-700/70 hover:text-white focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none"
                    >
                      <Eye className="h-3.5 w-3.5 text-zinc-400" />
                      <span>Inspect</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
