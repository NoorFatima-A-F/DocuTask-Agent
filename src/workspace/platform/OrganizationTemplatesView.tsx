import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const OrganizationTemplatesView: React.FC = () => {
  const [deployedId, setDeployedId] = useState<string | null>(null);

  const templates = [
    {
      id: 'tpl-healthcare-hospital',
      name: 'Regional Hospital Health System',
      industry: 'HEALTHCARE',
      icon: '🏥',
      description: 'Configures Clinical Ingestion, Medical Billing, HIPAA Privacy Shield, and Patient Record OCR.',
      departments: ['Executive', 'OCR', 'Clinical Extraction', 'HIPAA Compliance', 'QA'],
      plugins: ['plugin.medical.records', 'plugin.invoice.processing'],
      sla: '400 ms',
    },
    {
      id: 'tpl-finance-bank',
      name: 'Commercial & Investment Bank',
      industry: 'BANKING',
      icon: '🏦',
      description: 'Configures KYB/KYC Verification, Loan Application Parsing, Treasury Reconciliation, and Four-Eyes Governance.',
      departments: ['Executive', 'OCR', 'Financial Extraction', 'AML Compliance', 'Governance'],
      plugins: ['plugin.invoice.processing', 'plugin.legal.contracts'],
      sla: '250 ms',
    },
    {
      id: 'tpl-legal-lawfirm',
      name: 'Corporate Law & M&A Firm',
      industry: 'LEGAL',
      icon: '⚖️',
      description: 'Deploys Clause Risk Analyzer, Regulatory Redlining, Non-Compete Reviewers, and Forensic Evidence DAG.',
      departments: ['Executive', 'Perception', 'Clause Analysis', 'Risk Review', 'Forensic Audit'],
      plugins: ['plugin.legal.contracts'],
      sla: '500 ms',
    },
    {
      id: 'tpl-insurance-carrier',
      name: 'P&C Insurance Carrier',
      industry: 'INSURANCE',
      icon: '🛡️',
      description: 'Automates First Notice of Loss (FNOL), Medical Injury Extraction, Adjuster Fraud Detection, and Payout Validation.',
      departments: ['Executive', 'Perception', 'Claims Extraction', 'Fraud Detection', 'QA'],
      plugins: ['plugin.medical.records', 'plugin.invoice.processing'],
      sla: '350 ms',
    },
  ];

  const handleDeploy = (tplId: string) => {
    setDeployedId(tplId);
    setTimeout(() => {
      setDeployedId(null);
    }, 2500);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Organization Blueprint Templates</h1>
            <Badge variant="success" size="sm">1-Click Enterprise Deployment</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Instantiate full-scale multi-department autonomous organizations with pre-configured plugins, policies, and SLA targets.
          </p>
        </div>
        <Badge variant="outline" size="md">
          {templates.length} Industry Blueprints
        </Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {templates.map((tpl) => {
          const isJustDeployed = deployedId === tpl.id;
          return (
            <Card key={tpl.id} className="p-6 space-y-4 flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-3xl">{tpl.icon}</span>
                    <div>
                      <h2 className="text-base font-bold text-foreground">{tpl.name}</h2>
                      <div className="text-xs text-muted-foreground mt-0.5">{tpl.industry} Blueprint</div>
                    </div>
                  </div>
                  <Badge variant="intelligence" size="sm">SLA: {tpl.sla}</Badge>
                </div>

                <p className="text-xs text-muted-foreground leading-relaxed">
                  {tpl.description}
                </p>

                <div className="space-y-1 text-xs">
                  <div className="font-semibold text-muted-foreground">Pre-Configured Departments:</div>
                  <div className="flex flex-wrap gap-1">
                    {tpl.departments.map((d) => (
                      <span key={d} className="px-2 py-0.5 bg-muted/40 rounded text-[11px] font-mono text-foreground">
                        {d}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t border-border/40 flex items-center justify-between">
                <div className="text-xs font-mono text-muted-foreground">
                  Bundles {tpl.plugins.length} Plugins
                </div>
                <button
                  onClick={() => handleDeploy(tpl.id)}
                  disabled={isJustDeployed}
                  className={`px-4 py-2 rounded-lg text-xs font-bold font-mono transition-all cursor-pointer ${
                    isJustDeployed
                      ? 'bg-emerald-600 text-white'
                      : 'bg-primary hover:bg-primary/90 text-primary-foreground'
                  }`}
                >
                  {isJustDeployed ? '✓ Organization Deployed!' : '🚀 1-Click Provision'}
                </button>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
};
