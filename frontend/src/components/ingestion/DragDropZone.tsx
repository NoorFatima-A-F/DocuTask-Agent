import React, { useState, useRef, ChangeEvent, DragEvent } from 'react';
import { UploadCloud, FileCheck, ArrowRight, Eye, RefreshCw, Loader2 } from 'lucide-react';
import { validateDocumentFile } from '../../utils/fileValidation';
import { DocumentValidationResult } from '../../types/document';
import { useDocumentUpload } from '../../hooks/useDocumentUpload';
import { StatusBadge } from '../layout/StatusBadge';

interface DragDropZoneProps {
  onJobCreated: (jobId: string, documentId: string) => void;
  onNavigateToReview: (documentId: string) => void;
}

interface IngestionQueueRow {
  taskId: string;
  documentId: string;
  filename: string;
  schemaType: string;
  priority: 'LOW' | 'NORMAL' | 'HIGH';
  confidence: number;
  latencyMs: number;
  status: 'COMPLETED' | 'PROCESSING' | 'REVIEW_REQUIRED' | 'FAILED';
  timestamp: string;
}

const INITIAL_QUEUE: IngestionQueueRow[] = [
  {
    taskId: 'task_e847c91a',
    documentId: 'doc_e847c910a2',
    filename: 'INV-2026-8894.pdf',
    schemaType: 'Invoice',
    priority: 'HIGH',
    confidence: 0.942,
    latencyMs: 640,
    status: 'REVIEW_REQUIRED',
    timestamp: '1 min ago',
  },
  {
    taskId: 'task_b921fa02',
    documentId: 'doc_b921fa0281',
    filename: 'Cloudflare_Subscription_Q3.pdf',
    schemaType: 'Invoice',
    priority: 'NORMAL',
    confidence: 0.985,
    latencyMs: 412,
    status: 'COMPLETED',
    timestamp: '8 mins ago',
  },
  {
    taskId: 'task_3821a99f',
    documentId: 'doc_3821a99fa4',
    filename: 'Uber_Business_Receipt_98.png',
    schemaType: 'Receipt',
    priority: 'LOW',
    confidence: 0.971,
    latencyMs: 380,
    status: 'COMPLETED',
    timestamp: '22 mins ago',
  },
  {
    taskId: 'task_1120aa44',
    documentId: 'doc_1120aa44bc',
    filename: 'Master_Services_Agmt_v4.pdf',
    schemaType: 'Contract',
    priority: 'HIGH',
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
  const [schemaType, setSchemaType] = useState<string>('Invoice');
  const [priority, setPriority] = useState<'LOW' | 'NORMAL' | 'HIGH'>('HIGH');
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
        status: 'REVIEW_REQUIRED',
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
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 w-full">
      {/* --- LEFT COLUMN: Compact Ingestion Hub (35% / 4 cols) --- */}
      <div className="lg:col-span-4 flex flex-col gap-4">
        <div className="border border-[#27272a] bg-[#121215] rounded p-4 space-y-4">
          <div className="flex items-center justify-between border-b border-[#27272a] pb-3">
            <span className="text-xs font-semibold text-zinc-100 uppercase tracking-wider font-mono flex items-center gap-1.5">
              <UploadCloud className="w-3.5 h-3.5 text-zinc-400" />
              Ingestion Studio
            </span>
            <span className="text-[10px] font-mono text-zinc-500 bg-zinc-900 border border-zinc-800 px-1.5 py-0.2 rounded">
              MAX 15MB
            </span>
          </div>

          {/* Compact Dropzone */}
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`border border-dashed rounded p-5 text-center cursor-pointer transition-colors ${
              isDragging
                ? 'border-zinc-500 bg-zinc-800/40'
                : 'border-zinc-700/80 bg-zinc-900/30 hover:border-zinc-500 hover:bg-zinc-900/60'
            }`}
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleInputChange}
              accept=".pdf,.png,.jpg,.jpeg,.tiff,.tif"
              className="hidden"
            />
            <div className="flex flex-col items-center gap-2">
              <UploadCloud className="w-6 h-6 text-zinc-400" />
              <span className="text-xs font-medium text-zinc-200">
                {selectedFile ? selectedFile.name : 'Select or drag document'}
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
          </div>

          {/* Defensive Validation Result Indicator */}
          {validationResult && (
            <div
              className={`p-2.5 rounded border text-xs font-mono flex items-start gap-2 ${
                validationResult.isValid
                  ? 'bg-emerald-950/20 border-emerald-800/40 text-emerald-400'
                  : 'bg-rose-950/20 border-rose-800/40 text-rose-400'
              }`}
            >
              <FileCheck className="w-3.5 h-3.5 shrink-0 mt-0.5" />
              <div className="space-y-0.5 flex-1 min-w-0">
                <div className="flex justify-between">
                  <span className="font-semibold">{validationResult.detectedMimeType || 'Binary'}</span>
                  <span>{(validationResult.sizeBytes / (1024 * 1024)).toFixed(2)} MB</span>
                </div>
                {validationResult.error && (
                  <p className="text-[11px] leading-tight text-rose-300">{validationResult.error}</p>
                )}
              </div>
            </div>
          )}

          {/* Form Selectors */}
          <div className="space-y-3 pt-1">
            <div>
              <label className="text-[11px] font-mono text-zinc-400 uppercase block mb-1">
                Document Schema
              </label>
              <select
                value={schemaType}
                onChange={(e) => setSchemaType(e.target.value)}
                className="w-full bg-zinc-900 border border-zinc-700/80 rounded px-2.5 py-1.5 text-xs text-zinc-200 font-mono focus:outline-none focus:border-zinc-500"
              >
                <option value="Invoice">InvoiceTaxonomy.v2</option>
                <option value="Receipt">CommercialReceipt.v1</option>
                <option value="Contract">EnterpriseContract.v1</option>
                <option value="Identity">IdentityCredential.v1</option>
              </select>
            </div>

            <div>
              <label className="text-[11px] font-mono text-zinc-400 uppercase block mb-1">
                Queue Priority
              </label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value as 'LOW' | 'NORMAL' | 'HIGH')}
                className="w-full bg-zinc-900 border border-zinc-700/80 rounded px-2.5 py-1.5 text-xs text-zinc-200 font-mono focus:outline-none focus:border-zinc-500"
              >
                <option value="HIGH">High (P0 - Immediate Ingestion)</option>
                <option value="NORMAL">Normal (P1 - Standard Queue)</option>
                <option value="LOW">Low (P2 - Batch Processing)</option>
              </select>
            </div>
          </div>

          {/* Dispatch CTA Button */}
          <button
            onClick={handleDispatch}
            disabled={!selectedFile || isUploading || (validationResult && !validationResult.isValid)}
            className="w-full py-2 px-3 rounded bg-zinc-100 hover:bg-white disabled:bg-zinc-800 disabled:text-zinc-500 text-zinc-950 text-xs font-semibold font-mono flex items-center justify-center gap-1.5 transition-colors cursor-pointer disabled:cursor-not-allowed"
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

      {/* --- RIGHT COLUMN: High-Density Live Ingestion Queue (65% / 8 cols) --- */}
      <div className="lg:col-span-8 flex flex-col gap-4">
        <div className="border border-[#27272a] bg-[#121215] rounded p-4 flex flex-col flex-1">
          <div className="flex items-center justify-between border-b border-[#27272a] pb-3 mb-3">
            <div>
              <span className="text-xs font-semibold text-zinc-100 uppercase tracking-wider font-mono">
                Recent Ingestion Batches &amp; Telemetry
              </span>
              <p className="text-[11px] text-zinc-500 font-mono mt-0.5">
                Live asynchronous pipeline status (<code className="text-zinc-400">/api/v1/jobs</code>)
              </p>
            </div>
            <button
              onClick={() => {}}
              className="p-1 rounded bg-zinc-900 border border-zinc-800 text-zinc-400 hover:text-zinc-200 transition-colors"
              title="Refresh queue"
            >
              <RefreshCw className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* High Density Table */}
          <div className="overflow-x-auto flex-1">
            <table className="w-full text-left text-xs font-mono">
              <thead>
                <tr className="border-b border-zinc-800 text-zinc-500 text-[10px] uppercase">
                  <th className="pb-2 font-medium">Task ID</th>
                  <th className="pb-2 font-medium">Document / Schema</th>
                  <th className="pb-2 font-medium text-center">Priority</th>
                  <th className="pb-2 font-medium text-center">Confidence</th>
                  <th className="pb-2 font-medium text-right">Latency</th>
                  <th className="pb-2 font-medium text-center">Status</th>
                  <th className="pb-2 font-medium text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800/60 text-zinc-300 text-[11px]">
                {queue.map((row) => (
                  <tr key={row.taskId} className="hover:bg-zinc-800/30 transition-colors">
                    <td className="py-2.5 text-zinc-200 font-semibold truncate max-w-[110px]">
                      {row.taskId}
                    </td>
                    <td className="py-2.5 max-w-[180px] truncate" title={row.filename}>
                      <div className="flex flex-col">
                        <span className="text-zinc-200 truncate">{row.filename}</span>
                        <span className="text-[10px] text-zinc-500">{row.schemaType}</span>
                      </div>
                    </td>
                    <td className="py-2.5 text-center">
                      <span className="text-[10px] font-mono px-1 py-0.2 rounded bg-zinc-900 border border-zinc-800 text-zinc-400">
                        {row.priority}
                      </span>
                    </td>
                    <td className="py-2.5 text-center">
                      <StatusBadge confidence={row.confidence} size="sm" />
                    </td>
                    <td className="py-2.5 text-right text-zinc-400">
                      {row.latencyMs}ms
                    </td>
                    <td className="py-2.5 text-center">
                      <span
                        className={`inline-flex items-center gap-1 font-mono text-[10px] px-1.5 py-0.5 rounded border ${
                          row.status === 'COMPLETED'
                            ? 'bg-emerald-950/40 text-emerald-400 border-emerald-800/50'
                            : row.status === 'REVIEW_REQUIRED'
                            ? 'bg-amber-950/40 text-amber-400 border-amber-800/50'
                            : 'bg-zinc-800 text-zinc-300 border-zinc-700'
                        }`}
                      >
                        {row.status === 'REVIEW_REQUIRED' ? 'Review Req' : row.status}
                      </span>
                    </td>
                    <td className="py-2.5 text-right">
                      <button
                        onClick={() => onNavigateToReview(row.documentId)}
                        className="px-2 py-1 rounded bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-[10px] font-mono inline-flex items-center gap-1 border border-zinc-700 transition-colors"
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
