import React from 'react';
import { ShieldCheck, AlertCircle, FileCheck, Hash, HardDrive } from 'lucide-react';
import { DocumentValidationResult } from '../../types/document';

interface FileValidatorProps {
  validationResult: DocumentValidationResult | null;
  filename: string;
}

export const FileValidator: React.FC<FileValidatorProps> = ({
  validationResult,
  filename,
}) => {
  if (!validationResult) return null;

  const { isValid, error, detectedMimeType, sizeBytes, sha256Hex } = validationResult;
  const sizeMb = (sizeBytes / (1024 * 1024)).toFixed(2);

  return (
    <div
      className={`p-4 rounded-xl border transition-all ${
        isValid
          ? 'bg-emerald-950/20 border-emerald-500/30'
          : 'bg-rose-950/20 border-rose-500/30'
      }`}
    >
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-2.5">
          {isValid ? (
            <ShieldCheck className="w-5 h-5 text-emerald-400 shrink-0" />
          ) : (
            <AlertCircle className="w-5 h-5 text-rose-400 shrink-0" />
          )}
          <div>
            <h4 className="text-xs font-semibold text-slate-100 flex items-center gap-2">
              <span>{filename}</span>
              <span
                className={`text-[10px] font-mono px-1.5 py-0.5 rounded border ${
                  isValid
                    ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30'
                    : 'text-rose-400 bg-rose-500/10 border-rose-500/30'
                }`}
              >
                {isValid ? 'VALIDATED' : 'REJECTED'}
              </span>
            </h4>
            <p className="text-[11px] text-slate-400 mt-0.5">
              {isValid
                ? 'Passed magic-byte inspection and payload size perimeter.'
                : error}
            </p>
          </div>
        </div>
      </div>

      {/* Defensive Guard Inspection Breakdown */}
      {isValid && (
        <div className="mt-3 pt-3 border-t border-slate-800/80 grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs font-mono">
          <div className="flex items-center gap-2 p-2 rounded-lg bg-slate-900/60 border border-slate-800">
            <FileCheck className="w-3.5 h-3.5 text-indigo-400" />
            <div className="flex flex-col">
              <span className="text-[10px] text-slate-400 uppercase">MIME Type</span>
              <span className="text-slate-200 truncate">{detectedMimeType}</span>
            </div>
          </div>

          <div className="flex items-center gap-2 p-2 rounded-lg bg-slate-900/60 border border-slate-800">
            <HardDrive className="w-3.5 h-3.5 text-cyan-400" />
            <div className="flex flex-col">
              <span className="text-[10px] text-slate-400 uppercase">Payload Size</span>
              <span className="text-slate-200">{sizeMb} MB &lt; 15 MB</span>
            </div>
          </div>

          <div className="flex items-center gap-2 p-2 rounded-lg bg-slate-900/60 border border-slate-800">
            <Hash className="w-3.5 h-3.5 text-emerald-400" />
            <div className="flex flex-col">
              <span className="text-[10px] text-slate-400 uppercase">SHA-256 Digest</span>
              <span className="text-slate-200 truncate" title={sha256Hex}>
                {sha256Hex ? `${sha256Hex.substring(0, 12)}...` : 'Computing...'}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
