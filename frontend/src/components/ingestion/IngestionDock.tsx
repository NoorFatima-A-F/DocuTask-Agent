import React, { useState, useRef } from 'react';
import { UploadCloud, FileText, ArrowRight, Loader2, Sparkles } from 'lucide-react';

interface IngestionDockProps {
  onDispatch: (data: { file: File; schema: string; priority: 'P0' | 'P1' | 'P2' }) => void;
  isSubmitting: boolean;
}

const SCHEMAS = [
  { id: 'Commercial Invoices', badge: 'v2.1', description: 'Extracts line items, VAT/tax breakdowns, and vendor details' },
  { id: 'Point-of-Sale Receipts', badge: 'v1.0', description: 'Itemized totals, tip calculation, and payment tokens' },
  { id: 'Enterprise Contracts & MSAs', badge: 'v1.4', description: 'Indemnity clauses, effective dates, and governing law' },
  { id: 'Identity & Passports', badge: 'v1.2', description: 'MRZ validation, biometric fields, and expiration dates' }
];

export function IngestionDock({ onDispatch, isSubmitting }: IngestionDockProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [schema, setSchema] = useState(SCHEMAS[0].id);
  const [priority, setPriority] = useState<'P0' | 'P1' | 'P2'>('P0');
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const activeSchemaObj = SCHEMAS.find((s) => s.id === schema) || SCHEMAS[0];

  const handleFile = (file: File) => {
    if (file.size > 15 * 1024 * 1024) {
      alert('File size exceeds 15MB limit.');
      return;
    }
    setSelectedFile(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;
    onDispatch({ file: selectedFile, schema, priority });
  };

  return (
    <div className="flex flex-col h-full rounded-xl border border-zinc-800 bg-zinc-900/70 p-5 shadow-sm backdrop-blur-sm justify-between">
      {/* Dock Header */}
      <div>
        <div className="flex items-center justify-between pb-3 border-b border-zinc-800/80">
          <div className="flex items-center gap-2">
            <UploadCloud className="h-4 w-4 text-indigo-400" />
            <h2 className="text-xs font-semibold uppercase tracking-wider text-zinc-200">
              Ingestion Dock
            </h2>
          </div>
          <span className="rounded border border-zinc-800 bg-zinc-950 px-2 py-0.5 text-[10px] font-mono text-zinc-400">
            Max 15MB Payload
          </span>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4 mt-4">
          {/* Concealed Native File Input */}
          <input
            ref={fileInputRef}
            type="file"
            id="hidden-file-input"
            className="sr-only"
            tabIndex={-1}
            aria-hidden="true"
            accept=".pdf,.png,.tiff,.jpeg,.jpg"
            onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
          />

          {/* Compact Dropzone Container */}
          <div
            onClick={() => fileInputRef.current?.click()}
            onDragOver={(e) => {
              e.preventDefault();
              setIsDragging(true);
            }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={handleDrop}
            className={`group relative flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed py-5 px-3 text-center transition-all ${
              isDragging
                ? 'border-indigo-500 bg-indigo-500/10'
                : 'border-zinc-800 bg-zinc-950/50 hover:border-zinc-700 hover:bg-zinc-900/60'
            }`}
          >
            <div className="mb-1.5 rounded-full border border-zinc-800 bg-zinc-900 p-2 text-zinc-400 group-hover:border-zinc-700 group-hover:text-zinc-200 transition-colors">
              <UploadCloud className="h-4 w-4 stroke-[1.75]" />
            </div>
            <p className="text-xs font-medium text-zinc-200">
              <span className="text-indigo-400 group-hover:underline">Click to upload</span> or drag and drop
            </p>
            <p className="text-[10px] text-zinc-400 mt-0.5 font-sans">
              PDF, PNG, TIFF, or JPEG (Max 15MB)
            </p>

            {selectedFile && (
              <div className="mt-2.5 inline-flex items-center gap-1.5 rounded-md border border-indigo-500/30 bg-indigo-500/10 px-2.5 py-1 text-xs text-indigo-300">
                <FileText className="h-3.5 w-3.5 shrink-0" />
                <span className="max-w-[180px] truncate font-mono text-[11px]">{selectedFile.name}</span>
                <span className="text-[10px] text-indigo-400 font-mono">
                  ({(selectedFile.size / (1024 * 1024)).toFixed(2)}MB)
                </span>
              </div>
            )}
          </div>

          {/* Document Schema Taxonomy Selector */}
          <div className="flex flex-col gap-1.5 max-w-full">
            <div className="flex items-center justify-between">
              <label htmlFor="schema-select" className="text-xs font-medium text-zinc-300">
                Document Schema Taxonomy
              </label>
              <span className="text-[10px] font-mono text-zinc-400 bg-zinc-800 px-1.5 py-0.2 rounded border border-zinc-700/60">
                {activeSchemaObj.badge}
              </span>
            </div>
            <select
              id="schema-select"
              value={schema}
              onChange={(e) => setSchema(e.target.value)}
              className="w-full rounded-lg border border-zinc-800 bg-zinc-950 px-3 py-2 text-xs text-zinc-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            >
              {SCHEMAS.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.id} ({s.badge})
                </option>
              ))}
            </select>
            <p className="text-[11px] text-zinc-400 leading-snug">
              {activeSchemaObj.description}
            </p>
          </div>

          {/* Accessible Queue Priority Toggle */}
          <div className="flex flex-col gap-1.5" role="radiogroup" aria-label="Queue Priority Policy">
            <label className="text-xs font-medium text-zinc-300">Queue Priority Policy</label>
            <div className="grid grid-cols-3 gap-2">
              {[
                { id: 'P0', label: 'P0 Realtime', desc: '<1s SLA' },
                { id: 'P1', label: 'P1 Standard', desc: 'Default' },
                { id: 'P2', label: 'P2 Batch', desc: 'Background' }
              ].map((p) => {
                const active = priority === p.id;
                return (
                  <button
                    key={p.id}
                    type="button"
                    role="radio"
                    aria-checked={active}
                    onClick={() => setPriority(p.id as 'P0' | 'P1' | 'P2')}
                    className={`flex flex-col items-center justify-center rounded-lg border py-2 px-1 transition-all cursor-pointer ${
                      active
                        ? 'border-indigo-500 bg-indigo-500/15 text-indigo-200 ring-1 ring-indigo-500/50'
                        : 'border-zinc-800 bg-zinc-950/60 text-zinc-400 hover:border-zinc-700 hover:bg-zinc-800/40 hover:text-zinc-200'
                    }`}
                  >
                    <span className="text-xs font-semibold">{p.label}</span>
                    <span className="text-[10px] text-zinc-400 font-mono">{p.desc}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </form>
      </div>

      {/* Primary CTA Button */}
      <div className="pt-4 mt-2">
        <button
          type="button"
          onClick={handleSubmit}
          disabled={!selectedFile || isSubmitting}
          className="w-full flex items-center justify-center gap-2 rounded-lg bg-indigo-600 py-2.5 px-4 text-xs font-semibold text-white shadow-sm transition-all hover:bg-indigo-500 disabled:cursor-not-allowed disabled:bg-zinc-800 disabled:text-zinc-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 cursor-pointer"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin text-zinc-300" />
              <span>Routing to Ingestion Pipeline...</span>
            </>
          ) : (
            <>
              <Sparkles className="h-3.5 w-3.5" />
              <span>Dispatch Ingestion</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </>
          )}
        </button>
      </div>
    </div>
  );
}
