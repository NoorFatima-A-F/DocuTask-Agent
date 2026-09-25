import React, { useState, useRef, DragEvent, ChangeEvent } from 'react';
import {
  UploadCloud,
  FileCheck2,
  Sparkles,
  Zap,
} from 'lucide-react';
import { validateDocumentFile } from '../../utils/fileValidation';
import { DocumentValidationResult } from '../../types/document';
import { FileValidator } from './FileValidator';
import { UploadQueue } from './UploadQueue';
import { useDocumentUpload } from '../../hooks/useDocumentUpload';

interface DragDropZoneProps {
  onJobCreated: (jobId: string, documentId: string) => void;
}

export const DragDropZone: React.FC<DragDropZoneProps> = ({ onJobCreated }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [validationResult, setValidationResult] = useState<DocumentValidationResult | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const {
    isUploading,
    uploadProgress,
    uploadedDocument,
    submittedJob,
    uploadAndProcess,
  } = useDocumentUpload((jobId, documentId) => {
    onJobCreated(jobId, documentId);
  });

  const handleFile = async (file: File) => {
    setSelectedFile(file);
    const result = await validateDocumentFile(file);
    setValidationResult(result);

    if (result.isValid) {
      await uploadAndProcess(file);
    }
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
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header & Ingestion Specs */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <UploadCloud className="w-5 h-5 text-indigo-400" />
            Document Ingestion Hub
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Enterprise boundary ingestion with client-side defensive checks and &lt;100ms async job dispatch.
          </p>
        </div>

        <div className="flex items-center gap-2 font-mono text-[11px]">
          <span className="px-2 py-1 rounded bg-slate-900 border border-slate-800 text-slate-300">
            MAX PAYLOAD: <strong className="text-indigo-400">15 MB</strong>
          </span>
          <span className="px-2 py-1 rounded bg-slate-900 border border-slate-800 text-slate-300">
            FORMATS: <strong className="text-cyan-400">PDF, TIFF, PNG, JPEG</strong>
          </span>
        </div>
      </div>

      {/* Drag & Drop Area */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition-all duration-200 group ${
          isDragging
            ? 'border-indigo-500 bg-indigo-950/20 scale-[0.99]'
            : 'border-slate-800 hover:border-indigo-500/50 bg-slate-900/30 hover:bg-slate-900/50'
        }`}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleInputChange}
          accept=".pdf,.png,.jpg,.jpeg,.tiff,.tif"
          className="hidden"
        />

        <div className="flex flex-col items-center justify-center space-y-4">
          <div className="w-16 h-16 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 group-hover:scale-110 group-hover:bg-indigo-500/20 transition-all">
            <UploadCloud className="w-8 h-8" />
          </div>

          <div className="space-y-1.5">
            <h3 className="text-sm font-semibold text-slate-200">
              Drag & drop document here, or <span className="text-indigo-400 underline underline-offset-2">browse filesystem</span>
            </h3>
            <p className="text-xs text-slate-400 font-mono">
              Binary sniffing will verify headers before transmitting to backend
            </p>
          </div>

          <div className="flex flex-wrap justify-center gap-2 pt-2 text-[11px] font-mono">
            {['%PDF-1.7', 'image/png', 'image/jpeg', 'image/tiff'].map((type) => (
              <span
                key={type}
                className="px-2.5 py-1 rounded-md bg-slate-950/80 border border-slate-800/80 text-slate-400 flex items-center gap-1"
              >
                <FileCheck2 className="w-3 h-3 text-indigo-400" />
                {type}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Defensive Validation Real-Time Inspector */}
      {selectedFile && (
        <FileValidator
          filename={selectedFile.name}
          validationResult={validationResult}
        />
      )}

      {/* Asynchronous Ingestion & Dispatch Queue Status */}
      <UploadQueue
        isUploading={isUploading}
        progress={uploadProgress}
        uploadedDocument={uploadedDocument}
        submittedJob={submittedJob}
        onNavigateToJob={(jobId) => {
          if (uploadedDocument) {
            onJobCreated(jobId, uploadedDocument.id);
          }
        }}
      />

      {/* Enterprise Feature Highlights */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">
        <div className="p-3.5 rounded-xl border border-slate-800/80 bg-slate-900/30 flex items-start gap-3">
          <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400">
            <Zap className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-xs font-semibold text-slate-200">Idempotency & SHA-256</h4>
            <p className="text-[11px] text-slate-400 mt-0.5">
              Identical document uploads are deduplicated instantly without redundant OCR cost.
            </p>
          </div>
        </div>

        <div className="p-3.5 rounded-xl border border-slate-800/80 bg-slate-900/30 flex items-start gap-3">
          <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-xs font-semibold text-slate-200">Multimodal Gemini 1.5</h4>
            <p className="text-[11px] text-slate-400 mt-0.5">
              Combines OCR bounding coordinates with neural entity extraction and schema binding.
            </p>
          </div>
        </div>

        <div className="p-3.5 rounded-xl border border-slate-800/80 bg-slate-900/30 flex items-start gap-3">
          <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
            <FileCheck2 className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-xs font-semibold text-slate-200">Human-In-The-Loop</h4>
            <p className="text-[11px] text-slate-400 mt-0.5">
              Confidence scores &lt; 90% automatically trigger synchronized visual review.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
