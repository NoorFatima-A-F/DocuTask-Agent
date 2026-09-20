import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const PluginMarketplaceView: React.FC = () => {
  const [installedMap, setInstalledMap] = useState<Record<string, boolean>>({
    'pkg.fintech.invoice_pro': true,
    'pkg.hr.talent_matcher': true,
    'pkg.health.hipaa_shield': true,
    'pkg.legal.lexis_covenant': true,
  });

  const packages = [
    {
      id: 'pkg.fintech.invoice_pro',
      name: 'InvoicePro Elite Agent',
      version: '1.4.0',
      author: 'DocuTask Labs',
      category: 'FINANCE',
      description: 'State-of-the-art multi-lingual invoice extraction with Mod11 VAT checksum verification.',
      securityAuditScore: 99.4,
      downloadCount: 14200,
      rating: 4.95,
      tags: ['invoices', 'ocr', 'reconciliation'],
    },
    {
      id: 'pkg.hr.talent_matcher',
      name: 'TalentMatcher ATS Screener',
      version: '1.2.0',
      author: 'TalentAI Labs',
      category: 'HUMAN_RESOURCES',
      description: 'Parses complex multi-column resumes and scores talent against job requisitions.',
      securityAuditScore: 98.1,
      downloadCount: 8900,
      rating: 4.88,
      tags: ['resumes', 'ats', 'hiring'],
    },
    {
      id: 'pkg.health.hipaa_shield',
      name: 'HIPAA Clinical Shield',
      version: '2.0.1',
      author: 'MedSecure Systems',
      category: 'HEALTHCARE',
      description: 'Zero-leakage PHI redactor and ICD-10 diagnostic coding extractor.',
      securityAuditScore: 100.0,
      downloadCount: 6400,
      rating: 4.98,
      tags: ['healthcare', 'hipaa', 'phi'],
    },
    {
      id: 'pkg.legal.lexis_covenant',
      name: 'LexisCovenant Contract Reviewer',
      version: '1.1.5',
      author: 'LexisCorp AI',
      category: 'LEGAL',
      description: 'Identifies risky indemnities, non-competes, and liabilities in MSAs and NDAs.',
      securityAuditScore: 97.8,
      downloadCount: 11200,
      rating: 4.91,
      tags: ['contracts', 'legal', 'indemnity'],
    },
  ];

  const handleToggleInstall = (pkgId: string) => {
    setInstalledMap((prev) => ({ ...prev, [pkgId]: !prev[pkgId] }));
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Agent Marketplace</h1>
            <Badge variant="success" size="sm">Verified Ecosystem</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Discover, install, and update certified domain agent plugins with 1-click sandboxed deployment.
          </p>
        </div>
        <Badge variant="outline" size="md">
          {packages.length} Packages Verified
        </Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {packages.map((pkg) => {
          const isInstalled = !!installedMap[pkg.id];
          return (
            <Card key={pkg.id} className="p-6 space-y-4 flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex items-start justify-between">
                  <div>
                    <Badge variant="outline" size="sm" className="mb-1">{pkg.category}</Badge>
                    <h2 className="text-base font-bold text-foreground">{pkg.name}</h2>
                    <div className="text-xs text-muted-foreground mt-0.5">
                      by <span className="text-foreground font-semibold">{pkg.author}</span> • v{pkg.version}
                    </div>
                  </div>
                  <div className="text-right">
                    <Badge variant="success" size="sm">★ {pkg.rating}</Badge>
                    <div className="text-[10px] text-muted-foreground mt-1">{pkg.downloadCount.toLocaleString()} installs</div>
                  </div>
                </div>

                <p className="text-xs text-muted-foreground leading-relaxed">
                  {pkg.description}
                </p>

                <div className="flex flex-wrap gap-1.5 pt-1">
                  {pkg.tags.map((tag) => (
                    <span key={tag} className="px-2 py-0.5 bg-muted/40 text-muted-foreground rounded text-[10px] font-mono">
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>

              <div className="pt-4 border-t border-border/40 flex items-center justify-between">
                <div className="text-xs font-mono">
                  <span className="text-muted-foreground">Security Audit: </span>
                  <span className="text-emerald-400 font-bold">{pkg.securityAuditScore}%</span>
                </div>
                <button
                  onClick={() => handleToggleInstall(pkg.id)}
                  className={`px-4 py-1.5 rounded-lg text-xs font-bold font-mono transition-all cursor-pointer ${
                    isInstalled
                      ? 'bg-muted/40 hover:bg-red-500/20 text-muted-foreground hover:text-red-400 border border-border/40'
                      : 'bg-primary hover:bg-primary/90 text-primary-foreground'
                  }`}
                >
                  {isInstalled ? '✓ Installed (Uninstall)' : '⬇ 1-Click Install'}
                </button>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
};
