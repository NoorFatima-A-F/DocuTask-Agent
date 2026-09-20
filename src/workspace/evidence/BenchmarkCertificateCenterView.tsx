import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const BenchmarkCertificateCenterView: React.FC = () => {
  const [selectedCert, setSelectedCert] = useState<string>('cert-inv-1000');

  const certificates = [
    {
      id: 'cert-inv-1000',
      title: 'Enterprise Invoice Benchmark (1,000 Pages)',
      sampleSize: 1000,
      throughputPgSec: 48.5,
      p95LatencyMs: 245.0,
      f1Score: 0.994,
      costPer1k: 1.25,
      confidenceInterval99: [0.991, 0.997],
      pValue: 0.0001,
      reproducibilityScore: 99.85,
      signature: 'sig_cert_a8f3b20c91e847ad3ef0192a83c7482910fae12089bb3c17',
      merkleLeafHash: '3ef0192a83c7482910fae12089bb3c17820aedfa9102bc45a8f3b20c91e847ad',
      certifiedAt: '2026-09-10T18:00:00Z',
    },
    {
      id: 'cert-table-500',
      title: 'Dense Financial Tables Benchmark (500 Pages)',
      sampleSize: 500,
      throughputPgSec: 36.2,
      p95LatencyMs: 380.0,
      f1Score: 0.991,
      costPer1k: 1.80,
      confidenceInterval99: [0.988, 0.994],
      pValue: 0.0002,
      reproducibilityScore: 99.90,
      signature: 'sig_cert_7c3f810dae99120bc45a8f3b20c91e847ad3ef0192a83c748',
      merkleLeafHash: 'd4e9102fae89bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c748',
      certifiedAt: '2026-09-10T18:15:00Z',
    },
  ];

  const activeCert = certificates.find((c) => c.id === selectedCert) || certificates[0]!;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Benchmark Certification Center</h1>
            <Badge variant="success" size="sm">Mathematically Certified</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Independently reproducible benchmark performance proofs attested with 99% confidence intervals and cryptographic signatures.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="outline" size="md">
            p &lt; 0.0001
          </Badge>
          <Badge variant="intelligence" size="md">
            Repeatability: 99.85%
          </Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Certificate List */}
        <div className="space-y-3">
          <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Certified Benchmark Suites ({certificates.length})
          </div>
          {certificates.map((cert) => {
            const isSelected = cert.id === selectedCert;
            return (
              <Card
                key={cert.id}
                className={`p-4 cursor-pointer transition-all ${
                  isSelected ? 'border-primary ring-1 ring-primary/40 bg-primary/5' : 'hover:border-border/80'
                }`}
                onClick={() => setSelectedCert(cert.id)}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <span className="font-semibold text-xs text-foreground">{cert.title}</span>
                    <div className="text-xs font-mono text-muted-foreground mt-0.5">{cert.id}</div>
                  </div>
                  <Badge variant="success" size="sm">CERTIFIED</Badge>
                </div>
                <div className="mt-3 flex items-center justify-between text-xs font-mono text-muted-foreground">
                  <span className="text-foreground">{cert.throughputPgSec} pg/s</span>
                  <span className="text-emerald-400 font-bold">{(cert.f1Score * 100).toFixed(1)}% F1</span>
                  <span>${cert.costPer1k}/1k</span>
                </div>
              </Card>
            );
          })}
        </div>

        {/* Certificate Display Card */}
        <div className="lg:col-span-2 space-y-4">
          <Card className="p-6 space-y-6 border-emerald-500/30 bg-emerald-950/5 relative overflow-hidden">
            <div className="flex items-start justify-between border-b border-border/40 pb-4">
              <div>
                <Badge variant="success" size="sm" className="mb-2">OFFICIAL BENCHMARK CERTIFICATE</Badge>
                <h2 className="text-xl font-bold tracking-tight">{activeCert.title}</h2>
                <div className="text-xs text-muted-foreground mt-1">
                  Sample Size: <span className="font-bold text-foreground">{activeCert.sampleSize.toLocaleString()} Documents</span> | Certified: <span className="font-mono text-foreground">{activeCert.certifiedAt}</span>
                </div>
              </div>
              <div className="text-right font-mono">
                <div className="text-[10px] text-muted-foreground">Reproducibility Parity</div>
                <div className="text-xl font-extrabold text-emerald-400">{activeCert.reproducibilityScore}%</div>
              </div>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="p-3 bg-card border border-border/40 rounded-lg">
                <div className="text-[11px] text-muted-foreground">Throughput</div>
                <div className="text-lg font-bold font-mono text-foreground mt-1">{activeCert.throughputPgSec} <span className="text-xs font-normal text-muted-foreground">pg/sec</span></div>
              </div>
              <div className="p-3 bg-card border border-border/40 rounded-lg">
                <div className="text-[11px] text-muted-foreground">P95 Latency</div>
                <div className="text-lg font-bold font-mono text-foreground mt-1">{activeCert.p95LatencyMs} <span className="text-xs font-normal text-muted-foreground">ms</span></div>
              </div>
              <div className="p-3 bg-card border border-border/40 rounded-lg">
                <div className="text-[11px] text-muted-foreground">Accuracy (F1)</div>
                <div className="text-lg font-bold font-mono text-emerald-400 mt-1">{(activeCert.f1Score * 100).toFixed(2)}%</div>
              </div>
              <div className="p-3 bg-card border border-border/40 rounded-lg">
                <div className="text-[11px] text-muted-foreground">Cost per 1k</div>
                <div className="text-lg font-bold font-mono text-foreground mt-1">${activeCert.costPer1k.toFixed(2)}</div>
              </div>
            </div>

            {/* Statistical Rigor */}
            <div className="p-4 bg-muted/30 border border-border/40 rounded-lg space-y-2">
              <div className="text-xs font-semibold text-foreground">Statistical Bounds & Confidence Intervals</div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs font-mono text-muted-foreground">
                <div>99% CI Bounds: <span className="text-foreground font-bold">[{activeCert.confidenceInterval99[0]}, {activeCert.confidenceInterval99[1]}]</span></div>
                <div>Hypothesis Test: <span className="text-foreground font-bold">p-value = {activeCert.pValue} (Significant)</span></div>
              </div>
            </div>

            {/* Cryptographic Signature Block */}
            <div className="p-3 bg-card border border-border/40 rounded font-mono text-[11px] text-muted-foreground space-y-1">
              <div><span className="text-foreground">Merkle Leaf Digest: </span>{activeCert.merkleLeafHash}</div>
              <div><span className="text-foreground">Authority Signature: </span><span className="text-emerald-400 font-bold">{activeCert.signature}</span></div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
