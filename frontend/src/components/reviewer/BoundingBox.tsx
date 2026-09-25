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
  const left = `${box.x_min * 100}%`;
  const top = `${box.y_min * 100}%`;
  const width = `${(box.x_max - box.x_min) * 100}%`;
  const height = `${(box.y_max - box.y_min) * 100}%`;

  let borderColor = 'border-emerald-500/80 bg-emerald-500/10 text-emerald-300';
  if (confidence < 0.70) {
    borderColor = 'border-rose-500/80 bg-rose-500/15 text-rose-300';
  } else if (confidence < 0.90) {
    borderColor = 'border-amber-500/80 bg-amber-500/15 text-amber-300';
  }

  return (
    <div
      onMouseEnter={() => onHover(true)}
      onMouseLeave={() => onHover(false)}
      style={{ left, top, width, height }}
      className={`absolute border rounded-[2px] transition-all cursor-pointer pointer-events-auto ${borderColor} ${
        isHovered ? 'ring-1 ring-white z-20 shadow' : 'z-10'
      }`}
    >
      <div className="absolute -top-4 left-0 px-1 py-0.2 rounded bg-zinc-950 border border-zinc-700 text-[9px] font-mono font-medium whitespace-nowrap shadow flex items-center gap-1">
        <span>{label}</span>
        <span className="text-zinc-400">({(confidence * 100).toFixed(0)}%)</span>
      </div>
    </div>
  );
};
