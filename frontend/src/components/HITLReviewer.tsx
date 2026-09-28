import React, { useState } from 'react';
import { DocumentJob, StructuredInvoiceData, LineItem } from '../types/document';
import {
  CheckCircle2,
  AlertTriangle,
  FileText,
  ZoomIn,
  ZoomOut,
  RotateCw,
  Download,
  Eye,
  Code,
  Check,
  Sparkles,
  Layers,
  ArrowLeft,
} from 'lucide-react';

interface HITLReviewerProps {
  job: DocumentJob;
  onBack: () => void;
  onSave: (updatedJob: DocumentJob) => void;
}

export const HITLReviewer: React.FC<HITLReviewerProps> = ({ job, onBack, onSave }) => {
  const [data, setData] = useState<StructuredInvoiceData>(
    job.extracted_data || {
      invoice_number: { value: 'INV-1001', confidence: 0.95 },
      vendor_name: { value: 'Acme Corp', confidence: 0.92 },
      invoice_date: { value: '2026-09-20', confidence: 0.76 },
      due_date: { value: '2026-10-20', confidence: 0.90 },
      subtotal: { value: 1200.0, confidence: 0.98 },
      tax_amount: { value: 120.0, confidence: 0.95 },
      total_amount: { value: 1320.0, confidence: 0.82 },
      currency: { value: 'USD', confidence: 0.99 },
      payment_terms: { value: 'Net 30', confidence: 0.88 },
      line_items: [],
    }
  );

  const [activeTab, setActiveTab] = useState<'form' | 'json' | 'ocr'>('form');
  const [zoomLevel, setZoomLevel] = useState<number>(100);
  const [rotation, setRotation] = useState<number>(0);
  const [isSaved, setIsSaved] = useState<boolean>(false);

  const lowConfidenceCount = Object.entries(data).filter(([key, val]) => {
    if (key === 'line_items') {
      return (val as LineItem[]).some((li) => li.confidence < 0.85);
    }
    return (val as any)?.confidence < 0.85;
  }).length;

  const handleFieldChange = (fieldKey: keyof StructuredInvoiceData, newValue: any) => {
    setData((prev: StructuredInvoiceData) => ({
      ...prev,
      [fieldKey]: {
        ...(prev[fieldKey] as any),
        value: newValue,
        is_verified_by_human: true,
        confidence: 1.0, // Human verified gets 100% confidence
      },
    }));
    setIsSaved(false);
  };

  const handleLineItemChange = (id: string, field: keyof LineItem, val: any) => {
    setData((prev: StructuredInvoiceData) => ({
      ...prev,
      line_items: prev.line_items.map((item: LineItem) =>
        item.id === id ? { ...item, [field]: val, confidence: 1.0 } : item
      ),
    }));
    setIsSaved(false);
  };

  const handleVerifyAll = () => {
    const verifiedData = { ...data };
    Object.keys(verifiedData).forEach((k) => {
      if (k !== 'line_items' && (verifiedData as any)[k]) {
        (verifiedData as any)[k].is_verified_by_human = true;
        (verifiedData as any)[k].confidence = 1.0;
      }
    });
    setData(verifiedData);
    setIsSaved(true);
    onSave({
      ...job,
      extracted_data: verifiedData,
      requires_hitl: false,
      overall_confidence: 1.0,
      current_step: 'Human-in-the-Loop Verification Approved & Committed',
    });
  };

  const handleExportJSON = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${job.document_name}_verified.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-2xl">
      {/* Top Action Bar */}
      <div className="flex items-center justify-between px-6 py-3 bg-slate-950/80 border-b border-slate-800 backdrop-blur-md">
        <div className="flex items-center space-x-4">
          <button
            onClick={onBack}
            className="flex items-center space-x-1.5 text-xs text-slate-400 hover:text-white px-2.5 py-1.5 rounded-lg bg-slate-800/60 hover:bg-slate-800 transition"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Queue</span>
          </button>
          <div className="h-4 w-px bg-slate-800" />
          <div className="flex items-center space-x-2">
            <FileText className="w-4 h-4 text-blue-400" />
            <span className="text-sm font-semibold text-white truncate max-w-[240px]">
              {job.document_name}
            </span>
            <span className="text-xs text-slate-500 font-mono">({job.file_size})</span>
          </div>
          {lowConfidenceCount > 0 ? (
            <span className="flex items-center space-x-1 text-xs px-2.5 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 font-medium">
              <AlertTriangle className="w-3 h-3 text-amber-400" />
              <span>{lowConfidenceCount} Fields Require Sign-off (&lt;85%)</span>
            </span>
          ) : (
            <span className="flex items-center space-x-1 text-xs px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-medium">
              <CheckCircle2 className="w-3 h-3 text-emerald-400" />
              <span>HITL Certified (100% Verified)</span>
            </span>
          )}
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleExportJSON}
            className="flex items-center space-x-1.5 text-xs px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export Verified JSON</span>
          </button>
          <button
            onClick={handleVerifyAll}
            className="flex items-center space-x-1.5 text-xs px-4 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-medium shadow-lg shadow-blue-600/20 transition"
          >
            <Check className="w-3.5 h-3.5" />
            <span>Approve &amp; Commit to DB</span>
          </button>
        </div>
      </div>

      {/* Two-Pane Workspace Layout */}
      <div className="grid grid-cols-12 flex-1 overflow-hidden">
        {/* LEFT PANE: Document Scan / PDF Viewer */}
        <div className="col-span-6 border-r border-slate-800 flex flex-col bg-slate-950/50">
          {/* Viewer Toolbar */}
          <div className="flex items-center justify-between px-4 py-2 bg-slate-900/60 border-b border-slate-800 text-xs text-slate-400">
            <span className="flex items-center space-x-1 font-medium">
              <Layers className="w-3.5 h-3.5 text-blue-400" />
              <span>Raw Document Binary (Left Canvas)</span>
            </span>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setZoomLevel((z) => Math.max(50, z - 15))}
                className="p-1 hover:text-white bg-slate-800/60 rounded"
                title="Zoom Out"
              >
                <ZoomOut className="w-3.5 h-3.5" />
              </button>
              <span className="font-mono text-[11px] text-slate-300 w-10 text-center">
                {zoomLevel}%
              </span>
              <button
                onClick={() => setZoomLevel((z) => Math.min(180, z + 15))}
                className="p-1 hover:text-white bg-slate-800/60 rounded"
                title="Zoom In"
              >
                <ZoomIn className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => setRotation((r) => (r + 90) % 360)}
                className="p-1 hover:text-white bg-slate-800/60 rounded"
                title="Rotate Clockwise"
              >
                <RotateCw className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Document Canvas Area */}
          <div className="flex-1 overflow-auto p-6 flex items-center justify-center bg-slate-950/80">
            <div
              className="relative transition-all duration-200 bg-white rounded-lg shadow-2xl p-8 max-w-full text-slate-900 select-none"
              style={{
                transform: `scale(${zoomLevel / 100}) rotate(${rotation}deg)`,
                transformOrigin: 'center center',
                width: '560px',
                minHeight: '720px',
              }}
            >
              {/* Simulated Visual Document Canvas with Bounding Boxes */}
              <div className="border-b-2 border-slate-200 pb-4 mb-6 flex justify-between items-start">
                <div>
                  <h1 className="text-2xl font-black tracking-tight text-slate-900">
                    {data.vendor_name.value || 'APEX LOGISTICS INC.'}
                  </h1>
                  <p className="text-xs text-slate-500 mt-1">100 Tech Enterprise Blvd, Suite 400</p>
                  <p className="text-xs text-slate-500">San Francisco, CA 94107</p>
                </div>
                <div className="text-right">
                  <span className="text-xs font-bold uppercase tracking-widest text-blue-600 block">
                    INVOICE
                  </span>
                  <span className="text-sm font-mono font-bold text-slate-800">
                    {data.invoice_number.value}
                  </span>
                </div>
              </div>

              {/* Invoice Metadata Grid */}
              <div className="grid grid-cols-2 gap-4 mb-6 text-xs border p-3 rounded bg-slate-50">
                <div>
                  <span className="text-slate-400 block font-semibold">INVOICE DATE:</span>
                  <span
                    className={`font-mono font-bold ${
                      data.invoice_date.confidence < 0.85
                        ? 'bg-amber-100 text-amber-900 px-1 rounded border border-amber-300'
                        : 'text-slate-800'
                    }`}
                  >
                    {data.invoice_date.value}
                  </span>
                </div>
                <div>
                  <span className="text-slate-400 block font-semibold">DUE DATE:</span>
                  <span className="font-mono text-slate-800 font-bold">{data.due_date.value}</span>
                </div>
                <div>
                  <span className="text-slate-400 block font-semibold">PAYMENT TERMS:</span>
                  <span className="text-slate-800">{data.payment_terms?.value || 'N/A'}</span>
                </div>
                <div>
                  <span className="text-slate-400 block font-semibold">CURRENCY:</span>
                  <span className="font-mono text-slate-800 font-bold">{data.currency.value}</span>
                </div>
              </div>

              {/* Line Items Table Canvas */}
              <table className="w-full text-left text-xs mb-6 border-collapse">
                <thead>
                  <tr className="border-b border-slate-300 text-slate-500 font-semibold">
                    <th className="py-1">Description</th>
                    <th className="py-1 text-center">Qty</th>
                    <th className="py-1 text-right">Unit Price</th>
                    <th className="py-1 text-right">Total</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {data.line_items.map((item: LineItem) => (
                    <tr key={item.id} className="hover:bg-blue-50/50 transition">
                      <td className="py-2 text-slate-800 pr-2">{item.description}</td>
                      <td className="py-2 text-center font-mono text-slate-700">{item.quantity}</td>
                      <td className="py-2 text-right font-mono text-slate-700">
                        ${item.unit_price.toFixed(2)}
                      </td>
                      <td className="py-2 text-right font-mono font-bold text-slate-900">
                        ${item.total_price.toFixed(2)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {/* Financial Totals Box */}
              <div className="border-t-2 border-slate-200 pt-4 flex justify-end">
                <div className="w-48 space-y-1.5 text-xs">
                  <div className="flex justify-between text-slate-600">
                    <span>Subtotal:</span>
                    <span className="font-mono">${Number(data.subtotal.value || 0).toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-slate-600">
                    <span>Tax (8.5%):</span>
                    <span className="font-mono">${Number(data.tax_amount.value || 0).toFixed(2)}</span>
                  </div>
                  <div
                    className={`flex justify-between text-sm font-bold pt-2 border-t border-slate-300 ${
                      data.total_amount.confidence < 0.85
                        ? 'bg-amber-100 text-amber-900 p-1.5 rounded border border-amber-300'
                        : 'text-slate-900'
                    }`}
                  >
                    <span>Total:</span>
                    <span className="font-mono">${Number(data.total_amount.value || 0).toFixed(2)}</span>
                  </div>
                </div>
              </div>

              {/* Verified Stamp Overlay */}
              {isSaved && (
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 rotate-[-18deg] border-4 border-emerald-600 text-emerald-600 font-black text-2xl uppercase tracking-widest px-6 py-2 rounded-lg opacity-85 pointer-events-none bg-emerald-50/90 shadow-xl">
                  HITL APPROVED
                </div>
              )}
            </div>
          </div>
        </div>

        {/* RIGHT PANE: Structured Schema & Human Verification Editor */}
        <div className="col-span-6 flex flex-col bg-slate-900 overflow-hidden">
          {/* Pane View Switcher */}
          <div className="flex items-center justify-between px-6 py-2 bg-slate-950/60 border-b border-slate-800 text-xs">
            <div className="flex items-center space-x-1 bg-slate-900 p-1 rounded-lg border border-slate-800">
              <button
                onClick={() => setActiveTab('form')}
                className={`flex items-center space-x-1.5 px-3 py-1 rounded-md transition ${
                  activeTab === 'form' ? 'bg-blue-600 text-white font-medium' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <Eye className="w-3.5 h-3.5" />
                <span>Structured Form</span>
              </button>
              <button
                onClick={() => setActiveTab('json')}
                className={`flex items-center space-x-1.5 px-3 py-1 rounded-md transition ${
                  activeTab === 'json' ? 'bg-blue-600 text-white font-medium' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <Code className="w-3.5 h-3.5" />
                <span>Pydantic JSON</span>
              </button>
            </div>

            <div className="flex items-center space-x-2 text-slate-400">
              <Sparkles className="w-3.5 h-3.5 text-blue-400" />
              <span className="text-[11px]">Gemini Multimodal AI + Pydantic Schema</span>
            </div>
          </div>

          {/* Pane Content */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {activeTab === 'form' && (
              <>
                {/* Confidence Guidance Banner */}
                {lowConfidenceCount > 0 && (
                  <div className="flex items-start space-x-3 p-3.5 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-200 text-xs">
                    <AlertTriangle className="w-4 h-4 text-amber-400 mt-0.5 flex-shrink-0" />
                    <div>
                      <span className="font-semibold block text-amber-300">
                        Human-in-the-Loop Sign-off Required
                      </span>
                      Highlighted fields have model confidence scores below 85% (e.g. handwritten/blurry
                      source text). Please verify or edit the values before committing to the database.
                    </div>
                  </div>
                )}

                {/* Core Extracted Header Fields */}
                <div className="grid grid-cols-2 gap-4">
                  {/* Vendor Name */}
                  <FieldEditor
                    label="Vendor / Entity Name"
                    fieldKey="vendor_name"
                    field={data.vendor_name}
                    onChange={(val) => handleFieldChange('vendor_name', val)}
                  />

                  {/* Invoice Number */}
                  <FieldEditor
                    label="Invoice Number"
                    fieldKey="invoice_number"
                    field={data.invoice_number}
                    onChange={(val) => handleFieldChange('invoice_number', val)}
                  />

                  {/* Invoice Date (Potential Low Confidence) */}
                  <FieldEditor
                    label="Invoice Date"
                    fieldKey="invoice_date"
                    field={data.invoice_date}
                    onChange={(val) => handleFieldChange('invoice_date', val)}
                    type="date"
                  />

                  {/* Due Date */}
                  <FieldEditor
                    label="Due Date"
                    fieldKey="due_date"
                    field={data.due_date}
                    onChange={(val) => handleFieldChange('due_date', val)}
                    type="date"
                  />
                </div>

                {/* Financial Summary Fields */}
                <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800 space-y-4">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center justify-between">
                    <span>Financial Totals &amp; Tax Extraction</span>
                    <span className="text-[11px] font-mono text-slate-500">Currency: {String(data.currency.value)}</span>
                  </h3>
                  <div className="grid grid-cols-3 gap-4">
                    <FieldEditor
                      label="Subtotal ($)"
                      fieldKey="subtotal"
                      field={data.subtotal}
                      onChange={(val) => handleFieldChange('subtotal', parseFloat(val) || 0)}
                      type="number"
                    />
                    <FieldEditor
                      label="Tax Amount ($)"
                      fieldKey="tax_amount"
                      field={data.tax_amount}
                      onChange={(val) => handleFieldChange('tax_amount', parseFloat(val) || 0)}
                      type="number"
                    />
                    <FieldEditor
                      label="Total Amount ($)"
                      fieldKey="total_amount"
                      field={data.total_amount}
                      onChange={(val) => handleFieldChange('total_amount', parseFloat(val) || 0)}
                      type="number"
                    />
                  </div>
                </div>

                {/* Line Items Table */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                      Line Items Breakdown ({data.line_items.length})
                    </h3>
                  </div>

                  <div className="border border-slate-800 rounded-lg overflow-hidden bg-slate-950/40">
                    <table className="w-full text-left text-xs">
                      <thead className="bg-slate-900/80 text-slate-400 border-b border-slate-800">
                        <tr>
                          <th className="p-2.5">Item Description</th>
                          <th className="p-2.5 w-16 text-center">Qty</th>
                          <th className="p-2.5 w-24 text-right">Unit Price</th>
                          <th className="p-2.5 w-24 text-right">Total</th>
                          <th className="p-2.5 w-20 text-center">Score</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/60">
                        {data.line_items.map((li: LineItem) => (
                          <tr key={li.id} className="hover:bg-slate-800/30 transition">
                            <td className="p-2">
                              <input
                                type="text"
                                value={li.description}
                                onChange={(e) => handleLineItemChange(li.id, 'description', e.target.value)}
                                className="w-full bg-slate-900/80 border border-slate-800 rounded px-2 py-1 text-slate-200 focus:border-blue-500 focus:outline-none"
                              />
                            </td>
                            <td className="p-2">
                              <input
                                type="number"
                                value={li.quantity}
                                onChange={(e) => handleLineItemChange(li.id, 'quantity', parseInt(e.target.value) || 0)}
                                className="w-full bg-slate-900/80 border border-slate-800 rounded px-2 py-1 text-center font-mono text-slate-200 focus:border-blue-500 focus:outline-none"
                              />
                            </td>
                            <td className="p-2">
                              <input
                                type="number"
                                step="0.01"
                                value={li.unit_price}
                                onChange={(e) => handleLineItemChange(li.id, 'unit_price', parseFloat(e.target.value) || 0)}
                                className="w-full bg-slate-900/80 border border-slate-800 rounded px-2 py-1 text-right font-mono text-slate-200 focus:border-blue-500 focus:outline-none"
                              />
                            </td>
                            <td className="p-2 text-right font-mono font-semibold text-slate-300">
                              ${(li.quantity * li.unit_price).toFixed(2)}
                            </td>
                            <td className="p-2 text-center">
                              <span
                                className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${
                                  li.confidence >= 0.85
                                    ? 'bg-emerald-500/10 text-emerald-400'
                                    : 'bg-amber-500/10 text-amber-400 font-bold'
                                }`}
                              >
                                {(li.confidence * 100).toFixed(0)}%
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </>
            )}

            {activeTab === 'json' && (
              <div className="relative">
                <pre className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-emerald-400 font-mono text-xs overflow-auto max-h-[500px]">
                  {JSON.stringify(data, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

interface FieldEditorProps {
  label: string;
  fieldKey: string;
  field: any;
  onChange: (val: any) => void;
  type?: string;
}

const FieldEditor: React.FC<FieldEditorProps> = ({ label, field, onChange, type = 'text' }) => {
  const isLowConfidence = field.confidence < 0.85;

  return (
    <div
      className={`p-3 rounded-lg border transition-all ${
        isLowConfidence
          ? 'bg-amber-500/5 border-amber-500/40 shadow-sm shadow-amber-500/10'
          : 'bg-slate-950/40 border-slate-800/80 focus-within:border-blue-500'
      }`}
    >
      <div className="flex items-center justify-between mb-1.5">
        <label className="text-xs font-medium text-slate-300">{label}</label>
        <div className="flex items-center space-x-1.5">
          <span
            className={`text-[10px] font-mono px-1.5 py-0.5 rounded font-semibold ${
              isLowConfidence
                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                : 'bg-emerald-500/15 text-emerald-400'
            }`}
          >
            {(field.confidence * 100).toFixed(0)}% Conf
          </span>
          {field.is_verified_by_human && (
            <span className="text-[10px] text-blue-400 flex items-center space-x-0.5" title="Verified by Human">
              <CheckCircle2 className="w-3 h-3" />
            </span>
          )}
        </div>
      </div>
      <input
        type={type}
        value={field.value ?? ''}
        onChange={(e) => onChange(e.target.value)}
        className="w-full bg-slate-900/90 border border-slate-800 rounded px-2.5 py-1.5 text-xs text-white focus:outline-none focus:border-blue-500 transition font-mono"
      />
    </div>
  );
};
