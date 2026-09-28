import React from 'react';
import { X, ShieldCheck, Code, CheckCircle2 } from 'lucide-react';

interface SchemaRuleDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  selectedSchemaId?: string;
}

const SCHEMAS_RULES_DATA: Record<string, {
  name: string;
  version: string;
  description: string;
  pydanticModel: string;
  invariants: Array<{ rule: string; type: 'FATAL' | 'WARNING'; description: string }>;
}> = {
  'Commercial Invoices': {
    name: 'Commercial Invoices Taxonomy',
    version: 'v2.1',
    description: 'Validates line items, VAT calculations, vendor tax ID regex, and currency invariants.',
    pydanticModel: `class CommercialInvoiceSchema(BaseModel):
    invoice_number: str = Field(..., pattern=r"^INV-[0-9]{4}-[0-9]{4}$")
    vendor_tax_id: str = Field(..., pattern=r"^[A-Z]{2}-[0-9]{9}$")
    subtotal: Decimal = Field(..., ge=0)
    tax_amount: Decimal = Field(..., ge=0)
    total_amount: Decimal = Field(..., ge=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)

    @model_validator(mode="after")
    def verify_financial_invariant(self):
        expected_total = self.subtotal + self.tax_amount
        if abs(self.total_amount - expected_total) > Decimal("0.05"):
            raise ValueError(f"Total mismatch: {self.total_amount} != {expected_total}")
        return self`,
    invariants: [
      { rule: 'Tax Equation Checksum', type: 'FATAL', description: 'subtotal + tax_amount == total_amount (within ±0.05 tolerance)' },
      { rule: 'Vendor VAT Regex', type: 'WARNING', description: 'Checks valid ISO country code prefix followed by 9-digit tax identifier' },
      { rule: 'Due Date After Issue Date', type: 'FATAL', description: 'payment_due_date >= invoice_issue_date' },
      { rule: 'Confidence Floor >= 0.85', type: 'WARNING', description: 'Flags any field below 85% posterior probability for operator sign-off' },
    ],
  },
  'Point-of-Sale Receipts': {
    name: 'Point-of-Sale Receipts Taxonomy',
    version: 'v1.0',
    description: 'Itemized totals, tip calculation, and payment authorization tokens.',
    pydanticModel: `class POSReceiptSchema(BaseModel):
    merchant_name: str = Field(..., min_length=2)
    transaction_time: datetime
    subtotal: Decimal = Field(..., ge=0)
    tip_amount: Optional[Decimal] = Field(default=0, ge=0)
    total_amount: Decimal = Field(..., ge=0)
    auth_code: Optional[str] = Field(None, pattern=r"^[0-9A-Z]{6,10}$")`,
    invariants: [
      { rule: 'Itemized Summation', type: 'FATAL', description: 'sum(line_item.total) == subtotal' },
      { rule: 'Tip Variance Limit', type: 'WARNING', description: 'Flags tip amounts exceeding 35% of subtotal for operator audit' },
    ],
  },
  'Enterprise Contracts & MSAs': {
    name: 'Enterprise Contracts & MSAs Taxonomy',
    version: 'v1.4',
    description: 'Indemnity clauses, effective dates, termination windows, and governing law.',
    pydanticModel: `class ContractSchema(BaseModel):
    contract_title: str
    effective_date: date
    governing_law_jurisdiction: str
    indemnity_cap_amount: Optional[Decimal]
    auto_renewal: bool = False
    notice_period_days: int = Field(default=30, ge=0)`,
    invariants: [
      { rule: 'Jurisdiction Validation', type: 'WARNING', description: 'Matches US state law or recognized international commercial venues' },
      { rule: 'Effective Date Precedence', type: 'FATAL', description: 'Effective date must not be older than 5 years' },
    ],
  },
  'Identity & Passports': {
    name: 'Identity & Passports Taxonomy',
    version: 'v1.2',
    description: 'MRZ checksum validation, biometric document fields, and expiration dates.',
    pydanticModel: `class IdentityPassportSchema(BaseModel):
    document_type: str = Field(default="PASSPORT")
    document_number: str = Field(..., min_length=6, max_length=12)
    country_code: str = Field(..., min_length=3, max_length=3)
    expiration_date: date
    mrz_checksum_valid: bool = Field(...)`,
    invariants: [
      { rule: 'ICAO Doc 9303 MRZ Checksum', type: 'FATAL', description: 'Computes modulo 10 check digits on passport number, birth date, and expiry' },
      { rule: 'Document Expiration Verification', type: 'WARNING', description: 'Flags documents expiring within 6 months of current UTC date' },
    ],
  },
};

export const SchemaRuleDrawer: React.FC<SchemaRuleDrawerProps> = ({
  isOpen,
  onClose,
  selectedSchemaId = 'Commercial Invoices',
}) => {
  if (!isOpen) return null;

  const data = SCHEMAS_RULES_DATA[selectedSchemaId] || SCHEMAS_RULES_DATA['Commercial Invoices'];

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label="Schema Invariant Rules"
      className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex justify-end"
      onClick={onClose}
    >
      <div
        className="w-full max-w-xl bg-[#121215] border-l border-zinc-700/80 h-full shadow-2xl flex flex-col justify-between"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div>
          <div className="flex items-center justify-between px-5 py-4 border-b border-zinc-800 bg-zinc-950/60">
            <div className="flex items-center gap-2.5">
              <ShieldCheck className="w-5 h-5 text-emerald-400" />
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-xs font-semibold text-zinc-100 font-mono">{data.name}</h3>
                  <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-zinc-900 border border-zinc-700 text-zinc-300">
                    {data.version}
                  </span>
                </div>
                <p className="text-[11px] text-zinc-400 font-sans mt-0.5">{data.description}</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-1 rounded text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 transition-colors cursor-pointer"
              aria-label="Close drawer"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Body Content */}
          <div className="p-5 space-y-5 overflow-y-auto max-h-[calc(100vh-140px)]">
            {/* Invariants Checklist */}
            <div className="space-y-2">
              <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-400 font-semibold block">
                Deterministic Validation Invariants
              </span>
              <div className="space-y-2">
                {data.invariants.map((inv, idx) => (
                  <div
                    key={idx}
                    className="p-3 rounded-lg border border-zinc-800/80 bg-zinc-950/60 space-y-1 text-xs font-mono"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-zinc-200 flex items-center gap-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                        {inv.rule}
                      </span>
                      <span
                        className={`text-[9px] px-1.5 py-0.2 rounded border font-semibold ${
                          inv.type === 'FATAL'
                            ? 'bg-rose-950/40 text-rose-400 border-rose-800/60'
                            : 'bg-amber-950/40 text-amber-400 border-amber-800/60'
                        }`}
                      >
                        {inv.type}
                      </span>
                    </div>
                    <p className="text-[11px] text-zinc-400 font-sans">{inv.description}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Pydantic Model Code */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-400 font-semibold flex items-center gap-1.5">
                  <Code className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Pydantic v2 Contract Schema</span>
                </span>
                <span className="text-[10px] font-mono text-zinc-400">Strict Typing</span>
              </div>
              <pre className="p-3.5 rounded-lg border border-zinc-800 bg-zinc-950 text-emerald-300/90 text-[11px] font-mono overflow-x-auto leading-relaxed whitespace-pre-wrap">
                {data.pydanticModel}
              </pre>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-5 py-3.5 bg-zinc-950/90 border-t border-zinc-800 text-[11px] font-mono text-zinc-400 flex items-center justify-between">
          <div className="flex items-center gap-1 text-emerald-400">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Active in Production Pipeline</span>
          </div>
          <button
            onClick={onClose}
            className="px-3 py-1 rounded bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-zinc-200 text-xs font-mono transition-colors cursor-pointer"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
