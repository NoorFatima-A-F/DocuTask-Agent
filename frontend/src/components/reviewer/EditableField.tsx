import React, { useRef, useEffect } from 'react';
import {
  AlertTriangle,
  Check,
  Edit2,
  Sparkles,
} from 'lucide-react';
import { ExtractedField } from '../../types/extraction';

interface EditableFieldProps {
  field: ExtractedField<string | number>;
  onValueChange: (key: string, newValue: string | number) => void;
  isHovered?: boolean;
  onHover?: (hovered: boolean) => void;
  autoFocusOnLowConfidence?: boolean;
}

export const EditableField: React.FC<EditableFieldProps> = ({
  field,
  onValueChange,
  isHovered,
  onHover,
  autoFocusOnLowConfidence = true,
}) => {
  const inputRef = useRef<HTMLInputElement>(null);
  const confidence = field.confidence;
  const isLow = confidence < 0.70;
  const isMedium = confidence >= 0.70 && confidence < 0.90;
  const isHigh = confidence >= 0.90;

  // Auto-focus field if confidence is low to prompt operator verification
  useEffect(() => {
    if (autoFocusOnLowConfidence && isLow && inputRef.current) {
      inputRef.current.focus();
    }
  }, [autoFocusOnLowConfidence, isLow]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const rawVal = e.target.value;
    const isNum = typeof field.value === 'number';
    const parsedVal = isNum ? parseFloat(rawVal) || 0 : rawVal;
    onValueChange(field.key, parsedVal);
  };

  return (
    <div
      onMouseEnter={() => onHover?.(true)}
      onMouseLeave={() => onHover?.(false)}
      className={`p-3 rounded-xl border transition-all ${
        isHovered
          ? 'bg-indigo-950/20 border-indigo-500/50 shadow-md'
          : isLow
          ? 'bg-rose-950/20 border-rose-500/40'
          : isMedium
          ? 'bg-amber-950/20 border-amber-500/40'
          : 'bg-slate-900/40 border-slate-800/80 hover:border-slate-700'
      }`}
    >
      <div className="flex items-center justify-between gap-2 mb-1.5">
        <label className="text-xs font-medium text-slate-300 flex items-center gap-1.5">
          <span>{field.label}</span>
          {field.isModified && (
            <span className="text-[10px] font-mono text-indigo-400 bg-indigo-500/10 px-1 py-0.2 rounded border border-indigo-500/30">
              MODIFIED
            </span>
          )}
        </label>

        {/* Confidence Tier Badge */}
        <div className="flex items-center gap-1 font-mono text-[11px]">
          {isHigh && (
            <span className="flex items-center gap-1 text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded border border-emerald-500/30">
              <Check className="w-3 h-3" />
              {(confidence * 100).toFixed(0)}%
            </span>
          )}
          {isMedium && (
            <span className="flex items-center gap-1 text-amber-400 bg-amber-500/10 px-1.5 py-0.5 rounded border border-amber-500/30">
              <Sparkles className="w-3 h-3" />
              {(confidence * 100).toFixed(0)}% Low Conf
            </span>
          )}
          {isLow && (
            <span className="flex items-center gap-1 text-rose-400 bg-rose-500/10 px-1.5 py-0.5 rounded border border-rose-500/30 animate-pulse">
              <AlertTriangle className="w-3 h-3" />
              {(confidence * 100).toFixed(0)}% Review Req
            </span>
          )}
        </div>
      </div>

      {/* Input Form Field */}
      <div className="relative">
        <input
          ref={inputRef}
          type={typeof field.value === 'number' ? 'number' : 'text'}
          value={field.value}
          onChange={handleChange}
          className={`w-full bg-slate-950/80 rounded-lg px-3 py-1.5 text-xs font-mono text-slate-100 border transition-all focus:outline-none focus:ring-1 ${
            isLow
              ? 'border-rose-500/50 focus:ring-rose-500'
              : isMedium
              ? 'border-amber-500/50 focus:ring-amber-500'
              : 'border-slate-800 focus:border-indigo-500 focus:ring-indigo-500'
          }`}
        />
        <div className="absolute right-2.5 top-2 text-slate-500 pointer-events-none">
          <Edit2 className="w-3 h-3" />
        </div>
      </div>

      {/* Validation regex or boundary helper */}
      {field.validationRegex && (
        <span className="text-[10px] font-mono text-slate-400 mt-1 block">
          Regex Rule: <code className="text-slate-400">{field.validationRegex}</code>
        </span>
      )}
    </div>
  );
};
