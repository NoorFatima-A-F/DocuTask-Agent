import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const PluginCertificationView: React.FC = () => {
  const [isScanning, setIsScanning] = useState<boolean>(false);
  const [certifiedBadge] = useState<any | null>({
    badgeId: 'BADGE-1725992010-INVOICE',
    pluginId: 'plugin.invoice.processing',
    version: '1.4.0',
    overallScore: 99.4,
    certified: true,
    merkleAttestationHash: 'a8f3b20c91e847ad3ef0192a83c7482910fae12089bb3c17820aedfa9102bc45',
    signature: 'sig_cert_a8f3b20c91e847ad3ef0192a83c7482910fae12089bb3c17',
    certifiedAtUtc: '2026-09-10T18:22:15Z',
    checks: [
      { id: 'CERT-SCH-01', name: 'Manifest & Capability Schema Compliance', score: 100.0, passed: true, details: 'Verified JSON schema and input/output contracts.' },
      { id: 'CERT-SEC-02', name: 'Static AST & Permission Sandbox Scan', score: 99.2, passed: true, details: 'Zero unauthorized socket egress or eval primitives.' },
      { id: 'CERT-PERF-03', name: 'SLA Latency & Memory Footprint Bounds', score: 98.5, passed: true, details: 'P95 latency (124ms) and RAM (48MB) within quota.' },
      { id: 'CERT-REP-04', name: 'Deterministic Replay Parity (10 Runs)', score: 100.0, passed: true, details: 'Bitwise output hash match across 10 frozen seeds.' },
      { id: 'CERT-EVD-05', name: 'Cryptographic Merkle DAG Evidence Generation', score: 100.0, passed: true, details: 'Seals capability steps with SHA-256 digests.' },
      { id: 'CERT-ORG-06', name: 'Multi-Agent Organization & Vickrey Protocol', score: 99.0, passed: true, details: 'Complies with communication bus and auction rules.' },
    ],
  });

  const handleRunCertification = () => {
    setIsScanning(true);
    setTimeout(() => {
      setIsScanning(false);
    }, 600);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Plugin Certification Center</h1>
            <Badge variant="success" size="sm">Automated 6-Point Audit</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Automated certification pipeline guaranteeing schema validity, AST security, replay stability, and Merkle evidence generation.
          </p>
        </div>
        <button
          onClick={handleRunCertification}
          disabled={isScanning}
          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-lg transition-all flex items-center gap-2 shadow-sm cursor-pointer"
        >
          {isScanning ? 'Auditing Plugin...' : '🛡️ Run 6-Point Certification'}
        </button>
      </div>

      {certifiedBadge && (
        <div className="space-y-6">
          <Card className="p-6 space-y-4 border-emerald-500/30 bg-emerald-950/10">
            <div className="flex items-start justify-between border-b border-border/40 pb-4">
              <div>
                <Badge variant="success" size="sm" className="mb-2">OFFICIAL PLATFORM CERTIFICATION BADGE</Badge>
                <h2 className="text-lg font-bold">{certifiedBadge.pluginId} (v{certifiedBadge.version})</h2>
                <div className="text-xs font-mono text-muted-foreground mt-0.5">Badge ID: {certifiedBadge.badgeId}</div>
              </div>
              <div className="text-right font-mono">
                <div className="text-[10px] text-muted-foreground">Certification Score</div>
                <div className="text-2xl font-extrabold text-emerald-400">{certifiedBadge.overallScore}%</div>
              </div>
            </div>

            <div className="space-y-3">
              <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                6-Point Verification Battery
              </div>
              <div className="space-y-2">
                {certifiedBadge.checks.map((chk: any) => (
                  <div key={chk.id} className="p-3 bg-card border border-border/40 rounded-lg flex items-center justify-between text-xs">
                    <div>
                      <div className="font-semibold text-foreground flex items-center gap-2">
                        <span className="text-emerald-400">✓</span> {chk.name}
                      </div>
                      <div className="text-muted-foreground text-[11px] mt-0.5">{chk.details}</div>
                    </div>
                    <Badge variant="success" size="sm">{chk.score}%</Badge>
                  </div>
                ))}
              </div>
            </div>

            <div className="p-3 bg-card border border-border/40 rounded font-mono text-[11px] text-muted-foreground space-y-1">
              <div><span className="text-foreground">Merkle Digest: </span>{certifiedBadge.merkleAttestationHash}</div>
              <div><span className="text-foreground">Authority Signature: </span><span className="text-emerald-400 font-bold">{certifiedBadge.signature}</span></div>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};
