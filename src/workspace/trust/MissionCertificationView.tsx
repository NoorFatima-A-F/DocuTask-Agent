import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const MissionCertificationView: React.FC = () => {
  const certificates = [
    {
      certId: 'cert_msn_1001',
      missionId: 'msn_1001',
      domain: 'Invoice',
      tier: 'ENTERPRISE_HIGHEST_ASSURANCE',
      trustScore: 98.4,
      completeness: '100.0%',
      replayFidelity: '99.98%',
      invariants: '100.0%',
      issuedAt: 'Today, 14:20 UTC',
      seal: '0x8f2ac31b4e5d6a7b',
    },
    {
      certId: 'cert_msn_1002',
      missionId: 'msn_1002',
      domain: 'Contract',
      tier: 'SCIENTIFIC_REPRODUCIBLE',
      trustScore: 96.2,
      completeness: '100.0%',
      replayFidelity: '99.92%',
      invariants: '100.0%',
      issuedAt: 'Today, 14:15 UTC',
      seal: '0x3c7eb44a1d9e2f8c',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Mission Execution Certification</h1>
            <Badge variant="intelligence" size="sm">Pillar 8</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Official certification tiers derived strictly from mathematical thresholds: Bronze (&ge;70), Silver (&ge;80), Gold (&ge;90), Scientific (&ge;95), Enterprise (&ge;98).
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            Issuer: DACA Authority
          </Badge>
        </div>
      </div>

      {/* Certificates List */}
      <div className="space-y-4">
        {certificates.map((cert) => (
          <Card key={cert.certId} className="p-5 border-border/60">
            <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2 border-b border-border/40 pb-3 mb-4">
              <div>
                <span className="font-mono text-xs text-primary font-semibold">{cert.certId}</span>
                <h3 className="text-sm font-semibold text-foreground mt-0.5">
                  Certification Dossier for Mission <strong className="font-mono text-primary">{cert.missionId}</strong>
                </h3>
                <span className="text-xs text-muted-foreground">Domain: <strong>{cert.domain}</strong></span>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant={cert.tier.includes('ENTERPRISE') ? 'success' : 'intelligence'} size="sm">
                  {cert.tier}
                </Badge>
              </div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center text-xs mb-4">
              <div className="p-3 rounded bg-muted/20 border border-border/40">
                <div className="text-[10px] text-muted-foreground">Trust Score</div>
                <div className="font-mono font-bold text-emerald-400 text-sm mt-0.5">{cert.trustScore} / 100</div>
              </div>
              <div className="p-3 rounded bg-muted/20 border border-border/40">
                <div className="text-[10px] text-muted-foreground">Evidence Completeness</div>
                <div className="font-mono font-bold text-foreground text-sm mt-0.5">{cert.completeness}</div>
              </div>
              <div className="p-3 rounded bg-muted/20 border border-border/40">
                <div className="text-[10px] text-muted-foreground">Replay State Fidelity</div>
                <div className="font-mono font-bold text-emerald-400 text-sm mt-0.5">{cert.replayFidelity}</div>
              </div>
              <div className="p-3 rounded bg-muted/20 border border-border/40">
                <div className="text-[10px] text-muted-foreground">Invariant Pass Rate</div>
                <div className="font-mono font-bold text-primary text-sm mt-0.5">{cert.invariants}</div>
              </div>
            </div>

            <div className="text-xs text-muted-foreground flex items-center justify-between border-t border-border/40 pt-3 font-mono">
              <span>Cryptographic Seal: <strong className="text-foreground">{cert.seal}</strong></span>
              <button className="text-primary hover:underline font-medium font-sans">Download Signed Certificate &rarr;</button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
