import React, { useState } from 'react';
import { ZoomIn, ZoomOut, RotateCw, ChevronLeft, ChevronRight, FileText } from 'lucide-react';
import { ExtractedField } from '../../types/extraction';
import { BoundingBox } from './BoundingBox';

interface DocumentCanvasProps {
  fields: ExtractedField<string | number>[];
  hoveredFieldKey: string | null;
  onHoverField: (key: string | null) => void;
  documentTitle?: string;
}

export const DocumentCanvas: React.FC<DocumentCanvasProps> = ({
  fields,
  hoveredFieldKey,
  onHoverField,
  documentTitle = 'INV-2026-8894.pdf',
}) => {
  const [zoom, setZoom] = useState<number>(100);
  const [rotation, setRotation] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const totalPages = 1;

  const handleZoomIn = () => setZoom((prev) => Math.min(200, prev + 25));
  const handleZoomOut = () => setZoom((prev) => Math.max(50, prev - 25));
  const handleFit = () => setZoom(100);
  const handleRotate = () => setRotation((prev) => (prev + 90) % 360);

  return (
    <div className="flex flex-col h-full rounded border border-[#27272a] bg-[#121215] overflow-hidden">
      {/* Top Toolbar */}
      <div className="h-10 border-b border-[#27272a] bg-[#18181b]/60 px-3 flex items-center justify-between shrink-0 text-xs font-mono select-none">
        <div className="flex items-center gap-2 text-zinc-300">
          <FileText className="w-3.5 h-3.5 text-zinc-400" />
          <span className="font-semibold truncate max-w-[160px] sm:max-w-xs">{documentTitle}</span>
        </div>

        {/* Canvas Controls */}
        <div className="flex items-center gap-1.5">
          <div className="flex items-center bg-zinc-950 rounded border border-zinc-800 p-0.5">
            <button
              onClick={handleZoomOut}
              className="p-1 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 rounded transition-colors"
              title="Zoom Out"
            >
              <ZoomOut className="w-3 h-3" />
            </button>
            <span className="px-1 text-[11px] text-zinc-300 min-w-[36px] text-center">{zoom}%</span>
            <button
              onClick={handleZoomIn}
              className="p-1 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 rounded transition-colors"
              title="Zoom In"
            >
              <ZoomIn className="w-3 h-3" />
            </button>
          </div>

          <button
            onClick={handleFit}
            className="px-1.5 py-1 bg-zinc-950 hover:bg-zinc-800 rounded border border-zinc-800 text-zinc-400 hover:text-zinc-200 text-[10px] transition-colors"
          >
            Fit
          </button>

          <button
            onClick={handleRotate}
            className="p-1 bg-zinc-950 hover:bg-zinc-800 rounded border border-zinc-800 text-zinc-400 hover:text-zinc-200 transition-colors"
            title="Rotate 90°"
          >
            <RotateCw className="w-3 h-3" />
          </button>

          {/* Page Controls */}
          <div className="flex items-center gap-1 pl-1 border-l border-zinc-800">
            <button
              disabled={currentPage <= 1}
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              className="p-1 text-zinc-400 hover:text-zinc-200 disabled:opacity-30 rounded transition-colors"
            >
              <ChevronLeft className="w-3 h-3" />
            </button>
            <span className="text-[10px] text-zinc-400">
              {currentPage}/{totalPages}
            </span>
            <button
              disabled={currentPage >= totalPages}
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              className="p-1 text-zinc-400 hover:text-zinc-200 disabled:opacity-30 rounded transition-colors"
            >
              <ChevronRight className="w-3 h-3" />
            </button>
          </div>
        </div>
      </div>

      {/* Document Canvas Viewport */}
      <div className="flex-1 overflow-auto p-4 flex items-center justify-center bg-[#09090b] relative">
        <div
          style={{
            transform: `scale(${zoom / 100}) rotate(${rotation}deg)`,
            transformOrigin: 'center center',
            transition: 'transform 0.12s ease-out',
          }}
          className="relative w-[500px] min-h-[660px] bg-[#121215] border border-zinc-800 rounded p-7 shadow text-zinc-200 select-none"
        >
          {/* High Contrast Invoice Header */}
          <div className="border-b border-zinc-700 pb-3 mb-5 flex justify-between items-start">
            <div>
              <h1 className="text-lg font-bold tracking-tight text-white font-mono">
                ACME CLOUD CORP
              </h1>
              <p className="text-[11px] text-zinc-400 mt-0.5">Enterprise Cloud Infrastructure</p>
              <p className="text-[11px] text-zinc-500 font-mono">Tax ID: US-948291048</p>
            </div>
            <div className="text-right">
              <span className="text-[11px] font-mono font-semibold px-1.5 py-0.5 bg-zinc-800 text-zinc-200 border border-zinc-700 rounded">
                COMMERCIAL INVOICE
              </span>
              <p className="text-xs font-mono text-zinc-300 mt-1.5 font-semibold">#INV-2026-8894</p>
              <p className="text-[11px] text-zinc-400 font-mono">2026-09-24</p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 mb-5 text-xs">
            <div className="p-2.5 bg-zinc-950 rounded border border-zinc-800/80">
              <span className="text-[10px] text-zinc-500 uppercase font-mono block mb-0.5">Billed To</span>
              <p className="font-semibold text-zinc-200">Global Logistics Corp</p>
              <p className="text-[11px] text-zinc-400">742 Evergreen Terrace</p>
            </div>
            <div className="p-2.5 bg-zinc-950 rounded border border-zinc-800/80">
              <span className="text-[10px] text-zinc-500 uppercase font-mono block mb-0.5">Terms</span>
              <p className="text-zinc-200 font-mono">Net 30 Days</p>
              <p className="text-[11px] text-zinc-400 font-mono">Due: 2026-10-24</p>
            </div>
          </div>

          {/* Line items table */}
          <div className="mb-5">
            <table className="w-full text-left text-xs font-mono">
              <thead>
                <tr className="border-b border-zinc-800 text-zinc-500 text-[10px] uppercase">
                  <th className="pb-1.5">Description</th>
                  <th className="pb-1.5 text-center">Qty</th>
                  <th className="pb-1.5 text-right">Unit Price</th>
                  <th className="pb-1.5 text-right">Total</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800/60 text-zinc-300 text-[11px]">
                <tr>
                  <td className="py-2">GPU Compute Cluster (A100 x8)</td>
                  <td className="py-2 text-center">2</td>
                  <td className="py-2 text-right">$4,250.00</td>
                  <td className="py-2 text-right">$8,500.00</td>
                </tr>
                <tr>
                  <td className="py-2">Managed High-Throughput NVMe</td>
                  <td className="py-2 text-center">1</td>
                  <td className="py-2 text-right">$1,200.00</td>
                  <td className="py-2 text-right">$1,200.00</td>
                </tr>
                <tr>
                  <td className="py-2">Enterprise Direct Connect 10G</td>
                  <td className="py-2 text-center">1</td>
                  <td className="py-2 text-right">$850.00</td>
                  <td className="py-2 text-right">$850.00</td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Financial summary */}
          <div className="border-t border-zinc-800 pt-3 flex justify-end">
            <div className="w-48 space-y-1 text-xs font-mono">
              <div className="flex justify-between text-zinc-400">
                <span>Subtotal:</span>
                <span>$10,550.00</span>
              </div>
              <div className="flex justify-between text-zinc-400">
                <span>Tax (8.25%):</span>
                <span>$870.38</span>
              </div>
              <div className="flex justify-between text-zinc-100 font-bold border-t border-zinc-800 pt-1 text-xs">
                <span>Grand Total:</span>
                <span className="text-zinc-100">$11,420.38</span>
              </div>
            </div>
          </div>

          {/* Bounding box overlays */}
          {fields.map((field) => {
            if (!field.boundingBox) return null;
            return (
              <BoundingBox
                key={field.key}
                box={field.boundingBox}
                label={field.label}
                confidence={field.confidence}
                isHovered={hoveredFieldKey === field.key}
                onHover={(hovered) => onHoverField(hovered ? field.key : null)}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
};
