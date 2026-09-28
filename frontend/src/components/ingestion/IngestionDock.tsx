import React, { useState, useRef, DragEvent, ChangeEvent } from 'react';
import { UploadCloud, Upload, FileText, ArrowRight, Loader2, AlertTriangle } from 'lucide-react';
import { validateDocumentFile } from '../../utils/fileValidation';
import { DocumentValidationResult } from '../../types/document';

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

export interface IngestionDockProps {
  isSubmitting?: boolean;
  uploadProgress?: number;
  onDispatch: (file: File, schemaType: string, priority: 'P0' | 'P1' | 'P2') => void;
}

export const IngestionDock: React.FC<IngestionDockProps> = ({
  isSubmitting = false,
  uploadProgress = 0,
  onDispatch,
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [schemaType, setSchemaType] = useState<string>('InvoiceTaxonomy.v2');
  const [priority, setPriority] = useState<'P0' | 'P1' | 'P2'>('P0');
  const [validationResult, setValidationResult] = useState<DocumentValidationResult | null>(null);
  const [isDragging, setIsDragging] = useState<boolean>(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = async (file: File) => {
    setSelectedFile(file);
    const result = await validateDocumentFile(file);
    setValidationResult(result);
  };

  const handleFileChange = async (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      await handleFile(e.target.files[0]);
    }
  };

  const handleFileDrop = async (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      await handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = () => {
    if (!selectedFile || (validationResult !== null && !validationResult.isValid)) return;
    onDispatch(selectedFile, schemaType, priority);
  };

  return (
    <div className="flex flex-col justify-between rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 shadow-sm space-y-4 h-full">
      <div className="space-y-4">
        {/* Header Bar */}
        <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
          <div className="flex items-center gap-2">
            <UploadCloud className="h-4 w-4 text-indigo-400" />
            <h2 className="text-xs font-semibold uppercase tracking-wider text-zinc-200">
              Ingestion Dock
            </h2>
          </div>
          <span className="rounded border border-zinc-800 bg-zinc-800/50 px-2 py-0.5 text-[10px] font-medium text-zinc-400">
            Max 15MB Payload
          </span>
        </div>

        {/* Accessible Drag-and-Drop Target with Hidden Native Input */}
        <div
          onClick={() => fileInputRef.current?.click()}
          onDragOver={(e) => {
            e.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleFileDrop}
          role="button"
          tabIndex={0}
          aria-label="Upload document drag and drop area"
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              fileInputRef.current?.click();
            }
          }}
          className={`group relative flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed py-8 px-4 text-center transition-all focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none ${
            isDragging
              ? 'border-indigo-500 bg-indigo-500/5'
              : 'border-zinc-800 bg-zinc-950/40 hover:border-zinc-700 hover:bg-zinc-900/60'
          }`}
        >
          <input
            ref={fileInputRef}
            type="file"
            id="document-upload-input"
            className="sr-only"
            accept=".pdf,.png,.tiff,.jpeg,.jpg"
            onChange={handleFileChange}
          />
          <div className="mb-2 rounded-full border border-zinc-800 bg-zinc-900 p-2.5 text-zinc-400 transition-colors group-hover:border-zinc-700 group-hover:text-zinc-200">
            <Upload className="h-5 w-5 stroke-[1.75]" />
          </div>
          <p className="text-xs font-medium text-zinc-200">
            <span className="text-indigo-400 group-hover:underline">Click to upload</span> or drag and drop
          </p>
          <p className="mt-1 text-[11px] text-zinc-500 font-sans">PDF, PNG, TIFF, or JPEG (Max 15MB)</p>
          {selectedFile && (
            <div className="mt-3 inline-flex items-center gap-1.5 rounded-md border border-indigo-500/30 bg-indigo-500/10 px-2.5 py-1 text-xs text-indigo-300">
              <FileText className="h-3.5 w-3.5" />
              <span className="max-w-[180px] truncate font-mono">{selectedFile.name}</span>
              <span className="text-[10px] text-indigo-400 font-mono">
                ({(selectedFile.size / 1024 / 1024).toFixed(2)}MB)
              </span>
            </div>
          )}
        </div>

        {/* Header Inspection Error Notice */}
        {validationResult && !validationResult.isValid && (
          <div className="p-3 rounded-lg border border-rose-800/50 bg-rose-950/30 text-rose-300 text-xs font-mono flex items-start gap-2.5">
            <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
            <div className="space-y-0.5 flex-1 min-w-0">
              <span className="font-semibold block text-rose-200">Binary Header Verification Failed</span>
              <p className="text-[11px] leading-tight text-rose-300">{validationResult.error}</p>
            </div>
          </div>
        )}

        {/* Schema Selector */}
        <div className="space-y-1.5">
          <label htmlFor="dock-schema-select" className="text-xs font-medium text-zinc-300 flex items-center justify-between">
            <span>Document Schema Taxonomy</span>
            <span className="text-[10px] font-mono text-zinc-400">
              {SCHEMA_CONFIG[schemaType]?.badge || 'v2.1'}
            </span>
          </label>
          <select
            id="dock-schema-select"
            value={schemaType}
            onChange={(e) => setSchemaType(e.target.value)}
            className="w-full bg-zinc-950 border border-zinc-700/80 rounded-lg px-3 py-2 text-xs text-zinc-200 font-medium focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none"
          >
            {Object.entries(SCHEMA_CONFIG).map(([key, config]) => (
              <option key={key} value={key} className="bg-zinc-900 text-zinc-200 py-1">
                {config.label} ({config.badge})
              </option>
            ))}
          </select>
          <p className="text-[11px] text-zinc-500 font-sans">
            {SCHEMA_CONFIG[schemaType]?.description}
          </p>
        </div>

        {/* Queue Priority Toggle Group Accessibility (WCAG 2.2 AA) */}
        <div role="radiogroup" aria-label="Queue Priority Policy" className="mt-4">
          <label className="mb-1.5 block text-xs font-medium text-zinc-400">Queue Priority Policy</label>
          <div className="grid grid-cols-3 gap-2">
            {[
              { id: 'P0' as const, label: 'P0 Realtime', desc: '<1s SLA' },
              { id: 'P1' as const, label: 'P1 Standard', desc: 'Default' },
              { id: 'P2' as const, label: 'P2 Batch', desc: 'Background' },
            ].map((p) => {
              const active = priority === p.id;
              return (
                <button
                  key={p.id}
                  type="button"
                  role="radio"
                  aria-checked={active}
                  onClick={() => setPriority(p.id)}
                  className={`flex flex-col items-center justify-center rounded-lg border py-2 px-1 transition-all focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none ${
                    active
                      ? 'border-indigo-500 bg-indigo-500/15 text-indigo-200 ring-1 ring-indigo-500/50 font-medium'
                      : 'border-zinc-800 bg-zinc-950/60 text-zinc-400 hover:border-zinc-700 hover:bg-zinc-800/40 hover:text-zinc-200'
                  }`}
                >
                  <span className="text-xs font-semibold">{p.label}</span>
                  <span className="text-[10px] text-zinc-500">{p.desc}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Dispatch Ingestion CTA */}
      <button
        type="button"
        disabled={!selectedFile || isSubmitting || (validationResult !== null && !validationResult.isValid)}
        onClick={handleSubmit}
        className="mt-5 flex w-full items-center justify-center gap-2 rounded-lg bg-indigo-600 py-2.5 px-4 text-xs font-semibold text-white shadow-sm transition-all hover:bg-indigo-500 disabled:cursor-not-allowed disabled:bg-zinc-800/60 disabled:text-zinc-600 focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none"
      >
        {isSubmitting ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin text-zinc-300" />
            <span>Routing to Extraction Engine {uploadProgress > 0 ? `(${uploadProgress}%)` : ''}...</span>
          </>
        ) : (
          <>
            <span>Dispatch Ingestion</span>
            <ArrowRight className="h-3.5 w-3.5" />
          </>
        )}
      </button>
    </div>
  );
};
