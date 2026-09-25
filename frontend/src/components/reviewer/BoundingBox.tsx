import React from 'react';
import { BoundingBox as BoundingBoxType } from '../../types/extraction';

interface BoundingBoxProps {
  box: BoundingBoxType;
  label: string;
  confidence: number;
  isHovered: boolean;
  onHover: (hovered: boolean) => void;
}

export const BoundingBox: React.FC<BoundingBoxProps> = ({
  box,
  label,
  confidence,
  isHovered,
  onHover,
}) => {
  // Convert normalized [0, 1] coordinates to percentages
  const left = `${box.x_min * 100}%`;
  const top = `${box.y_min * 100}%`;
  const width = `${(box.x_max - box.x_min) * 100}%`;
  const height = `${(box.y_max - box.y_min) * 100}%`;

  let borderColor = 'border-emerald-400 bg-emerald-500/10 text-emerald-300';
  if (confidence < 0.70) {
    borderColor = 'border-rose-500 bg-rose-500/15 text-rose-300';
  } else if (confidence < 0.90) {
    borderColor = 'border-amber-400 bg-amber-500/15 text-amber-300';
  }

  return (
    <div
      onMouseEnter={() => onHover(true)}
      onMouseLeave={() => onHover(false)}
      style={{ left, top, width, height }}
      className={`absolute border-2 rounded transition-all cursor-pointer pointer-events-auto ${borderColor} ${
        isHovered
          ? 'ring-2 ring-indigo-400 ring-offset-1 ring-offset-slate-950 scale-[1.02] z-20 shadow-lg'
          : 'z-10'
      }`}
    >
      <div className="absolute -top-5 left-0 px-1.5 py-0.2 rounded bg-slate-950/90 border border-slate-700 text-[10px] font-mono font-semibold whitespace-nowrap shadow-md flex items-center gap-1">
        <span>{label}</span>
        <span className="opacity-75">({(confidence * 100).toFixed(0)}%)</span>
      </div>
    </div>
  );
};
