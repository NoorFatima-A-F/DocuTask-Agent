import React, { useState, useRef, ChangeEvent, DragEvent } from 'react';
import { UploadCloud, FileCheck, ArrowRight, Eye, RefreshCw, Loader2, AlertTriangle, CheckCircle2, X, FileText } from 'lucide-react';
import { validateDocumentFile } from '../../utils/fileValidation';
import { DocumentValidationResult } from '../../types/document';
import { useDocumentUpload } from '../../hooks/useDocumentUpload';

interface DragDropZoneProps {
  onJobCreated: (jobId: string, documentId: string) => void;
  onNavigateToReview: (documentId: string) => void;
}

export interface IngestionQueueRow {
  taskId: string;
  documentId: string;
  filename: string;
  schemaType: string;
  priority: 'P0 - High' | 'P1 - Normal' | 'P2 - Low';
  confidence: number;
  latencyMs: number;
  status: 'COMPLETED' | 'REVIEW_REQ' | 'PROCESSING';
  reviewReason?: string;
  timestamp: string;
}

const INITIAL_QUEUE: IngestionQueueRow[] = [
  {
    taskId: 'task_e847c91a',
    documentId: 'doc_e847c910a2',
    filename: 'INV-2026-8894.pdf',
    schemaType: 'InvoiceTaxonomy.v2',
    priority: 'P0 - High',
    confidence: 0.942,
    latencyMs: 640,
    status: 'REVIEW_REQ',
    reviewReason: 'Tax Anomaly (Tax 68% < 85%)',
    timestamp: '1 min ago',
  },
  {
    taskId: 'task_b921fa02',
    documentId: 'doc_b921fa0281',
    filename: 'Cloudflare_Subscription_Q3.pdf',
    schemaType: 'InvoiceTaxonomy.v2',
    priority: 'P1 - Normal',
    confidence: 0.985,
    latencyMs: 412,
    status: 'COMPLETED',
    timestamp: '8 mins ago',
  },
  {
    taskId: 'task_3821a99f',
    documentId: 'doc_3821a99fa4',
    filename: 'Uber_Business_Receipt_98.png',
    schemaType: 'CommercialReceipt.v1',
    priority: 'P2 - Low',
    confidence: 0.724,
    latencyMs: 380,
    status: 'REVIEW_REQ',
    reviewReason: 'Low Confidence (72.4% < 75%)',
    timestamp: '22 mins ago',
  },
  {
    taskId: 'task_1120aa44',
    documentId: 'doc_1120aa44bc',
    filename: 'Master_Services_Agmt_v4.pdf',
    schemaType: 'EnterpriseContract.v1',
    priority: 'P0 - High',
    confidence: 0.912,
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
  const [priority, setPriority] = useState<'P0 - High' | 'P1 - Normal' | 'P2 - Low'>('P0 - High');
  const [validationResult, setValidationResult] = useState<DocumentValidationResult | null>(null);
  const [queue, setQueue] = useState<IngestionQueueRow[]>(INITIAL_QUEUE);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const { isUploading, uploadProgress, uploadAndProcess } = useDocumentUpload(
    (jobId, documentId) => {
      const newRow: IngestionQueueRow = {
        taskId: `task_${jobId.substring(0, 8)}`,
        documentId: documentId,
        filename: selectedFile?.name || 'document.pdf',
        schemaType,
        priority,
        confidence: 0.942,
        latencyMs: 640,
        status: 'REVIEW_REQ',
        reviewReason: 'Tax Anomaly (Tax 68% < 85%)',
        timestamp: 'Just now',
      };
      setQueue((prev) => [newRow, ...prev]);
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
    if (!selectedFile || !validationResult?.isValid) return;
    await uploadAndProcess(selectedFile);
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
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

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-3.5 w-full h-full overflow-hidden select-none min-h-0">
      {/* --- LEFT COLUMN: Compact Ingestion Dock (4 cols / ~33% width) --- */}
      <div className="lg:col-span-4 flex flex-col h-full overflow-hidden min-h-0">
        <div className="border border-[#27272a] bg-[#121215] rounded-lg p-3.5 flex flex-col justify-between h-full overflow-y-auto min-h-0 space-y-3">
          <div className="space-y-3">
            {/* Dock Header */}
            <div className="flex items-center justify-between border-b border-[#27272a] pb-2">
              <span className="text-xs font-semibold text-zinc-100 uppercase tracking-wider font-mono flex items-center gap-1.5">
                <UploadCloud className="w-3.5 h-3.5 text-zinc-400" />
                Ingestion Dock
              </span>
              <span className="text-[10px] font-mono text-zinc-500 bg-zinc-900 border border-zinc-800 px-1.5 py-0.2 rounded">
                MAX 15MB
              </span>
            </div>

            {/* Compact Dropzone or Staged File Chip */}
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleInputChange}
              accept=".pdf,.png,.jpg,.jpeg,.tiff,.tif"
              className="hidden"
            />

            {!selectedFile ? (
              <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className={`h-28 border border-dashed rounded-lg p-3 text-center cursor-pointer transition-colors flex flex-col items-center justify-center gap-1.5 ${
                  isDragging
                    ? 'border-zinc-400 bg-zinc-800/40'
                    : 'border-zinc-700/80 bg-zinc-900/30 hover:border-zinc-500 hover:bg-zinc-900/60'
                }`}
              >
                <UploadCloud className="w-5 h-5 text-zinc-400" />
                <span className="text-xs font-medium text-zinc-200">
                  Drop file here or click to browse
                </span>
                <div className="flex items-center gap-1 text-[10px] font-mono text-zinc-500">
                  <span>PDF</span>
                  <span>•</span>
                  <span>PNG</span>
                  <span>•</span>
                  <span>TIFF</span>
                  <span>•</span>
                  <span>JPEG</span>
                </div>
              </div>
            ) : (
              <div className="p-3 rounded-lg border border-zinc-700/80 bg-zinc-900/60 flex items-center justify-between gap-2.5">
                <div className="flex items-center gap-2.5 min-w-0 flex-1">
                  <div className="w-7 h-7 rounded bg-zinc-800 border border-zinc-700 flex items-center justify-center shrink-0">
                    <FileText className="w-4 h-4 text-zinc-300" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="text-xs font-medium text-zinc-100 truncate" title={selectedFile.name}>
                      {selectedFile.name}
                    </div>
                    <div className="flex items-center gap-1.5 text-[10px] font-mono text-zinc-400">
                      <span>{(selectedFile.size / (1024 * 1024)).toFixed(2)} MB</span>
                      <span>•</span>
                      <span className="text-emerald-400 font-semibold">{validationResult?.detectedMimeType || 'Binary Validated'}</span>
                    </div>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={handleClearFile}
                  className="p-1 rounded text-zinc-500 hover:text-zinc-200 hover:bg-zinc-800 transition-colors shrink-0"
                  title="Remove staged file"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>
            )}

            {/* Validation Error Banner */}
            {validationResult && !validationResult.isValid && (
              <div className="p-2.5 rounded border border-rose-800/40 bg-rose-950/20 text-rose-400 text-xs font-mono flex items-start gap-2">
                <FileCheck className="w-3.5 h-3.5 shrink-0 mt-0.5" />
                <div className="space-y-0.5 flex-1 min-w-0">
                  <span className="font-semibold block">Header Verification Failed</span>
                  <p className="text-[11px] leading-tight text-rose-300">{validationResult.error}</p>
                </div>
              </div>
            )}

            {/* Schema Selector */}
            <div className="space-y-1">
              <label className="text-[11px] font-mono text-zinc-400 uppercase block">
                Document Schema
              </label>
              <select
                value={schemaType}
                onChange={(e) => setSchemaType(e.target.value)}
                className="w-full bg-zinc-900 border border-zinc-700/80 rounded px-2.5 py-1.5 text-xs text-zinc-200 font-mono focus:outline-none focus:border-zinc-500"
              >
                <option value="InvoiceTaxonomy.v2">InvoiceTaxonomy.v2</option>
                <option value="CommercialReceipt.v1">CommercialReceipt.v1</option>
                <option value="EnterpriseContract.v1">EnterpriseContract.v1</option>
                <option value="IdentityCredential.v1">IdentityCredential.v1</option>
              </select>
            </div>

            {/* Segmented Priority Control */}
            <div className="space-y-1">
              <label className="text-[11px] font-mono text-zinc-400 uppercase block">
                Queue Priority
              </label>
              <div className="grid grid-cols-3 gap-1.5">
                {(['P0 - High', 'P1 - Normal', 'P2 - Low'] as const).map((p) => (
                  <button
                    key={p}
                    type="button"
                    onClick={() => setPriority(p)}
                    className={`px-2 py-1.5 rounded border text-[11px] font-mono transition-colors text-center ${
                      priority === p
                        ? 'bg-zinc-800 border-zinc-600 text-zinc-100 font-semibold'
                        : 'bg-zinc-900/60 border-zinc-800 text-zinc-500 hover:text-zinc-300'
                    }`}
                  >
                    {p.split(' ')[0]}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Dispatch Ingestion CTA */}
          <div className="pt-2">
            <button
              onClick={handleDispatch}
              disabled={!selectedFile || isUploading || (validationResult !== null && !validationResult.isValid)}
              className="w-full py-2 px-3 rounded bg-zinc-100 hover:bg-white disabled:bg-zinc-800 disabled:text-zinc-500 text-zinc-950 text-xs font-semibold font-mono flex items-center justify-center gap-1.5 transition-colors cursor-pointer disabled:cursor-not-allowed shadow-sm"
            >
              {isUploading ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  <span>Enqueuing ({uploadProgress}%)...</span>
                </>
              ) : (
                <>
                  <span>Dispatch Ingestion</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* --- RIGHT COLUMN: Live Ingestion Stream & Telemetry (8 cols / ~67% width) --- */}
      <div className="lg:col-span-8 flex flex-col h-full overflow-hidden min-h-0">
        <div className="border border-[#27272a] bg-[#121215] rounded-lg flex flex-col h-full overflow-hidden min-h-0">
          {/* Table Header Bar */}
          <div className="px-4 py-2.5 border-b border-zinc-800 flex items-center justify-between bg-[#121215] shrink-0">
            <div>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                <span className="text-xs font-semibold text-zinc-100 uppercase tracking-wider font-mono">
                  Live Ingestion Stream
                </span>
                <span className="text-[10px] font-mono text-zinc-500 bg-zinc-900 border border-zinc-800 px-1.5 py-0.2 rounded">
                  /api/v1/jobs
                </span>
              </div>
              <p className="text-[10px] text-zinc-500 font-mono mt-0.5">
                Real-time asynchronous pipeline queue • Click any row to inspect in HITL Reviewer
              </p>
            </div>
            <button
              onClick={() => {}}
              className="p-1 rounded bg-zinc-900 border border-zinc-800 text-zinc-400 hover:text-zinc-200 transition-colors"
              title="Refresh queue"
            >
              <RefreshCw className="w-3 h-3" />
            </button>
          </div>

          {/* Fixed-Layout Independently Scrollable Table */}
          <div className="flex-1 overflow-y-auto overflow-x-auto min-h-0">
            <table className="table-fixed w-full text-left text-xs font-mono">
              <thead className="sticky top-0 bg-[#121215] z-10 border-b border-zinc-800 text-zinc-500 text-[10px] uppercase">
                <tr>
                  <th className="w-28 py-2.5 px-3 font-medium">Task ID</th>
                  <th className="w-44 py-2.5 px-3 font-medium">Document / Schema</th>
                  <th className="w-16 py-2.5 px-2 font-medium text-center">Priority</th>
                  <th className="w-24 py-2.5 px-2 font-medium text-center">Confidence</th>
                  <th className="w-20 py-2.5 px-3 font-medium text-right">Latency</th>
                  <th className="w-56 py-2.5 px-3 font-medium">Status &amp; Reason</th>
                  <th className="w-20 py-2.5 px-3 font-medium text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800/60 text-zinc-300 text-[11px]">
                {queue.map((row) => (
                  <tr
                    key={row.taskId}
                    onClick={() => onNavigateToReview(row.documentId)}
                    className="hover:bg-zinc-800/40 cursor-pointer transition-colors"
                  >
                    {/* Task ID */}
                    <td className="py-2.5 px-3 text-zinc-200 font-semibold truncate">
                      {row.taskId}
                    </td>

                    {/* Document / Schema */}
                    <td className="py-2.5 px-3 truncate" title={row.filename}>
                      <div className="flex flex-col truncate">
                        <span className="text-zinc-200 truncate font-medium">{row.filename}</span>
                        <span className="text-[10px] text-zinc-500 truncate">{row.schemaType}</span>
                      </div>
                    </td>

                    {/* Priority */}
                    <td className="py-2.5 px-2 text-center">
                      <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-zinc-900 border border-zinc-800 text-zinc-400">
                        {row.priority.split(' ')[0]}
                      </span>
                    </td>

                    {/* Confidence */}
                    <td className="py-2.5 px-2 text-center">
                      <span
                        className={`text-[10px] font-mono px-1.5 py-0.5 rounded border ${
                          row.confidence >= 0.90
                            ? 'bg-emerald-950/40 text-emerald-400 border-emerald-800/50'
                            : row.confidence >= 0.75
                            ? 'bg-amber-950/40 text-amber-400 border-amber-800/50'
                            : 'bg-rose-950/40 text-rose-400 border-rose-800/50'
                        }`}
                      >
                        {(row.confidence * 100).toFixed(1)}%
                      </span>
                    </td>

                    {/* Latency */}
                    <td className="py-2.5 px-3 text-right text-zinc-400">
                      {row.latencyMs}ms
                    </td>

                    {/* Status & Reason */}
                    <td className="py-2.5 px-3">
                      <div className="flex items-center gap-1.5">
                        {row.status === 'COMPLETED' ? (
                          <span className="inline-flex items-center gap-1 font-mono text-[10px] px-1.5 py-0.2 rounded border bg-emerald-950/40 text-emerald-400 border-emerald-800/50">
                            <CheckCircle2 className="w-2.5 h-2.5" />
                            COMPLETED
                          </span>
                        ) : (
                          <span
                            className="inline-flex items-center gap-1 font-mono text-[10px] px-1.5 py-0.2 rounded border bg-amber-950/40 text-amber-400 border-amber-800/50"
                            title={row.reviewReason}
                          >
                            <AlertTriangle className="w-2.5 h-2.5 shrink-0" />
                            <span className="truncate">{row.reviewReason || 'Review Req'}</span>
                          </span>
                        )}
                      </div>
                    </td>

                    {/* Action */}
                    <td className="py-2.5 px-3 text-right">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onNavigateToReview(row.documentId);
                        }}
                        className="px-2 py-0.5 rounded bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-[10px] font-mono inline-flex items-center gap-1 border border-zinc-700 transition-colors"
                      >
                        <Eye className="w-3 h-3" />
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
    </div>
  );
};
