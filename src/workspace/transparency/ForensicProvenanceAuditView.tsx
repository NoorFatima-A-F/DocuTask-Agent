import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ForensicProvenanceAuditView: React.FC = () => {
  const provenanceSteps = [
    {
      step: 1,
      stage: 'RAW_DOCUMENT_INGESTION',
      description: 'Raw PDF page 1 ingested (300 DPI, SHA-256: 9f82ab...)',
      actor: 'DocumentIngestionWorker',
      timestamp: '16:00:00.120',
      artifact: 'page_1.png (2480x3508)',
    },
    {
      step: 2,
      stage: 'OCR_BOUNDING_BOX',
      description: 'Optical bounding box [x:1840, y:3120, w:240, h:48] -> "$1,420.50"',
      actor: 'LayoutLMOCRWorker',
      timestamp: '16:00:00.310',
      artifact: 'Confidence: 0.985',
    },
    {
      step: 3,
      stage: 'LLM_STRUCTURED_EXTRACTION',
      description: 'Structured parsing routed to Gemini 2.5 Flash -> 1420.50 USD',
      actor: 'LLMReasoningWorker',
      timestamp: '16:00:00.740',
      artifact: 'Field Confidence: 0.965',
    },
    {
      step: 4,
      stage: 'INVARIANT_VALIDATION',
      description: 'Subtotal ($1,300.00) + Tax ($120.50) == Total ($1,420.50) arithmetic verification',
      actor: 'InvariantValidationWorker',
      timestamp: '16:00:00.790',
      artifact: 'Status: 100% VALIDATED',
    },
    {
      step: 5,
      stage: 'CRYPTOGRAPHIC_SIGN_COMMIT',
      description: 'Persisted to Postgres + ED25519 signature manifest generated',
      actor: 'AuditSecurityWorker',
      timestamp: '16:00:00.825',
      artifact: 'Signature: ED25519_SIG_8F3A20B1',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">🔬</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Forensic Field Provenance & Cryptographic Lineage
              </h2>
              <Badge variant="success" size="sm">
                TAMPER-PROOF MERKLE CHAIN
              </Badge>
            </div>
            <p className="text-sm font-mono text-[#94A3B8] mt-1">
              End-to-end auditability tracing any extracted field back to pixel coordinates, OCR tokens, LLM responses, and database commits.
            </p>
          </div>
        </div>
      </div>

      {/* Provenance Card */}
      <Card className="p-6 bg-[#0F172A] border-[#1E293B]">
        <div className="flex items-center justify-between pb-4 border-b border-[#1E293B]">
          <div>
            <span className="text-xs font-mono text-cyan-400 font-bold">FIELD LINEAGE TRACE:</span>
            <h3 className="text-base font-bold font-mono text-[#F8FAFC]">
              invoice_total_amount → $1,420.50 USD
            </h3>
            <div className="text-xs font-mono text-[#64748B] mt-0.5">
              Document: DOC-INV-2026 • Status: Cryptographically Sealed
            </div>
          </div>
          <Badge variant="success" size="md">
            100% TRACEABLE
          </Badge>
        </div>

        {/* Lineage Steps Timeline */}
        <div className="space-y-4 mt-6">
          {provenanceSteps.map((s) => (
            <div key={s.step} className="p-4 rounded-xl bg-[#020617] border border-[#1E293B]">
              <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-2">
                <div className="flex items-center gap-3">
                  <span className="w-6 h-6 rounded-full bg-cyan-950 border border-cyan-500/50 flex items-center justify-center text-xs font-mono font-bold text-cyan-300">
                    {s.step}
                  </span>
                  <div>
                    <h4 className="text-xs font-bold font-mono text-[#F8FAFC]">{s.stage}</h4>
                    <p className="text-xs font-mono text-[#94A3B8] mt-0.5">{s.description}</p>
                  </div>
                </div>
                <div className="text-right font-mono text-xs">
                  <div className="text-[#64748B] text-[11px]">{s.timestamp}</div>
                  <div className="text-emerald-400 font-bold mt-0.5">{s.artifact}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
