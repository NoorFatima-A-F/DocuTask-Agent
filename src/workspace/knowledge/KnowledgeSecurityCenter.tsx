import React from 'react';
import { Shield, Lock, EyeOff, UserCheck } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

export const KnowledgeSecurityCenter: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
          <Shield className="w-7 h-7 text-indigo-400" />
          Knowledge Security & Classification Center
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Strict tenant isolation, attribute-based access control (ABAC), and automated PII sanitization.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-3">
          <Lock className="w-6 h-6 text-indigo-400" />
          <h3 className="text-base font-semibold text-slate-200">Security Clearance Tiers</h3>
          <p className="text-xs text-slate-400">
            Assets categorized under PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED, STRICT_SECRET.
          </p>
          <Badge variant="success">Strictly Enforced</Badge>
        </Card>

        <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-3">
          <EyeOff className="w-6 h-6 text-amber-400" />
          <h3 className="text-base font-semibold text-slate-200">PII Redaction Engine</h3>
          <p className="text-xs text-slate-400">
            Automated regex & NER masking of emails, phone numbers, SSNs, and credit cards before indexing.
          </p>
          <Badge variant="warning">Auto-Sanitized</Badge>
        </Card>

        <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-3">
          <UserCheck className="w-6 h-6 text-emerald-400" />
          <h3 className="text-base font-semibold text-slate-200">Tenant Isolation Boundary</h3>
          <p className="text-xs text-slate-400">
            Cryptographic tenant isolation ensuring zero cross-tenant vector space leakage.
          </p>
          <Badge variant="outline" className="text-emerald-400 border-emerald-500/30">100% Isolated</Badge>
        </Card>
      </div>
    </div>
  );
};
