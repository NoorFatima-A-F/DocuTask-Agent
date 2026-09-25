import React, { useRef, useEffect } from 'react';
import { Check, AlertTriangle, Edit2 } from 'lucide-react';
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
  const isHighConfidence = confidence >= 0.90;

  useEffect(() => {
    if (autoFocusOnLowConfidence && !isHighConfidence && inputRef.current) {
      inputRef.current.focus();
    }
  }, [autoFocusOnLowConfidence, isHighConfidence]);

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
      className={`p-2.5 rounded border transition-colors ${
        isHovered
          ? 'bg-zinc-800/80 border-zinc-600'
          : !isHighConfidence
          ? 'bg-amber-950/20 border-amber-800/40'
          : 'bg-zinc-900/40 border-zinc-800/80 hover:border-zinc-700'
      }`}
    >
      <div className="flex items-center justify-between gap-2 mb-1">
        <label className="text-xs font-medium text-zinc-300 flex items-center gap-1.5">
          <span>{field.label}</span>
          {field.isModified && (
            <span className="text-[10px] font-mono text-zinc-300 bg-zinc-800 px-1 py-0.2 rounded border border-zinc-700">
              MODIFIED
            </span>
          )}
        </label>

        {/* Confidence Tag */}
        <div className="flex items-center font-mono text-[11px]">
          {isHighConfidence ? (
            <span className="flex items-center gap-1 text-zinc-400 bg-zinc-900 px-1.5 py-0.2 rounded border border-zinc-800 text-[10px]">
              <Check className="w-3 h-3 text-zinc-500" />
              {(confidence * 100).toFixed(0)}%
            </span>
          ) : (
            <span className="flex items-center gap-1 text-amber-400 bg-amber-950/40 px-1.5 py-0.2 rounded border border-amber-800/50 text-[10px]">
              <AlertTriangle className="w-3 h-3 text-amber-400" />
              {(confidence * 100).toFixed(0)}% Review Req
            </span>
          )}
        </div>
      </div>

      <div className="relative">
        <input
          ref={inputRef}
          type={typeof field.value === 'number' ? 'number' : 'text'}
          value={field.value}
          onChange={handleChange}
          className={`w-full bg-zinc-950 rounded px-2.5 py-1.5 text-xs font-mono text-zinc-100 border transition-colors focus:outline-none ${
            !isHighConfidence
              ? 'border-amber-700/60 focus:border-amber-500'
              : 'border-zinc-800 focus:border-zinc-500'
          }`}
        />
        <div className="absolute right-2 top-2 text-zinc-600 pointer-events-none">
          <Edit2 className="w-3 h-3" />
        </div>
      </div>
    </div>
  );
};
