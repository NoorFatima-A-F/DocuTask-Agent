import React, { useState } from 'react';
import {
  ZoomIn,
  ZoomOut,
  RotateCw,
  Maximize2,
  ChevronLeft,
  ChevronRight,
  Layers,
} from 'lucide-react';
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
  const handleFitWidth = () => setZoom(100);
  const handleRotate = () => setRotation((prev) => (prev + 90) % 360);

  return (
    <div className="flex flex-col h-full rounded-2xl border border-slate-800 bg-slate-950/60 overflow-hidden">
      {/* Top Toolbar */}
      <div className="h-11 border-b border-slate-800 bg-slate-900/60 px-3 flex items-center justify-between shrink-0 text-xs font-mono">
        <div className="flex items-center gap-2 text-slate-300">
          <Layers className="w-4 h-4 text-indigo-400" />
          <span className="font-semibold truncate max-w-[140px] sm:max-w-xs">
            {documentTitle}
          </span>
        </div>

        {/* Canvas Controls */}
        <div className="flex items-center gap-1.5">
          {/* Zoom Controls */}
          <div className="flex items-center bg-slate-950 rounded-lg border border-slate-800 p-0.5">
            <button
              onClick={handleZoomOut}
              className="p-1 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded transition-colors"
              title="Zoom Out"
            >
              <ZoomOut className="w-3.5 h-3.5" />
            </button>
            <span className="px-1.5 text-[11px] text-slate-300 min-w-[42px] text-center">
              {zoom}%
            </span>
            <button
              onClick={handleZoomIn}
              className="p-1 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded transition-colors"
              title="Zoom In"
            >
              <ZoomIn className="w-3.5 h-3.5" />
            </button>
          </div>

          <button
            onClick={handleFitWidth}
            className="p-1.5 bg-slate-950 hover:bg-slate-800 rounded-lg border border-slate-800 text-slate-400 hover:text-slate-200 transition-colors"
            title="Fit Width"
          >
            <Maximize2 className="w-3.5 h-3.5" />
          </button>

          <button
            onClick={handleRotate}
            className="p-1.5 bg-slate-950 hover:bg-slate-800 rounded-lg border border-slate-800 text-slate-400 hover:text-slate-200 transition-colors"
            title="Rotate 90°"
          >
            <RotateCw className="w-3.5 h-3.5" />
          </button>

          {/* Page Navigation */}
          <div className="flex items-center gap-1 pl-1 border-l border-slate-800">
            <button
              disabled={currentPage <= 1}
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              className="p-1 text-slate-400 hover:text-slate-200 disabled:opacity-30 rounded transition-colors"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
            </button>
            <span className="text-[11px] text-slate-400">
              {currentPage}/{totalPages}
            </span>
            <button
              disabled={currentPage >= totalPages}
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              className="p-1 text-slate-400 hover:text-slate-200 disabled:opacity-30 rounded transition-colors"
            >
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Document Viewport Area */}
      <div className="flex-1 overflow-auto p-6 flex items-center justify-center bg-slate-950/80 relative">
        <div
          style={{
            transform: `scale(${zoom / 100}) rotate(${rotation}deg)`,
            transformOrigin: 'center center',
            transition: 'transform 0.15s ease-out',
          }}
          className="relative w-[540px] min-h-[720px] bg-slate-900 border border-slate-800 rounded-lg p-8 shadow-2xl text-slate-200 select-none"
        >
          {/* Document Sample Layout Skeleton */}
          <div className="border-b-2 border-indigo-500/40 pb-4 mb-6 flex justify-between items-start">
            <div>
              <h1 className="text-xl font-bold tracking-tight text-white font-mono">
                ACME CLOUD CORP
              </h1>
              <p className="text-[11px] text-slate-400 mt-1">
                Enterprise Cloud Infrastructure & Platform Services
              </p>
              <p className="text-[11px] text-slate-400">Tax ID: US-948291048</p>
            </div>
            <div className="text-right">
              <span className="text-xs font-mono font-bold px-2 py-1 bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 rounded">
                COMMERCIAL INVOICE
              </span>
              <p className="text-xs font-mono text-slate-300 mt-2">
                #INV-2026-8894
              </p>
              <p className="text-[11px] text-slate-400">Date: 2026-09-24</p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-6 text-xs">
            <div className="p-3 bg-slate-950/60 rounded border border-slate-800">
              <span className="text-[10px] text-slate-400 uppercase font-mono block mb-1">
                Billed To:
              </span>
              <p className="font-semibold text-slate-200">Global Logistics Corp</p>
              <p className="text-[11px] text-slate-400">742 Evergreen Terrace</p>
              <p className="text-[11px] text-slate-400">Tax ID: US-482910391</p>
            </div>
            <div className="p-3 bg-slate-950/60 rounded border border-slate-800">
              <span className="text-[10px] text-slate-400 uppercase font-mono block mb-1">
                Payment Terms:
              </span>
              <p className="text-slate-200 font-mono">Net 30 Days</p>
              <p className="text-[11px] text-slate-400">Due Date: 2026-10-24</p>
              <p className="text-[11px] text-slate-400">Currency: USD ($)</p>
            </div>
          </div>

          {/* Line Items Table Skeleton */}
          <div className="mb-6">
            <table className="w-full text-left text-xs font-mono">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 text-[10px] uppercase">
                  <th className="pb-2">Description</th>
                  <th className="pb-2 text-center">Qty</th>
                  <th className="pb-2 text-right">Unit Price</th>
                  <th className="pb-2 text-right">Total</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-300 text-[11px]">
                <tr>
                  <td className="py-2.5">GPU Compute Cluster (A100 x8)</td>
                  <td className="py-2.5 text-center">2</td>
                  <td className="py-2.5 text-right">$4,250.00</td>
                  <td className="py-2.5 text-right">$8,500.00</td>
                </tr>
                <tr>
                  <td className="py-2.5">Managed High-Throughput NVMe (10TB)</td>
                  <td className="py-2.5 text-center">1</td>
                  <td className="py-2.5 text-right">$1,200.00</td>
                  <td className="py-2.5 text-right">$1,200.00</td>
                </tr>
                <tr>
                  <td className="py-2.5">Enterprise Direct Connect 10Gbps</td>
                  <td className="py-2.5 text-center">1</td>
                  <td className="py-2.5 text-right">$850.00</td>
                  <td className="py-2.5 text-right">$850.00</td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Financial Totals */}
          <div className="border-t border-slate-800 pt-4 flex justify-end">
            <div className="w-52 space-y-1.5 text-xs font-mono">
              <div className="flex justify-between text-slate-400">
                <span>Subtotal:</span>
                <span>$10,550.00</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Sales Tax (8.25%):</span>
                <span>$870.38</span>
              </div>
              <div className="flex justify-between text-slate-100 font-bold border-t border-slate-800 pt-1.5 text-sm">
                <span>Total Amount:</span>
                <span className="text-emerald-400">$11,420.38</span>
              </div>
            </div>
          </div>

          {/* Interactive Bounding Box Coordinate Overlays */}
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
