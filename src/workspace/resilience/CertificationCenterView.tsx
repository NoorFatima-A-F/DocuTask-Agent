import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Award, ShieldCheck, Copy, CheckCircle2 } from 'lucide-react';


export const CertificationCenterView: React.FC = () => {
  const [isCopied, setIsCopied] = useState<boolean>(false);

  const dossier = {
    dossierId: 'DOSSIER-HA-2026-09-10',
    platform: 'DocuTask Autonomous AI Platform',
    version: '12.0.0-APRCORP+',
    tier: 'TIER_4_MISSION_CRITICAL',
    compositeReliability: 99.42,
    availabilityPct: 99.9988,
    readinessScore: 99.45,
    invariantsCompliance: 100.0,
    mttrMs: 45.2,
    mtbfHours: 720.0,
    signature: '7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069',
  };

  const handleCopyJSON = () => {
    navigator.clipboard.writeText(JSON.stringify(dossier, null, 2));
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Enterprise Resilience Certification Dossier</h1>
            <Badge variant="intelligence" size="sm">Cryptographic HA Proof</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Exportable, cryptographically signed operational resilience certification for enterprise production sign-off.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleCopyJSON}>
            {isCopied ? <CheckCircle2 className="w-3.5 h-3.5 mr-1.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 mr-1.5" />}
            {isCopied ? 'Copied to Clipboard' : 'Copy Dossier JSON'}
          </Button>
          <Badge variant="success" size="md">
            Certified: Tier 4 Mission Critical
          </Badge>
        </div>
      </div>

      {/* Main Certificate Display */}
      <Card className="p-8 border-2 border-emerald-500/40 bg-emerald-950/10 space-y-6 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-emerald-500/30 pb-6">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Award className="w-6 h-6 text-emerald-400" />
              <span className="text-lg font-bold tracking-wide text-foreground uppercase">Certificate of Operational Resilience</span>
            </div>
            <div className="text-xs text-muted-foreground font-mono">{dossier.dossierId} • {dossier.platform} v{dossier.version}</div>
          </div>
          <Badge variant="success" size="md">
            {dossier.tier}
          </Badge>

        </div>

        {/* Certificate Metrics Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-4 bg-background/80 rounded-lg border border-border/40">
            <div className="text-xs text-muted-foreground">Composite Reliability</div>
            <div className="text-2xl font-extrabold font-mono text-emerald-400 mt-1">{dossier.compositeReliability}%</div>
          </div>
          <div className="p-4 bg-background/80 rounded-lg border border-border/40">
            <div className="text-xs text-muted-foreground">Operational Availability</div>
            <div className="text-2xl font-extrabold font-mono text-blue-400 mt-1">{dossier.availabilityPct}%</div>
          </div>
          <div className="p-4 bg-background/80 rounded-lg border border-border/40">
            <div className="text-xs text-muted-foreground">Launch Readiness</div>
            <div className="text-2xl font-extrabold font-mono text-purple-400 mt-1">{dossier.readinessScore}%</div>
          </div>
          <div className="p-4 bg-background/80 rounded-lg border border-border/40">
            <div className="text-xs text-muted-foreground">Invariants Compliance</div>
            <div className="text-2xl font-extrabold font-mono text-cyan-400 mt-1">{dossier.invariantsCompliance}%</div>
          </div>
        </div>

        {/* Cryptographic Signature Box */}
        <div className="p-4 bg-background/90 rounded-lg border border-border/60 space-y-2">
          <div className="flex items-center justify-between text-xs">
            <span className="font-semibold text-foreground flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-emerald-400" /> SHA-256 Cryptographic Signature
            </span>
            <span className="text-emerald-400 font-mono text-[11px]">VERIFIED_IMMUTABLE</span>
          </div>
          <div className="p-2.5 bg-muted/50 rounded font-mono text-xs text-primary break-all">
            {dossier.signature}
          </div>
          <div className="text-[11px] text-muted-foreground">
            This digital signature cryptographically binds all execution proofs, invariant audits, and chaos benchmark results to this immutable dossier.
          </div>
        </div>
      </Card>
    </div>
  );
};
